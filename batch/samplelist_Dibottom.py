#!/usr/bin/env python

samplelists = [
####### DATA

### Run2016B
'METRun2016B-23Sep2016-v2',
'METRun2016B-23Sep2016-v3',
'SingleElectronRun2016B-23Sep2016-v2',
'SingleElectronRun2016B-23Sep2016-v3',

### RunC
'METRun2016C-23Sep2016-v1',
'SingleElectronRun2016C-23Sep2016-v1',

### RunD
'METRun2016D-23Sep2016-v1',
'SingleElectronRun2016D-23Sep2016-v1',

### RunE
'METRun2016E-23Sep2016-v1',
###'METRun2016E-PromptReco-v2',
'SingleElectronRun2016E-23Sep2016-v1',

### RunF
'METRun2016F-23Sep2016-v1',
###'METRun2016F-PromptReco-v1',
'SingleElectronRun2016F-23Sep2016-v1',

### RunG
'METRun2016G-23Sep2016-v1',
###'METRun2016G-PromptReco-v1',
'SingleElectronRun2016G-23Sep2016-v1',

### RunH
'METRun2016H-PromptReco-v1',
'METRun2016H-PromptReco-v2',
'METRun2016H-PromptReco-v3',
###'SingleElectronRun2016H-PromptReco-v1',
'SingleElectronRun2016H-PromptReco-v2',
'SingleElectronRun2016H-PromptReco-v3',

######## MC

### Z(ll)+jets
'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v2',
'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',

#'DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1',
#'DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1',
#'DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1',
#'DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1',

### ZJetsToNuNu
'ZJetsToNuNu_HT-100To200_13TeV-madgraph_ext1-v1',
'ZJetsToNuNu_HT-200To400_13TeV-madgraph_ext1-v1',
'ZJetsToNuNu_HT-400To600_13TeV-madgraph_ext1-v1',
'ZJetsToNuNu_HT-600To800_13TeV-madgraph-v1',
'ZJetsToNuNu_HT-800To1200_13TeV-madgraph-v1',
'ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_ext1-v1',
'ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph-v1',


### W(lnu)+jets
'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1',
'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1',
'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',

### TTbar inclusive
'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-v1',

### Single Top
'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1-v1',
#'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_ext1-v1',
#'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_ext1-v1',

### Diboson
'WW_TuneCUETP8M1_13TeV-pythia8-v1', 
#'WZ_TuneCUETP8M1_13TeV-pythia8-v1',
#'ZZ_TuneCUETP8M1_13TeV-pythia8-v1',

### ZJetsToNuNu - PtZ binned
#'DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext4-v1',
#'DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1',
#'DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1',
#'DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1',  

### INCLUSIVE V+jet
#'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1',
#'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1',

### QCD
#'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
#'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
#'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
#'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
#'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
#'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v2',
#'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
#'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
#'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
#'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
#'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
#'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',
#'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1',
#'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1',

]
