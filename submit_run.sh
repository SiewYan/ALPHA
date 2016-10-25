#!/bin/bash

python batch/submitLSFjobs.py --cfg python/Dibottom.py --samplelists BB --output Prod_v03_1
#python batch/chk_filelist.py  --samplelists BB
#python batch/njob_estimate.py --filelists BB_v1_2 