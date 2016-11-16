#! /usr/bin/env python

import os, multiprocessing
import copy
import math
from array import array
from ROOT import ROOT, gROOT, gStyle, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1, TH1F, TH2F, THStack, TGraph, TGraphAsymmErrors
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TLine, TBox

from Analysis.ALPHA.drawUtils import *
from Analysis.ALPHA.variables import *
from Analysis.ALPHA.selections_bb import *
from Analysis.ALPHA.samples import sample

import collections

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
parser.add_option("-u", "--User_cutflow", action="store", type="string", dest="cutflow", default="")
(options, args) = parser.parse_args()
if options.bash: gROOT.SetBatch(True)

########## SETTINGS ##########

gStyle.SetOptStat(0)

#NTUPLEDIR   = "/lustre/cmswork/hoh/CMSSW_8_0_12/src/Analysis/ALPHA/Prod_v03/"
NTUPLEDIR   = "/lustre/cmswork/pazzini/VZ/CMSSW_8_0_12/src/Analysis/ALPHA/DMbb_v02/Skim/"
LUMI        = 12900 # in pb-1
SIGNAL      = 1.
RATIO       = 4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
BLIND       = False
POISSON     = False
jobs        = []
verbal = False
########## SAMPLES ##########
data = ["data_obs"]
#data = []
back = ["ZJetsToNuNu_HT", "DYJetsToLL_HT", "WJetsToLNu_HT", "TTbar", "ST", "VVIncl", "QCD"] #ZJetsToNuNu_HT, DYJetsToLL_HT, WJetsToLNu_HT, TTbar, ST, VVIncl, QCD
#back = ["QCD", "VVIncl", "ST", "TTbar", "WJetsToLNu_HT", "DYJetsToLL_HT", "ZJetsToNuNu_HT"]
#back = ["DYJetsToLL_HT","WJetsToLNu_HT","ZJetsToNuNu_HT","TTbar", "ST", "VVIncl", "QCD"]
#back=["VVIncl","QCD"]
sign = []
########## ######## ##########


CutFlow={
    "Signal" : [selection["triggerMET"],"MEt.pt>200","nJets<4","Jet1.pt>50 && abs(Jet1.eta)<2.5","MinJetMetDPhi>0.5","nElectrons==0","nMuons==0","nTaus==0","nPhotons==0","MEt.pt>250","MEt.pt>300","MEt.pt>350","MEt.pt>400","MEt.pt>450","MEt.pt>500","MEt.pt>550"
                ],
}


def projectv1(var, cut, cutflow, weight, samplelist, pd, ntupledir):
    # Create dict                                                                                                                                  
    file = {}
    tree = {}
    chain = {}
    hist = {}
    dummy=[]
    hist0={}
    car=[]

    #create and fill MC histogram
    for i, s in enumerate(samplelist):
        if verbal:
            print 
            print "Projecting from tree of sample %s" %s
            print
            print "Reading samples files"
            print str(samples[s]['files'])
            print
        chain[s] = TChain("ntuple/tree")
        #looping on three files
        for j, ss in enumerate(samples[s]['files']):
            if not 'data' in s or ('data' in s and ss in pd):
                if verbal: print "Interpreting "
                if verbal: print str(ntupledir + ss + ".root")
                chain[s].Add(ntupledir + ss + ".root")
            #initializing histogram
            if verbal: print
        if variable[var]['nbins']>0: hist[s] = TH1F(s, ";"+variable[var]['title'], variable[var]['nbins'], variable[var]['min'], variable[var]['max'])
        else: hist[s] = TH1F(s, ";"+variable[var]['title'], len(variable[var]['bins'])-1, array('f', variable[var]['bins']))
        hist[s].Sumw2()

            #tmpcut = cut
        tmpcut =""

        cutstring = "("+weight+")" + ("*("+tmpcut+")" if len(tmpcut)>0 else "")

        cutsq=""
        final = []
        logic=False
        for value in CutFlow[cutflow]:
            
            dummy=hist
            
            if len(cutsq)==0:
                cutsq+=value
            else:
                cutsq+=" && "+value
            if verbal: print (cutsq)
            chain[s].Project(s, var, cutsq) # histogram name, string, selection
            dummy[s].SetOption("%s" % chain[s].GetTree().GetEntriesFast())
            dummy[s].Scale(samples[s]['weight'] if dummy[s].Integral() >= 0 else 0)
            #print(dummy[s].Integral())
            if not "&&" in cutsq:
                car.append("MET Trigger")
            elif ("MinJetMetDPhi" in cutsq and not logic):
                logic=True
                car.append("DPhiJMET>0.5")
            elif(logic):
                car.append(value)
            else:
                car.append(value)
            car.append(dummy[s].Integral())
            final.append(car)
            car=[]
        hist0[s]=final
    
    #print (hist0)
    if "HIST" in cut: hist["files"] = file
    #return hist
    return hist0

def printTablev1(hist, sign=[]):
    samplelist = [x for x in hist.keys() if not 'data' in x and not 'BkgSum' in x and not x in sign and not x=="files"]
    for x in hist.keys():
        if 'data_obs' in x:
            datalist=hist['data_obs']
        else:
            datalist=["0",1]
    #print(datalist)
    #print(len(datalist))
    print "|\t\t|",
    for i in samplelist:
        print "%s\t |" %i,
    print " MC\t | DATA\t | DATA/MC\t |"
    print "-"*80
    count=0

        #print (samplelist[i]) # bkg key
        #print (hist[samplelist[i]]) #list of value in bkg key
        #print (len(hist[samplelist[i]])) #number of cut in pair
        #print((hist[samplelist[i]][0])[0]) # first cut first element -> triggerbit
        #print (len(samplelist)) -> 2
    for l in range(0,len(hist[samplelist[0]])):
        print "|%s\t|" %((hist[samplelist[0]][l])[0]), # order cut
        count=0
        MC=0
        for i in range(0,len(samplelist)):
            print "%-10.2f |" %((hist[samplelist[i]][l])[1]),
            MC+=(hist[samplelist[i]][l])[1]
        print "%-10.2f |" %MC,
        if len(data)==0:
            print "%-10.2f |" %datalist[1],
            print "%-10.2f |" %((datalist[1]/MC)*100)
        else:
            print "%-10.2f |" %datalist[l][1],
            print "%-10.2f |" %((datalist[l][1]/MC)*100)
    print "-"*80

def printTable_html(hist,sign=[]):
    samplelist = [x for x in hist.keys() if not 'data' in x and not 'BkgSum' in x and not x in sign and not x=="files"]
    ###SORRY, its not working, will check 
    datalist=hist['data_obs']
    #for x in hist.keys():
    #    if 'data_obs' in x:
    #        datalist=hist['data_obs']
    #    else:
    #        datalist=["0",1]
    #print(datalist)
    #print(len(datalist))

    print '<!DOCTYPE html>'
    print '<html>'
    print '<head>'
    print '<style>'
    print 'table, th, td {'
    print 'border: 1px solid black;}'
    print 'background-color: lemonchiffon;'
    print '</style>'
    print '<table>'
    print '<tr>'
    print '<th></th>'

    for i in samplelist:
        print "<th>%s</th>" %i,        
    print "<th>MC</th><th>DATA</th><th>DATA/MC</th>"
    print '</tr>'

    for l in range(0,len(hist[samplelist[0]])):
        print '<tr>'
        print "<th>%s</th>" %((hist[samplelist[0]][l])[0]) # order cut 
        count=0
        MC=0
        for i in range(0,len(samplelist)):
            print "<th>%-10.2f</th>" %((hist[samplelist[i]][l])[1])
            MC+=(hist[samplelist[i]][l])[1]
        print "<th>%-10.2f</th>" %MC
        if len(data)==0:
            print "<th>%-10.2f</th>" %datalist[1]
            print "<th>%-10.2f</th>" %((datalist[1]/MC)*100)
        else:
            print "<th>%-10.2f</th>" %datalist[l][1]
            print "<th>%-10.2f</th>" %((datalist[l][1]/MC)*100)
        print '</tr>'
    print '</table>'
    print '</head>'
    print '</html>'


def cutflow(var, cut, cutflow, nm1=False, norm=False):
    ### Preliminary Operations ###
    if len(var)==0:
        var="nPV"
    
    # Substitute cut
    cut=""
    pd = ""
    channel = ""
    plotdir = ""
    shortcut = cut
    #if cut in selection: plotdir = cut
    #for i in range(3):
    #    for n, c in selection.iteritems():
    #        #n = ZeeCR , c == content cut
    #        if n in cut: 
    #            cut = cut.replace(n, c) 

    #print(CutFlow[cutflow][0])
    # Determine Primary Dataset
    #print(cut)
    pd = getPrimaryDataset(CutFlow[cutflow][0])
    if nm1: cut = getNm1Cut(var, cut) # N-1 cuts
    #if 'Pre' in shortcut and 'Mass' in var: cut += " && (isMC ? 0==0 : ("+var+"<65 || "+var+">135))"
    #if len(data)>0 and len(pd)==0: raw_input("Warning: Primary Dataset not recognized, continue?")
    
    # Determine weight
    weight = "EventWeight"
    
    if verbal:
        print "Plotting", var, "in", channel, "channel with:"
        print "  dataset:", pd
        print "Cutflow type:", cutflow
        print "  weight :", weight
        print
    #print "  cut    :", cut
        print
        print "  data+back :", data+back+sign
    
    ### Create and fill MC histograms ###
    if not sign:
        hist = projectv1(var, cut, cutflow, weight, data+back, pd, NTUPLEDIR)
    else:
        hist = projectv1(var, cut, cutflow, weight, data+back+sign, pd, NTUPLEDIR)

    if verbal: print(hist)
    # Background sum
    #if len(back)>0:
    #    hist['BkgSum'] = hist['data_obs'].Clone("BkgSum") if 'data_obs' in hist else hist[back[0]].Clone("BkgSum")
    #    hist['BkgSum'].Reset("MICES")
    #    hist['BkgSum'].SetFillStyle(3003)
    #    hist['BkgSum'].SetFillColor(1)
    #    for i, s in enumerate(back): hist['BkgSum'].Add(hist[s])
    
    #if len(back)==0 and len(data)==0:
    #    for i, s in enumerate(sign):
    #        hist[s].Scale(1./hist[s].Integral())
    #        hist[s].SetFillStyle(0)
    #        #hist[s].Rebin(2)
    
    #if norm:
    #    sfnorm = hist['data_obs'].Integral()/hist['BkgSum'].Integral()
    #    for i, s in enumerate(back+['BkgSum']): hist[s].Scale(sfnorm)
    
    #if 'hp' in shortcut:
    #    print "Applying HP SF to backgrounds"
    #    for i, s in enumerate(back+['BkgSum']): hist[s].Scale(1.154)
    #if 'lp' in shortcut:
    #    print "Applying LP SF to backgrounds"
    #    for i, s in enumerate(back+['BkgSum']): hist[s].Scale(0.960)

    ### Plot ###
    #if len(data+back)>0:
    #    out = draw(hist, data if not BLIND else [], back, sign, SIGNAL, RATIO, POISSON, variable[var]['log'])
    #else:
    #    out = drawSignal(hist, sign)
    #out[0].cd(1)
    #drawCMS(LUMI, "Preliminary")
    #drawRegion(shortcut)
    #drawAnalysis(channel)
    #out[0].Update()
    
    # Save
    #pathname = "plots/"+plotdir
    #if gROOT.IsBatch():
    #    if not os.path.exists(pathname): os.makedirs(pathname)
    #    out[0].Print(pathname+"/"+var.replace('.', '_')+".png")
    #    out[0].Print(pathname+"/"+var.replace('.', '_')+".pdf")
    
    ### Other operations ###
    # Print table
    #if len(data+back)>0: printTablev1(hist, sign)
    if len(data+back)>0: printTable_html(hist,sign)
    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")

#if options.final:
#    plotFinal()
#elif options.all:
#    plotAll()
#else:
cutflow(options.variable, options.cut, options.cutflow)


