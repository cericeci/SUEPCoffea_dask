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
    out = ((hlt & 1) == 1)*(pt >= 210) +  ((hlt & 2) == 2)*(pt >= 115)*(pt < 210) +  ((hlt & 4) == 4)*(pt >= 105)*(pt < 115) +  ((hlt & 16) == 16)*(pt >= 80)*(pt < 105) +((hlt & 32) == 32)*(pt >= 55)*(pt < 80) +  ((hlt & 64) == 64)*(pt >= 30)*(pt < 55) +  ((hlt & 128) == 128)*(pt >= 20)*(pt < 55)
  else:
    out = ((hlt & 1) == 1)*(pt >= 230) +  1.76*((hlt & 2) == 2)*(pt >= 130)*(pt < 230) +  8.00*1.76*((hlt & 4) == 4)*(pt >= 105)*(pt < 130) +  2.87*24.12*((hlt & 16) == 16)*(pt >= 85)*(pt < 105) + 2.87*97.46*((hlt & 32) == 32)*(pt >= 60)*(pt < 85) +  2.87*2534*((hlt & 64) == 64)*(pt >= 30)*(pt < 60) +  2.87*59.96/0.0032*((hlt & 128) == 128)*(pt >= 20)*(pt < 30) 
  return out

# Main path where samples are stored
main_path = "/eos/cms/store/user/cericeci/SUEPS/hdf5_photon/UL18/" #"/eos/cms/store/user/cericeci/SUEPS/hdf5s_withMeanMode/UL16/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_ANv8/"# "/eos/home-c/cericeci/SUEP/SUEPCoffea_dask/SyncExercise/UL16/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_ANv4/"
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

