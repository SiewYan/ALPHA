#!/usr/bin/env python                                                                                                                                         
import os, re
import commands
import math, time
import sys
import importlib
from Analysis.ALPHA.samples import sample

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option('-b', '--base',         action='store', type='string', dest='base',         default='$CMSSW_BASE/src/Analysis/ALPHA/')
parser.add_option('-l', '--samplelists'   , action='store', type='string', dest='samplelists',    default='base')

(options, args) = parser.parse_args()

filelistmod = importlib.import_module('samplelist_'+options.samplelists)
samplelists = filelistmod.samplelists

path = os.getcwd()

for l in samplelists:
    if not l in sample:
        print l, 'not in samples\n'
        continue
    dir= 'Run2016' if 'Run2016' in l else 'Spring16'
    if not l in options.base+'filelists/'+dir+'/'+l:
        print l, 'is not in filelists/'

    
