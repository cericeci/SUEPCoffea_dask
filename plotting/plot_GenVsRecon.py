import pandas as pd
import ROOT
import os

output = "/eos/user/j/jkil/www"

ZH = [pd.HDFStore("../outputZH/"+f, 'r') for f in os.listdir("../outputZH/")]

px = False
py = False
pz = False
pt = True
boost_px = False
boost_py = False
boost_pz = False
boost_pt = False
HpxHpy = False

if pt:

    Zpt1 = [0]*len(ZH[0]["onetrack"]["Z_pt"])
    Hpt1 = [0]*len(ZH[0]["onetrack"]["genHpt"])
    Zpt2 = [0]*len(ZH[1]["onetrack"]["Z_pt"])
    Hpt2 = [0]*len(ZH[1]["onetrack"]["genHpt"])

    for i, Zpt in enumerate(ZH[0]["onetrack"]["Z_pt"]) :
        Zpt1[i] = Zpt
    for i, Zpt in enumerate(ZH[1]["onetrack"]["Z_pt"]) :
        Zpt2[i] = Zpt

    Zpt = Zpt1 + Zpt2

    for i, genHpt in enumerate(ZH[0]["onetrack"]["genHpt"]):
        Hpt1[i] = genHpt
    for i, genHpt in enumerate(ZH[1]["onetrack"]["genHpt"]):
        Hpt2[i] = genHpt

    Hpt = Hpt1 + Hpt2

    h_pt = ROOT.TH2F("genHpt_vs_recZpt","generated Hpt vs reconstructed Zpt",100,0,500,100,0,500)
    c_pt = ROOT.TCanvas("c_pt", "", 800,600)

    for i in range(len(Zpt)):
        h_pt.Fill(Zpt[i],Hpt[i])

    f = ROOT.TF1("f","[0]*x",0,500)
    h_pt.Fit("f") # Draws the best fit curve to the plot.
    correlation = h_pt.GetCorrelationFactor()
    #var = f.GetParameter(0)

    h_pt.Draw()
    c_pt.Draw()
    h_pt.GetXaxis().SetTitle("pt of Z [GeV]")
    h_pt.GetYaxis().SetTitle("pt of H [GeV]")
    c_pt.SaveAs("%s/%s.pdf"%(output,"generated Hpt vs reconstructed Zpt"))
    c_pt.SaveAs("%s/%s.png"%(output,"generated Hpt vs reconstructed Zpt"))

if pz:

    Zpz1 = [0]*len(ZH[0]["onetrack"]["Z_pz"])
    Hpz1 = [0]*len(ZH[0]["onetrack"]["genHpz"])
    Zpz2 = [0]*len(ZH[1]["onetrack"]["Z_pz"])
    Hpz2 = [0]*len(ZH[1]["onetrack"]["genHpz"])

    for i, Zpz in enumerate(ZH[0]["onetrack"]["Z_pz"]) :
        Zpz1[i] = Zpz
    for i, Zpz in enumerate(ZH[1]["onetrack"]["Z_pz"]) :
        Zpz2[i] = Zpz

    Zpz = Zpz1 + Zpz2

    for i, genHpz in enumerate(ZH[0]["onetrack"]["genHpz"]):
        Hpz1[i] = genHpz
    for i, genHpz in enumerate(ZH[1]["onetrack"]["genHpz"]):
        Hpz2[i] = genHpz

    Hpz = Hpz1 + Hpz2


    h_pz = ROOT.TH2F("genHpz_vs_recZpz","generated Hpz vs reconstructed Zpz",100,-300,300,100,-300,300)
    c_pz = ROOT.TCanvas("c_pz", "", 800,600)

    for i in range(len(Zpz)):
        h_pz.Fill(Zpz[i],Hpz[i])

    h_pz.Draw()
    c_pz.Draw()
    h_pz.GetXaxis().SetTitle("pz of Z [GeV]")
    h_pz.GetYaxis().SetTitle("pz of H [GeV]")
    c_pz.SaveAs("%s/%s.pdf"%(output,"generated Hpz vs reconstructed Zpz"))
    c_pz.SaveAs("%s/%s.png"%(output,"generated Hpz vs reconstructed Zpz"))

if px:

    Zpx1 = [0]*len(ZH[0]["onetrack"]["Z_px"])
    Hpx1 = [0]*len(ZH[0]["onetrack"]["genHpx"])
    Zpx2 = [0]*len(ZH[1]["onetrack"]["Z_px"])
    Hpx2 = [0]*len(ZH[1]["onetrack"]["genHpx"])

    for i, Zpx in enumerate(ZH[0]["onetrack"]["Z_px"]) :
        Zpx1[i] = Zpx
    for i, Zpx in enumerate(ZH[1]["onetrack"]["Z_px"]) :
        Zpx2[i] = Zpx

    Zpx = Zpx1 + Zpx2

    for i, genHpx in enumerate(ZH[0]["onetrack"]["genHpx"]):
        Hpx1[i] = genHpx
    for i, genHpx in enumerate(ZH[1]["onetrack"]["genHpx"]):
        Hpx2[i] = genHpx

    Hpx = Hpx1 + Hpx2


    h_px = ROOT.TH2F("genHpx_vs_recZpx","generated Hpx vs reconstructed Zpx",100,-300,300,100,-300,300)
    c_px = ROOT.TCanvas("c_px", "", 800,600)

    for i in range(len(Zpx)):
        h_px.Fill(Zpx[i],Hpx[i])

    h_px.Draw()
    c_px.Draw()
    h_px.GetXaxis().SetTitle("px of Z [GeV]")
    h_px.GetYaxis().SetTitle("px of H [GeV]")
    c_px.SaveAs("%s/%s.pdf"%(output,"generated Hpx vs reconstructed Zpx"))
    c_px.SaveAs("%s/%s.png"%(output,"generated Hpx vs reconstructed Zpx"))

if py:

    Zpy1 = [0]*len(ZH[0]["onetrack"]["Z_py"])
    Hpy1 = [0]*len(ZH[0]["onetrack"]["genHpy"])
    Zpy2 = [0]*len(ZH[1]["onetrack"]["Z_py"])
    Hpy2 = [0]*len(ZH[1]["onetrack"]["genHpy"])

    for i, Zpy in enumerate(ZH[0]["onetrack"]["Z_py"]) :
        Zpy1[i] = Zpy
    for i, Zpy in enumerate(ZH[1]["onetrack"]["Z_py"]) :
        Zpy2[i] = Zpy

    Zpy = Zpy1 + Zpy2

    for i, genHpy in enumerate(ZH[0]["onetrack"]["genHpy"]):
        Hpy1[i] = genHpy
    for i, genHpy in enumerate(ZH[1]["onetrack"]["genHpy"]):
        Hpy2[i] = genHpy

    Hpy = Hpy1 + Hpy2


    h_py = ROOT.TH2F("genHpy_vs_recZpy","generated Hpy vs reconstructed Zpy",100,-300,300,100,-300,300)
    c_py = ROOT.TCanvas("c_py", "", 800,600)

    for i in range(len(Zpy)):
        h_py.Fill(Zpy[i],Hpy[i])

    h_py.Draw()
    c_py.Draw()
    h_py.GetXaxis().SetTitle("py of Z [GeV]")
    h_py.GetYaxis().SetTitle("py of H [GeV]")
    c_py.SaveAs("%s/%s.pdf"%(output,"generated Hpy vs reconstructed Zpy"))
    c_py.SaveAs("%s/%s.png"%(output,"generated Hpy vs reconstructed Zpy"))

if boost_px:

    Zboost1 = [0]*len(ZH[0]["onetrack"]["boostT_px"])
    Hpx1 = [0]*len(ZH[0]["onetrack"]["genHpx"])
    Zboost2 = [0]*len(ZH[1]["onetrack"]["boostT_px"])
    Hpx2 = [0]*len(ZH[1]["onetrack"]["genHpx"])

    for i, Zboost in enumerate(ZH[0]["onetrack"]["boostT_px"]) :
        Zboost1[i] = Zboost
    for i, Zboost in enumerate(ZH[1]["onetrack"]["boostT_px"]) :
        Zboost2[i] = Zboost

    Zboost = Zboost1 + Zboost2

    for i, genHpx in enumerate(ZH[0]["onetrack"]["genHpx"]):
        Hpx1[i] = genHpx
    for i, genHpx in enumerate(ZH[1]["onetrack"]["genHpx"]):
        Hpx2[i] = genHpx

    Hpx = Hpx1 + Hpx2

    h_px = ROOT.TH2F("genHpx_vs_boostZpx","generated Hpx vs Tboost Zpx",100,-300,300,-300,0,300)
    c_px = ROOT.TCanvas("c_px", "", 800,600)

    for i in range(len(Zboost)):
        h_px.Fill(Zboost[i],Hpx[i])

    h_px.Draw()
    c_px.Draw()
    h_px.GetXaxis().SetTitle("px of Z [GeV]")
    h_px.GetYaxis().SetTitle("px of H [GeV]")
    c_px.SaveAs("%s/%s.pdf"%(output,"generated Hpx vs Tboost Zpx"))
    c_px.SaveAs("%s/%s.png"%(output,"generated Hpx vs Tboost Zpx"))

if boost_py:

    Zboost1 = [0]*len(ZH[0]["onetrack"]["boostT_py"])
    Hpy1 = [0]*len(ZH[0]["onetrack"]["genHpy"])
    Zboost2 = [0]*len(ZH[1]["onetrack"]["boostT_py"])
    Hpy2 = [0]*len(ZH[1]["onetrack"]["genHpy"])

    for i, Zboost in enumerate(ZH[0]["onetrack"]["boostT_py"]) :
        Zboost1[i] = Zboost
    for i, Zboost in enumerate(ZH[1]["onetrack"]["boostT_py"]) :
        Zboost2[i] = Zboost

    Zboost = Zboost1 + Zboost2

    for i, genHpy in enumerate(ZH[0]["onetrack"]["genHpy"]):
        Hpy1[i] = genHpy
    for i, genHpy in enumerate(ZH[1]["onetrack"]["genHpy"]):
        Hpy2[i] = genHpy

    Hpy = Hpy1 + Hpy2

    h_py = ROOT.TH2F("genHpy_vs_boostZpy","generated Hpy vs Tboost Zpy",100,-300,300,-300,0,300)
    c_py = ROOT.TCanvas("c_py", "", 800,600)

    for i in range(len(Zboost)):
        h_py.Fill(Zboost[i],Hpy[i])

    h_py.Draw()
    c_py.Draw()
    h_py.GetXaxis().SetTitle("py of Z [GeV]")
    h_py.GetYaxis().SetTitle("py of H [GeV]")
    c_py.SaveAs("%s/%s.pdf"%(output,"generated Hpy vs Tboost Zpy"))
    c_py.SaveAs("%s/%s.png"%(output,"generated Hpy vs Tboost Zpy"))

if boost_pz:

    Zboost1 = [0]*len(ZH[0]["onetrack"]["boostT_pz"])
    Hpz1 = [0]*len(ZH[0]["onetrack"]["genHpz"])
    Zboost2 = [0]*len(ZH[1]["onetrack"]["boostT_pz"])
    Hpz2 = [0]*len(ZH[1]["onetrack"]["genHpz"])

    for i, Zboost in enumerate(ZH[0]["onetrack"]["boostT_pz"]) :
        Zboost1[i] = Zboost
    for i, Zboost in enumerate(ZH[1]["onetrack"]["boostT_pz"]) :
        Zboost2[i] = Zboost

    Zboost = Zboost1 + Zboost2

    for i, genHpz in enumerate(ZH[0]["onetrack"]["genHpz"]):
        Hpz1[i] = genHpz
    for i, genHpz in enumerate(ZH[1]["onetrack"]["genHpz"]):
        Hpz2[i] = genHpz

    Hpz = Hpz1 + Hpz2

    h_pz = ROOT.TH2F("genHpz_vs_boostZpz","generated Hpz vs Tboost Zpz",100,-300,300,100,-300,300)
    c_pz = ROOT.TCanvas("c_pz", "", 800,600)

    for i in range(len(Zboost)):
        h_pz.Fill(Zboost[i],Hpz[i])

    h_pz.Draw()
    c_pz.Draw()
    h_pz.GetXaxis().SetTitle("pz of Z [GeV]")
    h_pz.GetYaxis().SetTitle("pz of H [GeV]")
    c_pz.SaveAs("%s/%s.pdf"%(output,"generated Hpz vs Tboost Zpz"))
    c_pz.SaveAs("%s/%s.png"%(output,"generated Hpz vs Tboost Zpz"))

if boost_pt:

    Zboost1 = [0]*len(ZH[0]["onetrack"]["boostT_pt"])
    Hpt1 = [0]*len(ZH[0]["onetrack"]["genHpt"])
    Zboost2 = [0]*len(ZH[1]["onetrack"]["boostT_pt"])
    Hpt2 = [0]*len(ZH[1]["onetrack"]["genHpt"])

    for i, Zboost in enumerate(ZH[0]["onetrack"]["boostT_pt"]) :
        Zboost1[i] = Zboost
    for i, Zboost in enumerate(ZH[1]["onetrack"]["boostT_pt"]) :
        Zboost2[i] = Zboost

    Zboost = Zboost1 + Zboost2

    for i, genHpt in enumerate(ZH[0]["onetrack"]["genHpt"]):
        Hpt1[i] = genHpt
    for i, genHpt in enumerate(ZH[1]["onetrack"]["genHpt"]):
        Hpt2[i] = genHpt

    Hpt = Hpt1 + Hpt2

    h_pt = ROOT.TH2F("genHpt_vs_boostZpt","generated Hpt vs Tboost Zpt",100,0,500,100,0,500)
    c_pt = ROOT.TCanvas("c_pt", "", 800,600)

    for i in range(len(Zboost)):
        h_pt.Fill(Zboost[i],Hpt[i])

    h_pt.Draw()
    c_pt.Draw()
    h_pt.GetXaxis().SetTitle("pt of Z [GeV]")
    h_pt.GetYaxis().SetTitle("pt of H [GeV]")
    c_pt.SaveAs("%s/%s.pdf"%(output,"generated Hpt vs Tboost Zpt"))
    c_pt.SaveAs("%s/%s.png"%(output,"generated Hpt vs Tboost Zpt"))

if HpxHpy:

    Hpx1 = [0]*len(ZH[0]["onetrack"]["genHpx"])
    Hpy1 = [0]*len(ZH[0]["onetrack"]["genHpy"])
    Hpx2 = [0]*len(ZH[1]["onetrack"]["genHpx"])
    Hpy2 = [0]*len(ZH[1]["onetrack"]["genHpy"])

    for i, px in enumerate(ZH[0]["onetrack"]["genHpx"]) :
        Hpx1[i] = px
    for i, px in enumerate(ZH[1]["onetrack"]["genHpx"]) :
        Hpx2[i] = px

    Hpx = Hpx1 + Hpx2

    for i, py in enumerate(ZH[0]["onetrack"]["genHpy"]):
        Hpy1[i] = py
    for i, py in enumerate(ZH[1]["onetrack"]["genHpy"]):
        Hpy2[i] = py

    Hpy = Hpy1 + Hpy2

    h_pxpy = ROOT.TH2F("genHpx_vs_genHpy","generated Hpx vs generated Hpy",100,-300,300,100,-300,300)
    c_pxpy = ROOT.TCanvas("c_pxpy", "", 800,600)

    for i in range(len(Hpx)):
        h_pxpy.Fill(Hpx[i],Hpy[i])

    h_pxpy.Draw()
    c_pxpy.Draw()
    h_pxpy.GetXaxis().SetTitle("px of H [GeV]")
    h_pxpy.GetYaxis().SetTitle("py of H [GeV]")
    c_pxpy.SaveAs("%s/%s.pdf"%(output,"generated Hpx vs generated Hpy"))
    c_pxpy.SaveAs("%s/%s.png"%(output,"generated Hpx vs generated Hpy"))