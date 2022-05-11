import pandas as pd
import os
import sys

######### Configuration parameters ##########
SFile  = "../outputZH_archive/NumTrk[1.5,1.0]out.hdf5" # signal file
BFile  = "../outputDY_archive/NumTrk[1.5,1.0]out.hdf5" # background file
channel= "numtrkvars" # Channel name inside the analyzer
var    = "Ntracks" #Var name inside the analyzer
cut    = float(sys.argv[1]) # Cut value
where  = sys.argv[2] # L == less than, G== great than. For which region to compute significance
what   = "StoSqrtSB" # What to report: StoB, StoSqrtSB, StoSqrtB
addSys = float(sys.argv[3])

## Conf but shouldn't change
lumi  = 137.0 # Luminosity of Run 2
xsecS = 870*0.0336*3  # ZH, times BR to leptons
xsecB = 7181000*0.0336*3 # DY, times BR to leptons

######## Code itself

S = pd.HDFStore(SFile, 'r') # Input file for the signal
B = pd.HDFStore(BFile, 'r') # Input file for the background

# Normalization factors
normS = lumi*xsecS/(S.get_storer(channel).attrs.metadata["gensumweight"])
normB = lumi*xsecB/(B.get_storer(channel).attrs.metadata["gensumweight"])

# Vectors of weights
weightS = S[channel]["genweight"]
weightB = B[channel]["genweight"]

# Loop over events and fill counters
nSpass = 0
nBpass = 0

## Signal loop
for idx, val in enumerate(S[channel][var]):
  if where == "L" and val <= cut:
    nSpass += weightS[idx]*normS
  if where == "G" and val >= cut:
    nSpass += weightS[idx]*normS
    #print(idx,nBpass,"This is index and nSpass")

## Background loop
for idx, val in enumerate(B[channel][var]):
  if where == "L" and val <= cut:
    nBpass += weightB[idx]*normB
  if where == "G" and val >= cut:
    nBpass += weightB[idx]*normB
    #print(idx,nBpass,"This is index and nBpass")

print(nSpass, "This is final nSpass")
print(nBpass, "This is final nBpass")
print((addSys*nBpass), "This is systematic uncertainty")

if what == "StoSqrtSB":
  print("S/sqrt(S+B) = %1.3f for a cut of %1.3f in %s"%(nSpass/(nSpass+nBpass+(addSys*nBpass)**2)**0.5, cut, var))
elif what == "StoB":
  print("S/B = %1.3f for a cut of %1.3f in %s"%(nSpass/nBpass, cut, var))
elif what == "StoSqrtB":
  print("S/sqrt(B) = %1.3f for a cut of %1.3f in %s"%(nSpass/nBpass**0.5, cut, var))
