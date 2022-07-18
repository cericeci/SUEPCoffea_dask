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
        ### PARTICLE FLOW CANDIDATES ###
        # Every particle in particle flow (clean PFCand matched to tracks collection)
        Cands = ak.zip({
            "pt": events.PFCands.trkPt,
            "eta": events.PFCands.trkEta,
            "phi": events.PFCands.trkPhi,
            "mass": events.PFCands.mass,
            "fromPV": events.PFCands.fromPV,
            "d0": events.PFCands.d0,
            "d0Err": events.PFCands.d0Err,
            "dz": events.PFCands.dz,
            "dzErr": events.PFCands.dzErr,
            "puppiWeight": events.PFCands.puppiWeight,
            "puppiWeightNoLep": events.PFCands.puppiWeightNoLep,
            "vtxChi2": events.PFCands.vtxChi2,
            "pvAssocQuality": events.PFCands.pvAssocQuality,
            "fromSUEP": False,
        }, with_name="Momentum4D")

        cutPF = (events.PFCands.fromPV > 0) & \
            (events.PFCands.trkPt >= 0.5) & \
            (abs(events.PFCands.trkEta) <= 5) & \
            (abs(events.PFCands.dz) < 10) & \
            (events.PFCands.dzErr < 1.0)
        Cleaned_cands = ak.packed(Cands[cutPF])

	### LOST TRACKS ###
        # Unidentified tracks, usually SUEP Particles
        LostTracks = ak.zip({
            "pt": events.lostTracks.pt,
            "eta": events.lostTracks.eta,
            "phi": events.lostTracks.phi,
            "mass": 0.0,
            "fromPV": events.lostTracks.fromPV,
            "d0": events.lostTracks.d0,
            "d0Err": events.lostTracks.d0Err,
            "dz": events.lostTracks.dz,
            "dzErr": events.lostTracks.dzErr,
            "puppiWeight": events.lostTracks.puppiWeight,
            "puppiWeightNoLep": events.lostTracks.puppiWeightNoLep,
            "vtxChi2": events.lostTracks.vtxChi2,
            "pvAssocQuality": events.lostTracks.pvAssocQuality,
            "fromSUEP": False,
        }, with_name="Momentum4D")

        cutLost = (events.lostTracks.fromPV > 0) & \
            (events.lostTracks.pt >= 0.5) & \
            (abs(events.lostTracks.eta) <= 5.0) \
            & (abs(events.lostTracks.dz) < 10) & \
            (events.lostTracks.dzErr < 1.0)
        Lost_Tracks_cands = ak.packed(LostTracks[cutLost])

        # dimensions of tracks = events x tracks in event x 4 momenta
        totalTracks = ak.concatenate([Cleaned_cands, Lost_Tracks_cands], axis=1)

        # Sorting out the tracks that overlap with leptons
        totalTracks = totalTracks[(totalTracks.deltaR(leptons[:,0])>= 0.4) & (totalTracks.deltaR(leptons[:,1])>= 0.4)]
        nTracks = ak.num(totalTracks,axis=1)
        
        #### SIMTRACKS, for gen matching association ####
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
            "status"  : events.GenPart.status,
            "fromSUEP": -1,
        })
        while(ak.any(GenParts.fromSUEP < 0)):
          print(ak.sum(GenParts.fromSUEP == -4), ak.sum(GenParts.fromSUEP == -3), ak.sum(GenParts.fromSUEP == -1), ak.sum(GenParts.fromSUEP == -0), ak.sum(GenParts.fromSUEP == 1),ak.sum(GenParts.fromSUEP == 2), ak.sum(GenParts.fromSUEP == 3), ak.sum(GenParts.fromSUEP == 4))
          GenParts.fromSUEP = ak.where((GenParts.motherId == -1) & (GenParts.fromSUEP==-3) ,   3, GenParts.fromSUEP) # UE
          GenParts.fromSUEP = ak.where((GenParts.motherId == -1) & (GenParts.fromSUEP==-4) ,   4, GenParts.fromSUEP) # ISR
          GenParts.fromSUEP = ak.where((GenParts.motherId == -1) & (GenParts.fromSUEP==-1) ,   0, GenParts.fromSUEP)    # 0 means matched to PU
          GenParts.fromSUEP = ak.where(GenParts.pdgId    ==  999998, 1, GenParts.fromSUEP) # 1 means matched to SUEP
          GenParts.fromSUEP = ak.where(GenParts.pdgId    ==  23    , 2, GenParts.fromSUEP) # 2 means matched to Z
          GenParts.fromSUEP = ak.where((GenParts.status   ==  63) & (GenParts.fromSUEP < 0)  , -3, GenParts.fromSUEP) # -3 means UE track
          GenParts.fromSUEP = ak.where((GenParts.status   ==  61) & (GenParts.fromSUEP < 0)  , -4, GenParts.fromSUEP) # -4 means emission from primary but it can still be H/Z so -1 until chain ends
          GenParts.pdgId    = ak.where(GenParts.fromSUEP < 0, GenParts[GenParts.motherId].pdgId, GenParts.pdgId)
          GenParts.motherId = ak.where(GenParts.fromSUEP < 0, GenParts[GenParts.motherId].motherId, GenParts.motherId)
          GenParts.status = ak.where(GenParts.fromSUEP < 0, GenParts[GenParts.motherId].status, GenParts.status)
          GenParts.fromSUEP = ak.where(GenParts.pdgId    ==  999998, 1, GenParts.fromSUEP) 

        SimTracks.fromSUEP   = ak.where(SimTracks.igen >= 0, GenParts.fromSUEP[SimTracks.igen] == 1, False)
        newtotaltracks, newsimtracks = ak.unzip(ak.cartesian([totalTracks, SimTracks], axis=1, nested=True))
        alldr2 = newtotaltracks.deltaR2(newsimtracks)
        totalTracks.fromSUEP = ak.where(ak.min(alldr2, axis=2) < 0.01, SimTracks.fromSUEP[ak.argmin(alldr2, axis=2)], False)

        suepTracks = totalTracks[totalTracks.fromSUEP == True]
        backTracks = totalTracks[totalTracks.fromSUEP == False]
        return events, totalTracks, suepTracks, backTracks


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
        self.doGen    = True # In case we want info on the gen level 
        # Main processor code


        # ------------------------------------------------------------------------------------
        # ------------------------------- DEFINE OUTPUTS -------------------------------------
        # ------------------------------------------------------------------------------------

        accumulator    = self.accumulator.identity()
        # Each track is one selection level
        outputs = {
            "twoleptons"  :[{},[]], # Has Two Leptons, pT and Trigger requirements
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
        
        # Right now no track cuts, only selecting tracks
        self.events, self.tracks, self.sueptracks, self.backtracks = self.selectByTracks(self.events, self.leptons)
        if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
        if debug: print("%i events pass track cuts. Doing more stuff..."%len(self.events))

        # Now deal with the Z candidate
        self.Zcands = self.leptons[:,0] + self.leptons[:,1]
        
        # ------------------------------------------------------------------------------
        # ------------------------------- SELECTION + PLOTTING -------------------------
        # ------------------------------------------------------------------------------
        self.isSpherable = False # So we don't do sphericity plots
        outputs["twoleptons"] = [self.doAllPlots("twoleptons", debug), self.events]
        if not(self.shouldContinueAfterCut(self.events, outputs)): return accumulator
        if debug: print("%i events pass twoleptons cuts. Doing more stuff..."%len(self.events))


        

        # ------------------------------------------------------------------------------
        # -------------------------------- SAVING --------------------------------------
        # ------------------------------------------------------------------------------

        for out in outputs:
            if self.isMC:
                outputs[out][0]["genweight"] = outputs[out][1].genWeight[:]
            if debug: print("Conversion to pandas...")
            if not isinstance(outputs[out][0], pd.DataFrame):
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
          self.sueptracks  = self.sueptracks[cut]
          self.backtracks  = self.backtracks[cut]

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

        # Object: leptons
        out["leadlep_pt"]    = self.leptons.pt[:,0]
        out["subleadlep_pt"] = self.leptons.pt[:,1]
        out["leadlep_eta"]   = self.leptons.eta[:,0]
        out["subleadlep_eta"]= self.leptons.eta[:,1]
        out["nleptons"]      = ak.num(self.leptons, axis=1)[:]


        # Object: reconstructed Z
        out["Z_pt"]  = self.Zcands.pt[:]
        out["Z_eta"] = self.Zcands.eta[:]
        out["Z_phi"] = self.Zcands.phi[:]
        out["Z_m"]   = self.Zcands.mass[:]
        
        # Object: jets, a bit tricky as number varies per event!
        out["njets"]          = ak.num(self.jets, axis=1)[:]
        out["nBLoose"]        = ak.sum((self.jets.btag >= 0.0490), axis=1)[:]
        out["nBMedium"]       = ak.sum((self.jets.btag >= 0.2783), axis=1)[:]
        out["nBTight"]        = ak.sum((self.jets.btag >= 0.7100), axis=1)[:]

        #### ALL JETS PROPERTIES ####
        ##maxnjets = ak.max(ak.num(self.jets, axis=1)) # We need to know the maximum to do the proper padding
        ##out["alljets_pt"]      = ak.fill_none(ak.pad_none(self.jets.pt,  maxnjets, axis=1, clip=True), 0.)
        ##out["alljets_eta"]     = ak.fill_none(ak.pad_none(self.jets.eta,  maxnjets, axis=1, clip=True), -999.)
        ##out["alljets_phi"]     = ak.fill_none(ak.pad_none(self.jets.phi,  maxnjets, axis=1, clip=True), -999.)


        if self.doTracks:
            maxntracks         = ak.max(ak.num(self.tracks, axis=1))
            for prop in ["pt", "eta", "phi", "mass", "d0", "d0Err", "dz", "dzErr", "puppiWeight", "puppiWeightNoLep", "vtxChi2", "fromPV", "pvAssocQuality", "fromSUEP"]:
              out["tracks_" + prop] = ak.fill_none(ak.pad_none(getattr(self.tracks, prop),  maxntracks, axis=1, clip=True), -999.)

        return out

    def postprocess(self, accumulator):
        return accumulator
