#!/bin/bash

#set -e
MC=1

if [[ MC == "0" ]]
then

for r in ZeeCR ZmmCR WenCR WmnCR TemCR
do
for va in hadronicRecoil.pt MEt.pt Jet1.pt Jet1.eta Jet2.pt Jet2.eta Jet3.pt Jet3.eta Lepton1.pt Lepton1.eta Lepton2.pt Lepton2.eta MinJetMetDPhi V.pt V.eta V.mass V.tmass Lepton1.pfIso04 Lepton2.pfIso04 Jet1.chf Jet1.nhf Jet2.chf Jet2.nhf nMuons nElectrons nPhotons nTaus nPV nBTagJets
do
python plot.py -b -c ${r} -v ${va}
done
done

else

for va in MEt.pt Jet1.pt Jet1.eta Jet2.pt Jet2.eta Jet3.pt Jet3.eta MinJetMetDPhi nBTagJets nPV
do
python plot.py -b -v ${va}
done

fi
