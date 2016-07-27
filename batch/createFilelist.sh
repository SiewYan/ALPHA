#!/bin/bash

if [[ "$1" != "MC" ]] && [[ "$1" != "DATA" ]]
then
    echo specify DATA or MC
    return
fi

# step 0: execute script with PhedEx request number
#python2.6 filelists/get_ds_file_info.py -n 669099 > query.txt
if [[ "$1" == "MC" ]]
then
    python2.6 batch/get_ds_file_info.py -d "/*/*RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2*/MINIAOD*" > query.txt   # for MC
else
    if [[ "$2" == "B" ]] || [[ "$2" == "C" ]] || [[ "$2" == "D" ]] || [[ "$2" == "E" ]]
        python2.6 batch/get_ds_file_info.py -d "/*/Run2016$2*/MINIAOD" > query.txt   # for Data
    fi
fi

# step 1: get name of the temporary file
tmpname=$(cat query.txt | awk '{print $4}' | sed -e 's/to//g')
echo File to be read: $tmpname

# step 2: get list of the samples names (with postfix)
cat query.txt | grep MINIAOD | awk '{print $1}' | sed -e 's/\/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2//g' | sed -e 's/\/MINIAODSIM//g' | sed -e 's/\/MINIAOD//g' | sed -e 's/\///g' > samplelist.txt

# step 3: get filelist form the dump, filter it, and dump it into appropriate files
cat samplelist.txt | while read sample
do
    if [[ "$1" == "MC" ]]
    then
        trimname=${sample%_v*} # for MC
        dirname="Spring16" # for MC
        versionname="v" # for MC
    else
        trimname=${sample%Run*} # for Data
        dirname="Run2016" # for Data
        versionname=${sample: -2} # for Data
    fi
    cat $tmpname | grep store | grep $trimname | grep $versionname > filelists/$dirname/$sample.txt
    sed -i -e 's/^/dcap:\/\/t2-srm-02.lnl.infn.it\/pnfs\/lnl.infn.it\/data\/cms\//' filelists/$dirname/$sample.txt
    echo Created filelist filelists/$dirname/$sample.txt
done

# final step: clean up
rm query.txt
rm samplelist.txt

# removed unused lists
if [[ "$1" == "MC" ]]
then
    rm filelists/Spring16/QCD*GenJets5*
    rm filelists/Spring16/QCD*BGenFilter*
    #rm filelists/Spring16/DYB*
    rm filelists/Spring16/*Contin*
    rm filelists/Spring16/GJets*
    rm filelists/Spring16/GGJets*
    rm filelists/Spring16/WWTo4Q_13TeV-powheg_v0-v1.txt
    rm filelists/Spring16/TT_TuneCUETP8M1_alphaS01273_13TeV-powheg-scaleup-pythia8_v0-v1.txt
    rm filelists/Spring16/GluGluSpin0ToZG*
    rm filelists/Spring16/WpWp*
    rm filelists/Spring16/WprimeToMuNu*
fi

# source batch/createFilelist.sh
