"""
    Plotting (max difference of) eta against z momentum of Higgs, 
    and (max difference of) phi against transverse momentum of Higgs.
    Objective is to determine the optimal strip size for an event.
    Raymond Kil, 2022
"""

#from this import d
import pandas as pd
import ROOT
import os
import numpy as np

output = "/eos/user/j/jkil/www/S-Frame_Property"
ZH = [pd.HDFStore("../outputZH/"+f, 'r') for f in os.listdir("../outputZH/")]

# Command for accessing the hdf5 files
# print(ZH[1]["onetrack"])

EtaPz = True
EtaPt = True
PhiPz = True
PhiPt = True

if EtaPz:
    #delta Eta vs pz
    h = ROOT.TH2F("deltaEta_vs_Hpz","deltaEta vs pz of Mediator",100,0,1500,100,0,4)
    c = ROOT.TCanvas("c", "", 800,600)
    
    for i in range(len(ZH)):
        deltaEta = ZH[i]["onetrack"]["boostS_deltaEta"]
        Hpz = ZH[i]["onetrack"]["genHpz"]
        for j in range(len(deltaEta)):
            h.Fill(Hpz[j],deltaEta[j])

    h.Draw("colz")
    c.Draw()
    h.GetXaxis().SetTitle("pz of genH [GeV]")
    h.GetYaxis().SetTitle("deltaEta")
    h.SetMarkerStyle(7)
    c.SaveAs("%s/%s.pdf"%(output,"deltaEta_vs_Hpz"))
    c.SaveAs("%s/%s.png"%(output,"deltaEta_vs_Hpz"))

if EtaPt:
    #delta Eta vs pt
    h = ROOT.TH2F("deltaEta_vs_Hptt","deltaEta vs pt of Mediator",100,0,1500,100,0,4)
    c = ROOT.TCanvas("c", "", 800,600)
    
    for i in range(len(ZH)):
        deltaEta = ZH[i]["onetrack"]["boostS_deltaEta"]
        Hpt = ZH[i]["onetrack"]["genHpt"]
        for j in range(len(deltaEta)):
            h.Fill(Hpt[j],deltaEta[j])

    h.Draw("colz")
    c.Draw()
    h.GetXaxis().SetTitle("pt of genH [GeV]")
    h.GetYaxis().SetTitle("deltaEta")
    h.SetMarkerStyle(7)
    c.SaveAs("%s/%s.pdf"%(output,"deltaEta_vs_Hpt"))
    c.SaveAs("%s/%s.png"%(output,"deltaEta_vs_Hpt"))

if PhiPz:
    #delta Phi vs pz
    h = ROOT.TH2F("deltaPhi_vs_Hpz","deltaPhi vs pz of Mediator",100,0,1500,100,0,4)
    c = ROOT.TCanvas("c", "", 800,600)
    
    for i in range(len(ZH)):
        deltaPhi = ZH[i]["onetrack"]["boostS_deltaPhi"]
        Hpz = ZH[i]["onetrack"]["genHpz"]
        for j in range(len(deltaPhi)):
            h.Fill(Hpz[j],deltaPhi[j])

    h.Draw("colz")
    c.Draw()
    h.GetXaxis().SetTitle("pz of genH [GeV]")
    h.GetYaxis().SetTitle("deltaPhi")
    h.SetMarkerStyle(7)
    c.SaveAs("%s/%s.pdf"%(output,"deltaPhi_vs_Hpz"))
    c.SaveAs("%s/%s.png"%(output,"deltaPhi_vs_Hpz"))

if PhiPt:
    #delta Phi vs pt
    h = ROOT.TH2F("deltaPhi_vs_Hpt","deltaPhi vs pt of Mediator",100,0,1500,100,0,4)
    c = ROOT.TCanvas("c", "", 800,600)
    
    for i in range(len(ZH)):
        deltaPhi = ZH[i]["onetrack"]["boostS_deltaPhi"]
        Hpt = ZH[i]["onetrack"]["genHpt"]
        for j in range(len(deltaPhi)):
            h.Fill(Hpt[j],deltaPhi[j])

    h.Draw("colz")
    c.Draw()
    h.GetXaxis().SetTitle("pt of genH [GeV]")
    h.GetYaxis().SetTitle("deltaPhi")
    h.SetMarkerStyle(7)
    c.SaveAs("%s/%s.pdf"%(output,"deltaPhi_vs_Hpt"))
    c.SaveAs("%s/%s.png"%(output,"deltaPhi_vs_Hpt"))
