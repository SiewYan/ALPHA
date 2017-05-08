#!/usr/bin/env python
import os, re
import multiprocessing
import commands
import math, time
import sys
from ROOT import TObject, TFile, TH1, TH1F
from Analysis.ALPHA.samplesMoriond_BB import sample
from array import array

#LUMI        = 12900 # in pb-1
#brilcalc lumi -b "STABLE BEAMS" --normtag /afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json -i Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt -u /pb
LUMI        = 35867 #in pb-1

# use the following lists to include/exclude samples to be merged

blacklist = []

whitelist = [
#    'SingleMuonRun2016B-PromptReco-v1', 
#    'SingleMuonRun2016B-PromptReco-v2',
#    'SingleElectronRun2016B-PromptReco-v1',
#    'SingleElectronRun2016B-PromptReco-v2',
#    'METRun2016B-PromptReco-v1',
#    'METRun2016B-PromptReco-v2',
#    'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#    'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#    'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    # Z(nunu)+jets
#    'DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#    'DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#    'DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#    'DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#    # W(lnu)+jets
#    'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#    'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#    'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#    'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#    'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
#    'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#    'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#    'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#    'TTToSemiLeptonic_13TeV-powheg_v0_ext1_red1-v1',
#    'TTTo2L2Nu_13TeV-powheg_v0_ext1_red1-v1',
#    'VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
#     # Signal
#    'BulkGravToZZToZlepZhad_narrow_M-600_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-800_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-1000_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-2000_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-1200_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-1600_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-1800_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-2000_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-3000_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-3500_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-4000_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    'BulkGravToZZToZlepZhad_narrow_M-4500_13TeV-madgraph_PRIVATE-MC_v0-v1',
#    # AZh
#    'GluGluToAToZhToLLBB_M225_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M250_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M275_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M300_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M325_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M350_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M400_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M500_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M600_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M700_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M800_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M900_13TeV-amcatnlo',
#    'GluGluToAToZhToLLBB_M1000_13TeV-amcatnlo',
]



########## DO NOT TOUCH BELOW THIS POINT ##########

import argparse

parser = argparse.ArgumentParser(description='combine the LSF outputs into one tree')
parser.add_argument('folder', help='the folder containing the LSF output')
args = parser.parse_args()

if not os.path.exists(os.path.expandvars(args.folder)):
    print '--- ERROR ---'
    print '  \''+args.folder+'\' path not found'
    print '  please point to the correct path to the folder containing the LSF output' 
    print 
    exit()

jobs = []



def rescale(dir, weight):
    print "-", dir.GetName()
    # Looping over directory content
    for key in dir.GetListOfKeys():
        if not key.GetCycle() == 1: continue
        obj = key.ReadObj()
        # rescale histograms
        if obj.IsA().InheritsFrom('TH1'):
            obj.Scale(weight)
            obj.Write()#"", TObject.kOverwrite)
        # Copy trees
        elif obj.IsA().InheritsFrom('TTree'):
            obj.SetWeight(weight)
            obj.AutoSave()
        elif obj.IsFolder():
            subdir = obj.GetName()
            dir.cd(subdir)
            rescale(dir.GetDirectory(subdir), weight)
            dir.cd("..")
    #
    



def hadd(name):
    if len(whitelist)>0 and not name in whitelist: return
    if len(blacklist)>0 and name in blacklist: return
    #if '_ext' in name: return

    #name_noext = name.replace('_ext1', '').replace('_ext2', '').replace('_ext3', '').replace('_ext4', '').replace('_v0-v1', '').replace('_v0-v2', '')
    #_noext+'*
    os.system('hadd -f '+name+'.root '+name+'/*/*.root')
    # Add weight
    file = TFile(name+'.root', "UPDATE")
    # Calculate weight
    if 'Run2016' in name: weight = 1.
    else:
        nevents = file.Get("counter/c_nEvents").GetBinContent(1)
        xs = sample[name]['xsec'] * sample[name]['kfactor']
        weight = LUMI * xs / nevents
    
    tree = file.Get("ntuple/tree")
    tree.SetWeight(weight)
    tree.AutoSave()
    
    
#    rescale(file, weight)
    
#    for key in file.GetListOfKeys():
#        obj = key.ReadObj()
#        if obj.IsA().InheritsFrom('TH1'):
#            obj.Scale(weight)
#            obj.Write("", TObject.kOverwrite)
#        elif obj.IsFolder():
#            subdir = obj.GetName()
#            for subkey in file.GetDirectory(subdir).GetListOfKeys():
#                subobj = subkey.ReadObj()
#                if subobj.IsA().InheritsFrom('TH1'):
#                    subobj.Scale(weight)
#                    subobj.Write("", TObject.kOverwrite)
#                elif subobj.IsFolder():
#                    subsubdir = subobj.GetName()
#                    for subsubkey in file.GetDirectory(subsubdir).GetListOfKeys():
#                        subsubobj = subsubkey.ReadObj()
#                        if subsubobj.IsA().InheritsFrom('TH1'):
#                            subsubobj.Scale(weight)
#                            subsubobj.Write("", TObject.kOverwrite)
    
#    file.Close()
pass


subdirs = [x for x in os.listdir(args.folder) if os.path.isdir(os.path.join(args.folder, x))]

os.chdir(args.folder)

for s in subdirs:
#    hadd(s)
    p = multiprocessing.Process(target=hadd, args=(s,))
    jobs.append(p)
    p.start()

os.system('cd ..')
