#!/bin/bash

#python batch/submitLSFjobs.py --cfg python/Dibottom.py --filelists BB_v1_2 --output Prod_v03
#python batch/chk_filelist.py  --filelists BB_v1_2
python batch/njob_estimate.py --filelists BB_v1_2 