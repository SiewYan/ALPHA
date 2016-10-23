#!/usr/bin/env python                                                                                                                                         
import os, re
import commands
import math, time
import sys
import importlib
from Analysis.ALPHA.samples import sample

########## OPTIONS ##########                                                                                                                         

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-b', '--base',         action='store', type='string', dest='base',         default='$CMSSW_BASE/src/Analysis/ALPHA/')
#parser.add_option('-o', '--output',       action='store', type='string', dest='output',       default='')
#parser.add_option('-c', '--cfg',          action='store', type='string', dest='cfg',          default='python/Diboson.py')
parser.add_option('-l', '--filelists',  action='store', type='string', dest='filelists',  default='base')
#parser.add_option('-q', '--queue',        action='store', type='string', dest='queue',        default='local-cms-short')
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

#if not os.path.exists(os.path.expandvars(options.base+options.cfg)):
#    print '--- ERROR ---'
#    print '  \''+options.cfg+'\' file not found in '+options.base+options.cfg
#    print '  please point to a valid cfg file using option \'-c CFG-FILENAME\''
#    print
#    exit()

#path = os.getcwd()
#if len(options.output) == 0 or os.path.exists(options.output):
#    print '--- ERROR ---'
#    print '  \''+options.output+'\' folder already exists or is null!'
#    print '  please delete it or use a different name using option \'-o FOLDER-NAME\''
#    print
#    exit()
#os.system('mkdir '+options.output)


########## IMPORT SAMPLELIST ##########                                                                                                            

samplelistmod = importlib.import_module('filelist_'+options.filelists)
filelists = samplelistmod.filelists

########## LOOP ON SAMPLELISTS ##########                                                                                                         

for l in filelists:
    if not l in sample:
        print l, 'not in samples\n'
        continue
    dir= 'Run2016' if 'Run2016' in l else 'Spring16'
    file=open(os.path.expandvars(options.base+'filelists/'+dir+'/'+l+'.txt'),'r')
    filelist = file.readlines()
    splitting= max(int(float(sample[l]['nevents'])/(options.maxlsftime*3600*options.eventspersec)),1)
    njobs    = int(len(filelist)/splitting)+1
    sublists = [filelist[i:i+njobs] for i in range(0, len(filelist), njobs)]
    print '\nSplitting',l,'in',len(sublists),'chunk(s) of approximately',njobs,'files each'

