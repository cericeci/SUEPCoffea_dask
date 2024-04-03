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
main_path = "/eos/cms/store/user/cericeci/SUEPS/hdf5_1photon/UL17/" #"/eos/cms/store/user/cericeci/SUEPS/hdf5s_withMeanMode/UL17/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL17/hdf5_ANv8/"# "/eos/home-c/cericeci/SUEP/SUEPCoffea_dask/SyncExercise/UL17/"#"/eos/cms/store/group/phys_exotica/SUEPs/UL17/hdf5_ANv4/"
main_path_signal = main_path #"/eos/cms/store/group/phys_exotica/SUEPs/UL17/hdf5_withJECs/"
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
  "QCD_100to200": {
         "name"       : "QCD_100to200", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 23500000*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x: x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/QCD_HT_100to200/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_100to200/skims.root"
  },
  "QCD_200to300": {
         "name"       : "QCD_200to300", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 1552000*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x: x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/QCD_HT_200to300/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_200to300/skims.root"
  },
  "QCD_300to500": {
         "name"       : "QCD_300to500", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 324300*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x: x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]), 
         "files"      : hdf5inpath(main_path + "/QCD_HT_300to500/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_300to500/skims.root"
  },
  "QCD_500to700": {
         "name"       : "QCD_500to700", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 29990*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/QCD_HT_500to700/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_500to700/skims.root"
  },
  "QCD_700to1000": {
         "name"       : "QCD_700to1000", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 6374*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/QCD_HT_700to1000/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_700to1000/skims.root"
  },
  "QCD_1000to1500": {
         "name"       : "QCD_1000to1500", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 1095*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/QCD_HT_1000to1500/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_1000to1500/skims.root"
  },
  "QCD_1500to2000": {
         "name"       : "QCD_1500to2000", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 99.27*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/QCD_HT_1500to2000/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_1500to2000/skims.root"
  },
  "QCD_2000toInf": {
         "name"       : "QCD_2000toInf", #Here plain text
         "label"      : "QCD",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 20.25*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kRed, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/QCD_HT_2000toInf/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/QCD_HT_2000toInf/skims.root"
  },
  "GJets_40to100": {
         "name"       : "GJets_40to100", #Here plain text
         "label"      : "GJets40100",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 18700.0*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kBlack, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/GJets_HT_40To100/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/GJets_HT_40To100/skims.root"
  },
  "GJets_100to200": {
         "name"       : "GJets_100to200", #Here plain text
         "label"      : "GJets100200",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 8640*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kBlue, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/GJets_HT_100To200/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/GJets_HT_100To200/skims.root"
  },
  "GJets_200to400": {
         "name"       : "GJets_200to400", #Here plain text
         "label"      : "GJets200400",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 2183*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kGreen, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/GJets_HT_200To400/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/GJets_HT_200To400/skims.root"
  },
  "GJets_400to600": {
         "name"       : "GJets_400to600", #Here plain text
         "label"      : "GJets400600",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 260.7*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kOrange, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/GJets_HT_400To600/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/GJets_HT_400To600/skims.root"
  },
  "GJets_600toInf": {
         "name"       : "GJets_600toInf", #Here plain text
         "label"      : "GJets600Inf",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 86.50*1000, # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : ROOT.kYellow, # White
         "isSig"      : False,
         "extraWeights": lambda x : x["PUWeight"]*np.array([c[0] for c in x["PhotonSF"]]),
         "files"      : hdf5inpath(main_path + "/GJets_HT_600ToInf/", "hdf5"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL17/skim_1photon/GJets_HT_600ToInf/skims.root"
  },
}
