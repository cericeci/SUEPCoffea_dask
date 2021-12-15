import os, sys, subprocess
import time
import pandas as pd 
import numpy as np
from hist import Hist
import argparse
import os
import awkward as ak
import uproot
import getpass
import pickle
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Famous Submitter')
parser.add_argument("-t"   , "--tag"   , type=str, default="IronMan"  , help="production tag", required=True)
parser.add_argument("-b"   , "--blind"   , dest='blind',  action='store_true', help="blind", required=False)
parser.add_argument("-u"   , "--unblind"  , dest='blind',  action='store_false', help="unblind", required=False)
dhelp = """
Which dataset to run. Currently supports:
'combined' -- every 'JetHT' label found in "/work/submit/USERNAME/SUEP/TAG/"
'JetHT-XXX' -- grabs "/work/submit/USERNAME/SUEP/TAG/JetHT-XXX/*"
"""
parser.add_argument("-d"   , "--dataset"  , type=str, default="IronMan"  , help=dhelp, required=True)
parser.set_defaults(blind=True)
options = parser.parse_args()

# parameters for ABCD method
var1_label = 'spher'
var2_label = 'nconst'
var1_val = 0.50
var2_val = 25
nbins = 100
labels = ['ch']
output_label = 'V5_pt300'

# blinding warning
if not options.blind: 
    print("WARNING: YOU ARE RUNNING THIS SCRIPT WITHOUT BLINDING.")
    answer = input("Do you understand? Type 'I want to unblind' if you want to unblind: ")
    if answer != 'I want to unblind': sys.exit("Safely exited program before unblinding the analysis. Nice!")
    if answer == 'I want to unblind': print("Unblinding...")

# merge all JetHT samples together, or just import all files from a specific directory
username = getpass.getuser()
if options.dataset == 'combined':
    dataDir = "/work/submit/{}/SUEP/{}/".format(username,options.tag)
    files = []
    for subdir in list(os.listdir(dataDir)):
        if 'JetHT' not in subdir: continue
        files += [subdir+"/"+file for file in os.listdir(dataDir + subdir)]
else:
    dataDir = "/work/submit/{}/SUEP/{}/{}/".format(username,options.tag,options.dataset)
    files = [file for file in os.listdir(dataDir)]
    
# output histos
def create_output_file(label):
    output = {
            # ABCD hists
            "A_"+label: Hist.new.Reg(nbins, 0, 1, name="A_"+label).Weight(),
            "B_"+label: Hist.new.Reg(nbins, 0, 1, name="B_"+label).Weight(),
            "C_"+label: Hist.new.Reg(nbins, 0, 1, name="C_"+label).Weight(),
            "D_exp_"+label: Hist.new.Reg(nbins, 0, 1, name="D_exp_"+label).Weight(),
        
            # AB and AC combined, kinematic variables
            "SUEP_" + label + "_A_pt" : Hist.new.Reg(100, 0, 2000, name="A pt_"+label, label=r"$p_T$").Weight(),
            "SUEP_" + label + "_B_pt" : Hist.new.Reg(100, 0, 2000, name="B pt_"+label, label=r"$p_T$").Weight(),
            "SUEP_" + label + "_C_pt" : Hist.new.Reg(100, 0, 2000, name="C pt_"+label, label=r"$p_T$").Weight(),
            "SUEP_"+label+"_A_nconst" : Hist.new.Reg(499, 0, 500, name="A nconst_"+label, label="# Tracks in SUEP").Weight(),
            "SUEP_"+label+"_B_nconst" : Hist.new.Reg(499, 0, 500, name="B nconst_"+label, label="# Tracks in SUEP").Weight(),
            "SUEP_"+label+"_C_nconst" : Hist.new.Reg(499, 0, 500, name="C nconst_"+label, label="# Tracks in SUEP").Weight(),
            "SUEP_" + label + "_AB_pt" : Hist.new.Reg(100, 0, 2000, name="AB pt_"+label, label=r"$p_T$").Weight(),
            "SUEP_" + label + "_AB_eta" : Hist.new.Reg(100, -5, 5, name="AB eta_"+label, label=r"$\eta$").Weight(),
            "SUEP_" + label + "_AB_phi" : Hist.new.Reg(100, 0, 6.5, name="AB phi_"+label, label=r"$\phi$").Weight(),
            "SUEP_" + label + "_AC_pt" : Hist.new.Reg(100, 0, 2000, name="AC pt_"+label, label=r"$p_T$").Weight(),
            "SUEP_" + label + "_AC_eta" : Hist.new.Reg(100, -5, 5, name="AC eta_"+label, label=r"$\eta$").Weight(),
            "SUEP_" + label + "_AC_phi" : Hist.new.Reg(100, 0, 6.5, name="AC phi_"+label, label=r"$\phi$").Weight(),
            "SUEP_" + label + "_A_pt_nconst" : Hist.new.Reg(100, 0, 2000, name="A pt_"+label).Reg(499, 0, 500, name="A nconst_"+label).Weight(),
            "SUEP_" + label + "_B_pt_nconst" : Hist.new.Reg(100, 0, 2000, name="B pt_"+label).Reg(499, 0, 500, name="B nconst_"+label).Weight(),
            "SUEP_" + label + "_C_pt_nconst" : Hist.new.Reg(100, 0, 2000, name="C pt_"+label).Reg(499, 0, 500, name="C nconst_"+label).Weight(),
        }
    if not options.blind: 
        output.update({"D_obs_"+label: Hist.new.Reg(nbins, 0, 1, name="D_obs_"+label).Weight()})

    return output

# load hdf5 with pandas
def h5load(ifile, label):
    try:
        with pd.HDFStore(ifile) as store:
            try:
                data = store[label] 
                metadata = store.get_storer(label).attrs.metadata
                return data, metadata
            except ValueError: 
                print("Empty file!", ifile)
                return 0, 0
            except KeyError:
                print("No key",label,ifile)
                return 0, 0
    except:
        print(ifile)
        return 0, 0 

# fill ABCD hists with dfs from hdf5 files
frames = {"mult":[],"ch":[]}
nfailed = 0
fpickle =  open("outputs/" + options.dataset+ "_" + output_label + '.pkl', "wb")
output = {}
for label in labels: output.update({label: create_output_file(label)})

for ifile in tqdm(files):
    ifile = dataDir+"/"+ifile
    for label in labels:
        df, metadata = h5load(ifile, label)
        if type(df) == int: 
            nfailed += 1
            continue
        if df.shape[0] == 0: continue
        
        # variables for ABCD plots
        var1 = 'SUEP_'+label+'_' + var1_label
        var2 = 'SUEP_'+label+'_' + var2_label

        sizeA, sizeC = 0,0
        
        # set the D region to 0
        df.loc[(df[var1] >= var1_val) & (df[var2] >= var2_val)] = 0

        if var2_label == 'nconst': df = df.loc[df['SUEP_'+label+'_nconst'] >= 10]
        if var1_label == 'spher': df = df.loc[df['SUEP_'+label+'_spher'] >= 0.25]
        df = df.loc[df['SUEP_'+label+'_pt'] >= 300]

        # divide the dfs by region and select the variable we want to plot
        df_A = df.loc[(df[var1] < var1_val) & (df[var2] < var2_val)]
        df_B = df.loc[(df[var1] >= var1_val) & (df[var2] < var2_val)]
        df_C = df.loc[(df[var1] < var1_val) & (df[var2] >= var2_val)]
        #----------------------------------
        # DO NOT EVEN FILL ANY D observed!
        #----------------------------------

        sizeC += df_C.shape[0]
        sizeA += df_A.shape[0]
        
        # fill the ABCD histograms
        output[label]["A_"+label].fill(df_A[var1])
        output[label]["B_"+label].fill(df_B[var1])
        output[label]["D_exp_"+label].fill(df_B[var1])
        output[label]["C_"+label].fill(df_C[var1])
        if not options.blind: 
            output[label]["D_obs_"+label].fill(df_D_obs[var1])

        # fill some new distribuions
        output[label]["SUEP_" + label + "_A_pt"].fill(df_A['SUEP_' + label + '_pt'])
        output[label]["SUEP_" + label + "_B_pt"].fill(df_B['SUEP_' + label + '_pt'])
        output[label]["SUEP_" + label + "_C_pt"].fill(df_C['SUEP_' + label + '_pt'])
        output[label]["SUEP_" + label + "_A_nconst"].fill(df_A['SUEP_' + label + '_nconst'])
        output[label]["SUEP_" + label + "_B_nconst"].fill(df_B['SUEP_' + label + '_nconst'])
        output[label]["SUEP_" + label + "_C_nconst"].fill(df_C['SUEP_' + label + '_nconst'])
        output[label]["SUEP_" + label + "_AB_phi"].fill(df['SUEP_' + label + '_phi'].loc[(df[var2] < var2_val)])
        output[label]["SUEP_" + label + "_AB_eta"].fill(df['SUEP_' + label + '_eta'].loc[(df[var2] < var2_val)])
        output[label]["SUEP_" + label + "_AB_pt"].fill(df['SUEP_' + label + '_pt'].loc[(df[var2] < var2_val)])
        output[label]["SUEP_" + label + "_AC_phi"].fill(df['SUEP_' + label + '_phi'].loc[(df[var1] < var1_val)])
        output[label]["SUEP_" + label + "_AC_eta"].fill(df['SUEP_' + label + '_eta'].loc[(df[var1] < var1_val)])
        output[label]["SUEP_" + label + "_AC_pt"].fill(df['SUEP_' + label + '_pt'].loc[(df[var1] < var1_val)])
        output[label]["SUEP_" + label + "_A_pt_nconst"].fill(df_A['SUEP_' + label + '_pt'], df_A['SUEP_' + label + '_nconst'])
        output[label]["SUEP_" + label + "_B_pt_nconst"].fill(df_B['SUEP_' + label + '_pt'], df_B['SUEP_' + label + '_nconst'])
        output[label]["SUEP_" + label + "_C_pt_nconst"].fill(df_C['SUEP_' + label + '_pt'], df_C['SUEP_' + label + '_nconst'])

    
# ABCD method to obtain D expected
if sizeA>0.0:
    CoverA =  sizeC / sizeA
else:
    CoverA = 0.0
    print("A region has no occupancy")
output[label]["D_exp_"+label] = output[label]["D_exp_"+label]*(CoverA)

for label in labels: pickle.dump(output[label], fpickle)
print("Number of files that failed: ", nfailed*1.0 / len(labels))