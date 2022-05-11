import pandas as pd
import ROOT
import os
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
output = "/eos/user/j/jkil/www"
DY = [pd.HDFStore("../outputDY/"+f, 'r') for f in os.listdir("../outputDY/")]
ZH = [pd.HDFStore("../outputZH/"+f, 'r') for f in os.listdir("../outputZH/")]

#channel   = "numtrkvars" #remember to change this to sphervars
channel   = "sphervars"
normalize = True

plots = {
  #"Leading Lepton p_{T}": ["leadlep_pt", 50, 0, 200, "p_{T}^{l1} [GeV]"], 
  #"Leading Lepton eta":["leadlep_eta", 50, -2.5, 2.5, "eta"],
  #"Leading Lepton phi":["leadlep_phi",50,0,6.28,"phi"],
  #"Leading Lepton mass":["leadlep_mass",50,0,0.01,"mass"]
  #"SubLead Lepton p_{T}": ["subleadlep_pt", 50, 0, 200, "p_{T}^{l2} [GeV]"],
  #"SubLead Lepton eta":["subleadlep_eta", 50, -2.5, 2.5, "eta"],
  #"SubLead Lepton phi":["subleadlep_phi",50,0,6.28,"phi"],
  #"Zpt":["Z_pt",50,0,200,"p_{t_{Z}} [GeV]"],
  #"Zeta":["Z_eta",50,-2.5,2.5,"\eta_{Z}"],
  #"Zphi":["Z_phi",50,-np.pi,np.pi,"\phi_{Z}"],
  #"Zm":["Z_m",50,0,150,"m_{Z} [GeV]"],


  #"onejet p_{T}":["onejet_pt",50,0,150,"p_{T} [GeV]"],
  #"onejet eta":["onejet_eta",50,-3.14,3.14,"eta"],
  #"onejet phi":["onejet_phi",50,0,3.14,"phi"],

  #"twojets1 p_{T}":["twojets1_pt",50,0,150,"p_{T} [GeV]"],
  #"twojets1 eta":["twojets1_eta",50,-3.14,3.14,"eta"],
  #"twojets1 phi":["twojets1_phi",50,0,3.14,"phi"],

  #"twojets2 p_{T}":["twojets2_pt",50,0,150,"p_{T} [GeV]"],
  #"twojets2 eta":["twojets2_eta",50,-3.14,3.14,"eta"],
  #"twojets2 phi":["twojets2_phi",50,0,3.14,"phi"],

  #"threejets1 p_{T}":["threejets1_pt",50,0,150,"p_{T} [GeV]"],
  #"threejets1 eta":["threejets1_eta",50,-3.14,3.14,"eta"],
  #"threejets1 phi":["threejets1_phi",50,0,3.14,"phi"],

  #"threejets2 p_{T}":["threejets2_pt",50,0,150,"p_{T} [GeV]"],
  #"threejets2 eta":["threejets2_eta",50,-3.14,3.14,"eta"],
  #"threejets2 phi":["threejets2_phi",50,0,3.14,"phi"],

  #"threejets3 p_{T}":["threejets3_pt",50,0,150,"p_{T} [GeV]"],
  #"threejets3 eta":["threejets3_eta",50,-3.14,3.14,"eta"],
  #"threejets3 phi":["threejets3_phi",50,0,3.14,"phi"],

  #"NumTrk(3,3)":["Ntracks",50,0,100,"counts(pt = 3, fromPV = 3)"],

  "Eigenvalue #lambda_{1} (L)":["eval_L1",50,0,1,"1st Eigenvalue #lambda_{1} in Lab frame"],
  "Eigenvalue #lambda_{1} (S)":["eval_Z1",50,0,1,"1st Eigenvalue #lambda_{1} in -Z frame"],

  "Eigenvalue #lambda_{2} (L)":["eval_L2",50,0,1,"2nd Eigenvalue #lambda_{2} in Lab frame"],
  "Eigenvalue #lambda_{2} (S)":["eval_Z2",50,0,1,"2nd Eigenvalue #lambda_{2} in -Z frame"],

  "Eigenvalue #lambda_{3} (L)":["eval_L3",50,0,1,"3rd Eigenvalue #lambda_{3} in Lab frame"],
  "Eigenvalue #lambda_{3} (S)":["eval_Z3",50,0,1,"3rd Eigenvalue #lambda_{3} in -Z frame"],

  "Scalar Sphericity (L)":["scalarSpher_L",50,0,1,"Scalar Sphericity in Lab frame"],
  "Scalar Sphericity (S)":["scalarSpher_Z",50,0,1,"Scalar Sphericity in -Z frame"],
}

for p in plots:
  h1 = ROOT.TH1F(plots[p][0], plots[p][0], plots[p][1], plots[p][2], plots[p][3])
  h2 = h1.Clone(h1.GetName()+ "_2")

  sumwB = 0
  for d in DY:
    #print d.get_storer("vars").attrs.metadata
    sumwB += d.get_storer("numtrkvars").attrs.metadata["gensumweight"]
    weightsDY = d[channel]["genweight"]
    for idx, val in enumerate(d[channel][plots[p][0]]):
      if idx%1000 == 0: print (idx)
      h1.Fill(np.real(val),weightsDY[idx])

  sumwS = 0
  for d in ZH:
    if idx%1000 == 0: print (idx)
    #print d.get_storer("vars").attrs.metadata
    sumwS += d.get_storer("numtrkvars").attrs.metadata["gensumweight"]
    weightsZS = d[channel]["genweight"]
    for idx, val in enumerate(d[channel][plots[p][0]]):
      h2.Fill(val, weightsZS[idx])

  theColors = {"1":ROOT.kBlue, "2":ROOT.kRed}
  c = ROOT.TCanvas("c","c", 800,600)
  p1 = ROOT.TPad("mainpad", "mainpad", 0, 0.30, 1, 1)
  p1.SetBottomMargin(0.025)
  p1.SetTopMargin(0.08)
  p1.SetLeftMargin(0.12)
  p1.Draw()
  p1.SetLogy(True)
  p2 = ROOT.TPad("ratiopad", "ratiopad", 0, 0, 1, 0.30)
  p2.SetTopMargin(0.01)
  p2.SetBottomMargin(0.45)
  p2.SetLeftMargin(0.12)
  p2.SetFillStyle(0)
  p2.Draw()

  p1.cd()

  h1.SetTitle("")
  if normalize:
    h1.GetYaxis().SetTitle("Normalized events")
    h1.Scale(1./h1.Integral())
    h2.Scale(1./h2.Integral())
    h1.SetMaximum(1.1)
    h1.SetMinimum(0.001)

  else: # Scale to 137 fb^{-1}, a lot of hard coding we need to fix
    xsecDY   = 7181000*0.0336*2
    xsecSUEP = 870 * 0.0336 * 2 # ZH*Br(Z->ll)*2 accounting for el/mu
    lumi     = 137.0
    h1.Scale(lumi*xsecDY/sumwB)
    h2.Scale(lumi*xsecSUEP/sumwS)
    maxY = max(h1.GetMaximum(), h2.GetMaximum())
    minY = max(min(h2.GetMinimum(), h2.GetMinimum()),1)
    h1.SetMaximum(maxY)
    h1.SetMinimum(minY)

  h1.SetLineColor(theColors["1"])
  h2.SetLineColor(theColors["2"])
  h1.Draw()
  h2.Draw("same")
  tl = ROOT.TLegend(0.6,0.7,0.9,0.9)
  tl.AddEntry(h1, "DY", "l")
  tl.AddEntry(h2, "ZS, m_{S} = 125 GeV", "l")
  tl.Draw("same")

  p2.cd()
  ratioOff = h1.Clone(h1.GetName().replace("h","r"))
  ratioCus = h2.Clone(h2.GetName().replace("h","r"))
  ratioOff.Divide(h1)
  ratioOff.GetYaxis().SetTitle("Events/DY Events")
  ratioOff.SetTitleSize(0.05)
  ratioCus.Divide(h1)
  ratioCus.SetLineColor(theColors["2"])
  ratioOff.SetMaximum(2.)
  ratioOff.SetMinimum(0.)
  ratioOff.GetXaxis().SetTitle(plots[p][4])
  ratioOff.GetXaxis().SetTitleSize(0.18)
  ratioOff.GetXaxis().SetTitleOffset(1.)
  ratioOff.GetXaxis().SetLabelSize(0.15)
  ratioOff.Draw()
  ratioCus.Draw("same")
  c.SaveAs("%s/%s.pdf"%(output,p))
  c.SaveAs("%s/%s.png"%(output,p))

