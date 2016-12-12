#! /usr/bin/env python

import os, multiprocessing
import copy
import math
from array import array
from ROOT import ROOT, gROOT, gStyle, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1, TH1F, TH2F, THStack, TGraph, TGraphAsymmErrors
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TLine, TBox

from Analysis.ALPHA.drawUtils_signal import *
from Analysis.ALPHA.variables import *
from Analysis.ALPHA.selections_bb import *
from Analysis.ALPHA.samples import sample

########## SETTINGS ##########

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-v", "--variable", action="store", type="string", dest="variable", default="")
parser.add_option("-c", "--cut", action="store", type="string", dest="cut", default="")
parser.add_option("-r", "--region", action="store", type="string", dest="region", default="")
parser.add_option("-a", "--all", action="store_true", default=False, dest="all")
parser.add_option("-b", "--bash", action="store_true", default=False, dest="bash")
parser.add_option("-B", "--blind", action="store_true", default=False, dest="blind")
parser.add_option("-f", "--final", action="store_true", default=False, dest="final")
(options, args) = parser.parse_args()
if options.bash: gROOT.SetBatch(True)

########## SETTINGS ##########

gStyle.SetOptStat(0)

NTUPLEDIR   = "/lustre/cmswork/hoh/CMSSW_8_0_12/src/Analysis/ALPHA/bbDM_v03_skim_processed/"
#NTUPLEDIR   = "/lustre/cmswork/pazzini/VZ/CMSSW_8_0_12/src/Analysis/ALPHA/DMbb_v01/Skim/"
LUMI        = 12900 # in pb-1
SIGNAL      = 1.
RATIO       = 4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
BLIND       = False
POISSON     = False
jobs        = []

########## SAMPLES ##########
#data = ["data_obs"]#data_obs
#back = ["ZJetsToNuNu_HT", "DYJetsToLL_HT", "WJetsToLNu_HT", "TTbar", "ST", "VVIncl", "QCD"] #ZJetsToNuNu_HT, DYJetsToLL_HT, WJetsToLNu_HT, TTbar, ST, VVIncl, QCD
#back = ["QCD", "VVIncl", "ST", "TTbar", "DYJetsToLL_HT","WJetsToLNu_HT" ,"ZJetsToNuNu_HT"]
#sign= []
####plot only sign
data=[]
back=[]
#sign = [s for s, p in sample.iteritems() if 'DM' in s]
###########################Scalar
######################BBBAR
###############mchi =1
#sign = ["bbDMs_Mchi1_Mphi10","bbDMs_Mchi1_Mphi20","bbDMs_Mchi1_Mphi50","bbDMs_Mchi1_Mphi100","bbDMs_Mchi1_Mphi200","bbDMs_Mchi1_Mphi300","bbDMs_Mchi1_Mphi500","bbDMs_Mchi1_Mphi10000"]
##############mchi =10
#sign = ["bbDMs_Mchi10_Mphi10","bbDMs_Mchi10_Mphi15","bbDMs_Mchi10_Mphi50","bbDMs_Mchi10_Mphi100"]
##############mchi =50
#sign = ["bbDMs_Mchi50_Mphi10","bbDMs_Mchi50_Mphi50","bbDMs_Mchi50_Mphi95","bbDMs_Mchi50_Mphi200","bbDMs_Mchi50_Mphi300"]
#####################TTBAR
#m############mchi =1
sign = ["ttDMs_Mchi1_Mphi10","ttDMs_Mchi1_Mphi20","ttDMs_Mchi1_Mphi50","ttDMs_Mchi1_Mphi100","ttDMs_Mchi1_Mphi200","ttDMs_Mchi1_Mphi300","ttDMs_Mchi1_Mphi500", "ttDMs_Mchi1_Mphi10000"]
#############mchi =10
#sign = ["ttDMs_Mchi10_Mphi10","ttDMs_Mchi10_Mphi15","ttDMs_Mchi10_Mphi50","ttDMs_Mchi10_Mphi100"]
#############mchi =50
#sign = ["ttDMs_Mchi50_Mphi10","ttDMs_Mchi50_Mphi50","ttDMs_Mchi50_Mphi95","ttDMs_Mchi50_Mphi200","ttDMs_Mchi50_Mphi300"]
###########################PseudoScalar
###############mchi =1                                                                                                                      
#sign = ["bbDMps_Mchi1_Mphi10","bbDMps_Mchi1_Mphi20","bbDMps_Mchi1_Mphi50","bbDMps_Mchi1_Mphi100","bbDMps_Mchi1_Mphi200","bbDMps_Mchi1_Mphi300","bbDMps_Mchi1_Mphi500","bbDMps_Mchi1_Mphi10000"]                                                                                                                
##############mchi =10                                                                                               
#sign = ["bbDMps_Mchi10_Mphi10","bbDMps_Mchi10_Mphi15","bbDMps_Mchi10_Mphi50","bbDMps_Mchi10_Mphi100"]                 
##############mchi =50                                                                                                                        
#sign = ["bbDMps_Mchi50_Mphi10","bbDMps_Mchi50_Mphi50","bbDMps_Mchi50_Mphi95","bbDMps_Mchi50_Mphi200","bbDMps_Mchi50_Mphi300"]
#####################TTBAR                                                                                                                                   #m############mchi =1                                                                                                                                        #sign = ["ttDMps_Mchi1_Mphi10","ttDMps_Mchi1_Mphi20","ttDMps_Mchi1_Mphi50","ttDMps_Mchi1_Mphi100","ttDMps_Mchi1_Mphi200","ttDMps_Mchi1_Mphi300","ttDMps_Mchi1_Mphi500", "ttDMps_Mchi1_Mphi10000"]                                                                                                     
#############mchi =10                                                                                                                                      
#sign = ["ttDMps_Mchi10_Mphi10","ttDMps_Mchi10_Mphi15","ttDMps_Mchi10_Mphi50","ttDMps_Mchi10_Mphi100"]
#############mchi =50                                                                                                                                    
#sign = ["ttDMps_Mchi50_Mphi10","ttDMps_Mchi50_Mphi50","ttDMps_Mchi50_Mphi95","ttDMps_Mchi50_Mphi200","ttDMps_Mchi50_Mphi300"] 


######Comparison-> Scalar
#sign = ["bbDMps_Mchi1_Mphi10","bbDMps_Mchi1_Mphi20","ttDMps_Mchi1_Mphi10","ttDMps_Mchi1_Mphi20"]


def plot(var, cut, nm1=False, norm=False):
    ### Preliminary Operations ###
    
    # Substitute cut
    pd = ""
    channel = ""
    plotdir = ""
    shortcut = cut
    if cut in selection: plotdir = cut
    for i in range(3):
        for n, c in selection.iteritems():
            if n in cut: cut = cut.replace(n, c)
    
    # Determine Primary Dataset
    pd = getPrimaryDataset(cut)
    if nm1: cut = getNm1Cut(var, cut) # N-1 cuts
    #if 'Pre' in shortcut and 'Mass' in var: cut += " && (isMC ? 0==0 : ("+var+"<65 || "+var+">135))"
    if len(data)>0 and len(pd)==0: raw_input("Warning: Primary Dataset not recognized, continue?")
    
    # Determine weight
    weight = "EventWeight*btagWeight"
    
    print "Plotting", var, "in", channel, "channel with:"
    print "  dataset:", pd
    print "  weight :", weight
    print "  cut    :", cut
    
    ### Create and fill MC histograms ###
    if not sign:
        hist = project(var, cut, weight, data+back, pd, NTUPLEDIR)
    else:
        hist = project(var, cut, weight, data+back+sign, pd, NTUPLEDIR)
        
    # Background sum
    if len(back)>0:
        hist['BkgSum'] = hist['data_obs'].Clone("BkgSum") if 'data_obs' in hist else hist[back[0]].Clone("BkgSum")
        hist['BkgSum'].Reset("MICES")
        hist['BkgSum'].SetFillStyle(3003)
        hist['BkgSum'].SetFillColor(1)
        for i, s in enumerate(back): hist['BkgSum'].Add(hist[s])
    
    if len(back)==0 and len(data)==0:
        for i, s in enumerate(sign):
            hist[s].Scale(1./hist[s].Integral())
            hist[s].SetFillStyle(0)
            #hist[s].Rebin(2)
    
    if norm:
        sfnorm = hist['data_obs'].Integral()/hist['BkgSum'].Integral()
        for i, s in enumerate(back+['BkgSum']): hist[s].Scale(sfnorm)
    
    #if 'hp' in shortcut:
    #    print "Applying HP SF to backgrounds"
    #    for i, s in enumerate(back+['BkgSum']): hist[s].Scale(1.154)
    #if 'lp' in shortcut:
    #    print "Applying LP SF to backgrounds"
    #    for i, s in enumerate(back+['BkgSum']): hist[s].Scale(0.960)

    ### Plot ###
    if len(data+back)>0:
        out = draw(hist, data if not BLIND else [], back, sign, SIGNAL, RATIO, POISSON, variable[var]['log'])
    else:
        out = drawSignal(hist, sign, variable[var]['log'])
    # Other plot operations
    #if 'VX' in out[3].GetXaxis().GetTitle(): out[3].GetXaxis().SetTitle(out[3].GetXaxis().GetTitle().replace('VX', channel))
    out[0].cd(1)
    if len(data+back)>0:
        drawCMS(LUMI, "Preliminary")
    else:
        drawCMS(LUMI, "Simulation")
    drawRegion(shortcut)
    drawAnalysis(channel)
    out[0].Update()
    
    # Save
    pathname = "plots/"+plotdir
    if gROOT.IsBatch():
        if not os.path.exists(pathname): os.makedirs(pathname)
        out[0].Print(pathname+"/"+var.replace('.', '_')+".png")
        out[0].Print(pathname+"/"+var.replace('.', '_')+".pdf")
    
    ### Other operations ###
    # Print table
    if len(data+back)>0: printTable(hist, sign)
    
    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")



#def plotAll():
    #vars = ["X.mass", "X.tmass", "X.dR", "X.dPhi", "X.dEta", "V.mass", "V.pt", "V.dPhi", "V.dR", "Lepton1.pt", "Lepton1.eta", "Lepton2.pt", "Lepton2.eta", "Lepton1.relIso04", "Lepton2.relIso04", "Lepton1.phi", "Lepton2.phi", "Lepton1.relIso03", "Lepton2.relIso03", "Lepton1.trkIso", "Lepton2.trkIso", "FatJet1.pt", "FatJet1.eta", "FatJet1.phi", "FatJet1.prunedMassCorr", "FatJet1.softdropMass", "FatJet1.softdropPuppiMass", "FatJet1.softdropPuppiMassCorr", "FatJet1.chsTau21", "FatJet1.puppiTau21", "FatJet1.ddtTau21", "FatJet1.CSV1", "FatJet1.CSV2", "FatJet1.dR", "nPV", "FatJet1.BDSV", "MaxFatJetBTag", "MinJetMetDPhi", "MEt.pt", "nFatJets", "nMuons", "nElectrons", "nTaus", "nPhotons", "nJets"]
##    for s in ["XVZmmPre", "XVZeePre", "XVZmmhpSB", "XVZmmlpSB", "XVZeehpSB", "XVZeelpSB", "XVZmehp", "XVZmelp", "XVZmmhpSR", "XVZmmlpSR", "XVZeehpSR", "XVZeelpSR"]:
    #for s in ["XVZmmhpSR", "XVZmmlpSR", "XVZeehpSR", "XVZeelpSR"]:
        #for v in vars:
            ##plot(v, s, (v in nm1v))
            #p = multiprocessing.Process(target=plot, args=(v, s, (v in nm1v),))
            #jobs.append(p)
            #p.start()
    
def plotAll():
    vars = ["V.mass", "V.pt", "FatJet1.pt", "FatJet1.softdropPuppiMassCorr", "FatJet1.puppiTau21", "nFatJets"]
#    for s in ["XVZmmPre", "XVZeePre", "XVZmmhpSB", "XVZmmlpSB", "XVZeehpSB", "XVZeelpSB", "XVZmehp", "XVZmelp", "XVZmmhpSR", "XVZmmlpSR", "XVZeehpSR", "XVZeelpSR"]:
    for s in ["XVZmmSR", "XVZeeSR", "XVZmmSB", "XVZeeSB", "XVZmmNR", "XVZeeNR"] + ["XVZmmlpSR", "XVZeelpSR", "XVZmmlpSB", "XVZeelpSB","XVZmmhpSR", "XVZeehpSR", "XVZmmhpSB", "XVZeehpSB"] + ["XVZllNR"]:
        for v in vars:
            #plot(v, s, (v in nm1v))
            p = multiprocessing.Process(target=plot, args=(v, s, (v in nm1v),))
            jobs.append(p)
            p.start()
    
def plotFinal():
#    for v in [["V.mass", "XZheePre"], ["V.mass", "XZhmmPre"], ["FatJet1.pt", "XZheeInc"], ["V.pt", "XZhmmInc"], ["FatJet1.prunedMassCorr", "XZheebSB"], ["X.mass", "XZhmmbbSB"], ["V.tmass", "XWhenInc"], ["Lepton1.pt", "XWhmnInc"], ["MaxFatJetBTag", "XWhenbSB"], ["FatJet1.prunedMassCorr", "XWhmnbbSB"], ["MEt.pt", "XZhnnInc"], ["MinJetMetDPhi", "XZhnnInc"], ["MaxFatJetBTag", "XZhnnbSB"], ["X.tmass", "XZhnnbbSB"], ["FatJet1.BDSV", "XWhlnbTR"], ["FatJet1.CSV1", "XWhlnbbTR"], ["FatJet1.CSV1", "XZhnnbTR"], ["FatJet1.CSV2", "XZhnnbbTR"], ["FatJet1.prunedMass", "XWhlnbTR"], ["FatJet1.prunedMassCorr", "XWhlnbTR"], ["FatJet1.softdropMass", "XWhlnbTR"], ["FatJet1.softdropPuppiMass", "XWhlnbTR"]]:
    for v in [["FatJet1.pt", "XWhlnbTR"], ["nFatJets", "XWhlnbbTR"], ["MEt.pt", "XZhnnbTR"], ["FatJet1.prunedMassCorr", "XZhnnbbTR"], ["FatJet1.BDSV", "XWhlnTR"], ["FatJet1.CSV1", "XWhlnTR"], ["FatJet1.CSV2", "XWhlnTR"], ["FatJet1.prunedMassCorr", "XWhlnTR"], ["FatJet1.prunedMass", "XWhlnbTR"], ["FatJet1.prunedMassCorr", "XWhlnbTR"], ["FatJet1.softdropMass", "XWhlnbTR"], ["FatJet1.softdropPuppiMass", "XWhlnbTR"]]:
        p = multiprocessing.Process(target=plot, args=(v[0], v[1], (v[0] in nm1v),))
        jobs.append(p)
        p.start()


nm1v = ["X.dPhi", "V.dPhi", "FatJet1.CSV1", "FatJet1.CSV2", "FatJet1.BDSV", "MaxFatJetBTag", "MinJetMetDPhi", "nFatJets", "nMuons", "nElectrons", "nTaus", "nPhotons"]

if options.final:
    plotFinal()
elif options.all:
    plotAll()
else:
    plot(options.variable, options.cut)


