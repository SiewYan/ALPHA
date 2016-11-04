#!/bin/bash

#set -e

for r in ZeeCR ZmmCR WenCR WmnCR TemCR Signal
do
for va in Jet1.pt Jet1.eta Jet2.pt Jet2.eta MEt.pt Fakemet Lepton1.pt Lepton1.eta Lepton2.pt Lepton2.eta nJets nMuons nElectrons nPhotons nTaus MinJetMetDPhi V.pt V.eta V.mass V.tmass nTightElectrons nTightMuons Lepton1.charge Lepton2.charge Jet1.chf Jet1.nhf Jet2.chf Jet2.nhf
do
python plot.py -b -c ${r} -v ${va}
done
done