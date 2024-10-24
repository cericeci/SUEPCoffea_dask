import os
import ROOT
from auxiliars import *
import copy

def hdf5inpath(path):
  ret = []
  for f in os.listdir(path):
    if "hdf5" in f: 
      ret.append(path + "/" + f)
  return ret

# Main path where samples are stored
main_path = "/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_ANv8/"
main_path_signal = "/eos/cms/store/user/gdecastr/HDF5s_NewSigs/2016/" #"/eos/cms/store/group/phys_exotica/SUEPs/UL16/hdf5_withJECs/"

samples = {
  "data": {
         "name" : "data",
         "label": "Data",
         "xsec" : -1,
         "lineColor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "data/"),#+ hdf5inpath(main_path + "data_RunB/")+hdf5inpath(main_path + "data_RunC/")+hdf5inpath(main_path + "data_RunD/"),
         "markerstyle": 20,
         "markersize" : 1,
  },
  "DY_Pt0": {
         "name"       : "DY_Pt0", #Here plain text
         "label"      : "DY",# (p_{T} = 0 GeV)", #Here we can use weird glyphs
         "xsec"       : 5804*1000., # in fb
         "linecolor"  : ROOT.kBlack,
         "fillcolor"  : 7, # White
         "isSig"      : False,
         "extraWeights": lambda x: 1*(x["genZpt"]==0.0)*x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"], 
         "files"      : hdf5inpath(main_path + "DYToLL_M50/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DYToLL_M50/skims.root"
  },      
  "DY_Pt0To50": {
         "name"     : "DY_Pt0To50", #Here plain text
         "label"    : "DY",# (p_{T} < 50 GeV)", #Here we can use weird glyphs
         "xsec"     : 1404.*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 7, # Light blue
         "isSig"    : False,
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "files"    : hdf5inpath(main_path + "DYToLL_M50_Pt0To50/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DYToLL_M50_Pt0To50/skims.root"
  },
  "DY_Pt50To100": {
         "name"     : "DY_Pt50To100", #Here plain text
         "label"    : "DY",# (50 < p_{T} < 100 GeV)", #Here we can use weird glyphs
         "xsec"     : 363.8*1000., # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 7, # Light blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "DYToLL_M50_Pt50To100/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DYToLL_M50_Pt50To100/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "DY_Pt100To250": {
         "name"     : "DY_Pt100To250", #Here plain text
         "label"    : "DY",# (100 < p_{T} < 250 GeV)", #Here we can use weird glyphs
         "xsec"     : 84.0*1000., # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 7, # Light blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "DYToLL_M50_Pt100To250/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DYToLL_M50_Pt100To250/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "DY_Pt250To400": {
         "name"     : "DY_Pt250To400", #Here plain text
         "label"    : "DY",# (250 < p_{T} < 400 GeV)", #Here we can use weird glyphs
         "xsec"     : 3.23*1000., # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 7, # Light blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "DYToLL_M50_Pt250To400/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DYToLL_M50_Pt250To400/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "DY_Pt400To650": {
         "name"     : "DY_Pt400To650", #Here plain text
         "label"    : "DY",# (400 < p_{T} < 650 GeV)", #Here we can use weird glyphs
         "xsec"     : 0.436*1000., # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 7, # Light blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "DYToLL_M50_Pt400To650/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DYToLL_M50_Pt400To650/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "DY_Pt650ToInf": {
         "name"     : "DY_Pt650ToInf", #Here plain text
         "label"    : "DY",# (p_{T} > 650 GeV)", #Here we can use weird glyphs
         "xsec"     : 0.041*1000., # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 7, # Light blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "DYToLL_M50_Pt650ToInf/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DYToLL_M50_Pt650ToInf/skims.root", 
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "ttto2l": {
         "name"     : "ttto2l", #Here plain text
         "label"    : "t#bar{t} (2l)", #Here we can use weird glyphs
         "xsec"     : 831.76*((3*0.108)**2)*1000., # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 2, # Red
         "isSig"    : False,
         "files"    :  hdf5inpath(main_path + "TTTo2L2Nu/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/TTTo2L2Nu/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "tW": {
         "name"     : "tW", #Here plain text
         "label"    : "tW", #Here we can use weird glyphs
         "xsec"     : 3.289*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kMagenta, # Red
         "isSig"    : False,
         "files"    :  hdf5inpath(main_path + "tW/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/tW/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "DY_lowmass": {
         "name"     : "DY_lowmass", #Here plain text
         "label"    : "DY (m_{ll} < 50 GeV)", #Here we can use weird glyphs
         "xsec"     : 20590.0*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kAzure, # Red
         "isSig"    : False,
         "files"    :  hdf5inpath(main_path + "DY_lowmass/"),
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/DY_lowmass/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },

  "ttto1l": {
         "name"     : "ttto1l", #Here plain text
         "label"    : "t#bar{t} (1l)", #Here we can use weird glyphs
         "xsec"     : 831.76*(3*0.108)*(1-3*0.108)*1000., # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 5, # Yellow
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "TTTo1L1Nu2Q/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/TTTo1L1Nu/skims.root",
  },
  "WW": {
         "name"     : "WW", #Here plain text
         "label"    : "VV", #Here we can use weird glyphs
         "xsec"     : 10.481*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 3, # Green
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "WWTo2L2Nu/"),
         "skim"       : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/WWTo2L2Nu/skims.root",
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "WZ2l2q": {
         "name"     : "WZ2l2q", #Here plain text
         "label"    : "VV", #Here we can use weird glyphs
         "xsec"     : 6.419*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 3, # Green
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "WZTo2L2Q/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/WZTo2L2Q/skims.root"
  },
  "WZ3lnu": {
         "name"     : "WZ3lnu", #Here plain text
         "label"    : "VV", #Here we can use weird glyphs
         "xsec"     : 4.664*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 3, # Green
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "WZTo3LNu/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/WZTo3LNu/skims.root"
  },
  "ZZ2l2q": {
         "name"     : "ZZ2l2q", #Here plain text
         "label"    : "VV", #Here we can use weird glyphs
         "xsec"     : 3.74*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 3, # Green
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "ZZTo2L2Q/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/ZZTo2L2Q/skims.root"
  },
  "ZZ2l2nu": {
         "name"     : "ZZ2l2nu", #Here plain text
         "label"    : "VV", #Here we can use weird glyphs
         "xsec"     : 0.8738*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 3, # Green
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "ZZTo2L2Nu/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/ZZTo2L2Nu/skims.root"
  },

  "ZZ4l": {
         "name"     : "ZZ4l", #Here plain text
         "label"    : "VV", #Here we can use weird glyphs
         "xsec"     : 1.325*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 3, # Green
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "ZZTo4L/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/ZZTo4L/skims.root"
  },
  "ZG": {
         "name"     : "ZG", #Here plain text
         "label"    : "VV", #Here we can use weird glyphs
         "xsec"     : 51.1*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 3, # Green
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "ZG/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/ZG/skims.root"
  },
  "ttZll": {
         "name"     : "ttZll", #Here plain text
         "label"    : "t#bar{t}X", #Here we can use weird glyphs
         "xsec"     : 0.2439*1000, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 9, # Dark blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "TTZToLL/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/TTZToLL/skims.root"
  },
  "ttWlnu": {
         "name"     : "ttWlnu", #Here plain text
         "label"    : "t#bar{t}X", #Here we can use weird glyphs
         "xsec"     : 0.2161*1000*0.4, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 9, # Dark blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "TTWToLNu/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/TTWToLNu/skims.root"
  },
  "ttWqq": {
         "name"     : "ttWqq", #Here plain text
         "label"    : "t#bar{t}X", #Here we can use weird glyphs
         "xsec"     : 0.4377*1000*0.4, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": 9, # Dark blue
         "isSig"    : False,
         "files"    : hdf5inpath(main_path + "TTWToQQ/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
         "skim"     : "/eos/cms/store/group/phys_exotica/SUEPs/UL16/skim_2l_20_10/TTWToQQ/skims.root"
  },
  "SUEP_hadronic_mS125_mD1.40_T0.35": {
         "name"     : "SUEP_hadronic_mS125_mD1.40_T0.35", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD1.40_T0.35/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD1.40_T0.70": {
         "name"     : "SUEP_hadronic_mS125_mD1.40_T0.70", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD1.40_T0.70/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD1.40_T1.40": {
         "name"     : "SUEP_hadronic_mS125_mD1.40_T1.40", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD1.40_T1.40/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD1.40_T2.80": {
         "name"     : "SUEP_hadronic_mS125_mD1.40_T2.80", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD1.40_T2.80/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD1.40_T5.60": {
         "name"     : "SUEP_hadronic_mS125_mD1.40_T5.60", #Here plain text
         "label"    : "ZS, hadronic, T=5.6, m_{\phi}=1.4 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD1.40_T5.60/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD2.00_T0.50": {
         "name"     : "SUEP_hadronic_mS125_mD2.00_T0.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD2.00_T0.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD2.00_T1.00": {
         "name"     : "SUEP_hadronic_mS125_mD2.00_T1.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD2.00_T1.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD2.00_T2.00": {
         "name"     : "SUEP_hadronic_mS125_mD2.00_T2.00", #Here plain text
         "label"    : "ZS, hadronic, T=2, m_{\phi}=2 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kRed,
         "fillcolor": ROOT.kRed,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD2.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD2.00_T4.00": {
         "name"     : "SUEP_hadronic_mS125_mD2.00_T4.00", #Here plain text
         "label"    : "ZS, hadronic, T=4, m_{\phi}=2 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD2.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD2.00_T8.00": {
         "name"     : "SUEP_hadronic_mS125_mD2.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_hadronic_mS125_mD2.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T0.75": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T0.75", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T0.75/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T0.99": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T0.99", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T0.99/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T1.50": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T1.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T1.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T1.98": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T1.98", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T1.98/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T12.00": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T12.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T12.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T3.00": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T3.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=T=3, hadronic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T3.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T4.50": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T4.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T4.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T6.00": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T6.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T6.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD3.00_T9.00": {
         "name"     : "SUEP_hadronic_mS125_mD3.00_T9.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD3.00_T9.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T1.00": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T1.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T1.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T1.32": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T1.32", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T1.32/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T12.00": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T12.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T12.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T16.00": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T16.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T16.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T2.00": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T2.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T2.64": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T2.64", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T2.64/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T4.00": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T4.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T6.00": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T6.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T6.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD4.00_T8.00": {
         "name"     : "SUEP_hadronic_mS125_mD4.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=4, T=8, hadronic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD4.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T1.25": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T1.25", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T1.25/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T1.65": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T1.65", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T1.65/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T10.00": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T10.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T10.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T15.00": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T15.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T15.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T2.50": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T2.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T2.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T20.00": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T20.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T20.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T3.30": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T3.30", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T3.30/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T5.00": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T5.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=T=5, hadronic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kRed,
         "fillcolor": ROOT.kRed,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T5.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD5.00_T7.50": {
         "name"     : "SUEP_hadronic_mS125_mD5.00_T7.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD5.00_T7.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T1.50": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T1.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T1.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T1.98": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T1.98", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T1.98/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T12.00": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T12.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T12.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T18.00": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T18.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T18.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T24.00": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T24.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T24.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T3.00": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T3.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=6, T=3, hadronic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kBlue,
         "fillcolor": ROOT.kBlue,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T3.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T3.96": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T3.96", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T3.96/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T6.00": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T6.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T6.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD6.00_T9.00": {
         "name"     : "SUEP_hadronic_mS125_mD6.00_T9.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD6.00_T9.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T1.75": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T1.75", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T1.75/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T10.50": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T10.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T10.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T14.00": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T14.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T14.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T2.31": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T2.31", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T2.31/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T21.00": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T21.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T21.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T28.00": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T28.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T28.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T3.50": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T3.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T3.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T4.62": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T4.62", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T4.62/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD7.00_T7.00": {
         "name"     : "SUEP_hadronic_mS125_mD7.00_T7.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD7.00_T7.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T12.00": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T12.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T12.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T16.00": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T16.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T16.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T2.00": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T2.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T2.64": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T2.64", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T2.64/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T24.00": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T24.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T24.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T32.00": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T32.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T32.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T4.00": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T4.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T5.28": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T5.28", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T5.28/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_hadronic_mS125_mD8.00_T8.00": {
         "name"     : "SUEP_hadronic_mS125_mD8.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path_signal+"SUEP_hadronic_mS125_mD8.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD1.00_T0.25": {
         "name"     : "SUEP_leptonic_mS125_mD1.00_T0.25", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD1.00_T0.25/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD1.00_T0.50": {
         "name"     : "SUEP_leptonic_mS125_mD1.00_T0.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD1.00_T0.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD1.00_T1.00": {
         "name"     : "SUEP_leptonic_mS125_mD1.00_T1.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD1.00_T1.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD1.00_T2.00": {
         "name"     : "SUEP_leptonic_mS125_mD1.00_T2.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD1.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD1.00_T4.00": {
         "name"     : "SUEP_leptonic_mS125_mD1.00_T4.00", #Here plain text
         "label"    : "ZS, leptonic, T=4.0, m_{\phi}=1 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD1.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD2.00_T0.50": {
         "name"     : "SUEP_leptonic_mS125_mD2.00_T0.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD2.00_T0.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD2.00_T1.00": {
         "name"     : "SUEP_leptonic_mS125_mD2.00_T1.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD2.00_T1.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD2.00_T2.00": {
         "name"     : "SUEP_leptonic_mS125_mD2.00_T2.00", #Here plain text
         "label"    : "ZS, leptonic, T=2, m_{\phi}=2 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kRed,
         "fillcolor": ROOT.kRed,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD2.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD2.00_T4.00": {
         "name"     : "SUEP_leptonic_mS125_mD2.00_T4.00", #Here plain text
         "label"    : "ZS, leptonic, T=4, m_{\phi}=2 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD2.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD2.00_T8.00": {
         "name"     : "SUEP_leptonic_mS125_mD2.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD2.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD3.00_T0.75": {
         "name"     : "SUEP_leptonic_mS125_mD3.00_T0.75", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD3.00_T0.75/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD3.00_T1.50": {
         "name"     : "SUEP_leptonic_mS125_mD3.00_T1.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD3.00_T1.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD3.00_T12.00": {
         "name"     : "SUEP_leptonic_mS125_mD3.00_T12.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD3.00_T12.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD3.00_T3.00": {
         "name"     : "SUEP_leptonic_mS125_mD3.00_T3.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=T=3, leptonic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD3.00_T3.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD3.00_T6.00": {
         "name"     : "SUEP_leptonic_mS125_mD3.00_T6.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD3.00_T6.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD4.00_T1.00": {
         "name"     : "SUEP_leptonic_mS125_mD4.00_T1.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD4.00_T1.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD4.00_T16.00": {
         "name"     : "SUEP_leptonic_mS125_mD4.00_T16.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD4.00_T16.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD4.00_T2.00": {
         "name"     : "SUEP_leptonic_mS125_mD4.00_T2.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD4.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD4.00_T4.00": {
         "name"     : "SUEP_leptonic_mS125_mD4.00_T4.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD4.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD4.00_T8.00": {
         "name"     : "SUEP_leptonic_mS125_mD4.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=4, T=8, leptonic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD4.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD8.00_T16.00": {
         "name"     : "SUEP_leptonic_mS125_mD8.00_T16.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD8.00_T16.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD8.00_T2.00": {
         "name"     : "SUEP_leptonic_mS125_mD8.00_T2.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD8.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD8.00_T32.00": {
         "name"     : "SUEP_leptonic_mS125_mD8.00_T32.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD8.00_T32.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD8.00_T4.00": {
         "name"     : "SUEP_leptonic_mS125_mD8.00_T4.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD8.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_leptonic_mS125_mD8.00_T8.00": {
         "name"     : "SUEP_leptonic_mS125_mD8.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_leptonic_mS125_mD8.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD2.00_T0.50": {
         "name"     : "SUEP_generic_mS125_mD2.00_T0.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD2.00_T0.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD2.00_T1.00": {
         "name"     : "SUEP_generic_mS125_mD2.00_T1.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD2.00_T1.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD2.00_T2.00": {
         "name"     : "SUEP_generic_mS125_mD2.00_T2.00", #Here plain text
         "label"    : "ZS, generic, T=2, m_{\phi}=2 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kRed,
         "fillcolor": ROOT.kRed,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD2.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD2.00_T4.00": {
         "name"     : "SUEP_generic_mS125_mD2.00_T4.00", #Here plain text
         "label"    : "ZS, generic, T=4, m_{\phi}=2 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD2.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD2.00_T8.00": {
         "name"     : "SUEP_generic_mS125_mD2.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD2.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD3.00_T0.75": {
         "name"     : "SUEP_generic_mS125_mD3.00_T0.75", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD3.00_T0.75/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD3.00_T1.50": {
         "name"     : "SUEP_generic_mS125_mD3.00_T1.50", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD3.00_T1.50/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD3.00_T12.00": {
         "name"     : "SUEP_generic_mS125_mD3.00_T12.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD3.00_T12.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD3.00_T3.00": {
         "name"     : "SUEP_generic_mS125_mD3.00_T3.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=T=3, generic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD3.00_T3.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD3.00_T6.00": {
         "name"     : "SUEP_generic_mS125_mD3.00_T6.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD3.00_T6.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD4.00_T1.00": {
         "name"     : "SUEP_generic_mS125_mD4.00_T1.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD4.00_T1.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD4.00_T16.00": {
         "name"     : "SUEP_generic_mS125_mD4.00_T16.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD4.00_T16.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD4.00_T2.00": {
         "name"     : "SUEP_generic_mS125_mD4.00_T2.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD4.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD4.00_T4.00": {
         "name"     : "SUEP_generic_mS125_mD4.00_T4.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD4.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD4.00_T8.00": {
         "name"     : "SUEP_generic_mS125_mD4.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV, m=4, T=8, generic", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kBlack,
         "fillcolor": ROOT.kBlack,
         "isSig"    : True,
         "doPlot"   : True,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD4.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD8.00_T16.00": {
         "name"     : "SUEP_generic_mS125_mD8.00_T16.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD8.00_T16.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD8.00_T2.00": {
         "name"     : "SUEP_generic_mS125_mD8.00_T2.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD8.00_T2.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD8.00_T32.00": {
         "name"     : "SUEP_generic_mS125_mD8.00_T32.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD8.00_T32.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD8.00_T4.00": {
         "name"     : "SUEP_generic_mS125_mD8.00_T4.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD8.00_T4.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
  "SUEP_generic_mS125_mD8.00_T8.00": {
         "name"     : "SUEP_generic_mS125_mD8.00_T8.00", #Here plain text
         "label"    : "ZS, m_{S} = 125 GeV", #Here we can use weird glyphs
         "xsec"     : 870 * 0.0336 * 3, # in fb
         "linecolor": ROOT.kGreen,
         "fillcolor": ROOT.kGreen,
         "isSig"    : True,
         "doPlot"   : False,
         "files"    : hdf5inpath(main_path+"SUEP_generic_mS125_mD8.00_T8.00/"),
         "extraWeights": lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"],
  },
}


toPrint = []
for s in samples:
    if ("SUEP" in s) and not("mD2.00_T4.00" in s and "hadronic" in s): samples[s]["doPlot"] = False
    elif "mD2.00_T4.00" in s and ("hadronic" in s): samples[s]["doPlot"] = True

print(toPrint)
for sample in samples:
  if "data" in sample: continue
  #if not(samples[sample]["isSig"]): 
  #  samples[sample]["variations"] = {}
  #  continue

  samples[sample]["variations"] = {
  "TrigSFUp": {
           "name"            :   "TrigSFUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: (x["TrigSF"]+x["TrigSF_Up"])/x["TrigSF"], # Relative to central
           "symmetrize"      :      False, 
  },
  "TrigSFDn": {
           "name"            :   "TrigSFDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: (x["TrigSF"]-x["TrigSF_Dn"])/x["TrigSF"], # Relative to central
           "symmetrize"      :      False,
  },
  "ElSFUp": {
           "name"            :   "ElSFUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["LepSF_ElUp"]/x["LepSF"], # Relative to central
           "symmetrize"      :      False,
  },
  "ElSFDn": {
           "name"            :   "ElSFDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["LepSF_ElDn"]/x["LepSF"],
           "symmetrize"      :      False,
  },
  "MuSFUp": {
           "name"            :   "MuSFUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["LepSF_MuUp"]/x["LepSF"],
           "symmetrize"      :      False,
  },
  "MuSFDn": {
           "name"            :   "MuSFDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["LepSF_MuDn"]/x["LepSF"],
           "symmetrize"      :      False,
  },
  "PUUp": {
           "name"            :   "PUUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["PUWeight_Up"]/x["PUWeight"],
           "symmetrize"      :      False,
  },
  "PUDn": {
           "name"            :   "PUDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["PUWeight_Dn"]/x["PUWeight"],
           "symmetrize"      :      False,
  },
  "L1Up": {
           "name"            :   "L1Up",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["L1prefireWeight_Up"]/x["L1prefireWeight"],
           "symmetrize"      :      False,
  },
  "L1Dn": {
           "name"            :   "L1Dn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["L1prefireWeight_Dn"]/x["L1prefireWeight"],
           "symmetrize"      :      False,
  },
  "ISRUp": {
           "name"            :   "ISRUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["ISRWeight_Up"],
           "symmetrize"      :      False,
  },
  "ISRDn": {
           "name"            :   "ISRDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["ISRWeight_Dn"],
           "symmetrize"      :      False,
  },
  "FSRUp": {
           "name"            :   "FSRUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["FSRWeight_Up"],
           "symmetrize"      :      False,
  },
  "FSRDn": {
           "name"            :   "FSRDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["FSRWeight_Dn"],
           "symmetrize"      :      False,
  },
  "LFCorrUp": {
           "name"            :   "LFCorrUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_LFCorr_Up"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "LFCorrDn": {
           "name"            :   "LFCorrDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_LFCorr_Dn"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "HFCorrUp": {
           "name"            :   "HFCorrUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_HFCorr_Up"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "HFCorrDn": {
           "name"            :   "HFCorrDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_HFCorr_Dn"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "LFUnCorrUp": {
           "name"            :   "LFUnCorrUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_LFUnCorr_Up"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "LFUnCorrDn": {
           "name"            :   "LFUnCorrDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_LFUnCorr_Dn"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "HFUnCorrUp": {
           "name"            :   "HFUnCorrUp",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_HFUnCorr_Up"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "HFUnCorrDn": {
           "name"            :   "HFUnCorrDn",
           "isSyst"          :       True,
           "replaceChannel"  :         {},
           "extraWeights"    :   lambda x: x["bTagWeight_HFUnCorr_Dn"]/x["bTagWeight"],
           "symmetrize"      :      False,
  },
  "Track": {
           "name"            : "Track",
           "isSyst"          :        True,
           "replaceChannel"  :         {"SR":"SR", "onecluster":"onecluster", "twoleptons":"twoleptons"},
           "extraWeights"    :  lambda x: x["PUWeight"]*x["L1prefireWeight"]*x["bTagWeight"]*x["TrigSF"]*x["LepSF"], # Transposer needs to recompute for all copies of varied ntracks 
           "transposer"      :  lambda x: transposeTracks(x, "UL16","leadcluster_ntracks"),
           "symmetrize"      : False
    },
}
  if (samples[sample]["isSig"]): 
    samples[sample]["variations"]["JECUp"] = {
           "name"            : "JEC",
           "isSyst"          :      True,
           "replaceChannel"  :  {"SR":"SR_JECUP", "onecluster":"onecluster_JECUP", "twoleptons":"twoleptons_JECUP"},
           "extraWeights"    :  lambda x, sample=sample: samples[sample]["extraWeights"](x),
           "symmetrize"      :      False,
    }
    samples[sample]["variations"]["JECDn"] = {
           "name"            : "JEC",
           "isSyst"          :      True,
           "replaceChannel"  :  {"SR":"SR_JECDOWN", "onecluster":"onecluster_JECDOWN", "twoleptons":"twoleptons_JECDOWN"},
           "extraWeights"    :  lambda x, sample=sample: samples[sample]["extraWeights"](x),
           "symmetrize"      :      False,
    }
    samples[sample]["variations"]["JERUp"] = {
           "name"            : "JER",
           "isSyst"          :      True,
           "replaceChannel"  :  {"SR":"SR_JERUP", "onecluster":"onecluster_JERUP", "twoleptons":"twoleptons_JERUP"},
           "extraWeights"    :  lambda x, sample=sample: samples[sample]["extraWeights"](x),
           "symmetrize"      :      False,
    }
    samples[sample]["variations"]["JERDn"] = {
           "name"            : "JER",
           "isSyst"          :      True,
           "replaceChannel"  :  {"SR":"SR_JERDOWN", "onecluster":"onecluster_JERDOWN", "twoleptons":"twoleptons_JERDOWN"},
           "extraWeights"    :  lambda x, sample=sample: samples[sample]["extraWeights"](x),
           "symmetrize"      :      False,
    }
