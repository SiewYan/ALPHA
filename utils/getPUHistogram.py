#! /usr/bin/env python

import os
from array import array
from ROOT import gStyle, TFile, TH1F, TCanvas, TLegend, ROOT, gROOT

gStyle.SetOptStat(0)

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
#parser.add_option("-d", "--dataFile", action="store", type="string", default=False, dest="dataFileName")
#parser.add_option("-m", "--mcFile", action="store", type="string", default=False, dest="mcFileName")
#parser.add_option("-r", "--mcReweightedFile", action="store", type="string", default=False, dest="mcReweightedFileName")
#parser.add_option("-p", "--plot", action="store_true", default=False, dest="doPlot")
parser.add_option("-s", "--save", action="store_true", default=False, dest="save")
parser.add_option("-b", "--batch", action="store_true", default=False, dest="batch")
(options, args) = parser.parse_args()
if options.batch: gROOT.SetBatch(True)

#scp lxplus.cern.ch:/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt data/JSON/
#pileupCalc.py -i data/JSON/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt --inputLumiJSON data/JSON/pileup_latest.txt --calcMode true --minBiasXsec 71300 --maxPileupBin 60 --numPileupBins 60 data/PU_71300.root


# https://raw.githubusercontent.com/cms-sw/cmssw/CMSSW_7_4_X/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py
#probValue = [4.8551E-07, 1.74806E-06, 3.30868E-06, 1.62972E-05, 4.95667E-05, 0.000606966, 0.003307249, 0.010340741, 0.022852296, 0.041948781, 0.058609363, 0.067475755, 0.072817826, 0.075931405, 0.076782504, 0.076202319, 0.074502547, 0.072355135, 0.069642102, 0.064920999, 0.05725576, 0.047289348, 0.036528446, 0.026376131, 0.017806872, 0.011249422, 0.006643385, 0.003662904, 0.001899681, 0.00095614, 0.00050028, 0.000297353, 0.000208717, 0.000165856, 0.000139974, 0.000120481, 0.000103826, 8.88868E-05, 7.53323E-05, 6.30863E-05, 5.21356E-05, 4.24754E-05, 3.40876E-05, 2.69282E-05, 2.09267E-05, 1.5989E-05, 4.8551E-06, 2.42755E-06, 4.8551E-07, 2.42755E-07, 1.21378E-07, 4.8551E-08]

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/SimGeneral/MixingModule/python/mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py
probValue = [0.000829312873542, 0.00124276120498, 0.00339329181587, 0.00408224735376, 0.00383036590008, 0.00659159288946, 0.00816022734493, 0.00943640833116, 0.0137777376066, 0.017059392038, 0.0213193035468, 0.0247343174676, 0.0280848773878, 0.0323308476564, 0.0370394341409, 0.0456917721191, 0.0558762890594, 0.0576956187107, 0.0625325287017, 0.0591603758776, 0.0656650815128, 0.0678329011676, 0.0625142146389, 0.0548068448797, 0.0503893295063, 0.040209818868, 0.0374446988111, 0.0299661572042, 0.0272024759921, 0.0219328403791, 0.0179586571619, 0.0142926728247, 0.00839941654725, 0.00522366397213, 0.00224457976761, 0.000779274977993, 0.000197066585944, 7.16031761328e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


mc = TH1F("2016_25ns_SpringMC_PUScenarioV1", "True nPV distribution", 60, 0, 60)
mc.Sumw2()
for i in range(60): mc.SetBinContent(i+1, probValue[i])
mc.SetLineWidth(3)
mc.SetLineColor(1)
mc.SetLineStyle(2)
mc.Scale(1./mc.Integral())

if options.save:
    outFile = TFile("../data/PU_MC.root", "RECREATE")
    outFile.cd()
    mc.Write()
    outFile.Close()
    print "Histograms written to ../data/PU_MC.root file"
    exit()
   
puFile = TFile("../data/PU_69000.root", "READ")
data = puFile.Get("pileup")
data.SetLineWidth(3)
data.SetLineColor(1)
data.Scale(1./data.Integral())

puUpFile = TFile("../data/PU_72450.root", "READ")
dataUp = puUpFile.Get("pileup")
dataUp.SetLineWidth(3)
dataUp.SetLineColor(634)
dataUp.Scale(1./dataUp.Integral())

puDownFile = TFile("../data/PU_65550.root", "READ")
dataDown = puDownFile.Get("pileup")
dataDown.SetLineWidth(3)
dataDown.SetLineColor(598)
dataDown.Scale(1./dataDown.Integral())

ratio = data.Clone("ratio")
ratioUp = dataUp.Clone("ratioUp")
ratioDown = dataDown.Clone("ratioDown")

ratio.Divide(mc)
ratioUp.Divide(mc)
ratioDown.Divide(mc)

#outFile = TFile("../data/PU.root", "RECREATE")
#outFile.cd()
#mc.Write()
#data.Write()
#dataUp.Write()
#dataDown.Write()
#ratio.Write()
#ratioUp.Write()
#ratioDown.Write()
#outFile.Close()
#print "Histograms written to ../data/PU.root file"

leg = TLegend(0.65, 0.7, 0.98, 0.9)
leg.SetBorderSize(0)
leg.SetFillStyle(0) #1001
leg.SetFillColor(0)
leg.SetHeader("pile-up reweighting")
leg.AddEntry(dataUp, "Up", "pl")
leg.AddEntry(data, "Central", "pl")
leg.AddEntry(dataDown, "Down", "pl")
leg.AddEntry(mc, "MC 25ns", "pl")

c1 = TCanvas("c1", "PileUp reweighting", 800, 800)
c1.cd()
c1.GetPad(0).SetTopMargin(0.06)
c1.GetPad(0).SetRightMargin(0.05)
c1.GetPad(0).SetTicks(1, 1)
dataDown.SetTitle(";number of true interactions")
dataDown.GetXaxis().SetRangeUser(0., 30)
dataDown.Draw("HIST")
dataUp.Draw("SAME, HIST")
data.Draw("SAME, HIST")
mc.Draw("SAME, L")
leg.Draw()
c1.Print("PU/PU_%s.pdf"%l)
c1.Print("PU/PU_%s.png"%l)

