import ROOT
import imp
import array 
import os
import pandas as pd
import CMS_lumi
from multiprocessing import Pool
import time
import copy
from contextlib import closing
import subprocess, sys
import math
import numpy as np
import re
from multiHadd import *
import root_numpy

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

class sample(object):
  def __init__(self, sampledict, options):
    self.dohadd = options.dohadd
    self.config  = sampledict
    if not("year" in self.config): self.config["year"] = "" # Safety replace 
    self.name    = sampledict["name"]
    self.hdfiles = []
    self.safefiles=[]
    self.nnorms = {}
    self.norms  = {}
    self.isData = (("data" in self.name) or ("Data" in self.name)) and not ("HEM" in self.name)
    self.histos  = {}
    self.plots   = {}
    self.channels= []
    self.plotsinchannel = {}
    self.varstoload = {}
    self.yields     = {}
    self.doSyst     = options.systFile
    #self.altChannels= {}
    self.variations = {} 
    self.noWeights = False
    if "noWeight" in self.config:
      print("Will not add weights for %s"%self.name)
      self.noWeights = self.config["noWeight"]
    if self.doSyst and not(self.isData): # Then we collect all possible channel alternatives
      self.variations = {}
      for var in self.config["variations"]:
        if not(self.doSyst) and self.config["variations"]["isSyst"]: 
          continue
        else:
          self.variations[var] = self.config["variations"][var]
    print("VARIATIONS", self.variations)
      #for var in self.variations:
      #  for orig in self.variations[var]["replaceChannel"]:
      #    if not(orig in self.altChannels):
      #      self.altChannels[orig] = self.variations[var]["replaceChannel"][orig]
      #    else:
      #      for alt in self.variations[var]["replaceChannel"][orig]:
      #        if not(alt in self.altChannels[orig]): 
      #          self.altChannels[orig].append(alt)

  def initAll(self, options):
    if options.queue: print("Loading sample %s"%self.name)
    iF = 0
    for f in self.config["files"]:
      iF +=1
      if (iF%100 == 1): print("Checking files %i/%i"%(iF, len(self.config["files"])))
      try:
        #if self.isData and options.dohadd: continue
        filename = f.split("/")[-1].replace("out_","").replace(".hdf5","")
        if options.toSave: 
          fullfilename = options.toSave.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_" + filename + ".root"
        if options.toLoad and not(options.fromROOT):
          fullfilename = options.toLoad.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_" + filename + ".root"
        if options.resubmit:
          if os.path.isfile(fullfilename):
            if os.path.getsize(fullfilename) > 100: #I.e., non corrupted
              continue    
        if not(options.toLoad and (("skim" in self.config) or (self.isData)) and os.path.isfile(fullfilename)) and not(options.fromROOT):
          if not("skim" in self.config) and not(self.isData) or (not(options.queue) and not(options.toLoad)):
            a = pd.HDFStore(f, "r")
          if not("skim" in self.config) and not(self.isData) and not(self.noWeights):
            self.nnorms[f] = a.get_storer("SR").attrs.metadata["gensumweight"]
          if not(options.queue) and not(options.toLoad):
            b = {}
            if len(a.keys()) == 0: #Empty file
              a.close()
              print("No keys in %s!"%f)
              continue
            for k in a.keys():
              try:
                b[k.replace("/","")] = a[k]
              except: # If we are here, there are no events at the cut level, so just save empty space (still need to count for normalizing)
                if options.debug: raise
                b[k.replace("/","")] = []
            self.hdfiles.append(b)
          if not("skim" in self.config) and not(self.isData) or (not(options.queue) and not(options.toLoad)):
            a.close()
        self.safefiles.append(f)
      except Exception as e:
        print("File %s broken, will skip loading it"%f)
        print(str(e))

    #print("SAFE FILES:", self.name, self.safefiles)
    if "skim" in self.config and not(self.isData):
      self.unskimmedyields, self.norm = self.getUnskimmedYields()

  def initAllForQueue(self, options): # Here don't load the whole hdf5 as it would break memory
    if options.queue: print("Loading sample %s"%self.name)
    iF = 0
    for f in self.config["files"]:
      iF +=1
      #if options.queue:
      if (iF % 100 == 1): print("Checking files %i/%i"%(iF, len(self.config["files"])))
      try:
        filename = f.split("/")[-1].replace("out_","").replace(".hdf5","")
        if options.toSave:
          fullfilename = options.toSave.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_" + filename + ".root"
        if options.toLoad:
          fullfilename = options.toLoad.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_" + filename + ".root"

        if options.resubmit:
          if os.path.isfile(fullfilename):
            if os.path.getsize(fullfilename) > 1000: #I.e., non corrupted
              #print("Corrupted!")
              continue
        self.safefiles.append(f)
        #print("File %s loaded succesfully"%f)
      except Exception as e:
        print("File %s broken, will skip loading it"%f)
        print(str(e))
  

  def getUnskimmedYields(self):
    if "auto" in self.config["skim"]:
      import json 
      skims = json.loads(open(self.config["skim"].replace("auto:",""), "r").read())
      out = {}
      norm = 0
      for f in self.safefiles:
        short = f.split("/")[-1]
        out[f] = skims[short]
        norm += skims[short]

    else:
      rf = ROOT.TFile(self.config["skim"])
      out = {}
      norm = 0
      for f in self.safefiles:
        print(f)
        run, luminosityBlock, event= f.split("/")[-1].replace("out_","").replace(".hdf5","").split("_")
        print(run, luminosityBlock, event)
        tt = rf.Get("Runs_"+str(event)+ "_" + str(luminosityBlock) + "_" + str(run))
        out[f] = 0
        for ev in tt:
          if self.noWeights:
            out[f] = 1 
            norm   += 1
          else:
            out[f] += ev.genEventSumw
            norm += ev.genEventSumw
          #break
    return out, norm

  def addPlot(self, plotdict):
    self.plots[plotdict["name"]] = plotdict
    if not(plotdict["channel"] in self.channels): 
      self.channels.append(plotdict["channel"])
      self.plotsinchannel[plotdict["channel"]] = [plotdict["name"]]
      self.varstoload[plotdict["channel"]]     = plotdict["vars"]
      #if plotdict["channel"] in self.altChannels and self.doSyst:
      #  for altChannel in self.altChannels[plotdict["channel"]]:
      #    self.channels.append(altChannel)
      #    self.plotsinchannel(altChannel) = [plotdict["name"]]
      #    self.varstoload[altChannel]     = plotdict["vars"]
    else:
      self.plotsinchannel[plotdict["channel"]].append(plotdict["name"])
      for v in plotdict["vars"]:
        if not(v in self.varstoload[plotdict["channel"]]): 
          self.varstoload[plotdict["channel"]].append(v)
      #if plotdict["channel"] in self.altChannels and self.doSyst:
      #  for altChannel in self.altChannels[plotdict["channel"]]:
      #    self.plotsinchannel(altChannel).append(plotdict["name"])
      #    for v in plotdict["vars"]:
      #      if not(v in self.varstoload[altChannel]):
      #        self.varstoload[altChannel].append(v)

  def getRawHistogramsAndNorms(self, options):
    for plotName in self.plots:
      p = self.plots[plotName]
      if p["bins"][0] == "uniform": #Then it is nbins, minX, maxX
        self.histos[plotName] = {}
        self.histos[plotName]["total"] = ROOT.TH1F(plotName + "_" + self.name, plotName + "_" + self.name, p["bins"][1], p["bins"][2], p["bins"][3])
      elif p["bins"][0] == "limits":
        self.histos[plotName] = {}
        self.histos[plotName]["total"] = ROOT.TH1F(plotName + "_" + self.name, plotName + "_" + self.name, p["bins"][2], array.array('f', p["bins"][1])) 
      elif p["bins"][0] == "2Duniform": 
        self.histos[plotName] = {}
        self.histos[plotName]["total"] = ROOT.TH2F(plotName + "_" + self.name, plotName + "_" + self.name, p["bins"][1], p["bins"][2], p["bins"][3], p["bins"][4], p["bins"][5], p["bins"][6])
      elif p["bins"][0] == "2Dlimits":
        self.histos[plotName] = {}
        self.histos[plotName]["total"] = ROOT.TH2F(plotName + "_" + self.name, plotName + "_" + self.name, p["bins"][1], array.array('f', p["bins"][2]), p["bins"][3],  array.array('f', p["bins"][4]))

      if not(self.isData): self.norms[plotName] = 0 if not("skim" in self.config) else self.norm
      if self.doSyst:
        for var in self.variations:
          if self.variations[var]["symmetrize"]:
            self.histos[plotName+ "_" + var + "Up"] = {}
            self.histos[plotName+ "_" + var + "Up"]["total"] = self.histos[plotName]["total"].Clone(plotName + "_" + self.name +  "_" + var + "Up")
            self.histos[plotName+ "_" + var + "Dn"] = {}
            self.histos[plotName+ "_" + var + "Dn"]["total"] = self.histos[plotName]["total"].Clone(plotName + "_" + self.name +  "_" + var + "Dn")
          else:
            self.histos[plotName+ "_" + var] = {}
            self.histos[plotName+ "_" + var]["total"] = self.histos[plotName]["total"].Clone(plotName + "_" + self.name +  "_" + var)

    print(self.name, "Pre-load")
    if not(options.toLoad):
      for iff, f in enumerate(self.hdfiles):
        if (iff %1 == 0): print("Loading file %i/%i : %s"%(iff, len(self.hdfiles),self.safefiles[iff]))
        self.getRawHistogramsAndNormsOneFile([f,self.safefiles[iff], options])
    elif self.dohadd: # Then, we collect from all files into a single hadd
      self.haddedfile = self.getRawHistogramsAndNormsHadd(options)
      self.haddedTFile = ROOT.TFile(self.haddedfile, "READ")
    elif options.fromROOT:
      self.getHistogramsAndNormsFromROOT()
    else:
      # Collect all filenames 
      outputFil = options.toLoad.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_hadded.root"

      if os.path.isfile(outputFil):
        print("Hadded file %s already exists, will read from there"%outputFil)
        self.haddedTFile = ROOT.TFile(outputFil, "READ")
        self.dohadd = True
      else:
        for iff, f in enumerate(self.safefiles):
          if (iff %1 == 0): print("Loading file %i/%i: %s"%(iff, len(self.safefiles), f))
          self.getRawHistogramsAndNormsOneFile(["",self.safefiles[iff], options])

    # After all is said and done, add up histograms and normalize to xsec
    if options.toSave or options.fromROOT: #If only saving or if already full histograms, no need to continue merging 
      return
    for c in self.channels:
      for plotName in self.plotsinchannel[c]:
        p = self.plots[plotName]
        for iff, f in enumerate(self.safefiles):
          if options.toLoad and not("skim" in self.config) and not(self.isData) and not(self.noWeights): # If loading and unskimmed, need to set the norm here
            self.norms[plotName] += self.nnorms[self.safefiles[iff]]
          elif self.noWeights: self.norms[plotName] = 1
          if not(self.dohadd):
            filename = self.safefiles[iff].split("/")[-1].replace("out_","").replace(".hdf5","")
            print(filename)#, plotName, self.histos[plotName][filename].Integral())
            self.histos[plotName]["total"].Add(self.histos[plotName][filename])
            del self.histos[plotName][filename]
            if self.doSyst:
              for var in self.variations:
                if self.variations[var]["symmetrize"]:
                  self.histos[plotName+ "_" + var + "Up"]["total"].Add(self.histos[plotName+ "_" + var + "Up"][filename])
                  self.histos[plotName+ "_" + var + "Dn"]["total"].Add(self.histos[plotName+ "_" + var + "Dn"][filename])
                  del self.histos[plotName+ "_" + var + "Up"][filename]
                  del self.histos[plotName+ "_" + var + "Dn"][filename]
                else:
                  self.histos[plotName+ "_" + var]["total"].Add(self.histos[plotName+ "_" + var][filename])
                  del self.histos[plotName+ "_" + var][filename]
        if not(self.dohadd):
          #print("Creating hadded file")
          outputFil = options.toLoad.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_hadded.root"
          self.haddedTFile = ROOT.TFile(outputFil, "UPDATE")
          self.haddedTFile.cd()
          self.histos[plotName]["total"].Write()
          if self.doSyst:
            for var in self.variations:
              if self.variations[var]["symmetrize"]:
                self.histos[plotName+ "_" + var + "Up"]["total"].Write()
                self.histos[plotName+ "_" + var + "Dn"]["total"].Write()
              else:
                self.histos[plotName+ "_" + var]["total"].Write()
          self.haddedTFile.Close()
        if self.dohadd:
          print(plotName + "_" + self.name)
          self.histos[plotName]["total"] = self.haddedTFile.Get(plotName + "_" + self.name)
          if self.doSyst:
            for var in self.variations:
              if self.variations[var]["symmetrize"]:
                self.histos[plotName+ "_" + var + "Up"]["total"] = self.haddedTFile.Get(plotName + "_" + self.name +  "_" + var + "Up")
                self.histos[plotName+ "_" + var + "Dn"]["total"] = self.haddedTFile.Get(plotName + "_" + self.name +  "_" + var + "Dn")
              else:
                self.histos[plotName+ "_" + var]["total"] = self.haddedTFile.Get(plotName + "_" + self.name +  "_" + var)
        # Not needed, as the sumw2 structure exists already
        #self.histos[plotName]["total"].Sumw2() # To get proper stat. unc.
        #if self.doSyst:
        #  for var in self.variations:
        #    if self.variations[var]["symmetrize"]:
        #      self.histos[plotName+ "_" + var + "Up"]["total"].Sumw2()
        #      self.histos[plotName+ "_" + var + "Dn"]["total"].Sumw2()
        #    else:
        #      self.histos[plotName+ "_" + var]["total"].Sumw2()

        if not(self.isData) and (self.norms[plotName] > 0): 
          print(self.name, plotName)
          if not(self.noWeights):
            self.histos[plotName]["total"].Scale((options.luminosity if not("partialLumi" in self.config) else self.config["partialLumi"])*self.config["xsec"]/self.norms[plotName])
        if "scale" in self.config:
          self.histos[plotName]["total"].Scale(self.config["scale"])

        self.yields[plotName] = self.histos[plotName]["total"].Integral()
        if self.doSyst:
          for var in self.variations:
            if self.variations[var]["symmetrize"]:
              if not(self.noWeights):
                self.histos[plotName+ "_" + var + "Up"]["total"].Scale((options.luminosity if not("partialLumi" in self.config) else self.config["partialLumi"])*self.config["xsec"]/max(0.0001,self.norms[plotName]))
                self.histos[plotName+ "_" + var + "Dn"]["total"].Scale((options.luminosity if not("partialLumi" in self.config) else self.config["partialLumi"])*self.config["xsec"]/max(0.0001,self.norms[plotName]))
              if "scale" in self.config:
                self.histos[plotName+ "_" + var + "Up"]["total"].Scale(self.config["scale"])
                self.histos[plotName+ "_" + var + "Dn"]["total"].Scale(self.config["scale"])
            else:
              if not(self.noWeights):
                print(var, plotName, self.name)
                self.histos[plotName+ "_" + var]["total"].Scale((options.luminosity if not("partialLumi" in self.config) else self.config["partialLumi"])*self.config["xsec"]/max(0.0001,self.norms[plotName]))
              if "scale" in self.config:
                self.histos[plotName+ "_" + var]["total"].Scale(self.config["scale"])
    
  def getHistogramsAndNormsFromROOT(self):
    print("FROMROOT")
    inROOT= ROOT.TFile(options.toLoad, "READ")
    for c in self.channels:
      for plotName in self.plotsinchannel[c]:
        print("1", self.histos)
        p = self.plots[plotName]
        print(self.config["th1"][""])
        self.histos[plotName]["total"]       = copy.deepcopy(inROOT.Get(self.config["th1"][""]))
        if not("data" in self.name):
          self.histos[plotName+"_Up"]["total"] = copy.deepcopy(inROOT.Get(self.config["th1"]["Up"]))
          self.histos[plotName+"_Dn"]["total"] = copy.deepcopy(inROOT.Get(self.config["th1"]["Dn"]))
        print("2", self.histos)

  def getRawHistogramsAndNormsOneFile(self, g):
    f, safefile, options = g[0], g[1], g[2]
    filename = safefile.split("/")[-1].replace("out_","").replace(".hdf5","")
    if not(options.toLoad):  
      if options.toSave:
        rf = ROOT.TFile(options.toSave.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_" + filename + ".root", "RECREATE")

      for plotName in self.plots:
        self.histos[plotName][filename]  = self.histos[plotName]["total"].Clone(self.histos[plotName]["total"].GetName() + "_" + filename)
        if self.doSyst:
          for var in self.variations:
            if self.variations[var]["symmetrize"]:
              self.histos[plotName+ "_" + var + "Up"][filename] = self.histos[plotName+ "_" + var + "Up"]["total"].Clone(self.histos[plotName+ "_" + var + "Up"]["total"].GetName() + "_" + filename)
              self.histos[plotName+ "_" + var + "Dn"][filename] = self.histos[plotName+ "_" + var + "Dn"]["total"].Clone(self.histos[plotName+ "_" + var + "Dn"]["total"].GetName() + "_" + filename)
            else:
              self.histos[plotName+ "_" + var][filename] = self.histos[plotName+ "_" + var]["total"].Clone(self.histos[plotName+ "_" + var]["total"].GetName() + "_" + filename)
      for cpre in self.channels:
        c = cpre
        if "replaceChannel" in  self.config:
          if cpre in self.config["replaceChannel"]: # This is needed for systematics that change event variables, like JES or TRACK
            c = self.config["replaceChannel"][cpre]
        empty = True if type(f[c]) == type([]) else False # Check if there are events there
        if empty: print("Is empty!", c)
        weights = {}
        if not(self.isData or self.noWeights):
          if empty or (len(f[c]) == 0):
            empty = True
            weights[""] = []
          else:
            weights[""] = f[c]["genweight"]
            if self.doSyst:
              for var in self.variations:
                if c in self.variations[var]["replaceChannel"]:
                  if not(self.variations[var]["replaceChannel"][c] in weights):
                    if empty or type(f[self.variations[var]["replaceChannel"][c]]) != type(f[c]):
                      weights[var] = []
                    else:
                      weights[var] = f[self.variations[var]["replaceChannel"][c]]["genweight"]
        else: 
          if empty:
            weights[""] = []
          else:
            weights[""] = np.ones(len(f[c]))
        if "extraWeights" in self.config:
          extraweights = {}
          if empty:
            extraweights[""] = []
          else:
            extraweights[""] = self.config["extraWeights"](f[c])

          if self.doSyst:
            for var in self.variations:
              if empty:
               extraweights[var] = []
              elif not(c in self.variations[var]["replaceChannel"]):
                extraweights[var] = extraweights[""]*self.variations[var]["extraWeights"](f[c])
              elif type(f[self.variations[var]["replaceChannel"][c]]) != type(f[c]): # Basically check if variation is empty, as variations might change selection
                extraweights[var] = []
              else:
                extraweights[var] = self.variations[var]["extraWeights"](f[self.variations[var]["replaceChannel"][c]])
        for plotName in self.plotsinchannel[cpre]:
          p = self.plots[plotName]
          if not("skim" in self.config) and not(self.isData) and not(self.noWeights):
            self.norms[plotName] += self.nnorms[safefile]
          if "2D" in p["bins"][0]:
            values, values2, weightsNom = {}, {} , {}
            if empty:
              values[""], values2[""], weightsNom[""] = [], [], []
              if self.doSyst:
                for var in self.variations:
                  if (c in self.variations[var]["replaceChannel"]):
                    values[var], values2[var], weightsNom[var] = [], [], []
            else:
              values[""], values2[""], weightsNom[""] = p["value"](f[c], weights[""])

              if self.doSyst:
                for var in self.variations:
                  if (c in self.variations[var]["replaceChannel"]) and type(f[self.variations[var]["replaceChannel"][c]]) == type(f[c]):
                    values[var], values2[var], weightsNom[var] = p["value"](f[self.variations[var]["replaceChannel"][c]], weights[var])
                  elif (c in self.variations[var]["replaceChannel"]):
                    values[var], values2[var], weightsNom[var] = [], [], []
          else:
            values, weightsNom = {}, {}
            if empty:
              values[""], weightsNom[""] = [], []
              if self.doSyst:
                for var in self.variations:
                  if (c in self.variations[var]["replaceChannel"]):
                    values[var], weightsNom[var] = [], []
            else:
              values[""], weightsNom[""] = p["value"](f[c], weights[""])

              if self.doSyst:
                for var in self.variations:
                  if (c in self.variations[var]["replaceChannel"]) and type(f[self.variations[var]["replaceChannel"][c]]) == type(f[c]):
                    values[var], weightsNom[var] = p["value"](f[self.variations[var]["replaceChannel"][c]], weights[var])
                  elif (c in self.variations[var]["replaceChannel"]):
                    values[var], weightsNom[var] = [], []
          if "extraWeights" in self.config:
            weightsHere = {}
            for var in extraweights:
                if empty:
                  weightsHere[var] = []
                elif var == "":
                  weightsHere[var] = weightsNom[var]*extraweights[var]
                elif (var in self.variations) and not(c in self.variations[var]["replaceChannel"]):
                  weightsHere[var] = weightsNom[""]*extraweights[var]
                elif type(f[self.variations[var]["replaceChannel"][c]]) == type(f[c]):
                  weightsHere[var] = weightsNom[var]*extraweights[var]
                else:
                  weightsHere[var] = weightsNom[var] # Empty, in fact
          else:
            weightsHere = weightsNom

          if "2D" in p["bins"][0]:
            #for iev in range(len(weightsHere[""])):
            #  if weightsHere[""][iev] > 0:
            #    print(iev, weightsHere[""][iev], values[""][iev], values2[""][iev])
            #print(sum(weightsHere[""]))

            root_numpy.fill_hist(self.histos[p["name"]][filename], np.vstack([values[""], values2[""]]).T, weightsHere[""])
            if self.doSyst:
              for var in self.variations:
                if not(c in self.variations[var]["replaceChannel"]):
                  root_numpy.fill_hist(self.histos[p["name"]+ "_" + var + ("Up" if self.variations[var]["symmetrize"] else "")][filename], np.vstack([values[""], values2[""]]).T, weightsHere[var])
          else:
            #for iev in range(len(weightsHere[""])):
            #  if weightsHere[""][iev] > 0:
            #    print(iev, weightsHere[""][iev], values[""][iev])
            #print(sum(weightsHere[""]))
            root_numpy.fill_hist(self.histos[p["name"]][filename], values[""], weightsHere[""])
            if self.doSyst:
              for var in self.variations:
                if not(c in self.variations[var]["replaceChannel"]):
                  root_numpy.fill_hist(self.histos[p["name"]+ "_" + var + ("Up" if self.variations[var]["symmetrize"] else "")][filename], values[""], weightsHere[var])

          for altchan in values:
            if altchan == "": continue # Skip nominal
            if "2D" in p["bins"][0]:
              for var in self.variations:
                if var == altchan:
                  root_numpy.fill_hist(self.histos[p["name"]+ "_" + var + ("Up" if self.variations[var]["symmetrize"] else "")][filename], np.vstack([values[var], values2[var]]).T, weightsHere[var])
            else:
              for var in self.variations:
                if var == altchan:
                  root_numpy.fill_hist(self.histos[p["name"]+ "_" + var + ("Up" if self.variations[var]["symmetrize"] else "")][filename], values[var], weightsHere[var])


          if self.doSyst:
            for var in self.variations:
              if self.variations[var]["symmetrize"]:
                if "2D" in p["bins"][0]:
                  for ibin in range(0, self.histos[p["name"]+ "_" + var + "Up"][filename].GetNbinsX()+1):
                    for jbin in range(0, self.histos[p["name"]+ "_" + var + "Up"][filename].GetNbinsY()+1):
                      cent = self.histos[p["name"]][filename].GetBinContent(ibin, jbin)
                      up   = self.histos[p["name"]+ "_" + var + "Up"][filename].GetBinContent(ibin, jbin)
                      down = max(0,cent*2 - up)
                      self.histos[p["name"]+ "_" + var + "Dn"][filename].SetBinContent(ibin, jbin, down)
                      self.histos[p["name"]+ "_" + var + "Dn"][filename].SetBinError(ibin, jbin, self.histos[p["name"]][filename].GetBinError(ibin, jbin))
                else:
                  for ibin in range(0, self.histos[p["name"]+ "_" + var + "Up"][filename].GetNbinsX()+1):
                    cent = self.histos[p["name"]][filename].GetBinContent(ibin)
                    up   = self.histos[p["name"]+ "_" + var + "Up"][filename].GetBinContent(ibin)
                    down = max(0,cent*2 - up)
                    self.histos[p["name"]+ "_" + var + "Dn"][filename].SetBinContent(ibin, down)
                    self.histos[p["name"]+ "_" + var + "Dn"][filename].SetBinError(ibin, self.histos[p["name"]][filename].GetBinError(ibin))

          if options.toSave:
            rf.cd()
            self.histos[p["name"]][filename].Write()
            if self.doSyst:
              for var in self.variations:
                if self.variations[var]["symmetrize"]:
                  self.histos[p["name"]+ "_" + var + "Up"][filename].Write()
                  self.histos[p["name"]+ "_" + var + "Dn"][filename].Write()
                else:
                  self.histos[p["name"]+ "_" + var][filename].Write()

      if options.toSave: 
        rf.Close() 
    else:
      rf = ROOT.TFile(options.toLoad.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_" + filename + ".root", "READ")
      for plotName in self.plots:
        self.histos[plotName][filename] = copy.copy(rf.Get(self.histos[plotName]["total"].GetName() + "_" + filename))
        if self.doSyst:
          for var in self.variations:
            if self.variations[var]["symmetrize"]:
              self.histos[plotName+ "_" + var + "Up"][filename] = copy.copy(rf.Get(self.histos[plotName+ "_" + var + "Up"]["total"].GetName() + "_" + filename))
              self.histos[plotName+ "_" + var + "Dn"][filename] = copy.copy(rf.Get(self.histos[plotName+ "_" + var + "Dn"]["total"].GetName() + "_" + filename))
            else:
              self.histos[plotName+ "_" + var][filename] = copy.copy(rf.Get(self.histos[plotName+ "_" + var]["total"].GetName() + "_" + filename))

  def getRawHistogramsAndNormsHadd(self, options):
    # Collect all filenames 
    inputFiles = []
    for iff, f in enumerate(self.safefiles):
      safefile = self.safefiles[iff]
      filename = safefile.split("/")[-1].replace("out_","").replace(".hdf5","")
      inputFiles.append(options.toLoad.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_" + filename + ".root")
    outputFil = options.toLoad.replace("{YEAR}", self.config["year"]) + "/" + self.name + "_hadded.root" 

    if os.path.isfile(outputFil):
      print("Hadded file %s already exists, will read from there"%outputFil)
    else:
      print("Will hadd %i files into %s"%(len(inputFiles), outputFil))
      # Run our paralellized hadd
      haddAll(inputFiles, outputFil, nThreads=options.jobs)
    return outputFil

  def setStyleOptions(self):
    for key in self.histos:
      if "linecolor" in self.config: 
        self.histos[key]["total"].SetLineColor(self.config["linecolor"])
      if "fillcolor" in self.config:
        self.histos[key]["total"].SetFillColor(self.config["fillcolor"])
        self.histos[key]["total"].SetMarkerColor(self.config["fillcolor"])
      if "style" in self.config:
        self.histos[key]["total"].SetLineStyle(self.config["style"])
      if "markerstyle" in self.config:
        self.histos[key]["total"].SetMarkerStyle(self.config["markerstyle"])
      if "markersize" in self.config:
        self.histos[key]["total"].SetMarkerSize(self.config["markersize"])


  def isBackground(self):
    bkg = True
    if "isSig" in self.config: bkg = not(self.config["isSig"])
    if self.isData: return False
    return bkg

  def isSignal(self):
    return not(self.isData or self.isBackground())


class plotter(object):
  def __init__(self, plotdicts, sampledicts, options):
    self.plots      = plotdicts #[plotdicts[d] for d in plotdicts]
    self.samples    = [sample(sampledicts[d], options) for d in sampledicts]
    self.doSyst     = options.systFile
    print("...Initializing plotter")
    print("...Will run over %i samples"%(sum([len(s.safefiles) for s in self.samples])))
    for p in self.plots:
      for s in self.samples:
        s.addPlot(self.plots[p])

  def createJobs(self, options, command):
    iJob = 0
    csize = 0
    clength = 0
    cfiles = []
    if options.toLoad: options.batchsize = 1e6 # No chunks when merging
    for s in self.samples:
      s.initAllForQueue(options)
      if len(s.safefiles) == 0: continue
      if options.toLoad: #toLoad jobs are hadding ones, let's check if needed
        outputFil = options.toLoad.replace("{YEAR}", s.config["year"]) + "/" + s.name + "_hadded.root"
        if os.path.isfile(outputFil):
          print("Hadded file %s already exists, will read from there"%outputFil)
          continue
      sname = s.name
      if not (options.smartSplitting):
        nfiles = len(s.safefiles)
        options.batchsize = int(options.batchsize)
        chunks = int(math.ceil(nfiles*1./(options.batchsize)))

        if chunks == 1:
          jobfile = open("%s/exec/_%i.sh"%(options.jobname, iJob),"w")
          jobfile.write("#!/bin/bash\n")
          #jobfile.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh\n")
          if not(options.queue == "local"):  jobfile.write("cd /eos/user/c/cericeci/CMSSW_10_6_29/src/\n")
          if not(options.queue == "local"):  jobfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
          if not(options.queue == "local"):  jobfile.write("cmsenv\n")
          if not(options.queue == "local"):  jobfile.write("cd %s\n"%os.getcwd())
          jobfile.write(command + " --sample %s --files %s"%(sname, ",".join(s.safefiles)))
          jobfile.close()
          iJob += 1
        else:
          for i in range(chunks-1):
            jobfile = open("%s/exec/_%i.sh"%(options.jobname, iJob),"w")
            jobfile.write("#!/bin/bash\n")
            #jobfile.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh\n")
            if not(options.queue == "local"): jobfile.write("cd /eos/user/c/cericeci/CMSSW_10_6_29/src/\n")
            if not(options.queue == "local"): jobfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
            if not(options.queue == "local"): jobfile.write("cmsenv\n")
            if not(options.queue == "local"): jobfile.write("cd /eos/home-c/cericeci/SUEP/SUEPCoffea_dask/plotting/\n")
            jobfile.write(command + " --sample %s --files %s"%(sname, ",".join(s.safefiles[i*options.batchsize:(i+1)*options.batchsize])))
            iJob += 1
            jobfile.close()

          jobfile = open("%s/exec/_%i.sh"%(options.jobname, iJob),"w")
          jobfile.write("#!/bin/bash\n")
          #jobfile.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh\n")
          if not(options.queue == "local"): jobfile.write("cd /eos/user/c/cericeci/CMSSW_10_6_29/src/\n")
          if not(options.queue == "local"): jobfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
          if not(options.queue == "local"): jobfile.write("cmsenv\n")
          if not(options.queue == "local"): jobfile.write("cd %s\n"%os.getcwd())
          jobfile.write(command + " --sample %s --files %s"%(sname, ",".join(s.safefiles[(chunks-1)*options.batchsize:])))
          jobfile.close()
          iJob += 1
      else: # For smart splitting we add files until we pass the size threshold 
        for f in s.safefiles:
          cfiles.append(f)
          csize += os.path.getsize(f)/(1024*1024)
          clength  += 1
          if (csize >= float(options.batchsize)) or (clength >= 500):
            jobfile = open("%s/exec/_%i.sh"%(options.jobname, iJob),"w")
            jobfile.write("#!/bin/bash\n")
            if not(options.queue == "local"): jobfile.write("cd /eos/user/c/cericeci/CMSSW_10_6_29/src/\n")
            if not(options.queue == "local"): jobfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
            if not(options.queue == "local"): jobfile.write("cmsenv\n")
            if not(options.queue == "local"): jobfile.write("cd %s\n"%os.getcwd())
            jobfile.write(command + " --files %s"%(",".join(cfiles)))
            jobfile.close()
            iJob += 1
            csize = 0
            clength = 0
            cfiles = []
    if options.smartSplitting and len(cfiles) != 0:
      jobfile = open("%s/exec/_%i.sh"%(options.jobname, iJob),"w")
      jobfile.write("#!/bin/bash\n")
      if not(options.queue == "local"): jobfile.write("cd /eos/user/c/cericeci/CMSSW_10_6_29/src/\n")
      if not(options.queue == "local"): jobfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
      if not(options.queue == "local"): jobfile.write("cmsenv\n")
      if not(options.queue == "local"): jobfile.write("cd %s\n"%os.getcwd())
      jobfile.write(command + " --files %s"%(",".join(cfiles)))
      jobfile.close()
      iJob += 1
      csize = 0
      clength = 0
      cfiles = []

    return iJob

  def doPlots(self, options):
    for s in self.samples:
      s.initAll(options)

    self.getRawHistogramsAndNorms(options)
    if not(options.toSave): self.doStackPlots(options) # I.e., we are loading and not in a hadd job

  def getRawHistogramsAndNorms(self, options):
    for s in self.samples:
      print("...Processing histograms for %s"%s.name)
      s.getRawHistogramsAndNorms(options)
      s.setStyleOptions()

  def doStackPlots(self, options):
    for plotName in self.plots:
      try:
        #if True:
        print("...Plotting %s"%plotName)
        mode = "stack"
        if "mode" in self.plots[plotName]: mode = self.plots[plotName]["mode"]
        if mode == "stack": self.doStackPlot(plotName, options)
        if mode == "colz": self.doColZPlots(plotName, options)
        ## More to be implemented
      except Exception as e:
        if options.debug: raise
        print("Something went wrong with %s: "%plotName, e)

  def doColZPlots(self, pname, options):
    theIndivs= []
    # Background go into the stack
    stacksize = 0
    back = False
    data = False
    if options.ordered:
      self.samples.sort(key= lambda x: x.yields[pname], reverse=False)
    for s in self.samples:
      #print(s.name, s.histos[pname]["total"].Integral())
      if s.isBackground():
        if not(back): back = s.histos[pname]["total"].Clone("total_background")
        else: back.Add(s.histos[pname]["total"])
        if not(options.onlytotal): self.draw2DColZ(pname, s.histos[pname]["total"], s.name, options)
      elif s.isData:
        if not(data): data = s.histos[pname]["total"].Clone("total_data")
        else:         data.Add(s.histos[pname]["total"])
        #self.draw2DColZ(pname, s.histos[pname]["total"], s.name, options)
      else:
        theIndivs.append(s.histos[pname]["total"])
        self.draw2DColZ(pname, s.histos[pname]["total"], s.name, options)

    self.draw2DColZ(pname, back, "background", options)
    self.draw2DColZ(pname, data, "data", options)

  def draw2DColZ(self, pname, histo, sname, options):
    if sname == "data" and options.blind: return
    p = self.plots[pname]
    c = ROOT.TCanvas(pname,pname, 900,600)
    p1 = ROOT.TPad("mainpad", "mainpad", 0, 0, 1, 1)
    p1.SetBottomMargin(0.1)
    p1.SetTopMargin(0.1)
    p1.SetLeftMargin(0.12)
    p1.SetRightMargin(0.15)
    if "margins" in p:
      p1.SetBottomMargin(p["margins"][0])
      p1.SetTopMargin(p["margins"][1])
      p1.SetLeftMargin(p["margins"][2])
      p1.SetRightMargin(p["margins"][3])
    p1.SetLogz(True)
    p1.Draw()
    p1.cd()
    if "maxZ" in p:
      histo.SetMaximum(p["maxZ"])
    if "minZ" in p:
      histo.SetMaximum(p["minZ"])

    #for ibin in range(1, histo.GetNbinsX()+1):
    #  for jbin in range(1, histo.GetNbinsY()+1):
    #    if histo.GetBinContent(ibin, jbin) < 0:
    #       histo.SetBinContent(ibin, jbin, 0)
    histo.SetTitle("")
    histo.Draw("colz")
    histo.GetXaxis().SetLabelSize(0.03)
    histo.GetYaxis().SetLabelSize(0.03)
    #histo.GetYaxis().SetTitleSize(0.08)
    histo.GetYaxis().SetTitleOffset(0.72)
    histo.GetZaxis().SetTitle("Events")
    histo.GetYaxis().SetTitle(p["ylabel"])
    histo.GetXaxis().SetTitle(p["xlabel"])

    if "normalizeX" in p:
      if p["normalizeX"]:
        p1.SetLogz(False)
        projY  = histo.ProjectionY() 
        for i in range(1,histo.GetNbinsX()+1):
          for j in range(1,histo.GetNbinsY()+1):
            histo.SetBinContent(i, j, histo.GetBinContent(i,j)/(max(projY.GetBinContent(j), 0.00001)))
        histo.SetMaximum(0.25)
        histo.SetMinimum(0.)
        histo.GetZaxis().SetTitle("Events/All events at %s band"%p["ylabel"])

    CMS_lumi.writeExtraText = True

    CMS_lumi.lumi_13TeV = "%.1f fb^{-1}" % options.luminosity if options.luminosity > 1. else "%.3f fb^{-1}" % options.luminosity
    CMS_lumi.extraText  = "Preliminary"
    CMS_lumi.lumi_sqrtS = "13"
    CMS_lumi.CMS_lumi(p1, 4, 0, 0.122)

    if len(options.addLines) > 0:
      tlines = []
      for l in options.addLines:
        #print("NEW LINE", l)
        x1, y1, x2, y2 = [float(x) for x in l.split(",")]
        tlines.append(ROOT.TLine(x1, y1, x2, y2))
        tlines[-1].SetLineStyle(3)
        tlines[-1].SetLineWidth(3)
        tlines[-1].SetLineColor(ROOT.kBlack)
        tlines[-1].Draw("same")
    if len(options.addText) > 0:
      ttext = []
      for l in options.addText:
        #print("NEW TEXT", l)
        text, coords, size = l.split(":")
        coords = [float(x) for x in coords.split(",")]
        ttext.append(ROOT.TText(coords[0], coords[1], text))
        ttext[-1].SetTextColor(ROOT.kBlack)
        ttext[-1].SetTextSize(float(size))
        ttext[-1].Draw("same")
    c.SaveAs(options.plotdir +  "/" + sname + "_"  +  p["plotname"] + ".pdf")
    c.SaveAs(options.plotdir +  "/" + sname + "_"  +  p["plotname"] + ".png")
    # Also save in root file 
    tf = ROOT.TFile(options.plotdir + "/" + p["plotname"] + ".root", "UPDATE")
    histo.Write()
    tf.Close()

  def doSystVariations(self, systfile, pname, options, nomstack):
    # Only background uncertainties for plotting
    theStacks = {} 
    histosToSave = {}
    systsFile = imp.load_source("systematicsAndShapes", systfile)
    systsFile = systsFile.systematicsAndShapes
    for syst in systsFile:
      if syst == "yields": continue
      # Background go into the stack
      backUp = False
      backDn = False
      #if debug: print("...Getting syst %s"%syst)
      nbins = self.samples[0].histos[pname]["total"].GetNbinsX()
      thePlotGroups = {}
      for s in self.samples:
        if "isSyst" in s.config:
          if s.config["isSyst"]:
            continue

        if s.isBackground():
          if systsFile[syst]["type"] == "lnN":
            # Flat, so no need to search for shapes
            tmpUp = s.histos[pname]["total"].Clone("tmp%s%sUp"%(s.name, syst))
            tmpDn = s.histos[pname]["total"].Clone("tmp%s%sDn"%(s.name, syst))
            if any([re.match(pr, s.name) for pr in systsFile[syst]["processes"]]):
              sizeHere  = 1.
              sizeinCfg = systsFile[syst]["size"]
              if type(sizeinCfg) == type(1.0001):
                sizeHere = sizeinCfg
              else: 
                sizeHere = 1. # TODO: do proper reading here 
              tmpUp.Scale(sizeHere)
              tmpDn.Scale(1./sizeHere)
          if systsFile[syst]["type"] == "shape":
            altNameUp = systsFile[syst]["match"].replace("$PROCESS", s.name).replace("$SYSTEMATIC", syst).replace("[VAR]_[CHANNEL]", pname).replace("[VAR]", pname) + systsFile[syst]["up"]
            altNameDn = systsFile[syst]["match"].replace("$PROCESS", s.name).replace("$SYSTEMATIC", syst).replace("[VAR]_[CHANNEL]", pname).replace("[VAR]", pname) + systsFile[syst]["down"]
            tmpUp, tmpDn = None, None
            if any([re.match(pr, s.name) for pr in systsFile[syst]["processes"]]): 
              # Then we need to find alternative histograms, they can be configured through alternative samples (i.e. alternative files) or through variations of a sample, so it is tricky to find
              tmpUp, tmpDn = None, None
              for ss in self.samples: # First check if it is a separate sample
                if ss.name == altNameUp:
                  ss.histos[pname]["total"] = ss.histos[pname]["total"].Rebin(options.rebin) if options.rebin else ss.histos[pname]["total"]
                  tmpUp = ss.histos[pname]["total"].Clone(altNameUp)
                if ss.name == altNameDn:
                  ss.histos[pname]["total"] = ss.histos[pname]["total"].Rebin(options.rebin) if options.rebin else ss.histos[pname]["total"]
                  tmpDn = ss.histos[pname]["total"].Clone(altNameDn)
              # If here and not found, let's look at variations of the nominal
              if not(tmpUp) or not(tmpDn):
                for var in s.variations:
                  if s.variations[var]["symmetrize"]:
                    testUp = s.name + "_" + var + "Up"
                    testDn = s.name + "_" + var + "Dn"
                    #print(testUp, altNameUp, testDn, altNameDn)
                    if testUp == altNameUp or altNameDn == testDn:
                      #print("Pass and save")
                      tmpUp = s.histos[pname+ "_" + var + "Up"]["total"].Clone(altNameUp).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var + "Up"]["total"].Clone(altNameUp)
                      tmpDn = s.histos[pname+ "_" + var + "Dn"]["total"].Clone(altNameDn).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var + "Dn"]["total"].Clone(altNameDn)
                      tmpNom = s.histos[pname]["total"]
                      for ibin in range(tmpUp.GetNbinsX()+1):
                        cent = tmpNom.GetBinContent(ibin)
                        up   = tmpUp.GetBinContent(ibin)
                        tmpDn.SetBinContent(ibin, max(0, 2*cent-up))
                  else:
                    test =  s.name + "_" + var 
                    if test == altNameUp:
                      tmpUp = s.histos[pname+ "_" + var]["total"].Clone(altNameUp).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var]["total"].Clone(altNameUp)
                    if test == altNameDn:
                      tmpDn = s.histos[pname+ "_" + var]["total"].Clone(altNameDn).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var]["total"].Clone(altNameDn)
              #print(altNameUp, tmpUp.GetName(), type(tmpUp))
              if altNameUp in histosToSave: # Weird stuff for the Run II systematics
                histosToSave[altNameUp].Add(tmpUp)  
              else:
                histosToSave[altNameUp] = copy.deepcopy(tmpUp)
              if altNameDn in histosToSave:
                histosToSave[altNameDn].Add(tmpDn)
              else:
                histosToSave[altNameDn] = copy.deepcopy(tmpDn)
            else:
              # In this case just read nominal
              tmpUp = s.histos[pname]["total"].Clone(altNameUp)
              tmpDn = s.histos[pname]["total"].Clone(altNameDn)
          if not(backUp):
            #print(s.name, syst, pname)
            backUp = tmpUp.Clone().Clone("total_background_%sUp"%syst)
            backDn = tmpDn.Clone().Clone("total_background_%sUp"%syst)
          else: 
            backUp.Add(tmpUp)
            backDn.Add(tmpDn)
        if systsFile[syst]["type"] == "shape" and s.isSignal() and any([re.match(pr, s.name) for pr in systsFile[syst]["processes"]]): # For signals just save
          # Then we need to find alternative histograms
          tmpUp, tmpDn = None, None
          altNameUp = systsFile[syst]["match"].replace("$PROCESS", s.name).replace("$SYSTEMATIC", syst).replace("[VAR]_[CHANNEL]_", "").replace("[VAR]_", "") + systsFile[syst]["up"]
          altNameDn = systsFile[syst]["match"].replace("$PROCESS", s.name).replace("$SYSTEMATIC", syst).replace("[VAR]_[CHANNEL]_", "").replace("[VAR]_", "") + systsFile[syst]["down"]
          for ss in self.samples:
            #print(ss.name, altNameUp, altNameDn)
            if ss.name == altNameUp:
              ss.histos[pname]["total"] = ss.histos[pname]["total"].Rebin(options.rebin) if options.rebin else ss.histos[pname]["total"]
              tmpUp = ss.histos[pname]["total"].Clone(altNameUp)
            if ss.name == altNameDn:
              ss.histos[pname]["total"] = ss.histos[pname]["total"].Rebin(options.rebin) if options.rebin else ss.histos[pname]["total"]
              tmpDn = ss.histos[pname]["total"].Clone(altNameDn)
          if not(tmpUp) or not(tmpDn):
            for var in s.variations:
              if s.variations[var]["symmetrize"]:
                testUp = s.name + "_" + var + "Up"
                testDn = s.name + "_" + var + "Dn"
                if testUp == altNameUp or altNameDn == testDn:
                  tmpUp = s.histos[pname+ "_" + var + "Up"]["total"].Clone(altNameUp).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var + "Up"]["total"].Clone(altNameUp)
                  tmpDn = s.histos[pname+ "_" + var + "Dn"]["total"].Clone(altNameDn).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var + "Up"]["total"].Clone(altNameDn)
                  tmpNom = s.histos[pname]["total"]
                  for ibin in range(tmpUp.GetNbinsX()+1):
                    cent = tmpNom.GetBinContent(ibin)
                    up   = tmpUp.GetBinContent(ibin)
                    tmpDn.SetBinContent(ibin, max(0, 2*cent-up))
              else:
                test =  s.name + "_" + var
                if test == altNameUp:
                  tmpUp = s.histos[pname+ "_" + var]["total"].Clone(altNameUp).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var]["total"].Clone(altNameUp)
                if test == altNameDn:
                  tmpDn = s.histos[pname+ "_" + var]["total"].Clone(altNameDn).Rebin(options.rebin) if options.rebin else s.histos[pname+ "_" + var]["total"].Clone(altNameDn)
          if not(tmpUp) or not(tmpDn): # Catch: otherwise we wil be overwritten one histogram for each signal 
            pass
          else:
            if tmpUp:
              if altNameUp in histosToSave:
                histosToSave[altNameUp].Add(tmpUp)
              else:
                histosToSave[altNameUp] = copy.deepcopy(tmpUp)
            if tmpDn:
              if altNameDn in histosToSave:
                histosToSave[altNameDn].Add(tmpDn)
              else:
                histosToSave[altNameDn] = copy.deepcopy(tmpDn)
 
      theStacks["%sUp"%syst] = backUp
      theStacks["%sDn"%syst] = backDn
      histosToSave["%sUp"%syst] = backUp
      histosToSave["%sDn"%syst] = backDn
    #print(histosToSave)
    # Here we have all systs saved in theStacks, now we add systematics bin by bin
    nomHistoSyst = nomstack.Clone(nomstack.GetName() + "_Syst")
    for ibin in range(0,nomstack.GetNbinsX()+1):
      nom = nomstack.GetBinContent(ibin)
      nomup, nomdown = nomstack.GetBinError(ibin)**2, nomstack.GetBinError(ibin)**2 # Initialize to MC stat
      for syst in systsFile:
        if syst == "yields": continue
        nomupHere, nomdownHere = theStacks["%sUp"%syst].GetBinContent(ibin) - nom, theStacks["%sDn"%syst].GetBinContent(ibin) - nom
        if nomupHere*nomdownHere >= 0: # if same side, take biggest
          var = max(abs(nomupHere), abs(nomdownHere))
          if nomupHere < 0:
            nomdown += var**2
          else:
            nomup   += var**2
        else:
          if nomupHere >= 0:
            nomup   += nomupHere**2
            nomdown += nomdownHere**2
          else:
            nomdown += nomupHere**2
            nomup   += nomdownHere**2
      nomHistoSyst.SetBinError(ibin, max(nomup**0.5, nomdown**0.5))
    return nomHistoSyst, histosToSave


  def doStackPlot(self, pname, options):
   debug = True
   if debug: print("Do stack plot")
   #if True:
   try:
    p = self.plots[pname]
    c = ROOT.TCanvas(pname,pname, 800,1050) if not(options.wide) else ROOT.TCanvas(pname,pname, 1600, 1050)
    # Set pads
    p1 = ROOT.TPad("mainpad", "mainpad", 0, 0.30 if options.doRatio else 0.00, 1, 1)
    p1.SetBottomMargin(0.025)
    p1.SetTopMargin(0.14)
    p1.SetLeftMargin(0.12)
    if "margins" in p:
      p1.SetBottomMargin(p["margins"][0])
      p1.SetTopMargin(p["margins"][1])
      p1.SetLeftMargin(p["margins"][2])
      p1.SetRightMargin(p["margins"][3])
    p1.Draw()
    p1.SetLogy(True)
    if "logY" in p:
      p1.SetLogy(p["logY"])
    if "logX" in p:
      p1.SetLogx(p["logX"])
    if options.doRatio:
      p2 = ROOT.TPad("ratiopad", "ratiopad", 0, 0, 1, 0.30)
      p2.SetTopMargin(0.01)
      p2.SetBottomMargin(0.45)
      p2.SetLeftMargin(0.12)
      p2.SetFillStyle(0)
      if "logX" in p:
        p2.SetLogx(p["logX"])

    if "margins" in p:
      p1.SetLeftMargin(p["margins"][2])
      p1.SetRightMargin(p["margins"][3])
    p2.Draw()
    p1.cd()
    if debug: print("...Pads set")
    tl = ROOT.TLegend(p1.GetLeftMargin() ,0.55, 1-p1.GetRightMargin(), 1-p1.GetTopMargin())
    tl.SetNColumns(2)
    if "legendPosition" in p:
      tl = ROOT.TLegend(p["legendPosition"][0], p["legendPosition"][1], p["legendPosition"][2], p["legendPosition"][3])  
      tl.SetNColumns(2)
    # Now get the histograms and build the stack
    theStack = ROOT.THStack(pname+"_stack", pname)
    theIndivs= []
    theData  = []
    # Background go into the stack
    stacksize = 0
    back = False
    if debug: print("...Stack set")

    if options.ordered:
      self.samples.sort(key= lambda x: x.yields[pname], reverse=False)
    nbins = self.samples[0].histos[pname]["total"].GetNbinsX()
    thePlotGroups = {}
    thePlotGroupsSignal = {}
    thePlotGroupsData   = {}
    GroupsYields = {}
    if debug: print("...Samples ordered")
    for s in self.samples:
      if "isSyst" in s.config:
        if s.config["isSyst"]:
          continue
      if s.isBackground():
        if options.rebin and nbins % options.rebin == 0: s.histos[pname]["total"] = s.histos[pname]["total"].Rebin(options.rebin)
        if not(back): back = s.histos[pname]["total"].Clone("total_background")
        else: back.Add(s.histos[pname]["total"])
        if not(s.config["label"] in thePlotGroups):
          thePlotGroups[s.config["label"]] = s.histos[pname]["total"].Clone(s.histos[pname]["total"].GetName().replace(s.name, s.config["label"]))
          GroupsYields[s.config["label"]]  = s.histos[pname]["total"].Integral()
        else:
          thePlotGroups[s.config["label"]].Add(s.histos[pname]["total"])
          GroupsYields[s.config["label"]] += s.histos[pname]["total"].Integral()
      elif s.isData:
        if options.rebin and nbins % options.rebin == 0: s.histos[pname]["total"] = s.histos[pname]["total"].Rebin(options.rebin)
        if not(s.config["label"] in thePlotGroupsData):
          thePlotGroupsData[s.config["label"]] = s.histos[pname]["total"].Clone(s.histos[pname]["total"].GetName().replace(s.name, s.config["label"]))
        else:
          thePlotGroupsData[s.config["label"]].Add(s.histos[pname]["total"])
      else: 
        if options.rebin and nbins % options.rebin == 0: s.histos[pname]["total"] = s.histos[pname]["total"].Rebin(options.rebin)
        s.histos[pname]["total"].SetFillStyle(0)
        s.histos[pname]["total"].SetLineWidth(3)
        s.histos[pname]["total"].SetLineStyle(1)
        if not(s.config["label"] in thePlotGroupsSignal):
          thePlotGroupsSignal[s.config["label"]] = s.histos[pname]["total"].Clone(s.histos[pname]["total"].GetName().replace(s.name, s.config["label"]))
        else:
          thePlotGroupsSignal[s.config["label"]].Add(s.histos[pname]["total"])
    if debug: print("...Groups created")
    #print(thePlotGroupsSignal, thePlotGroupsData, thePlotGroups)
    orderedPlotGroups = sorted(GroupsYields.keys(), key=lambda x: GroupsYields[x])
    for plotgroup in (orderedPlotGroups if options.ordered else thePlotGroups):
      if options.weightHisto:
        print("I will now weight %s"%plotgroup)
        tfname, thname = options.weightHisto.split(":")
        tf = ROOT.TFile(tfname,"READ")
        th = tf.Get(thname)
        for ibin in range(1, thePlotGroups[plotgroup].GetNbinsX()+1):
          print(ibin, thePlotGroups[plotgroup].GetBinContent(ibin), th.GetBinContent(th.FindBin(thePlotGroups[plotgroup].GetBinLowEdge(ibin)+0.5*thePlotGroups[plotgroup].GetBinWidth(ibin))))
          thePlotGroups[plotgroup].SetBinContent(ibin, thePlotGroups[plotgroup].GetBinContent(ibin)*th.GetBinContent(th.FindBin(thePlotGroups[plotgroup].GetBinLowEdge(ibin)+0.5*thePlotGroups[plotgroup].GetBinWidth(ibin))))
      theStack.Add(thePlotGroups[plotgroup])
      tl.AddEntry(thePlotGroups[plotgroup], plotgroup, "f")
      stacksize += thePlotGroups[plotgroup].Integral()
    for plotgroup in thePlotGroupsSignal:
      if options.scaleStoB:
        print(plotgroup, "scaling", back.Integral()/max(0.00001,thePlotGroupsSignal[plotgroup].Integral()))
        thePlotGroupsSignal[plotgroup].Scale(back.Integral()/max(0.00001,thePlotGroupsSignal[plotgroup].Integral()))
      if options.scaleS:
        print(thePlotGroupsSignal[plotgroup].Integral())
        thePlotGroupsSignal[plotgroup].Scale(options.scaleS)
        print(thePlotGroupsSignal[plotgroup].Integral())
      if options.scaleSYields > 0:
        if options.debug: print(plotgroup)
        thePlotGroupsSignal[plotgroup].Scale(options.scaleSYields/thePlotGroupsSignal[plotgroup].Integral())
      if options.AddBOnSignal:
        thePlotGroupsSignal[plotgroup].Add(back)
        if options.ExcludeAddBOnSignal:
          for theBPG in (orderedPlotGroups if options.ordered else thePlotGroups):
            print("Try to match", options.ExcludeAddBOnSignal, theBPG) 
            if re.match(options.ExcludeAddBOnSignal, theBPG):
              print("Will exclude %s from plot"%theBPG)
              thePlotGroupsSignal[plotgroup].Add(-1*thePlotGroups[theBPG])

      theIndivs.append(thePlotGroupsSignal[plotgroup])
      tl.AddEntry(thePlotGroupsSignal[plotgroup], plotgroup if not(options.AddBOnSignal) else "Bkg.+" +plotgroup, "l")
    for plotgroup in thePlotGroupsData:
      theData.append(thePlotGroupsData[plotgroup])
      tl.AddEntry(thePlotGroupsData[plotgroup], plotgroup, "pl")
    if options.weightHisto:
        tfname, thname = options.weightHisto.split(":")
        tf = ROOT.TFile(tfname,"READ")
        th = tf.Get(thname)
        for ibin in range(1, back.GetNbinsX()+1):
          print(ibin, back.GetBinContent(ibin), th.GetBinContent(th.FindBin(back.GetBinLowEdge(ibin)+0.5*back.GetBinWidth(ibin))))
          back.SetBinContent(ibin, back.GetBinContent(ibin)*th.GetBinContent(th.FindBin(back.GetBinLowEdge(ibin)+0.5*back.GetBinWidth(ibin))))

    backSyst = back
    if self.doSyst:
      backSyst, histosToSave = self.doSystVariations(options.systFile, pname, options, back)
      
    if p["normalize"]:
      for index in range(len(theIndivs)):
        theIndivs[index].Scale(1./max(0.000001,theIndivs[index].Integral()))
      theStack = ROOT.THStack(pname+"_stack_norm", pname+ "_norm")
      #print(back, backSyst)
      back.Scale(1./max(0.000001,back.Integral()))
      backSyst.Scale(1./max(0.0000001, backSyst.Integral()))
      for s in self.samples:
        if s.isBackground():
          s.histos[pname]["total"].Scale(1./stacksize)
          theStack.Add(s.histos[pname]["total"])
    if debug: print("...Plot normalized")
    # Now plotting stuff
    theStack.SetTitle("") 
    theStack.Draw("hist")
    theStack.GetXaxis().SetLabelSize(0)
    theStack.GetYaxis().SetLabelSize(0.04)
    theStack.GetYaxis().SetTitleSize(0.08)
    theStack.GetYaxis().SetTitleOffset(0.72)

    theStack.GetYaxis().SetTitle("Normalized events" if p["normalize"] else "Events")
    theStack.GetXaxis().SetTitle("") # Empty, as it goes into the ratio plot
    if "maxY" in p: 
      theStack.SetMaximum(p["maxY"]*options.scaleMax)
    if "minY" in p:
      theStack.SetMinimum(p["minY"])
    if debug: print("...Max and Min set")
    theStack.Draw("hist")
    if self.doSyst:
      backSyst.SetFillColor(ROOT.kBlack)
      backSyst.SetLineColor(ROOT.kBlack)
      backSyst.SetFillStyle(3244)
      tl.AddEntry(backSyst, "SM Unc.", "f")
      backSyst.Draw("E2same")
    for ind in theIndivs:
      ind.Draw("hist same")
    # Last, draw the data
    for d in theData:
      d.Draw("P0 same")

    if "lines" in p:
      tlines = []
      for l in p["lines"]:
        x1, y1, x2, y2 = l[:4]
        tlines.append(ROOT.TLine(x1, y1, x2, y2))
        tlines[-1].SetLineStyle(l[4])
        tlines[-1].SetLineWidth(l[5])
        tlines[-1].SetLineColor(l[6])
        tlines[-1].Draw("same")
    if "text" in p:
      ttext = []
      for l in p["text"]:
        text, coords, size, color = l
        ttext.append(ROOT.TLatex(coords[0], coords[1], text))
        ttext[-1].SetTextColor(color)
        ttext[-1].SetTextSize(size)
        ttext[-1].Draw("same")


    tl.Draw("same")
    if debug: print("...Main plot done")
    if options.doRatio:
      # Now we go to the ratio
      p2.cd()

      # By default S/B, data/MC, TODO: add more options
      den  = backSyst.Clone("backsyst_ratio")
      denForDivide = den.Clone("forDivide")
      nums = []
      for ind in  theIndivs + theData:
        try:
          nums.append(ind.Clone(ind.GetName()+ "_ratio"))
        except:
          if options.debug: raise
          print("Something went wrong in the ratio...")
      #nums = [ind.Clone(ind.GetName()+ "_ratio") for ind in  theIndivs + theData]
      for ib in range(0, den.GetNbinsX()+1):
        denForDivide.SetBinError(ib,0)
      for num in nums: 
        num.Divide(denForDivide)
        
      den.Divide(denForDivide)
      den.SetLineColor(ROOT.kBlack) #ROOT.kCyan if doSyst else ROOT.kGray)
      den.SetTitle("")
      den.GetYaxis().SetTitle(options.ratioylabel)
      den.GetXaxis().SetTitle(p["xlabel"])
      den.GetYaxis().SetTitleSize(0.12)
      den.GetYaxis().SetTitleOffset(0.32)
      den.GetXaxis().SetTitleSize(0.12)
      den.GetXaxis().SetLabelSize(0.1)
      den.GetYaxis().SetLabelSize(0.06)
      if "xbinlabels" in p:
        den.LabelsOption("v")
        den.GetXaxis().SetTitleOffset(1.75)
        for i in range(1,den.GetNbinsX()+1):
          print(i, p["xbinlabels"][i-1])
          den.GetXaxis().SetBinLabel(i, p["xbinlabels"][i-1])
          den.GetXaxis().SetLabelSize(0.12)
          den.GetXaxis().SetLabelOffset(0.02)
          #den.GetXaxis().ChangeLabel(i, -1,-1,-1,-1,-1,p["xbinlabels"][i-1])
      den.LabelsOption("v")

      if "ratiomaxY" in p:
        den.SetMaximum(p["ratiomaxY"] if not options.rmax else float(options.rmax))
      if "ratiominY" in p:
        den.SetMinimum(p["ratiominY"] if not options.rmin else float(options.rmin))
      denbar = den.Clone(den.GetName() + "_bar")
      denbar.SetFillColor(ROOT.kCyan if self.doSyst else ROOT.kGray)
      denbar.SetFillStyle(1001)
      denbar.Draw("E2")
      if self.doSyst:
        backratio = back.Clone("backratiostat")
        backratio.Divide(back)
        backratio.SetFillColor(ROOT.kGray)
        backratio.SetLineColor(ROOT.kGray)
        backratio.SetFillStyle(1001)
        backratio.Draw("E2 same")
      ncolumns = 3 if self.doSyst else 2 
      tlr = ROOT.TLegend(0.9-0.2*ncolumns,0.89,0.9,0.97)
      tlr.SetNColumns(ncolumns)
      tlr.SetBorderSize(0)
      if "legendRatioPosition" in p:
        tlr = ROOT.TLegend(p["legendRatioPosition"][0], p["legendRatioPosition"][1], p["legendRatioPosition"][2], p["legendRatioPosition"][3])
      if not options.fromROOT: tlr.AddEntry(denbar, "SM syst.+stat. Unc." if self.doSyst else options.ratiostatlabel, "f")
      if self.doSyst:
        tlr.AddEntry(backratio, options.ratiostatlabel, "f")
      for ib in range(0, den.GetNbinsX()+1):
        den.SetBinError(ib,0)
        den.SetBinContent(ib, 1)
      den.SetFillStyle(0)	
      den.Draw("same")
      for num in nums:
        if options.AddBOnRatio:
          if not("Data" in num.GetName()):
            for ib in range(1, num.GetNbinsX()+1):
              num.SetBinContent(ib, num.GetBinContent(ib)+1)
        if "Data" in num.GetName():
          num.Draw("Psame")
        elif options.AddBOnRatio:
          #num.SetFillColorAlpha(num.GetColor(), 0.35)
          num.Draw("histsame")
        else:
          num.Draw("same" + ("hist" if options.noratiostat else "")) 
        if "Data" in num.GetName(): 
          tlr.AddEntry(num, "Data", "pl")
        elif options.AddBOnRatio:
          tlr.AddEntry(num, "S+B", "pl") 
      if debug: print("...Ratio done")
      if "rlines" in p:
        rtlines = []
        for l in p["rlines"]:
          x1, y1, x2, y2 = l[:4]
          rtlines.append(ROOT.TLine(x1, y1, x2, y2))
          rtlines[-1].SetLineStyle(l[4])
          rtlines[-1].SetLineWidth(l[5])
          rtlines[-1].SetLineColor(l[6])
          rtlines[-1].Draw("same")
      if "rtext" in p:
        rttext = []
        for l in p["rtext"]:
          text, coords, size, color = l
          rttext.append(ROOT.TText(coords[0], coords[1], text))
          rttext[-1].SetTextColor(color)
          rttext[-1].SetTextSize(size)
          rttext[-1].Draw("same")
      tlr.Draw("same")

    CMS_lumi.writeExtraText = True
    CMS_lumi.lumi_13TeV = "%.1f fb^{-1}" % options.luminosity if options.luminosity > 1. else "%.0f pb^{-1}" % (options.luminosity*1000)
    if p["normalize"]: 
      CMS_lumi.lumi_13TeV = ""
    CMS_lumi.extraText  = "Preliminary"
    CMS_lumi.lumi_sqrtS = "13"
    if debug: print("...CMS_lumi configured")
    CMS_lumi.CMS_lumi(c, 4, 0, 0.077)
    if debug: print("...CMS_lumi set")
    if options.rebin:
      p["plotname"] = p["plotname"] + "_" + str(options.rebin) + "rebinned"

    c.SaveAs(options.plotdir + "/" + p["plotname"] + ".pdf")
    c.SaveAs(options.plotdir + "/" + p["plotname"] + ".png")
    if debug: print("...Files saved")
    # Also save as TH1 in root file 
    tf = ROOT.TFile(options.plotdir + "/" + p["plotname"] + ".root", "RECREATE")
    tf.cd()
    if debug: print("File created", tf)
    writableHistograms = {}
    for s in self.samples:
      if s.histos[pname]["total"].GetName() in writableHistograms:
        writableHistograms[ s.histos[pname]["total"].GetName()].Add( s.histos[pname]["total"])
      else:
        writableHistograms[ s.histos[pname]["total"].GetName()] = s.histos[pname]["total"]
    for h in writableHistograms:
      writableHistograms[h].Write()
    theStack.Write()
    back.Write()
    if self.doSyst:
      for h in histosToSave:
        print("histosToSave ---------------------------->", h)
        histosToSave[h].Write()
    tf.Close()
    if debug: print("...File closed")
    ROOT.SetOwnership(c,False) # This magic avoids segfault due to the garbage collector collecting non garbage stuff
   except Exception as e:
     if options.debug: raise
     print("Something went wrong, skipping plot...", e)

if __name__ == "__main__":
  print("Starting plotting script...")
  from optparse import OptionParser
  parser = OptionParser(usage="%prog [options] samples.py plots.py") 
  parser.add_option("-l","--luminosity", dest="luminosity", type="float", default=137, help="Luminosity")
  parser.add_option("-j","--jobs", dest="jobs", type="int", default=1, help="Number of jobs (cores to use)")
  parser.add_option("--toSave", dest="toSave", type="str", default=None, help="If active, instead of plotting save per file histograms in this folder")
  parser.add_option("--toLoad", dest="toLoad", type="str", default=None, help="If active, instead of reading hdf5 load per file histograms from this folder")
  parser.add_option("-p","--plotdir", dest="plotdir", type="string", default="./", help="Where to put the plots")
  parser.add_option("--strict-order", dest="ordered", action="store_true", default=False, help="If true, will stack samples in the order of yields")
  parser.add_option("--dohadd", dest="dohadd", action="store_true", default=False, help="If true, will run (or read) hadded files rather than individual .root files, faster for cases with high #files")
  parser.add_option("--blind", dest="blind", action="store_true", default=False, help="Activate for blinding (no data)")
  parser.add_option("--sample", dest ="sample", default=[], action="append", help="If not none, process only this specific sample")
  parser.add_option("--exclude", dest="exclude", default=[], action="append", help="Exclude samples matching this")
  parser.add_option("--files", dest="files", default=None, help="If not none, process only these set of comma separated files")
  parser.add_option("--queue", dest="queue", default=None, help="If not none, submit jobs to this queue")
  parser.add_option("--batchsize", dest="batchsize", default=1, help="Run this many files per batch job")
  parser.add_option("--jobname", dest="jobname", default="batchjobs", help="Folder in which to create the executable jobs")
  parser.add_option("--resubmit", dest="resubmit", default=False, action="store_true", help="If true, only run jobs that failed before (missing root files)")
  parser.add_option("--rebin", dest="rebin", default=None, type="int", help="Collapse bins by this factor")
  parser.add_option("--ratioylabel", dest="ratioylabel", type="string", default="X/SM", help="Title of the Y axis of the ratio plot")
  parser.add_option("--ratiostatlabel", dest="ratiostatlabel", type="string", default="SM Stat. Unc.", help="Legend entry for the uncertainty in the denominator of the ratio")
  parser.add_option("--sP", dest="singleplot", action="append", default=[], help="Run only these plots")
  parser.add_option("--test", dest="test", action="store_true", default=False, help="Activate test mode (1 file per sample) for quick checks")
  parser.add_option("--rmax", dest="rmax", type="float", default=None, help="Ratio maximum")
  parser.add_option("--rmin", dest="rmin", type="float", default=None, help="Ratio minimum")
  parser.add_option("--scaleY", dest="scaleMax", type="float", default=1., help="Scale Y axis maximum by this number (useful when plotting only signal, for example)")
  parser.add_option("--scaleStoB", dest="scaleStoB",default=False, action="store_true", help="Scale signal to background for normalization")
  parser.add_option("--scaleS", dest="scaleS", type="float", default=1., help="Scale signal by this")
  parser.add_option("--scaleSYields", dest="scaleSYields", type="float", default=-1., help="Scale signal to these yields")

  parser.add_option("--weight-histo", dest="weightHisto", type="string", default=None, help="File:histogram, reweight the output background histograms base on target histogram")
  parser.add_option("--noratiostat", dest="noratiostat", action="store_true", default=False, help="Do not show stat uncertainties in ratios (i.e. if num/dem are fully correlated this would mean double counting")
  parser.add_option("--systFile", dest="systFile", type="string", default=None, help="Systematics configuration file")
  parser.add_option("--pretend", dest="pretend", action="store_true", default=False, help="Activate pretend mode (create submit job files but don't submit)")
  parser.add_option("--onlytotal", dest="onlytotal", action="store_true", default=False, help="For colz plots, only plot total background")
  parser.add_option("--addLines", dest="addLines", default=[], action="append", help="Add lines in these coordinates (only 2D plots). Syntax is --addLines 'x1,y1,x2,y2'.")
  parser.add_option("--addText", dest="addText", default=[], action="append", help="Add text in these coordinates (only 2D plots). Syntax is --addText 'title:x1,y1:size'.")
  parser.add_option("--debug", dest="debug", default =False, action="store_true", help="If activated, turn off exception catching for full debugging")
  parser.add_option("--fromROOT", dest="fromROOT", default =False, action="store_true", help="If activated, read shapes from the toLoad file directly (i.e. a file with the global TH1F already)")
  parser.add_option("--wide", dest="wide", default =False, action="store_true", help="If activated, make long wide plots")
  parser.add_option("--ExcludeAddBOnSignal", dest="ExcludeAddBOnSignal", default=None, help="If AddBOnRatio is activated, do not add these specific backgrounds to the signal (i.e. if our signal is replacing some of the SM bkg like an EFT modification of a SM process. Accepts a regexp expression")
  parser.add_option("--AddBOnSignal", dest="AddBOnSignal", default =False, action="store_true", help="If activated, add background to signal")
  parser.add_option("--AddBOnRatio", dest="AddBOnRatio", default =False, action="store_true", help="If activated, add background on ratio")
  parser.add_option("--plotAll", dest="plotAll", default = False, action="store_true", help="If activated, plot even those that are to be skipped")
  parser.add_option("--doRatio", dest="doRatio", default = True, help="If activated, do the ratio (default is active)")
  parser.add_option("--smartSplitting", dest="smartSplitting", default=False, action="store_true", help="If activivated jobs are allowed to mix samples and --batchsize just denotes the max disk space of processed samples (as proxy of needed memory)")
  
  (options, args) = parser.parse_args()
  options.doRatio = int(options.doRatio) > 0
  samplesFile = imp.load_source("samples",args[0])
  plotsFile   = imp.load_source("plots",  args[1])
  if not(os.path.isdir(options.plotdir)):
    os.system("mkdir %s"%options.plotdir)
  os.system("cp index.php %s"%options.plotdir)
  if options.toSave and not(os.path.isdir(options.toSave)):
    os.system("mkdir %s"%options.toSave)
  os.system("cp %s %s %s"%(args[0], args[1], options.plotdir))
  samples = samplesFile.samples
  if not(options.systFile):
    # Then we take out all systematic variations because we don't need to process them
    newsamples = {}
    for s in samples:
      if "isSyst" in samples[s]:
        if samples[s]["isSyst"]:
          continue 
        else:
          newsamples[s] = samples[s]
      else:
        newsamples[s] = samples[s]
    samples = newsamples

  plots   = plotsFile.plots
  if options.sample != []:
    newsamples = {}
    for s in options.sample:
      for ss in samples.keys():
        if re.match(s, ss):
          print("Will run over:", ss)
          newsamples[ss] = samples[ss]
    samples = newsamples
  if options.exclude != []:
    newsamples = {}
    for ss in samples.keys():
      add = True
      for s in options.exclude:
        if re.match(s, ss):
          print("Will exclude sample:", ss)
          add = False
      if add:
        newsamples[ss] = samples[ss]
    samples = newsamples
  if options.toLoad:
    newsamples = {}
    for ss in samples.keys():
      add = True
      if "doPlot" in samples[ss]:
        add = samples[ss]["doPlot"]
      if add or options.plotAll:
        newsamples[ss] = samples[ss]
    samples = newsamples

  if options.test:
    for s in samples:
      samples[s]["files"] = [samples[s]["files"][0]]

  if options.blind:
    toDelete = []
    for s in samples:
      if "data" in s: 
        toDelete.append(s)
    for d in toDelete:
      del samples[d]
  if len(options.singleplot) > 0:
    newplots = {p: plots[p] for p in options.singleplot}
    plots = newplots

  if options.files:
    for s in samples:
      newfiles = []
      for f in samples[s]["files"]:
        if f in options.files:
          #print(f)
          newfiles.append(f)
      samples[s]["files"] = newfiles

  thePlotter = plotter(plots, samples, options)
  if options.queue:
    print(options.jobname, os.path.isdir(options.jobname))
    if not(os.path.isdir(options.jobname)):
      print("mkdir %s"%options.jobname) 
      os.system("mkdir %s"%options.jobname)
    if not(os.path.isdir(options.jobname+"/exec")):
      os.system("mkdir %s/exec"%options.jobname)
    else:
      os.system("rm %s/exec/*"%options.jobname)
    if not(os.path.isdir(options.jobname+"/batchlogs")):
      os.system("mkdir %s/batchlogs"%options.jobname)

    command = "python plotter_vh.py " + subprocess.list2cmdline(sys.argv[1:]).replace("--queue %s"%options.queue,"")
    if options.toSave: 
      savecommand = open("%s/command.txt"%options.toSave,"w")
      savecommand.write(command+ "\n")
      savecommand.close()
    nJobs = thePlotter.createJobs(options, command)
    os.system("rm submit.sub")
    subfile = open("submit.sub", "w")
    subfile.write("executable              = $(filename)\n")
    subfile.write("arguments               = $(ClusterId)$(ProcId)\n")
    subfile.write("output                  = %s/$(ClusterId).$(ProcId).out\n"%("%s/batchlogs"%options.jobname))
    subfile.write("error                   = %s/$(ClusterId).$(ProcId).err\n"%("%s/batchlogs"%options.jobname))
    subfile.write("log                     = %s/$(ClusterId).log\n"%("%s/batchlogs"%options.jobname))
    #subfile.write("requirements = (OpSysAndVer =?= \"CentOS7\")\n")
    subfile.write("MY.WantOS               = \"el7\"\n")
    #subfile.write("RequestCPUs             = %i\n"%options.jobs)
    subfile.write("+JobFlavour = \"%s\"\n"%(options.queue))
    subfile.write("queue filename matching (%s/exec/_*sh)\n"%("%s"%options.jobname))
    subfile.close()
    if not(options.pretend):
      if options.queue == "local":
        print("Running batched jobs locally, please be patient...")
        for iJob in range(nJobs):
          print("-----Job %i/%i"%(iJob, nJobs))
          if options.debug:
            os.system("sh %s/exec/_%i.sh"%(options.jobname,iJob))
          else:
            os.system("sh %s/exec/_%i.sh >> /dev/null"%(options.jobname,iJob))
      else: 
        os.system("condor_submit -spool submit.sub")

  else:
    thePlotter.doPlots(options)
