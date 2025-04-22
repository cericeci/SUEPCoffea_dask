import ROOT
import pandas as pd
import root_numpy
import numpy as np
import sys

ROOT.gStyle.SetOptStat(0)
inp  = pd.HDFStore(sys.argv[1],"r")
sr   = inp["SR"]
meta = inp.get_storer("SR").attrs.metadata
xsec = 900
lumi = 138.1
variable = "leadcluster_pt"
label = "p_{T}^{SUEP} [GeV]"
nbins = 25
minX  = 0
maxX  = 500

# Extract arrays
values         = sr[variable]
genweight      = sr["genweight"] # It is one for every event, though technically we should multiply by it everywhere
pdfweights     = [sr["PDFWeight_%i"%i] for i in range(1, 101)]
alfasupweights = sr["AlphaSWeight_Up"]
alfasdnweights = sr["AlphaSWeight_Down"]
gensumweight   = meta["gensumweight"]
gensumpdfweight= meta["gensumpdfweights"]

# As a reference, what happens if we do the averaging on the event weights instead
badpdfweightsUp = []
for iev in range(len(genweight)): 
    weightsInEvent = np.array([p[iev] for p in pdfweights] + [alfasupweights[iev], alfasdnweights[iev]]) # Note that this is 102 entries, as entry 0 has the mean
    mean = np.mean(weightsInEvent)
    std  = np.std(weightsInEvent)*(102)**0.5 # Multiply by sqrt(N-1) to transform std into quadratic sum
    badpdfweightsUp.append(1+ std/mean)
badpdfweightsUp = np.array(badpdfweightsUp)


# Central value
hC = ROOT.TH1F("hC", "hC", nbins, minX, maxX)

# One variation per Hessian copy plus separate ones for AlphaS
hPDFs = [hC.Clone("hPDF%i"%iPDF) for iPDF in range(1, 101)]
hASUp = hC.Clone("hASUp")
hASDn = hC.Clone("hASDn") 

# And the histos for the per event weights
hPDFBadEnv = hC.Clone("hPDFBadEnv")

# Fill histograms per replica
root_numpy.fill_hist(hC, values)
for iPDF in range(1, 101):
    root_numpy.fill_hist(hPDFs[iPDF-1], values, pdfweights[iPDF-1])

root_numpy.fill_hist(hASUp, values, alfasupweights)
root_numpy.fill_hist(hASDn, values, alfasdnweights)

root_numpy.fill_hist(hPDFBadEnv, values, badpdfweightsUp)


# Now create copies for cases where we do/do not fix normalization

hPDFsN = [hPDFs[iPDF-1].Clone("hPDFN%i"%iPDF) for iPDF in range(1,101)]
hASUpN = hASUp.Clone("hASUpN")
hASDnN = hASDn.Clone("hASDnN")

# Normalizing by central weights, i.e. pdf/aS variations change overall predicted x-section
hC.Scale(xsec*lumi/gensumweight)
for iPDF in range(1,101):
    hPDFs[iPDF-1].Scale(xsec*lumi/gensumweight)
hASUp.Scale(xsec*lumi/gensumweight)
hASDn.Scale(xsec*lumi/gensumweight)

hPDFBadEnv.Scale(xsec*lumi/gensumweight)

# Normalizing each sample by its weights, i.e. pdf/aS variations do not change overall predicted x-section

for iPDF in range(1,101):
    hPDFsN[iPDF-1].Scale(xsec*lumi/gensumpdfweight[iPDF])
hASUpN.Scale(xsec*lumi/gensumpdfweight[101])
hASDnN.Scale(xsec*lumi/gensumpdfweight[102])



# Take envelopes # Note that this breaks bin to bin correlation so it might not be fully correct if effects are big and cause effects in some phase spaces and defects in others
# In some cases one might prefer to take variations up and down separately if asymmetries are expected
hPDFEnv = hC.Clone("hPDFEnv")
hPDFNEnv = hC.Clone("hPDFNEnv")
for ibin in range(hC.GetNbinsX()+1):
    central = hC.GetBinContent(ibin)
    pdfvar = 0
    pdfnvar = 0
    for i in range(100):
        pdfvar = (pdfvar**2 + (hPDFs[i].GetBinContent(ibin) - central)**2)**0.5
        pdfnvar = (pdfnvar**2 + (hPDFsN[i].GetBinContent(ibin) - central)**2)**0.5
    # Total uncertainty is quadratic sum of PDF and alpha S
    pdfvar = (pdfvar**2 + (abs((hASUp.GetBinContent(ibin)- hASDn.GetBinContent(ibin)))/2.)**2)**0.5
    pdfnvar = (pdfnvar**2 + (abs((hASUpN.GetBinContent(ibin)- hASDnN.GetBinContent(ibin)))/2.)**2)**0.5
    # Total uncertainty is quadratic sum of PDF and alpha S
    hPDFEnv.SetBinContent(ibin, central + pdfvar)
    hPDFNEnv.SetBinContent(ibin, central + pdfnvar)

# And now plot stuff
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
hC.SetLineColor(ROOT.kBlack)
hPDFEnv.SetLineColor(ROOT.kRed)
hPDFNEnv.SetLineColor(ROOT.kBlue)
hPDFBadEnv.SetLineColor(ROOT.kGreen)

hC.GetXaxis().SetTitle("")
hC.GetXaxis().SetLabelSize(0)
hC.GetYaxis().SetTitle("Events")
hC.GetYaxis().SetTitleSize(0.05)
hC.SetTitle("")
hC.Draw("hist")
hPDFEnv.Draw("histsame")
hPDFNEnv.Draw("histsame")
hPDFBadEnv.Draw("histsame")

tl = ROOT.TLegend(0.6,0.7,0.9,0.9)
tl.AddEntry(hC, "Central", "l")
tl.AddEntry(hPDFEnv, "PDF Up, not norm", "l")
tl.AddEntry(hPDFNEnv, "PDF Up, norm", "l")
tl.AddEntry(hPDFBadEnv, "PDF Up, weight per event", "l")
tl.Draw("same")

p2.cd()
rC = hC.Clone("rC")
rP = hPDFEnv.Clone("rP")
rPN = hPDFNEnv.Clone("rPN")
rPB = hPDFBadEnv.Clone("rPB")

rC.Divide(hC)
rP.Divide(hC)
rPN.Divide(hC)
rPB.Divide(hC)

rC.GetXaxis().SetTitle(label)
rC.GetYaxis().SetTitle("X/Central")
rC.GetXaxis().SetTitleSize(0.2)
rC.GetXaxis().SetLabelSize(0.1)
rC.GetYaxis().SetTitleSize(0.06)
rC.GetYaxis().SetLabelSize(0.05)

rC.SetMaximum(1.1)
rC.SetMinimum(0.95)
rC.Draw("hist")
rP.Draw("histsame")
rPN.Draw("histsame")
rPB.Draw("histsame")
c.SaveAs("pdfstudies.pdf")
c.SaveAs("pdfstudies.png")

