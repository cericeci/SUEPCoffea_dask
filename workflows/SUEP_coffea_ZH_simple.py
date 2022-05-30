"""
SUEP_coffea_ZH.py
Coffea producer for SUEP analysis. Uses fastjet package to recluster large jets:
https://github.com/scikit-hep/fastjet
Chad Freer, 2021
"""

import os
import pathlib
import shutil
import awkward as ak
import pandas as pd
import numpy as np
import fastjet
from coffea import hist, processor
import vector
from typing import List, Optional
vector.register_awkward()

class SUEP_cluster(processor.ProcessorABC):
    def __init__(self, isMC: int, era: int, sample: str,  do_syst: bool, syst_var: str, weight_syst: bool, flag: bool, output_location: Optional[str]) -> None:
        self._flag = flag
        self.output_location = output_location
        self.do_syst = do_syst
        self.gensumweight = 1.0
        self.era = era
        self.isMC = isMC
        self.sample = sample
        self.syst_var, self.syst_suffix = (syst_var, f'_sys_{syst_var}') if do_syst and syst_var else ('', '')
        self.weight_syst = weight_syst
        self.prefixes = {"SUEP": "SUEP"}
        #Set up for the histograms
        self._accumulator = processor.dict_accumulator({})

    @property
    def accumulator(self):
        return self._accumulator

    def sphericity(self, events, particles, r):
        # In principle here we already have ak.num(particles) != 0
        # Some sanity replacements just in case the boosting broke
        px = ak.nan_to_num(particles.px, 0)
        py = ak.nan_to_num(particles.py, 0)
        pz = ak.nan_to_num(particles.pz, 0)
        p  = ak.nan_to_num(particles.p,  0)

        norm = np.squeeze(ak.sum(p ** r, axis=1, keepdims=True))
        s = np.array([[
                        ak.sum(px*px * p ** (r-2.0), axis=1 ,keepdims=True)/norm,
                        ak.sum(px*py * p ** (r-2.0), axis=1 ,keepdims=True)/norm,
                        ak.sum(px*pz * p ** (r-2.0), axis=1 ,keepdims=True)/norm
                        ],
                        [
                        ak.sum(py*px * p ** (r-2.0), axis=1 ,keepdims=True)/norm,
                        ak.sum(py*py * p ** (r-2.0), axis=1 ,keepdims=True)/norm,
                        ak.sum(py*pz * p ** (r-2.0), axis=1 ,keepdims=True)/norm
                        ],
                        [
                        ak.sum(pz*px * p ** (r-2.0), axis=1 ,keepdims=True)/norm,
                        ak.sum(pz*py * p ** (r-2.0), axis=1 ,keepdims=True)/norm,
                        ak.sum(pz*pz * p ** (r-2.0), axis=1 ,keepdims=True)/norm
                        ]])
        s = np.squeeze(np.moveaxis(s, 2, 0),axis=3)
        s = np.nan_to_num(s, copy=False, nan=1., posinf=1., neginf=1.) 

        evals = np.sort(np.linalg.eigvals(s))
        # eval1 < eval2 < eval3
        return evals

    def rho(self, number, jet, tracks, deltaR, dr=0.05):
        r_start = number*dr
        r_end = (number+1)*dr
        ring = (deltaR > r_start) & (deltaR < r_end)
        rho_values = ak.sum(tracks[ring].pt, axis=1)/(dr*jet.pt)
        return rho_values

    def ak_to_pandas(self, jet_collection: ak.Array) -> pd.DataFrame:
        output = pd.DataFrame()
        for field in ak.fields(jet_collection):
            prefix = self.prefixes.get(field, "")
            if len(prefix) > 0:
                for subfield in ak.fields(jet_collection[field]):
                    output[f"{prefix}_{subfield}"] = ak.to_numpy(
                        jet_collection[field][subfield]
                    )
            else:
                if not(isinstance(ak.to_numpy(jet_collection[field])[0],np.ndarray)):
                  output[field] = ak.to_numpy(jet_collection[field])
                else:
                  temp =  ak.to_numpy(jet_collection[field])
                  output[field] = [[k for k in kk] for kk in temp]
        return output

    def h5store(self, store: pd.HDFStore, df: pd.DataFrame, fname: str, gname: str, **kwargs: float) -> None:
        store.put(gname, df)
        store.get_storer(gname).attrs.metadata = kwargs
        
    def save_dfs(self, dfs, df_names, fname=None):
        if not(fname): fname = "out.hdf5"
        subdirs = []
        store = pd.HDFStore(fname)
        if self.output_location is not None:
            # pandas to hdf5
            for out, gname in zip(dfs, df_names):
                if self.isMC:
                    metadata = dict(gensumweight=self.gensumweight,era=self.era, mc=self.isMC,sample=self.sample)
                    #metadata.update({"gensumweight":self.gensumweight})
                else:
                    metadata = dict(era=self.era, mc=self.isMC,sample=self.sample)    
                    
                store_fin = self.h5store(store, out, fname, gname, **metadata)

            store.close()
            self.dump_table(fname, self.output_location, subdirs)
        else:
            print("self.output_location is None")
            store.close()

    def dump_table(self, fname: str, location: str, subdirs: Optional[List[str]] = None) -> None:
        subdirs = subdirs or []
        xrd_prefix = "root://"
        pfx_len = len(xrd_prefix)
        xrootd = False
        if xrd_prefix in location:
            try:
                import XRootD
                import XRootD.client

                xrootd = True
            except ImportError:
                raise ImportError(
                    "Install XRootD python bindings with: conda install -c conda-forge xroot"
                )
        local_file = (
            os.path.abspath(os.path.join(".", fname))
            if xrootd
            else os.path.join(".", fname)
        )
        merged_subdirs = "/".join(subdirs) if xrootd else os.path.sep.join(subdirs)
        destination = (
            location + merged_subdirs + f"/{fname}"
            if xrootd
            else os.path.join(location, os.path.join(merged_subdirs, fname))
        )
        if xrootd:
            copyproc = XRootD.client.CopyProcess()
            copyproc.add_job(local_file, destination)
            copyproc.prepare()
            copyproc.run()
            client = XRootD.client.FileSystem(
                location[: location[pfx_len:].find("/") + pfx_len]
            )
            status = client.locate(
                destination[destination[pfx_len:].find("/") + pfx_len + 1 :],
                XRootD.client.flags.OpenFlags.READ,
            )
            assert status[0].ok
            del client
            del copyproc
        else:
            dirname = os.path.dirname(destination)
            if not os.path.exists(dirname):
                pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
            if os.path.isfile(destination):
              if not os.path.samefile(local_file, destination):
                shutil.copy2(local_file, destination)
              else:
                fname = "condor_" + fname
                destination = os.path.join(location, os.path.join(merged_subdirs, fname))
                shutil.copy2(local_file, destination)
            else:
                shutil.copy2(local_file, destination)
            assert os.path.isfile(destination)
        pathlib.Path(local_file).unlink()


    def selectByTrigger(self, events, extraColls = []):
        ### Apply trigger selection
        ### TODO:: Save a per-event flag that classifies the event (ee or mumu)
        if self.era == 2018:
            cutAnyHLT = (events.HLT.IsoMu24) | (events.HLT.Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8) | (events.HLT.Ele32_WPTight_Gsf) | (events.HLT.Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) | (events.HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) | (events.HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL)
            return events[cutAnyHLT], [coll[cutAnyHLT] for coll in extraColls]
        if self.era == 2017:
            cutAnyHLT = (events.HLT.IsoMu27) | (events.HLT.Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) | (events.HLT.Ele35_WPTight_Gsf) | (events.HLT.Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) | (events.HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) | (events.HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)
            return events[cutAnyHLT], [coll[cutAnyHLT] for coll in extraColls]
        if self.era == 2016:
            cutAnyHLT = (events.HLT.IsoMu24) | (events.HLT.Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ) | (events.HLT.Ele27_WPTight_Gsf) | (events.HLT.Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) | (events.HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) | (events.HLT.Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ)
            return events[cutAnyHLT], [coll[cutAnyHLT] for coll in extraColls]
        return events, [coll[cutAnyHLT] for coll in extraColls]

    def selectByLeptons(self, events, extraColls = []):
    ###lepton selection criteria--4momenta collection for plotting

        muons = ak.zip({
            "pt": events.Muon.pt,
            "eta": events.Muon.eta,
            "phi": events.Muon.phi,
            "mass": events.Muon.mass,
            "charge": events.Muon.pdgId/(-13),
        }, with_name="Momentum4D")
	
        electrons = ak.zip({
            "pt": events.Electron.pt,
            "eta": events.Electron.eta,
            "phi": events.Electron.phi,
            "mass": events.Electron.mass,
            "charge": events.Electron.pdgId/(-11),
        }, with_name="Momentum4D")

        ###  Some very simple selections on ID ###
        ###  Muons: loose ID + dxy dz cuts mimicking the medium prompt ID https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
        ###  Electrons: loose ID + dxy dz cuts for promptness https://twiki.cern.ch/twiki/bin/view/CMS/EgammaCutBasedIdentification
        cutMuons     = (events.Muon.looseId) & (events.Muon.pt >= 10) & (abs(events.Muon.dxy) <= 0.02) & (abs(events.Muon.dz) <= 0.1)
        cutElectrons = (events.Electron.cutBased >= 2) & (events.Electron.pt >= 15)

        ### Apply the cuts
        # Object selection. selMuons contain only the events that are filtered by cutMuons criteria.
        selMuons     = muons[cutMuons]
        selElectrons = electrons[cutElectrons]

        ### Now global cuts to select events. Notice this means exactly two leptons with pT >= 10, and the leading one pT >= 25

        # cutHasTwoMuons imposes three conditions:
        #  First, number of muons (axis=1 means column. Each row is an event.) in an event is 2.
        #  Second, pt of the muons is greater than 25.
        #  Third, Sum of charge of muons should be 0. (because it originates from Z)
        cutHasTwoMuons = (ak.num(selMuons, axis=1)==2) & (ak.max(selMuons.pt, axis=1, mask_identity=False) >= 25) & (ak.sum(selMuons.charge,axis=1) == 0)
        cutHasTwoElecs = (ak.num(selElectrons, axis=1)==2) & (ak.max(selElectrons.pt, axis=1, mask_identity=False) >= 25) & (ak.sum(selElectrons.charge,axis=1) == 0)
        cutTwoLeps     = ((ak.num(selElectrons, axis=1)+ak.num(selMuons, axis=1)) < 4)
        cutHasTwoLeps  = ((cutHasTwoMuons) | (cutHasTwoElecs)) & cutTwoLeps

        ### Cut the events, also return the selected leptons for operation down the line

        events = events[ cutHasTwoLeps]
        return events, selElectrons[cutHasTwoLeps], selMuons[cutHasTwoLeps], [coll[cutHasTwoLeps] for coll in extraColls]

    def selectByJets(self, events, leptons = [],  extraColls = []):
        # These are just standard jets, as available in the nanoAOD
        Jets = ak.zip({
            "pt": events.Jet.pt,
            "eta": events.Jet.eta,
            "phi": events.Jet.phi,
            "mass": events.Jet.mass,
            "btag": events.Jet.btagDeepFlavB,
            "jetId": events.Jet.jetId
        }, with_name="Momentum4D")
        # Minimimum pT, eta requirements + jet-lepton recleaning
        jetCut = (Jets.pt > 30) & (abs(Jets.eta)<4.7) & (Jets.deltaR(leptons[:,0])>= 0.4) & (Jets.deltaR(leptons[:,1])>= 0.4)
        jets = Jets[jetCut]
        # The following is the collection of events and of jets
        return events, jets, [coll for coll in extraColls]

    def selectByTracks(self, events, leptons, extraColls = []):
        # region : PARTICLE FLOW CANDIDATES
        # Every particle in particle flow (clean PFCand matched to tracks collection)
        Cands = ak.zip({
            "pt": events.PFCands.trkPt,
            "eta": events.PFCands.trkEta,
            "phi": events.PFCands.trkPhi,
            "mass": events.PFCands.mass
        }, with_name="Momentum4D")

        cutPF = (events.PFCands.fromPV > 1) & \
            (events.PFCands.trkPt >= 1) & \
            (abs(events.PFCands.trkEta) <= 2.5) & \
            (abs(events.PFCands.dz) < 10) & \
            (events.PFCands.dzErr < 0.05)
        Cleaned_cands = ak.packed(Cands[cutPF])
        # endregion

	    # region: LOST TRACKS
        # Unidentified tracks, usually SUEP Particles
        LostTracks = ak.zip({
            "pt": events.lostTracks.pt,
            "eta": events.lostTracks.eta,
            "phi": events.lostTracks.phi,
            "mass": 0.0
        }, with_name="Momentum4D")

        cutLost = (events.lostTracks.fromPV > 1) & \
            (events.lostTracks.pt >= 1) & \
            (abs(events.lostTracks.eta) <= 1.0) \
            & (abs(events.lostTracks.dz) < 10) & \
            (events.lostTracks.dzErr < 0.05)
        Lost_Tracks_cands = ak.packed(LostTracks[cutLost])

        # dimensions of tracks = events x tracks in event x 4 momenta
        totalTracks = ak.concatenate([Cleaned_cands, Lost_Tracks_cands], axis=1)

        # Sorting out the tracks that overlap with leptons
        totalTracks = totalTracks[(totalTracks.deltaR(leptons[:,0])>= 0.4) & (totalTracks.deltaR(leptons[:,1])>= 0.4)]
        nTracks = ak.num(totalTracks,axis=1)
        # endregion

        # region: SIM TRACKS
        # This part tags tracks from signal and those from background.

        if self.SimTrack:
            SimTracks = ak.zip({
                "pt": events.SimTracks.pt,
                "eta": events.SimTracks.eta,
                "phi": events.SimTracks.phi,
                "mass":  events.SimTracks.mass,
                "igen": events.SimTracks.igenPart,
                "fromSUEP": False,
            }, with_name="Momentum4D")
            #### SIMTRACK - GENPART Matching
            GenParts  = ak.zip({ 
                "pdgId"   : events.GenPart.pdgId,
                "motherId": events.GenPart.genPartIdxMother,
                "fromSUEP": -1,
            })
            while(ak.any(GenParts.fromSUEP == -1)):
                GenParts.fromSUEP = ak.where(GenParts.motherId == -1, 0, GenParts.fromSUEP)
                GenParts.fromSUEP = ak.where(GenParts.pdgId    ==  999998, 1, GenParts.fromSUEP)
                GenParts.pdgId    = ak.where(GenParts.fromSUEP == -1, GenParts[GenParts.motherId].pdgId, GenParts.pdgId)
                GenParts.motherId = ak.where(GenParts.fromSUEP == -1, GenParts[GenParts.motherId].motherId, GenParts.motherId)
                GenParts.fromSUEP = ak.where(GenParts.pdgId    ==  999998, 1, GenParts.fromSUEP)

            SimTracks.fromSUEP   = ak.where(SimTracks.igen >= 0, GenParts.fromSUEP[SimTracks.igen] == 1, False)
            newtotaltracks, newsimtracks = ak.unzip(ak.cartesian([totalTracks, SimTracks], axis=1, nested=True))
            alldr2 = newtotaltracks.deltaR2(newsimtracks)
            totalTracks.fromSUEP = ak.where(ak.min(alldr2, axis=2) < 0.01, SimTracks.fromSUEP[ak.argmin(alldr2, axis=2)], False)

            suepTracks = totalTracks[totalTracks.fromSUEP == True]
            backTracks = totalTracks[totalTracks.fromSUEP == False]
            return events, totalTracks, suepTracks, backTracks, nTracks, [coll for coll in extraColls]
        # endregion
        
        return events, totalTracks, [coll for coll in extraColls]

    def clusterizeTracks(self, events, tracks):
         # anti-kt, dR=1.5 jets
         jetdef = fastjet.JetDefinition(fastjet.antikt_algorithm, 1.5)        
         cluster = fastjet.ClusterSequence(tracks, jetdef)
         ak15_jets   = ak.with_name(cluster.inclusive_jets(min_pt=0),"Momentum4D") # These are the ak15_jets
         ak15_consts = ak.with_name(cluster.constituents(min_pt=0),"Momentum4D")   # And these are the collections of constituents of the ak15_jets

         return events, ak15_jets, ak15_consts
    """
    def striptizeTracks(self, events, tracks):
        # This returns the number of SUEP tracks that lies in between certain eta selection.
        dEta = 0.8
        etas = np.linspace(-3,3,10)
        nSUEPtracksPerEta = [0] * len(etas)

        for i in range(len(etas)):
            nSUEPtrack = [0] * len(tracks)
            stripCut = ((etas[i] - dEta) < tracks.eta) & (tracks.eta < (etas[i] + dEta))
            for j in range(len(stripCut)): 
                nSUEPtrack[j] = [sum(stripCut[j]),etas[i]]
            nSUEPtracksPerEta[i] = nSUEPtrack

        nSUEPtracksPerEta = np.swapaxes(nSUEPtracksPerEta,0,2)

        maxEtaIdx = [np.argmax(i) for i in nSUEPtracksPerEta[0]]
        etas = nSUEPtracksPerEta[1]
        maxEtas = [etas[:,i][0] for i in maxEtaIdx]
        stripcut = [((np.array(maxEtas)-dEta)[i] < tracks[i].eta) & ((np.array(maxEtas)+dEta)[i] < tracks[i].eta) for i in range(len(tracks.eta))]
        striptizedTracks = tracks[stripcut]

        return events, tracks, striptizedTracks
    """

    def selectByGEN(self, events):
        GenParts = ak.zip({
            "pt": events.GenPart.pt,
            "eta": events.GenPart.eta,
            "phi": events.GenPart.phi,
            "mass": events.GenPart.mass
        }, with_name="Momentum4D")
        cutgenZ    = (events.GenPart.pdgId == 23) & (events.GenPart.status == 62)
        cutgenH    = (events.GenPart.pdgId == 25) & (events.GenPart.status == 62)
        cutgenSUEP = (events.GenPart.pdgId == 999999) & (events.GenPart.status == 2)
        return events, GenParts[cutgenZ], GenParts[cutgenH], GenParts[cutgenSUEP]

    def shouldContinueAfterCut(self, events, out):
        #if debug: print("Conversion to pandas...")
        if len(events) == 0:
            outdfs  = []
            outcols = []
            for channel in out.keys():
                outcols.append(channel)
                if out[channel][0] == {}:   
                    outdfs = pd.DataFrame(['empty'], columns=['empty'])
                else:              
                    if self.isMC:
                        out[channel][0]["genweight"] = out[channel][1].genWeight[:]

                    if not isinstance(out[channel][0], pd.DataFrame): 
                        out[channel][0] = self.ak_to_pandas(out[channel][0])


            self.save_dfs([out,out],["lepvars","jetvars"])
            return False
        else:
            return True

    def process(self, events):
        #print(events.event[0], events.luminosityBlock[0], events.run[0])
        # 255955082 94729 1
        #if not(events.event[0]==255955082 and events.luminosityBlock[0]==94729 and events.run[0]==1): return self.accumulator.identity()
        debug    = True  # If we want some prints in the middle
        chunkTag = "out_%i_%i_%i.hdf5"%(events.event[0], events.luminosityBlock[0], events.run[0]) #Unique tag to get different outputs per tag
        self.doTracks = True  # Make it false, and it will speed things up but not run the tracks
        self.doClusters = True
        self.doStrips = True
        self.doGen    = True # In case we want info on the gen level --- MAKE THIS FALSE FOR BG!
        # Main processor code


        # ------------------------------------------------------------------------------------
        # ------------------------------- DEFINE OUTPUTS -------------------------------------
        # ------------------------------------------------------------------------------------

        accumulator    = self.accumulator.identity()
        # Each track is one selection level
        outputs = {
            "twoleptons":[{},[]], # Has Two Leptons, pT and Trigger requirements
            "onetrack"  :[{},[]], # + at least one track
            "onecluster":[{},[]],
        #    "onestrip"  :[{},[]]
        }

        # Data dependant stuff
        dataset = events.metadata['dataset']
        if self.isMC:      self.gensumweight = ak.sum(events.genWeight)
        if not(self.isMC): doGen = False

        # ------------------------------------------------------------------------------------
        # ------------------------------- OBJECT LOADING -------------------------------------
        # ------------------------------------------------------------------------------------

        # Lepton selection
        if debug: print("Applying lepton requirements.... %i events in"%len(events))
        self.events, self.electrons, self.muons = self.selectByLeptons(events)[:3]
        if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator # If we have no events, we simply stop
        # Trigger selection
        if debug: print("%i events pass lepton cuts. Applying trigger requirements...."%len(self.events))
        self.events, [self.electrons, self.muons] = self.selectByTrigger(self.events,[self.electrons, self.muons])

        # Here we join muons and electrons into leptons and sort them by pT
        self.leptons = ak.concatenate([self.electrons, self.muons], axis=1)
        highpt_leptons = ak.argsort(self.leptons.pt, axis=1, ascending=False, stable=True)
        self.leptons = self.leptons[highpt_leptons]
        if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
        if debug: print("%i events pass trigger cuts. Selecting jets..."%len(self.events))

        # Now do jet selection, for the moment no jet cuts
        self.events, self.jets = self.selectByJets(self.events, self.leptons)[:2] # Leptons are needed to do jet-lepton cleaning
	    # Sorting jets by pt.
        highpt_jets = ak.argsort(self.jets.pt, axis=1, ascending=False, stable=True)
        self.jets   = self.jets[highpt_jets]

        if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
        if debug: print("%i events pass jet cuts. Selecting tracks..."%len(self.events))
        
        self.SimTrack = True

        if self.doTracks:
            if self.SimTrack:
                self.events, self.tracks, self.suepTracks, self.backTracks = self.selectByTracks(self.events, self.leptons)[:4]
            else:
                self.events, self.tracks = self.selectByTracks(self.events, self.leptons)[:2]
            if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
            if debug: print("%i events pass track cuts. Doing more stuff..."%len(self.events))

        if self.doClusters:
            self.events, self.clusters, self.constituents = self.clusterizeTracks(self.events, self.tracks)[:3]
            #each track in self.clusters has form {px: 0.817, py: 0.686, pz: -3.84, E: 3.99}

        """
        if self.doStrips:
            if self.SimTrack:
                self.suepEvents, self.totalSuepTracks, self.striptizedTracks = self.striptizeTracks(self.events, self.suepTracks)[:3]
            else:
                self.events, self.strips, self.striptizedTracks = self.striptizeTracks(self.events, self.tracks)[:3]
            if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
        """

        if self.doGen:
            self.events, self.genZ, self.genH, self.genSUEP = self.selectByGEN(self.events)[:4]
            if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
            if debug: print("%i events pass gen cuts. Doing more stuff..."%len(self.events))

        # Now deal with the Z candidate
        self.Zcands = self.leptons[:,0] + self.leptons[:,1]
        
        # ------------------------------------------------------------------------------
        # ------------------------------- SELECTION + PLOTTING -------------------------
        # ------------------------------------------------------------------------------
        self.isSpherable   = True # So we don't do sphericity plots
        self.isClusterable = False # So we don't do cluster plots without clusters
        self.isStripable   = False

        outputs["twoleptons"] = [self.doAllPlots("twoleptons", debug), self.events]
        if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
        if debug: print("%i events pass twoleptons cuts. Doing more stuff..."%len(self.events))

        if self.doTracks:
            cutOneTrack = (ak.num(self.tracks) != 0)
            self.applyCutToAllCollections(cutOneTrack)
            self.isSpherable = False # So we do sphericity plots
            outputs["onetrack"] = [self.doAllPlots("onetrack", debug), self.events]
            if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
            if debug: print("%i events pass onetrack cuts. Doing more stuff..."%len(self.events))

        if self.doClusters:
            cutOneCluster = (ak.num(self.clusters) != 0)
            self.applyCutToAllCollections(cutOneCluster)
            self.isClusterable = False # So we do cluster plots
            outputs["onecluster"] = [self.doAllPlots("onecluster", debug), self.events]
            if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
            if debug: print("%i events pass onecluster cuts. Doing more stuff..."%len(self.events))

        
        if self.doStrips:
            #cutOneStrip = (ak.num(self.striptizedTracks) != 0)
            #self.applyCutToAllCollections(cutOneStrip)
            self.isStripable = True
            #outputs["onestrip"] = [self.doAllPlots("onestrip", debug), self.events]
            #if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
            #if debug: print("%i events pass onestrip cuts. Doing more stuff..."%len(self.events))
        


        # ------------------------------------------------------------------------------
        # -------------------------------- SAVING --------------------------------------
        # ------------------------------------------------------------------------------

        for out in outputs:
            if self.isMC:
                outputs[out][0]["genweight"] = outputs[out][1].genWeight[:]
            if debug: print("Conversion to pandas...")
            if not isinstance(outputs[out][0], pd.DataFrame):
                if debug: print("......%s"%out)
                outputs[out][0] = self.ak_to_pandas(outputs[out][0])

        if debug: print("DFS saving....")

        self.save_dfs([outputs[key][0] for key in outputs], [key for key in outputs], chunkTag)

        return accumulator
   

    def applyCutToAllCollections(self, cut): # Cut has to by a selection applicable across all collections, i.e. something defined per event
        self.events    = self.events[cut]
        self.electrons = self.electrons[cut]
        self.muons     = self.muons[cut]
        self.leptons   = self.leptons[cut]
        self.jets      = self.jets[cut]
        self.Zcands    = self.Zcands[cut]
        if self.doTracks:
            self.tracks  = self.tracks[cut]
            if self.SimTrack:
                self.suepTracks = self.suepTracks[cut]
            if self.doClusters:
                self.clusters     = self.clusters[cut]
                self.constituents = self.constituents[cut]
            #if self.doStrips:
            #    self.striptizedTracks = self.striptizedTracks[cut]
        if self.doGen:
            self.genZ    = self.genZ[cut]
            self.genH    = self.genH[cut]
            self.genSUEP = self.genSUEP[cut]

    def doAllPlots(self, channel, debug=True):
        # ------------------------------------------------------------------------------
        # ------------------------------- PLOTTING -------------------------------------
        # ------------------------------------------------------------------------------
        out = {}
        # Define outputs for plotting
        if debug: print("Saving reco variables for channel %s"%channel)
        """
        # region Object: leptons
        out["leadlep_pt"]    = self.leptons.pt[:,0]
        out["subleadlep_pt"] = self.leptons.pt[:,1]
        out["leadlep_eta"]   = self.leptons.eta[:,0]
        out["subleadlep_eta"]= self.leptons.eta[:,1]
        out["leadlep_phi"]   = self.leptons.phi[:,0]
        out["subleadlep_phi"]= self.leptons.phi[:,1]
        out["nleptons"]      = ak.num(self.leptons, axis=1)[:]
        out["nmuons"]        = ak.num(self.muons) 
        out["nelectrons"]    = ak.num(self.electrons)
        #endregion

        # region Object: reconstructed Z
        out["Z_px"]  = self.Zcands.px[:]
        out["Z_py"]  = self.Zcands.py[:]
        out["Z_pz"]  = self.Zcands.pz[:]
        out["Z_pt"]  = self.Zcands.pt[:]

        out["Z_eta"] = self.Zcands.eta[:]
        out["Z_phi"] = self.Zcands.phi[:]
        out["Z_m"]   = self.Zcands.mass[:]
        #endregion
        
        # region Object: jets, a bit tricky as number varies per event!
        out["njets"]          = ak.num(self.jets, axis=1)[:]
        out["nBLoose"]        = ak.sum((self.jets.btag >= 0.0490), axis=1)[:]
        out["nBMedium"]       = ak.sum((self.jets.btag >= 0.2783), axis=1)[:]
        out["nBTight"]        = ak.sum((self.jets.btag >= 0.7100), axis=1)[:]

        out["leadjet_pt"]     = ak.fill_none(ak.pad_none(self.jets.pt,  1, axis=1, clip=True), 0.)[:,0] # So take all events, if there is no jet_pt fill it with none, then replace none with 0
        out["leadjet_eta"]    = ak.fill_none(ak.pad_none(self.jets.eta, 1, axis=1, clip=True), -999)[:,0] # So take all events, if there is no jet_pt fill it with none, then replace none with -999
        out["leadjet_phi"]    = ak.fill_none(ak.pad_none(self.jets.phi, 1, axis=1, clip=True), -999)[:,0] # So take all events, if there is no jet_pt fill it with none, then replace none with -999

        out["subleadjet_pt"]  = ak.fill_none(ak.pad_none(self.jets.pt,  2, axis=1, clip=True), 0.)[:,1] # So take all events, if there is no jet_pt fill it with none, then replace none with 0
        out["subleadjet_eta"] = ak.fill_none(ak.pad_none(self.jets.eta, 2, axis=1, clip=True), -999)[:,1] # So take all events, if there is no jet_pt fill it with none, then replace none with -999
        out["subleadjet_phi"] = ak.fill_none(ak.pad_none(self.jets.phi, 2, axis=1, clip=True), -999)[:,1] # So take all events, if there is no jet_pt fill it with none, then replace none with -999

        out["trailjet_pt"]    = ak.fill_none(ak.pad_none(self.jets.pt,  3, axis=1, clip=True), 0.)[:,2] # So take all events, if there is no jet_pt fill it with none, then replace none with 0
        out["trailjet_eta"]   = ak.fill_none(ak.pad_none(self.jets.eta, 3, axis=1, clip=True), -999)[:,2] # So take all events, if there is no jet_pt fill it with none, then replace none with -999
        out["trailjet_phi"]   = ak.fill_none(ak.pad_none(self.jets.phi, 3, axis=1, clip=True), -999)[:,2] # So take all events, if there is no jet_pt fill it with none, then replace none with -999

        #### ALL JETS PROPERTIES ####
        ##maxnjets = ak.max(ak.num(self.jets, axis=1)) # We need to know the maximum to do the proper padding
        ##out["alljets_pt"]      = ak.fill_none(ak.pad_none(self.jets.pt,  maxnjets, axis=1, clip=True), 0.)
        ##out["alljets_eta"]     = ak.fill_none(ak.pad_none(self.jets.eta,  maxnjets, axis=1, clip=True), -999.)
        ##out["alljets_phi"]     = ak.fill_none(ak.pad_none(self.jets.phi,  maxnjets, axis=1, clip=True), -999.)
        #endregion
        """

        if self.doTracks:
            out["ntracks"]     = ak.num(self.tracks, axis=1)[:]
            ##maxntracks         = ak.max(ak.num(self.tracks, axis=1))
            ##out["tracks_pt"]   = ak.fill_none(ak.pad_none(self.tracks.pt,  maxntracks, axis=1, clip=True), 0.)
            ##out["tracks_eta"]  = ak.fill_none(ak.pad_none(self.tracks.eta,  maxntracks, axis=1, clip=True), -999.)
            ##out["tracks_phi"]  = ak.fill_none(ak.pad_none(self.tracks.phi,  maxntracks, axis=1, clip=True), -999.)

            maxEta = ak.max(self.suepTracks.eta, axis=1)
            minEta = ak.min(self.suepTracks.eta, axis=1)
            out["boostS_deltaEta"] = (maxEta - minEta)[:]

            phi = ak.where(self.suepTracks.phi < 0,2*np.pi + self.suepTracks.phi, self.suepTracks.phi) #transform phi range to 0:2pi
            phiCombo = ak.combinations(phi,2,fields=["phi1","phi2"])
            phiComboDiff = abs(phiCombo.phi1-phiCombo.phi2) #difference in two phi values
            phiComboDiff = ak.where(phiComboDiff > np.pi, 2*np.pi - phiComboDiff, phiComboDiff)
            maxPhiComboDiff = ak.max(phiComboDiff,axis=1) #max difference in phi in each event
            
            out["boostS_deltaPhi"] = maxPhiComboDiff[:]

            if self.isSpherable:
              
                # Reconstructing by setting pS = -pZ 
                boost_Zinv = ak.zip({
                    "px": self.Zcands.px,
                    "py": self.Zcands.py,
                    "pz": self.Zcands.pz,
                    "mass": self.Zcands.mass
                }, with_name="Momentum4D") 

                # Reconstructing by summing all tracks
                boost_tracks = ak.zip({
                    "px": ak.sum(self.tracks.px, axis=1)*-1,
                    "py": ak.sum(self.tracks.py, axis=1)*-1,
                    "pz": ak.sum(self.tracks.pz, axis=1)*-1,
                    "mass": 125 # Assuming it is a Higgs?
                }, with_name="Momentum4D")

                tracks_boostedagainstZ      = self.tracks.boost_p4(boost_Zinv)
                tracks_boostedagainsttracks = self.tracks.boost_p4(boost_tracks)

                evalsL = self.sphericity(self.events, self.tracks, 2) # Gives the sphericity in Lab frame
                evalsZ = self.sphericity(self.events, tracks_boostedagainstZ, 2) #Gives the sphericity in -Z frame (-pZ = pS)
                evalsT = self.sphericity(self.events, tracks_boostedagainsttracks, 2) #Gives the sphericity in -Z frame (tracks)

                #region: OUTPUT FOR SPHERICITY

                ### Boosts ###
                out["boostZ_px"] = boost_Zinv.px
                out["boostZ_py"] = boost_Zinv.py
                out["boostZ_pz"] = boost_Zinv.pz
                out["boostZ_pt"] = boost_Zinv.pt
                
                out["boostT_px"] = boost_tracks.px
                out["boostT_py"] = boost_tracks.py
                out["boostT_pt"] = boost_tracks.pt
                out["boostT_pz"] = boost_tracks.pz

                ### Evals themselves ###
                out["eval_L1"] = evalsL[:,0]
                out["eval_L2"] = evalsL[:,1]
                out["eval_L3"] = evalsL[:,2]
                out["eval_Z1"] = evalsZ[:,0]
                out["eval_Z2"] = evalsZ[:,1]
                out["eval_Z3"] = evalsZ[:,2]
                out["eval_T1"] = evalsT[:,0]
                out["eval_T2"] = evalsT[:,1]
                out["eval_T3"] = evalsT[:,2]

                ### Scalar Sphericity ###
                out["scalarSpher_L"] = 1.5*(evalsL[:,0] + evalsL[:,1])
                out["scalarSpher_Z"] = 1.5*(evalsZ[:,0] + evalsZ[:,1])
                out["scalarSpher_T"] = 1.5*(evalsT[:,0] + evalsT[:,1])

                ### Mean Difference ###
                out["meanDiff_L"] = np.mean(np.stack([evalsL[:,2]-evalsL[:,1], evalsL[:,2]-evalsL[:,0], evalsL[:,1]-evalsL[:,0]]), axis=0)
                out["meanDiff_Z"] = np.mean(np.stack([evalsZ[:,2]-evalsZ[:,1], evalsZ[:,2]-evalsZ[:,0], evalsZ[:,1]-evalsZ[:,0]]), axis=0)
                out["meanDiff_T"] = np.mean(np.stack([evalsT[:,2]-evalsT[:,1], evalsT[:,2]-evalsT[:,0], evalsT[:,1]-evalsT[:,0]]), axis=0)
                #endregion

            if self.doClusters and self.isClusterable:

                out["nclusters"]           = ak.num(self.clusters, axis=1)[:]
                #maxnclusters              = ak.max(ak.num(self.clusters, axis=1))
                out["leadcluster_pt"]      = self.clusters.pt[:,-1]
                out["leadcluster_eta"]     = self.clusters.eta[:,-1]
                out["leadcluster_phi"]     = self.clusters.phi[:,-1]
                out["leadcluster_ntracks"] = ak.num(self.constituents[:,-1], axis = 1)
                
                boost_leading = ak.zip({
                    "px": self.clusters[:,-1].px*-1,
                    "py": self.clusters[:,-1].py*-1,
                    "pz": self.clusters[:,-1].pz*-1,
                    "mass": self.clusters[:,-1].mass
                }, with_name="Momentum4D")

                leadingclustertracks = self.constituents[:,-1]
                leadingclustertracks_boostedagainstZ      = leadingclustertracks.boost_p4(boost_Zinv)
                leadingclustertracks_boostedagainsttracks = leadingclustertracks.boost_p4(boost_tracks)
                leadingclustertracks_boostedagainstSUEP   = leadingclustertracks.boost_p4(boost_leading)

                evalsL = self.sphericity(self.events, leadingclustertracks, 2) 
                evalsZ = self.sphericity(self.events, leadingclustertracks_boostedagainstZ, 2)
                evalsT = self.sphericity(self.events, leadingclustertracks_boostedagainsttracks, 2)
                evalsC = self.sphericity(self.events, leadingclustertracks_boostedagainstSUEP, 2)

                out["boostC_px"] = boost_leading.px
                out["boostC_py"] = boost_leading.py
                out["boostC_pz"] = boost_leading.pz
                out["boostC_pt"] = boost_leading.pt

                out["leadclusterSpher_L"] =  np.real(1.5*(evalsL[:,0] + evalsL[:,1]))
                out["leadclusterSpher_Z"] =  np.real(1.5*(evalsZ[:,0] + evalsZ[:,1]))
                out["leadclusterSpher_T"] =  np.real(1.5*(evalsT[:,0] + evalsT[:,1]))
                out["leadclusterSpher_C"] =  np.real(1.5*(evalsC[:,0] + evalsC[:,1]))

        #if self.doStrips and self.isStripable:
            """
            boost_leadStrip = ak.zip({
                "px": ak.sum(self.striptizedTracks.px, axis=1)*-1,
                "py": ak.sum(self.striptizedTracks.py, axis=1)*-1,
                "pz": ak.sum(self.striptizedTracks.pz, axis=1)*-1,
                "mass": 125 # Assuming it is a Higgs?
            }, with_name="Momentum4D")

            out["boostS_px"] = boost_leadStrip.px
            out["boostS_py"] = boost_leadStrip.py
            out["boostS_pz"] = boost_leadStrip.pz
            out["boostS_pt"] = boost_leadStrip.pt
            """

        if self.doGen:
            if debug: print("Saving gen variables")
            
            out["genZpt"]  = self.genZ.pt[:,0]
            out["genZpz"]  = self.genZ.pz[:,0]
            out["genZeta"] = self.genZ.eta[:,0]
            out["genZphi"] = self.genZ.phi[:,0]

            out["genHpx"]  = self.genH.px[:,0]
            out["genHpy"]  = self.genH.py[:,0]
            out["genHpz"]  = self.genH.pz[:,0]
            out["genHpt"]  = self.genH.pt[:,0]
            
            out["genHeta"] = self.genH.eta[:,0]
            out["genHphi"] = self.genH.phi[:,0]

        return out

    def postprocess(self, accumulator):
        return accumulator