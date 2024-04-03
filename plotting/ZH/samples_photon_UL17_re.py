import os
import ROOT
from auxiliars import *
import copy

def hdf5inpath(path, filt=""):
  ret = []
  for f in os.listdir(path):
    if "hdf5" in f and filt in f: 
      ret.append(path + "/" + f)
  return ret

def binInPhotonPt(x, weight):
  out = np.array([])
  hlt = x["HLT_path"] 
  pt = x["Photon_pt"]
  if not(weight):
    out = ((hlt & 1) == 1)*(pt >= 230) +  ((hlt & 2) == 2)*(pt >= 175)*(pt < 230) +  ((hlt & 4) == 4)*(pt >= 130)*(pt < 175) + ((hlt & 8) == 8)*(pt >= 85)*(pt < 130) +  ((hlt & 16) == 16)*(pt >= 60)*(pt < 85) +  ((hlt & 32) == 32)*(pt >= 30)*(pt < 60) +  ((hlt & 64) == 64)*(pt >= 20)*(pt < 30) 
  else:
    out = ((hlt & 1) == 1)*(pt >= 230) +  41.54/28.34*((hlt & 2) == 2)*(pt >= 175)*(pt < 230) +  41.54/7.80*((hlt & 4) == 4)*(pt >= 130)*(pt < 175) + 41.54/1.32*((hlt & 8) == 8)*(pt >= 85)*(pt < 130) +  41.54/0.30*((hlt & 16) == 16)*(pt >= 60)*(pt < 85) + 92.7*41.54/0.30*((hlt & 32) == 32)*(pt >= 30)*(pt < 60) + 41.54/0.0004*((hlt & 64) == 64)*(pt >= 20)*(pt < 30)
  return out

# Main path where samples are stored
main_path = "/eos/cms/store/user/cericeci/SUEPS/hdf5_photon/UL17/" #"/eos/cms/store/user/cericeci/SUEPS/hdf5s_withMeanMode/UL16/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_ANv8/"# "/eos/home-c/cericeci/SUEP/SUEPCoffea_dask/SyncExercise/UL16/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_ANv4/"
main_path_signal = main_path #"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_withJECs/"
samples = {
  "data": {
         "name" : "data",
         "label": "Data (no cut)",
         "xsec" : -1,
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "/data/" , "hdf5") ,#+ hdf5inpath(main_path + "data_RunB/")+hdf5inpath(main_path + "data_RunC/")+hdf5inpath(main_path + "data_RunD/"),
         "markerstyle": 20,
         "markersize" : 1,
  },
  "prescaled": {
         "name" : "prescaled",
         "label": "Data (p_{T} binned)",
         "xsec" : -1,
         "linecolor": ROOT.kRed,
         "fillcolor": ROOT.kWhite,
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "/data/" , "hdf5") ,#+ hdf5inpath(main_path + "data_RunB/")+hdf5inpath(main_path + "data_RunC/")+hdf5inpath(main_path + "data_RunD/"),
         "markerstyle": 20,
         "markersize" : 1,
         "noWeight": True,
         "extraWeights": lambda x: binInPhotonPt(x, False),
  },
  "weighted": {
         "name" : "weighted",
         "label": "Data (p_{T} binned and weighted)",
         "xsec" : -1,
         "linecolor": ROOT.kBlue,
         "fillcolor": ROOT.kBlue,
         "files"    : hdf5inpath(main_path + "/data/" , "hdf5") ,#+ hdf5inpath(main_path + "data_RunB/")+hdf5inpath(main_path + "data_RunC/")+hdf5inpath(main_path + "data_RunD/"),
         "markerstyle": 20,
         "markersize" : 1,
         "noWeight": True,
         "extraWeights": lambda x: binInPhotonPt(x, True),
         "isSig": True
  }
}

