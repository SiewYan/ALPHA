#!/usr/bin/env python
import os, re
import commands
import math, time
import sys
from Analysis.ALPHA.samples import sample

########## FILELIST ##########

filelists = [ 
####### DATA
   ## Run2016B
  'SingleMuonRun2016B-PromptReco-v1', 
  'SingleMuonRun2016B-PromptReco-v2',
#  'DoubleMuonRun2016B-PromptReco-v1',
#  'DoubleMuonRun2016B-PromptReco-v2',
  'SingleElectronRun2016B-PromptReco-v1',
  'SingleElectronRun2016B-PromptReco-v2',
#  'DoubleEGRun2016B-PromptReco-v1',
#  'DoubleEGRun2016B-PromptReco-v2',
#  'METRun2016B-PromptReco-v1',
#  'METRun2016B-PromptReco-v2',

   # Run2016C
  'SingleMuonRun2016C-PromptReco-v2', 
#    'DoubleMuonRun2016C-PromptReco-v2',
  'SingleElectronRun2016C-PromptReco-v2',
#    'DoubleEGRun2016C-PromptReco-v2',
#  'METRun2016C-PromptReco-v2',

 # Run2016D
  'SingleMuonRun2016D-PromptReco-v2', 
#    'DoubleMuonRun2016D-PromptReco-v2',
  'SingleElectronRun2016D-PromptReco-v2',
#    'DoubleEGRun2016D-PromptReco-v2',
#  'METRun2016D-PromptReco-v2',

 # Run2016E
  'SingleMuonRun2016E-PromptReco-v2', 
#    'DoubleMuonRun2016E-PromptReco-v2',
  'SingleElectronRun2016E-PromptReco-v2',
#    'DoubleEGRun2016E-PromptReco-v2',
#  'METRun2016E-PromptReco-v2',
#    
####### MC
#   ## Z(ll)+jets
  'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#   #'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#   #'DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'DYBBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
#   #'DYBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
  'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
  'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
  'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
  'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
  'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#   ## Z(nunu)+jets
#   #'DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#   #'DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#   #'DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#   #'DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#   ## W(lnu)+jets
#   #'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#   #'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#   #'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#   #'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
#   #'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#   #'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   #'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
#   #'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
#   ## TTbar
#  'TTToSemiLeptonic_13TeV-powheg_v0_ext1_red1-v1',
#  'TTToSemiLeptonic_13TeV-powheg_v0_ext1_red2-v1',
#  'TTToSemiLeptonic_13TeV-powheg_v0_ext1_red3-v1',
#  'TTTo2L2Nu_13TeV-powheg_v0_ext1_red1-v1',
#  'TTTo2L2Nu_13TeV-powheg_v0_ext1_red2-v1',
#  'TTTo2L2Nu_13TeV-powheg_v0_ext1_red3-v1',
  'TTToSemiLeptonic_13TeV-powheg_v0_ext1-v1',
  'TTTo2L2Nu_13TeV-powheg_v0_ext1-v1',
   ## ST
  'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_v0-v1',
  #'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_v0-v1',
  'ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v0-v1',
  'ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1_v0-v1',
  #'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v0-v1',
  'ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1_v0-v1',
  #'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v0-v2',
#   ## VV
#   #'VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
#    #'ZZ_TuneCUETP8M1_13TeV-pythia8_v0-v1',
  'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
#  'ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
#    #'ZZTo4L_13TeV_powheg_pythia8_v0-v1',
#    #'ZZTo2L2Nu_13TeV_powheg_pythia8_v0-v1'
#    #'WZ_TuneCUETP8M1_13TeV-pythia8_v0-v1',
#    #'WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_v0-v1',
#    #'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8_v0-v1'
  'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
#    #'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
  'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
#    #'WW_TuneCUETP8M1_13TeV-pythia8_v0-v1',
#  'WWTo2L2Nu_Mll_1200To2500_13TeV-powheg_v0-v1',
#    ###'WWToLNuQQ_aTGC_13TeV-madgraph-pythia8_v0-v1',
#    ###'WZTo3LNu_mllmin01_13TeV-powheg-pythia8_v0-v1',
#   ## Signal
  'BulkGravToZZToZlepZhad_narrow_M-1000_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-1200_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-1400_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-1800_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-2000_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-2500_13TeV-madgraph_v14-v2',
  'BulkGravToZZToZlepZhad_narrow_M-3000_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-3500_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-4000_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-4500_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-600_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-650_13TeV-madgraph_v14-v2',
  'BulkGravToZZToZlepZhad_narrow_M-700_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-750_13TeV-madgraph_v14-v1',
  'BulkGravToZZToZlepZhad_narrow_M-800_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-1000_13TeV-madgraph_v14-v3',
  'WprimeToWZToWhadZlep_narrow_M-1200_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-1400_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-1600_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-1800_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-2000_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-2500_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-3000_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-3500_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-4000_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-4500_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-600_13TeV-madgraph_v14-v1',
  'WprimeToWZToWhadZlep_narrow_M-800_13TeV-madgraph_v14-v1',
   ## AZh
   #'GluGluToAToZhToLLBB_M225_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M250_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M275_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M300_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M325_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M350_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M400_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M500_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M600_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M700_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M800_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M900_13TeV-amcatnlo',
   #'GluGluToAToZhToLLBB_M1000_13TeV-amcatnlo',
]

########## DO NOT TOUCH BELOW THIS POINT ##########

########## OPTIONS ##########

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-b', '--base',         action='store', type='string', dest='base',         default='$CMSSW_BASE/src/Analysis/ALPHA/')
parser.add_option('-o', '--output',       action='store', type='string', dest='output',       default='')
parser.add_option('-c', '--cfg',          action='store', type='string', dest='cfg',          default='python/Diboson.py')
parser.add_option('-q', '--queue',        action='store', type='string', dest='queue',        default='local-cms-short')
parser.add_option('-m', '--maxlsftime',   action='store', type='int',    dest='maxlsftime',   default=4)
parser.add_option('-e', '--eventspersec', action='store', type='int',    dest='eventspersec', default=25)
(options, args) = parser.parse_args()

print
if not os.path.exists(os.path.expandvars(options.base)):
    print '--- ERROR ---'
    print '  \''+options.base+'\' path not found expanding '+options.base
    print '  please point to the correct path to ALPHA/ using option \'-b PATH-TO-ALPHA\'' 
    print 
    exit()

if not os.path.exists(os.path.expandvars(options.base+options.cfg)):
    print '--- ERROR ---'
    print '  \''+options.cfg+'\' file not found in '+options.base+options.cfg
    print '  please point to a valid cfg file using option \'-c CFG-FILENAME\'' 
    print 
    exit()

path = os.getcwd()
if len(options.output) == 0 or os.path.exists(options.output):
    print '--- ERROR ---'
    print '  \''+options.output+'\' folder already exists or is null!'
    print '  please delete it or use a different name using option \'-o FOLDER-NAME\'' 
    print 
    exit()
os.system('mkdir '+options.output)


########## LOOP ON FILELISTS ##########
for l in filelists:
    if not l in sample:
        print l
        continue
    dir= 'Run2016' if 'Run2016' in l else 'Spring16'
    file=open(os.path.expandvars(options.base+'filelists/'+dir+'/'+l+'.txt'),'r')
    filelist = file.readlines()
    splitting= max(int(float(sample[l]['nevents'])/(options.maxlsftime*3600*options.eventspersec)),1)
    njobs    = int(len(filelist)/splitting)+1
    sublists = [filelist[i:i+njobs] for i in range(0, len(filelist), njobs)]
    print '\nSplitting',l,'in',len(sublists),'chunk(s) of approximately',njobs,'files each'
    lfold = options.output+'/'+l
    os.system('mkdir '+lfold)

    ########## LOOP ON LSF JOB ##########
    for x in range(len(sublists)):
        lsubfold = lfold+'/'+str(x).zfill(4)
        os.system('mkdir '+lsubfold)
        os.chdir(lsubfold)
        splitlist=open('list.txt','w')  
        splitlist.write(''.join(str(x) for x in sublists[x]))
        splitlist.close()
        
        with open('job.sh', 'w') as fout:
            #fout.write('#!/bin/bash\n')
            #fout.write('#BSUB -J '+l+'_'+str(x).zfill(4)+'\n')
            fout.write('echo "PWD:"\n')
            fout.write('pwd\n')
            fout.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
            fout.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
            fout.write('echo "environment:"\n')
            fout.write('echo\n')
            fout.write('env > local.env\n')
            fout.write('env\n')
            fout.write('# ulimit -v 3000000 # NO\n')
            fout.write('echo "copying job dir to worker"\n')
            fout.write('eval `scram runtime -sh`\n')
            fout.write('ls\n')
            fout.write('echo "running"\n')
            fout.write('cmsRun '+options.base+options.cfg+' inputFiles='+options.base+lsubfold+'/list.txt\n')
            #fout.write('cmsRun '+options.base+options.cfg+' outputFile_clear outputFile='+outname+'.root inputFiles_clear inputFiles_load='+lsubfold+'/list.txt\n')
            fout.write('exit $?\n') 
            fout.write('echo ""\n')
        os.system('chmod 755 job.sh')
        
        ########## SEND JOB ON LSF QUEUE ##########
        os.system('bsub -q '+options.queue+' -o logs < job.sh')
        #print 'filelist ' + l + ' - job nr ' + str(x).zfill(4) + ' -> submitted'
        os.chdir('../../../')
   
print
print 'CURRENT JOB SUMMARY:'
os.system('bjobs')
print
