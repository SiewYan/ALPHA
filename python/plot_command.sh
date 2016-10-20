#!/bin/bash

#set -e

#region dependent
#WeCR WmCR WeInc WmInc ZeeCR ZmmCR ZeeInc ZmmInc
#sra srb wecr wmcr zeecr zmmcr

#Lepton1.pt Lepton2.pt Lepton1.eta Lepton2.eta V.pt V.eta V.tmass V.mass Lepton1.pfIso04 Lepton2.pfIso04 nPV nMuons nElectrons nTightElectrons nTightMuons nLooseMuons nLooseElectrons

for r in SR1 SR2 SR WeCR WmCR WeInc WmInc ZeeCR ZmmCR ZeeInc ZmmInc TInc TCR 
do
for va in Fakemet MEt.pt Jet1.pt Jet2.pt Jet3.pt Jet1.eta Jet2.eta Jet3.eta nJets Lepton1.pt Lepton2.pt Lepton1.eta Lepton2.eta V.pt V.eta V.tmass V.mass Lepton1.pfIso04 Lepton2.pfIso04 nPV nMuons nElectrons nTightElectrons nTightMuons nLooseElectrons nLooseMuons nBTagJets
do
python plot.py -b -c ${r} -v ${va}
done
done