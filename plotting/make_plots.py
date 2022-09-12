# Make plots for SUEP analysis. Reads in hdf5 files and outputs to pickle and root files
import os, sys, subprocess
import pandas as pd 
import numpy as np
import argparse
import getpass
import uproot
import getpass
import pickle
import json
from tqdm import tqdm
from hist import Hist
from collections import defaultdict
from copy import deepcopy

#Import our own functions
import pileup_weight
import triggerSF
from plot_utils import *

parser = argparse.ArgumentParser(description='Famous Submitter')
parser.add_argument("-dataset", "--dataset"  , type=str, default="QCD", help="dataset name", required=False)
parser.add_argument("-t"   , "--tag"   , type=str, default="IronMan"  , help="production tag", required=False)
parser.add_argument("-o"   , "--output"   , type=str, default="IronMan"  , help="output tag", required=False)
parser.add_argument("-e"   , "--era"   , type=int, default=2018  , help="era", required=False)
parser.add_argument('--doSyst', type=int, default=0, help="make systematic plots")
parser.add_argument('--isMC', type=int, default=1, help="Is this MC or data")
parser.add_argument('--scouting', type=int, default=0, help="Is this scouting or no")
parser.add_argument('--blind', type=int, default=1, help="Blind the data (default=True)")
parser.add_argument('--weights', type=str, default="None", help="Pass the filename of the weights, e.g. --weights weights.npy")
parser.add_argument('--xrootd', type=int, default=0, help="Local data or xrdcp from hadoop (default=False)")
parser.add_argument('--merged', type=int, default=1, help="Use merged files")
parser.add_argument('-f', '--file', type=str, default='', help="Use specific input file")
options = parser.parse_args()

# parameters for script
output_label = options.output
outDir = "/work/submit/{}/SUEP/outputs/".format(getpass.getuser())
redirector = "root://t3serv017.mit.edu/"

"""
Define output plotting methods, each draws from an input_method (outputs of SUEPCoffea),
and can have its own selections, ABCD regions, and signal region.
Multiple plotting methods can be defined for the same input method, as different
selections and ABCD methods can be applied.
N.B.: Include lower and upper bounds for all ABCD regions.
"""
config = {
    
    'Cluster' : {
        'input_method' : 'CL',
        'xvar' :'SUEP_S1_CL',
        'xvar_regions' : [0.35, 0.4, 0.5, 1.0],
        'yvar' : 'SUEP_nconst_CL',
        'yvar_regions' : [20, 40, 80, 1000],
        'SR' : [['SUEP_S1_CL', '>=', 0.5], ['SUEP_nconst_CL', '>=', 80]],
        'selections' : [['ht', '>', 1200], ['ntracks','>', 0], ["SUEP_S1_CL", ">=", 0.0]]
    },
    
    # 'ClusterInverted' : {
    #     'input_method' : 'CL',
    #     'xvar' : 'ISR_S1_CL',
    #     'xvar_regions' : [0.35, 0.4, 0.5, 1.0],
    #     'yvar' : 'ISR_nconst_CL',
    #     'yvar_regions' : [20, 40, 80, 1000],
    #     'SR' : [['ISR_S1_CL', '>=', 0.5], ['ISR_nconst_CL', '>=', 80]],
    #     'selections' : [['ht', '>', 1200], ['ntracks','>', 10], ["ISR_S1_CL", ">=", 0.0]]
    # },
    
    # 'ISRRemoval' : {
    #     'input_method' : 'IRM',
    #     'xvar' : 'SUEP_S1_IRM',
    #     'xvar_regions' : [0.35, 0.4, 0.5, 1.0],
    #     'yvar' : 'SUEP_nconst_IRM',
    #     'yvar_regions' : [10, 20, 40, 1000],
    #     'SR' : [['SUEP_S1_IRM', '>=', 0.5], ['SUEP_nconst_IRM', '>=', 40]],
    #     'selections' : [['ht', '>', 1200], ['ntracks','>', 0], ["SUEP_S1_IRM", ">=", 0.0]]
    # },
        
#     'ResNet' : {
#         'input_method' : 'ML',
#         'xvar' : 'resnet_SUEP_pred_ML',
#         'xvar_regions' : [0.0, 0.5, 1.0],
#         'yvar' : 'ntracks',
#         'yvar_regions' : [0, 100, 1000],
#         'SR' : [['resnet_SUEP_pred_ML', '>=', 0.5], ['ntracks', '>=', 100]],
#         'selections' : [['ht', '>', 600], ['ntracks','>',0]]
#     },
    
}

#############################################################################################################
            
def plot(df, output, abcd, label_out, sys):
    """
    INPUTS:
        df: input file DataFrame.
        output: dictionary of histograms to be filled.
        abcd: definitions of ABCD regions, signal region, event selections.
        label_out: label associated with the output (e.g. "ISRRemoval"), as keys in 
                   the config dictionary.
        
    OUTPUTS: 
        output: now with updated histograms.
        
    EXPLANATION:
    The DataFrame generated by ../workflows/SUEP_coffea.py has the form:
    event variables (ht, ...)   IRM vars (SUEP_S1_IRM, ...)  ML vars  Other Methods
          0                                 0                   0          ...
          1                                 NaN                 1          ...
          2                                 NaN                 NaN        ...
          3                                 1                   2          ...
    (The event vars are always filled, while the vars for each method are filled only
    if the event passes the method's selections, hence the NaNs).
    
    This function will plot, for each 'label_out':
        1. All event variables, e.g. output histogram = ht_label_out
        2. All columns from 'input_method', e.g. SUEP_S1_IRM column will be
           plotted to histogram SUEP_S1_ISRRemoval.
        3. 2D variables are automatically plotted, as long as hstogram is
           initialized in the output dict as "2D_var1_vs_var2"
    
    N.B.: Histograms are filled only if they are initialized in the output dictionary.

    e.g. We want to plot CL. 
    Event Selection:
        1. Grab only events that don't have NaN for CL variables.
        2. Blind for data! Use SR to define signal regions and cut it out of df.
        3. Apply selections as defined in the 'selections' in the dict.

    Fill Histograms:
        1. Plot variables from the DataFrame. 
           1a. Event wide variables
           1b. Cluster method variables
        2. Plot 2D variables.
        3. Plot variables from the different ABCD regions as defined in the abcd dict.
           3a. Event wide variables
           3b. Cluster method variables
    """

    input_method = abcd['input_method']
    if len(sys) > 0: label_out = label_out + "_" + sys
    
    # 1. keep only events that passed this method
    df = df[~df[abcd['xvar']].isnull()]
        
    # 2. blind
    if options.blind and not options.isMC:       
        SR = abcd['SR']
        if len(SR) != 2: sys.exit(label_out+": Make sure you have correctly defined your signal region. Exiting.")
        df = df.loc[~(make_selection(df, SR[0][0], SR[0][1], SR[0][2], apply=False) & make_selection(df, SR[1][0], SR[1][1], SR[1][2], apply=False))]
        
    # 3. apply selections
    for sel in abcd['selections']: 
        df = make_selection(df, sel[0], sel[1], sel[2], apply=True)
    
    # auto fill all histograms in the output dictionary
    auto_fill(df, output, abcd, label_out, isMC=options.isMC, do_abcd=True)
           
    return output
        
#############################################################################################################

# get list of files
username = getpass.getuser()
if options.file:
    files = [options.file]
elif options.xrootd:
    dataDir = "/scratch/{}/SUEP/{}/{}/".format(username,options.tag,options.dataset)
    if options.merged: dataDir += "merged/"
    result = subprocess.check_output(["xrdfs",redirector,"ls",dataDir])
    result = result.decode("utf-8")
    files = result.split("\n")
    files = [f for f in files if len(f) > 0]
else:
    dataDir = "/data/submit/{}/{}/{}/".format(username, options.tag, options.dataset)
    if options.merged: dataDir += "merged/"
    files = [dataDir + f for f in os.listdir(dataDir)]

# get cross section
xsection = 1.0
if options.isMC: xsection = getXSection(options.dataset, options.era)

# event weights
puweights, puweights_up, puweights_down = pileup_weight.pileup_weight(options.era)   
trig_bins, trig_weights, trig_weights_up, trig_weights_down = triggerSF.triggerSF(options.era)

# custom per region weights
scaling_weights = None
if options.weights != "None":
    w = np.load(options.weights, allow_pickle=True)
    scaling_weights = defaultdict(lambda: np.zeros(2))
    scaling_weights.update(w.item())

# output histos
def create_output_file(label, abcd, sys):

    # don't recreate histograms if called multiple times with the same output label
    if len(sys) > 0: label += "_" + sys
    if label in output["labels"]: return output
    else: output["labels"].append(label)
    
    # ABCD histogram
    xvar = abcd['xvar']
    yvar = abcd['yvar']
    xvar_regions = abcd['xvar_regions']
    yvar_regions = abcd['yvar_regions']
    output.update({"ABCDvars_"+label : Hist.new.Reg(100, 0, yvar_regions[-1], name=xvar).Reg(100, 0, xvar_regions[-1], name=yvar).Weight()})
 
    # defnie all the regions, will be used to make historgams for each region
    regions = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n_regions = ((len(xvar_regions) - 1) * (len(yvar_regions) - 1))
    regions_list =  [""] + [regions[i]+"_" for i in range(n_regions)]
    
    # variables from the dataframe for all the events, and those in A, B, C regions
    for r in regions_list:
        output.update({
            r+"ht_" + label : Hist.new.Reg(100, 0, 10000, name=r+"ht_"+label, label='HT').Weight(),
            r+"ht_JEC_" + label : Hist.new.Reg(100, 0, 10000, name=r+"ht_JEC_"+label, label='HT JEC').Weight(),
            r+"ht_JEC_JER_up_" + label : Hist.new.Reg(100, 0, 10000, name=r+"ht_JEC_JER_up_"+label, label='HT JEC up').Weight(),
            r+"ht_JEC_JER_down_" + label : Hist.new.Reg(100, 0, 10000, name=r+"ht_JEC_JER_down_"+label, label='HT JEC JER down').Weight(),
            r+"ht_JEC_JES_up_" + label : Hist.new.Reg(100, 0, 10000, name=r+"ht_JEC_JES_up_"+label, label='HT JEC JES up').Weight(),
            r+"ht_JEC_JES_down_" + label : Hist.new.Reg(100, 0, 10000, name=r+"ht_JEC_JES_down_"+label, label='HT JEC JES down').Weight(),
            r+"ntracks_" + label : Hist.new.Reg(101, 0, 500, name=r+"ntracks_"+label, label='# Tracks in Event').Weight(),
            r+"ngood_fastjets_" + label : Hist.new.Reg(9,0, 10, name=r+"ngood_fastjets_"+label, label='# FastJets in Event').Weight(),
            r+"PV_npvs_"+label : Hist.new.Reg(199,0, 200, name=r+"PV_npvs_"+label, label="# PVs in Event ").Weight(),
            r+"Pileup_nTrueInt_"+label : Hist.new.Reg(199,0, 200, name=r+"Pileup_nTrueInt_"+label, label="# True Interactions in Event ").Weight(),
            r+"ngood_ak4jets_" + label : Hist.new.Reg(19,0, 20, name=r+"ngood_ak4jets_"+label, label= '# ak4jets in Event').Weight(),
            r+"ngood_tracker_ak4jets_" + label : Hist.new.Reg(19,0, 20, name=r+"ngood_tracker_ak4jets_"+label, label= r'# ak4jets in Event ($|\eta| < 2.4$)').Weight(),
            r+"FNR_" + label : Hist.new.Reg(50,0, 1, name=r+"FNR_"+label, label= r'# SUEP Tracks in ISR / # SUEP Tracks').Weight(),
            r+"ISR_contamination_" + label : Hist.new.Reg(50,0, 1, name=r+"ISR_contamination_"+label, label= r'# SUEP Tracks in ISR / # ISR Tracks').Weight(),
        })
    
    if any([l in label for l in ['ISRRemoval','Cluster','Cone']]):
        # 2D histograms
        output.update({
            "2D_SUEP_S1_vs_ntracks_"+label : Hist.new.Reg(100, 0, 1.0, name="SUEP_S1_"+label, label='$Sph_1$').Reg(100, 0, 500, name="ntracks_"+label, label='# Tracks').Weight(),
            "2D_SUEP_S1_vs_SUEP_nconst_"+label : Hist.new.Reg(100, 0, 1.0, name="SUEP_S1_"+label, label='$Sph_1$').Reg(200, 0, 500, name="nconst_"+label, label='# Constituents').Weight(),     
            "2D_SUEP_nconst_vs_SUEP_pt_avg_"+label : Hist.new.Reg(200, 0, 500, name="SUEP_nconst_"+label, label='# Const').Reg(200, 0, 500, name="SUEP_pt_avg_"+label, label='$p_T Avg$').Weight(), 
            "2D_SUEP_nconst_vs_SUEP_pt_avg_b_"+label : Hist.new.Reg(200, 0, 500, name="SUEP_nconst_"+label, label='# Const').Reg(50, 0, 50, name="SUEP_pt_avg_b_"+label, label='$p_T Avg (Boosted frame)$').Weight(), 
           })
        
        # variables from the dataframe for all the events, and those in A, B, C regions
        for r in regions_list:
            output.update({
                r+"SUEP_nconst_"+label : Hist.new.Reg(199, 0, 500, name=r+"SUEP_nconst_"+label, label="# Tracks in SUEP").Weight(),
                r+"SUEP_pt_"+label : Hist.new.Reg(100, 0, 2000, name=r+"SUEP_pt_"+label, label=r"SUEP $p_T$ [GeV]").Weight(),
                r+"SUEP_pt_avg_"+label : Hist.new.Reg(200, 0, 500, name=r+"SUEP_pt_avg_"+label, label=r"SUEP Components $p_T$ Avg.").Weight(),
                r+"SUEP_pt_avg_b_"+label : Hist.new.Reg(50, 0, 50, name=r+"SUEP_pt_avg_b_"+label, label=r"SUEP Components $p_T$ avg (Boosted Frame)").Weight(),
                r+"SUEP_eta_"+label : Hist.new.Reg(100,-5,5, name=r+"SUEP_eta_"+label, label=r"SUEP $\eta$").Weight(),
                r+"SUEP_phi_"+label : Hist.new.Reg(100,-6.5,6.5, name=r+"SUEP_phi_"+label, label=r"SUEP $\phi$").Weight(),
                r+"SUEP_mass_"+label : Hist.new.Reg(150, 0, 2000, name=r+"SUEP_mass_"+label, label="SUEP Mass [GeV]").Weight(),
                r+"SUEP_delta_mass_genMass_"+label : Hist.new.Reg(400, -2000, 2000, name=r+"SUEP_delta_mass_genMass_"+label, label="SUEP Mass - genSUEP Mass [GeV]").Weight(),
                r+"SUEP_S1_"+label : Hist.new.Reg(100, 0, 1, name=r+"SUEP_S1_"+label, label='$Sph_1$').Weight(),
                r+"SUEP_girth": Hist.new.Reg(50, 0, 1.0, name=r+"SUEP_girth_"+label, label=r"SUEP Girth").Weight(),
                r+"SUEP_rho0_"+label : Hist.new.Reg(50, 0, 20, name=r+"SUEP_rho0_"+label, label=r"SUEP $\rho_0$").Weight(),
                r+"SUEP_rho1_"+label : Hist.new.Reg(50, 0, 20, name=r+"SUEP_rho1_"+label, label=r"SUEP $\rho_1$").Weight(),
            })
    
    if 'ClusterInverted' in label:
        output.update({
            # 2D histograms
            "2D_ISR_S1_vs_ntracks_"+label : Hist.new.Reg(100, 0, 1.0, name="ISR_S1_"+label, label='$Sph_1$').Reg(200, 0, 500, name="ntracks_"+label, label='# Tracks').Weight(),
            "2D_ISR_S1_vs_ISR_nconst_"+label : Hist.new.Reg(100, 0, 1.0, name="ISR_S1_"+label, label='$Sph_1$').Reg(200, 0, 500, name="nconst_"+label, label='# Constituents').Weight(),     
            "2D_ISR_nconst_vs_ISR_pt_avg_"+label : Hist.new.Reg(200, 0, 500, name="ISR_nconst_"+label).Reg(500, 0, 500, name="ISR_pt_avg_"+label).Weight(), 
            "2D_ISR_nconst_vs_ISR_pt_avg_b_"+label : Hist.new.Reg(200, 0, 500, name="ISR_nconst_"+label).Reg(100, 0, 100, name="ISR_pt_avg_"+label).Weight(),  
        })
        # variables from the dataframe for all the events, and those in A, B, C regions
        for r in regions_list:
            output.update({
                r+"ISR_nconst_"+label : Hist.new.Reg(199, 0, 500, name=r+"ISR_nconst_"+label, label="# Tracks in ISR").Weight(),
                r+"ISR_pt_"+label : Hist.new.Reg(100, 0, 2000, name=r+"ISR_pt_"+label, label=r"ISR $p_T$ [GeV]").Weight(),
                r+"ISR_pt_avg_"+label : Hist.new.Reg(500, 0, 500, name=r+"ISR_pt_avg_"+label, label=r"ISR Components $p_T$ Avg.").Weight(),
                r+"ISR_pt_avg_b_"+label : Hist.new.Reg(100, 0, 100, name=r+"ISR_pt_avg_b_"+label, label=r"ISR Components $p_T$ avg (Boosted Frame)").Weight(),
                r+"ISR_eta_"+label : Hist.new.Reg(100,-5,5, name=r+"ISR_eta_"+label, label=r"ISR $\eta$").Weight(),
                r+"ISR_phi_"+label : Hist.new.Reg(100,-6.5,6.5, name=r+"ISR_phi_"+label, label=r"ISR $\phi$").Weight(),
                r+"ISR_mass_"+label : Hist.new.Reg(150, 0, 4000, name=r+"ISR_mass_"+label, label="ISR Mass [GeV]").Weight(),
                r+"ISR_S1_"+label : Hist.new.Reg(100, 0, 1, name=r+"ISR_S1_"+label, label='$Sph_1$').Weight(),
                r+"ISR_girth": Hist.new.Reg(50, 0, 1.0, name=r+"ISR_girth_"+label, label=r"ISR Girth").Weight(),
                r+"ISR_rho0_"+label : Hist.new.Reg(100, 0, 20, name=r+"ISR_rho0_"+label, label=r"ISR $\rho_0$").Weight(),
                r+"ISR_rho1_"+label : Hist.new.Reg(100, 0, 20, name=r+"ISR_rho1_"+label, label=r"ISR $\rho_1$").Weight(),
            })
    
    if label == 'ML':
        for r in regions_list:
            output.update({
                r+"resnet_pred_"+label : Hist.new.Reg(100, 0, 1, name=r+"resnet_SUEP_pred_"+label, label="Resnet Output").Weight(),
                r+"ntracks_"+label : Hist.new.Reg(100, 0, 500, name=r+"ntracks"+label, label="# Tracks in Event").Weight(),
            })
                        
    return output

# fill ABCD hists with dfs from hdf5 files
nfailed = 0
weight = 0
fpickle =  open(outDir + options.dataset+ "_" + output_label + '.pkl', "wb")
output = {"labels":[]}

# systematics
if options.isMC:
    
    new_config = {}
    
    # track systematics
    # we need to use the trackDOWN version of the data,
    # which has the randomly deleted tracks (see SUEPCoffea.py)
    # so we need to modify the config to use the _trackDOWN vars
    for label_out, config_out in config.items():
        label_out_new = label_out+"_trackDOWN"
        new_config[label_out_new] = deepcopy(config[label_out])
        new_config[label_out_new]['input_method'] += "_trackDOWN"
        new_config[label_out_new]['xvar'] += "_trackDOWN"
        new_config[label_out_new]['yvar'] += "_trackDOWN"
        for iSel in range(len(new_config[label_out_new]['SR'])):
            new_config[label_out_new]['SR'][iSel][0] += "_trackDOWN"
        for iSel in range(len(new_config[label_out_new]['selections'])):
            if new_config[label_out_new]['selections'][iSel][0] in ['ht', 'ngood_ak4jets']: continue
            new_config[label_out_new]['selections'][iSel][0] += "_trackDOWN"
    
    # jet systematics
    # here, we just change ht to ht_SYS (e.g. ht -> ht_JEC_JES_up)
    for sys in ['JEC', 'JEC_JER_up', 'JEC_JER_down', 'JEC_JES_up', 'JEC_JES_down']: 
        for label_out, config_out in config.items():
            label_out_new = label_out+"_"+sys
            new_config[label_out_new] = deepcopy(config[label_out])
            for iSel in range(len(new_config[label_out_new]['selections'])):
                if 'ht' == new_config[label_out_new]['selections'][iSel][0]:
                    new_config[label_out_new]['selections'][iSel][0] += "_" + sys 

    config = new_config | config
    
### Plotting loop #######################################################################
for ifile in tqdm(files):
    
    #####################################################################################
    # ---- Load file
    #####################################################################################

    if options.xrootd:
        if os.path.exists(options.dataset+'.hdf5'): os.system('rm ' + options.dataset+'.hdf5')
        xrd_file = redirector + ifile
        os.system("xrdcp -s {} {}.hdf5".format(xrd_file, options.dataset))
        df, metadata = h5load(options.dataset+'.hdf5', 'vars')   
    else:
        df, metadata = h5load(ifile, 'vars')   
 
    # check if file is corrupted
    if type(df) == int: 
        nfailed += 1
        continue
            
    # update the gensumweight
    if options.isMC and metadata != 0: weight += metadata['gensumweight']

    # check if file is empty
    if 'empty' in list(df.keys()): continue
    if df.shape[0] == 0: continue    

    #####################################################################################
    # ---- Additional weights
    # Currently applies pileup weights through nTrueInt
    # and optionally (options.weights) scaling weights that are derived to force
    # MC to agree with data in one variable. Usage:
    # df['event_weight'] *= another event weight, etc
    # ---- Make plots
    #####################################################################################
    event_weight = np.ones(df.shape[0])
    sys_loop = ["","puweights_up","puweights_down",
                "trigSF_up","trigSF_down"]
    for sys in sys_loop:
        # prepare new event weight
        df['event_weight'] = event_weight

        # 1) pileup weights
        if options.isMC == 1 and options.scouting != 1:
            Pileup_nTrueInt = np.array(df['Pileup_nTrueInt']).astype(int)
            if "puweights_up" in sys:
                 pu = puweights_up[Pileup_nTrueInt]
            elif "puweights_down" in sys:
                 pu = puweights_down[Pileup_nTrueInt]
            else:
                 pu = puweights[Pileup_nTrueInt]
            df['event_weight'] *= pu

        # 2) TriggerSF weights
        if options.isMC == 1 and options.scouting != 1:
            ht = np.array(df['ht']).astype(int)
            ht_bin = np.digitize(ht,trig_bins)-1 #digitize the values to bins
            ht_bin = np.clip(ht_bin,0,49)        #Set overlflow to last SF
            if "trigSF_up" in sys:
                 trigSF = trig_weights_up[ht_bin]
            elif "trigSF_down" in sys:
                 trigSF = trig_weights_down[ht_bin]
            else:
                 trigSF = trig_weights[ht_bin]
            df['event_weight'] *= trigSF  

        # 4) scaling weights
        # N.B.: these aren't part of the systematics, just an optional scaling
        if options.isMC == 1 and scaling_weights is not None:
            df = apply_scaling_weights(df.copy(), scaling_weights,
                config['Cluster']['x_var_regions'],
                config['Cluster']['x_var_regions'],
                regions = "ABCDEFGHI",
                x_var = 'SUEP_S1_CL',
                y_var = 'SUEP_nconst_CL',
                z_var = 'ht')

        for label_out, config_out in config.items():
            if 'trackDOWN' in label_out and sys != "": continue
            output.update(create_output_file(label_out, config_out, sys))
            output = plot(df.copy(), output, config_out, label_out, sys)
        
    #####################################################################################
    # ---- End
    #####################################################################################
    
    # remove file at the end of loop   
    if options.xrootd: os.system('rm ' + options.dataset+'.hdf5')    

### End plotting loop ###################################################################

# do the tracks UP systematic
sys = 'trackUP'
for label_out, config_out in config.items():
    if 'trackDOWN' in label_out: continue
    
    new_output = {}
    for hist_name in output.keys():
        if not hist_name.endswith('_trackDOWN'): continue
        hDown = output[hist_name].copy()
        hNom = output[hist_name.replace('_trackDOWN','')].copy()
        hUp = get_tracks_up(hNom, hDown)
        new_output.update({hist_name.replace('_trackDOWN','_trackUP'): hUp})
    output = new_output | output
        
# apply normalization
output.pop("labels")
if options.isMC:
    if weight > 0.0:
        for plot in list(output.keys()): output[plot] = output[plot]*xsection/weight
    else:
        print("Weight is 0")
        
#Save to pickle
pickle.dump(output, fpickle)
print("Number of files that failed to be read:", nfailed)

# save to root
with uproot.recreate(outDir + options.dataset+ "_" + output_label + '.root') as froot:
    for h, hist in output.items():
        froot[h] = hist
