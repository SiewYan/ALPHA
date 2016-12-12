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
NTUPLEDIR   = "/lustre/cmswork/pazzini/VZ/CMSSW_8_0_12/src/Analysis/ALPHA/DMbb_v03/Skim/"
LUMI        = 12900 # in pb-1
SIGNAL      = 1.
RATIO       = 4 # 0: No ratio plot; !=0: ratio between the top and bottom pads
BLIND       = False
POISSON     = False
jobs        = []
verbal = True
########## SAMPLES ##########
#data = ["data_obs"]
data = []
back = ["ZJetsToNuNu_HT", "DYJetsToLL_HT", "WJetsToLNu_HT", "TTbar", "ST", "VVIncl", "QCD"] #ZJetsToNuNu_HT, DYJetsToLL_HT, WJetsToLNu_HT, TTbar, ST, VVIncl, QCD
#back = ["QCD", "VVIncl", "ST", "TTbar", "WJetsToLNu_HT", "DYJetsToLL_HT", "ZJetsToNuNu_HT"]
#back = ["DYJetsToLL_HT","WJetsToLNu_HT","ZJetsToNuNu_HT","TTbar", "ST", "VVIncl", "QCD"]
#back=["VVIncl","QCD"]
#back=["VVIncl","QCD"]
sign = []
########## ######## ##########

cat1="( ( nJets==1 && Jet1.CSV>0.800 ) || ( nJets==2 && ( ( Jet1.CSV>0.800 ) + ( Jet2.CSV>0.800 ) )==1 ) )"

cat2="( Jet2.pt>50 && ( ( nJets==2 && ( ( Jet1.CSV>0.800 ) + ( Jet2.CSV>0.800 ) )==2 ) || ( nJets==3 && ( ( Jet1.CSV>0.800 ) + ( Jet2.CSV>0.800 ) + ( Jet3.CSV>0.800 ) )==2  ) ))"

CutFlow={
    "Signal" : [selection["triggerMET"],"MEt.pt>200","nJets<4","Jet1.pt>50 && abs(Jet1.eta)<2.5","MinJetMetDPhi>0.5","(abs(MEt.ptCalo-MEt.pt)/MEt.pt)<0.5","nElectrons==0","nMuons==0","nTaus==0","nPhotons==0"
                ],
    "SR1" : [selection["triggerMET"],"MEt.pt>200","nJets<4","Jet1.pt>50 && abs(Jet1.eta)<2.5","MinJetMetDPhi>0.5","(abs(MEt.ptCalo-MEt.pt)/MEt.pt)<0.5","nElectrons==0","nMuons==0","nTaus==0","nPhotons==0","cat1"
             ],
    "SR2" : [selection["triggerMET"],"MEt.pt>200","nJets<4","Jet1.pt>50 && abs(Jet1.eta)<2.5","MinJetMetDPhi>0.5","(abs(MEt.ptCalo-MEt.pt)/MEt.pt)<0.5","nElectrons==0","nMuons==0","nTaus==0","nPhotons==0","cat2"
             ],
}

def projectv2(var, cut, cutflow, weight, samplelist, pd, ntupledir):

    file = {}
    tree = {}
    chain = {}
    hist = {}
    dummy=[]
    hist00={}
    car=[]

    for i, s in enumerate(samplelist):
        if verbal:
            print
            print "Projecting from tree of sample %s" %s
            print
            print "Reading samples files"
            print str(samples[s]['files'])
            print
        chain[s] = TChain("ntuple/tree")
        for j, ss in enumerate(samples[s]['files']):
            if not 'data' in s or ('data' in s and ss in pd):
                if verbal: print "Interpreting "
                if verbal: print str(ntupledir + ss + ".root")
                chain[s].Add(ntupledir + ss + ".root")
        if variable[var]['nbins']>0: hist[s] = TH1F(s, ";"+variable[var]['title'], variable[var]['nbins'], variable[var]['min'], variable[var]['max'])
        else: hist[s] = TH1F(s, ";"+variable[var]['title'], len(variable[var]['bins'])-1, array('f', variable[var]['bins']))
        hist[s].Sumw2()
        
        tmpcut =""

        cutstring = "("+weight+")" + ("*("+tmpcut+")" if len(tmpcut)>0 else "")

        cutsq=""
        final = []
        logic=False
        for value in CutFlow[cutflow]:
            dummy=hist[s]
            
            if len(cutsq)==0:
                cutsq+=value
            else:
                cutsq+=" && "+value
            if verbal: print (cutsq)
            chain[s].Project(s, var, cutsq) # histogram name, string, selection
            dummy.SetOption("%s" % chain[s].GetTree().GetEntriesFast())
            dummy.Scale(samples[s]['weight'] if dummy.Integral() >= 0 else 0)
            if not "&&" in cutsq:
                car.append("MET Trigger")
            elif ("MinJetMetDPhi" in cutsq and not logic):
                logic=True
                car.append("DPhiJMET>0.5")
            elif(logic):
                car.append(value)
            else:
                car.append(value)
            car.append(dummy.Clone())
            final.append(car)
            #print (final)
            car=[]
        hist00[s]=final
    return hist00

        
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
                if verbal: print "The number of files for", str(samples[s]['files'])
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
            if verbal: "cutting on ",s
            if verbal: print (cutsq)
            chain[s].Project(s, var, cutsq) # histogram name, string, selection
            dummy[s].SetOption("%s" % chain[s].GetTree().GetEntriesFast())
            dummy[s].Scale(samples[s]['weight'] if dummy[s].Integral() >= 0 else 0)
            #print(dummy[s].Integral())
            if not "&&" in cutsq:
                car.append("MET Trigger")
            elif ("MinJetMetDPhi" in cutsq and not logic):
                logic=True
                car.append("DPhiJMET>1.0")
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
    if len(data)>0:
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
    if len(data)==0:
        print "<th>MC</th>"
    else:
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
        if len(data)>0:
        #    print "<th>%-10.2f</th>" %datalist[1]
        #    print "<th>%-10.2f</th>" %((datalist[1]/MC)*100)
        #else:
            print "<th>%-10.2f</th>" %datalist[l][1]
            print "<th>%-10.2f</th>" %((datalist[l][1]/MC)*100)
        print '</tr>'
    print '</table>'
    print '</head>'
    print '</html>'

import copy
def draw_cutflow(cutflow,hist,sign=[]):

    if not 'BkgSum' in hist.keys():
        hist['BkgSum'] = copy.deepcopy(hist['data_obs']) if 'data_obs' in hist else copy.deepcopy(hist[back[0]])
        for i in hist['BkgSum']:
            i[1].Reset("MICES")

    for i, s in enumerate(back):
        print s
        count=0
        for h in hist['BkgSum']:
            print h
            print h[1]
            #print hist[s][count][1]
            h[1].Add(hist[s][count][1])
            count+=1

    for h in hist['BkgSum']:
        h[1].SetMarkerStyle(0)

    # Some style                                                                                                                                  
    for i, s in enumerate(data):
        for h in hist[s]:
            h[1].SetMarkerStyle(20)
            h[1].SetMarkerSize(1.25)
    
    for i, s in enumerate(data+back+sign+['BkgSum']):
        for h in hist[s]:
            addOverflow(h[1], False) # Add overflow

#    for (Int_t i=0 ; i< Xbinnum ; i++ ){
#    h->GetXaxis()->SetBinLabel((i+1),Xbins[i].c_str());
#  }

#    h->SetBinContent(a+1,1,xsec[j]);

    #bkg = THStack("Bkg", ";"+hist['BkgSum'].GetXaxis().GetTitle()+";Events")
    #for i, s in enumerate(back): bkg.Add(hist[s])

    #lencf=len(CutFlow[cutflow])

    #create TCanvas
    #c1 = TCanvas("c1", "test", 800, 800)
    #h = TH1F("h","test", lencf, -0.5 , lencf-0.5);
    #h.SetFillColor(38)
    #print (lencf)
    #for j in range(0,lencf):
    #    #print(j)
    #    print(CutFlow[cutflow][j])
    #    if j==0:
    #        h.GetXaxis().SetBinLabel(j+1,"MET trigger")
    #    else:
    #        h.GetXaxis().SetBinLabel(j+1,CutFlow[cutflow][j])

    #for key in hist.keys():
    #    #print (key)
    #    counts=1
    #    for k in hist[key]:
    #        print (k)
    #        print (int(k[1]))
    #        print counts
    #        for i in range(1,int(k[1])):
    #            h.Fill(counts)
    #        counts=counts+1
    #h.Draw()
    #c1.Update()
    #return c1

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
        #histcut =  projectv2(var, cut, cutflow, weight, data+back, pd, NTUPLEDIR)
    else:
        hist = projectv1(var, cut, cutflow, weight, data+back+sign, pd, NTUPLEDIR)

    #if verbal: print(histcut)
    #for i in histcut['VVIncl']:
    #    print i
    #    print(i[1].Integral())

    ### Plot ###
    #if len(data+back)>0:
    #    out = draw_cutflow(cutflow,histcut,sign)   


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
    if len(data+back)>0: 
        printTable_html(hist,sign)
        #out=draw_cutflow(cutflow,hist,sign)
    #out.Update()
    #out.Print("c1.png")
    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")

#if options.final:
#    plotFinal()
#elif options.all:
#    plotAll()
#else:
cutflow(options.variable, options.cut, options.cutflow)


