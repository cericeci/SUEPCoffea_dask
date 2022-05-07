import os
import subprocess
import shlex
import argparse
import multiprocessing
from multiprocessing.pool import ThreadPool
import time

parser = argparse.ArgumentParser(description='Famous Submitter')
parser.add_argument("-t"   , "--tag"   , type=str, default="IronMan"  , help="Production tag", required=True)
options = parser.parse_args()

print("""WARNING: This wrapper will launch a process per dataset with this tag, 
        each of which use large amounts of memory, depending on how many events
        are kept in each merged file, so make sure to run it somewhere where
        you have enough memory available.""")

def call_makeplots(cmd):
    """ This runs in a separate thread. """
    print("----[%] :", cmd)
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)

pool = ThreadPool(multiprocessing.cpu_count())

SUEP = [
           "SUEP-m1000-darkPho+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m1000-darkPhoHad+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m1000-generic+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m125-darkPho+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m125-darkPhoHad+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m125-generic+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m400-darkPho+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m400-darkPhoHad+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m400-generic+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m750-darkPho+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m750-darkPhoHad+RunIIAutumn18-private+MINIAODSIM",
           "SUEP-m750-generic+RunIIAutumn18-private+MINIAODSIM"
]

QCD_HT_2018 = [
   "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",
"QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",
"QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",
"QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",
"QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",
"QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",
"QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",
"QCD_HT50to100_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM"
]

QCD_2018 = [ 
    "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",          
    "QCD_Pt_120to170_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2+MINIAODSIM",          
    "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",          
    "QCD_Pt_15to30_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",        
    "QCD_Pt_170to300_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",          
    "QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",          
    "QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",          
    "QCD_Pt_300to470_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",          
    "QCD_Pt_30to50_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",          
    "QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",           
    "QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-pilot_106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",           
    "QCD_Pt_470to600_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",           
    "QCD_Pt_50to80_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",           
    "QCD_Pt_600to800_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",           
    "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",           
    "QCD_Pt_80to120_TuneCP5_13TeV_pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM"
]

data_2018 = [
           "JetHT+Run2018A-UL2018_MiniAODv2-v1+MINIAOD",
           "JetHT+Run2018B-UL2018_MiniAODv2-v1+MINIAOD",
           "JetHT+Run2018C-UL2018_MiniAODv2-v1+MINIAOD",
           "JetHT+Run2018D-UL2018_MiniAODv2-v1+MINIAOD"
]

data_2016 = [
    "JetHT+Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016C-HIPM_UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016D-HIPM_UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016E-HIPM_UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016F-HIPM_UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016F-UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016G-UL2016_MiniAODv2-v2+MINIAOD",
    "JetHT+Run2016H-UL2016_MiniAODv2-v2+MINIAOD"
]
    
data_2017 = [
    "JetHT+Run2017B-UL2017_MiniAODv2-v1+MINIAOD",
    "JetHT+Run2017C-UL2017_MiniAODv2-v1+MINIAOD",
    "JetHT+Run2017D-UL2017_MiniAODv2-v1+MINIAOD",
    "JetHT+Run2017E-UL2017_MiniAODv2-v1+MINIAOD",
    "JetHT+Run2017F-UL2017_MiniAODv2-v1+MINIAOD",
]

QCD_2017 = [
    "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_120to170_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_15to30_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_170to300_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_300to470_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_30to50_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_470to600_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_50to80_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_600to800_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_Pt_80to120_TuneCP5_13TeV_pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM"   
]

QCD_HT_2017 = [
    "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT50to100_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
    "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8+RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1+MINIAODSIM",
]

QCD_HT_2016 = [
    "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2+MINIAODSIM",
    "QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT50to100_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_HT50to100_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",    
]

QCD_2016 = [
   "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_120to170_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_120to170_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_15to30_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_15to30_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_170to300_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_170to300_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_300to470_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_300to470_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_30to50_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_30to50_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_470to600_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_470to600_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_50to80_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_50to80_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_600to800_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_600to800_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM",
    "QCD_Pt_80to120_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1+MINIAODSIM",
    "QCD_Pt_80to120_TuneCP5_13TeV_pythia8+RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1+MINIAODSIM"
]

results = []
start = time.time()

# for sample in data_2018:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample, 0)
#     results.append(pool.apply_async(call_makeplots, (cmd,))) 
# for sample in QCD_2018:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample, 1)
#     results.append(pool.apply_async(call_makeplots, (cmd,))) 
for sample in QCD_HT_2018:
    cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample, 1)
    results.append(pool.apply_async(call_makeplots, (cmd,))) 
# for sample in QCD_HT_2017:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample, 1)
#     results.append(pool.apply_async(call_makeplots, (cmd,)))
# for sample in QCD_2017:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample, 1)
#     results.append(pool.apply_async(call_makeplots, (cmd,)))
# for sample in QCD_HT_2016:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample)
#     results.append(pool.apply_async(call_makeplots, (cmd,)))
# for sample in data_2017:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample)
#     results.append(pool.apply_async(call_makeplots, (cmd,))) 
# for sample in data_2016:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample)
#     results.append(pool.apply_async(call_makeplots, (cmd,))) 
# for sample in SUEP:
#     cmd = 'python3 merge_plots.py --tag={} --dataset={} --isMC={}'.format(options.tag, sample, 1)
#     results.append(pool.apply_async(call_makeplots, (cmd,))) 

# Close the pool and wait for each running task to complete
pool.close()
pool.join() 
for result in results:
    out, err = result.get()
    if "No such file or directory" in str(err):
        print(str(err))
        print(" ----------------- ")
        print() 
end = time.time()
print("All done! merge_all.py took",round(end - start),"seconds to run.")