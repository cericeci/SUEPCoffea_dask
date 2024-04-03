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

# Main path where samples are stored
main_path = "/eos/cms/store/user/cericeci/SUEPS/hdf5_1photon/UL16/" #"/eos/cms/store/user/cericeci/SUEPS/hdf5s_withMeanMode/UL16/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_ANv8/"# "/eos/home-c/cericeci/SUEP/SUEPCoffea_dask/SyncExercise/UL16/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_ANv4/"
main_path_signal = main_path #"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_withJECs/"
samples = {
  "data": {
         "name" : "data",
         "label": "Data",
         "xsec" : -1,
         "lineColor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "/data/" , "hdf5"),#+ hdf5inpath(main_path + "data_RunB/")+hdf5inpath(main_path + "data_RunC/")+hdf5inpath(main_path + "data_RunD/"),
         "markerstyle": 20,
         "markersize" : 1,
  },
  "data_pre"
}
