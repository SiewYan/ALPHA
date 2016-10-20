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

#python plot.py -b -c triggerMET -v MEt.pt

#WCR
#python plot.py -b -c WeCR -v Fakemet
#python plot.py -b -c WeCR -v MEt.pt
#python plot.py -b -c WeCR -v Lepton1.pt
#python plot.py -b -c WeCR -v V.pt
#python plot.py -b -c WeCR -v V.eta
#python plot.py -b -c WeCR -v V.tmass
#python plot.py -b -c WeCR -v nPV

#python plot.py -b -c WmCR -v Fakemet
#python plot.py -b -c WmCR -v MEt.pt
#python plot.py -b -c WmCR -v Lepton1.pt
#python plot.py -b -c WmCR -v Lepton1.pfIso04
#python plot.py -b -c WmCR -v V.pt
#python plot.py -b -c WmCR -v V.eta
#python plot.py -b -c WmCR -v V.tmass
#python plot.py -b -c WmCR -v nPV

#WInc
#python plot.py -b -c WeInc -v Fakemet
#python plot.py -b -c WeInc -v MEt.pt
#python plot.py -b -c WeInc -v Lepton1.pt
#python plot.py -b -c WeInc -v V.pt
#python plot.py -b -c WeInc -v V.eta
#python plot.py -b -c WeInc -v V.tmass
#python plot.py -b -c WeInc -v nPV

#python plot.py -b -c WmInc -v Fakemet
#python plot.py -b -c WmInc -v MEt.pt
#python plot.py -b -c WmInc -v Lepton1.pt
#python plot.py -b -c WmInc -v Lepton1.pfIso04
#python plot.py -b -c WmInc -v V.pt
#python plot.py -b -c WmInc -v V.eta
#python plot.py -b -c WmInc -v V.tmass
#python plot.py -b -c WmInc -v nPV

#ZCR
#python plot.py -b -c ZeeCR -v Fakemet
#python plot.py -b -c ZeeCR -v MEt.pt
#python plot.py -b -c ZeeCR -v Lepton1.pt
#python plot.py -b -c ZeeCR -v Lepton2.pt
#python plot.py -b -c ZeeCR -v V.pt
#python plot.py -b -c ZeeCR -v V.eta
#python plot.py -b -c ZeeCR -v V.mass
#python plot.py -b -c ZeeCR -v nPV

#python plot.py -b -c ZmmCR -v Fakemet
#python plot.py -b -c ZmmCR -v MEt.pt
#python plot.py -b -c ZmmCR -v Lepton1.pt
#python plot.py -b -c ZmmCR -v Lepton2.pt
#python plot.py -b -c ZmmCR -v Lepton1.pfIso04
#python plot.py -b -c ZmmCR -v Lepton2.pfIso04
#python plot.py -b -c ZmmCR -v V.pt
#python plot.py -b -c ZmmCR -v V.eta
#python plot.py -b -c ZmmCR -v V.mass
#python plot.py -b -c ZmmCR -v nPV

#ZInc
#python plot.py -b -c ZeeInc -v Fakemet
#python plot.py -b -c ZeeInc -v MEt.pt
#python plot.py -b -c ZeeInc -v Lepton1.pt
#python plot.py -b -c ZeeInc -v Lepton2.pt
#python plot.py -b -c ZeeInc -v V.pt
#python plot.py -b -c ZeeInc -v V.eta
#python plot.py -b -c ZeeInc -v V.mass
#python plot.py -b -c ZeeInc -v nPV

#python plot.py -b -c ZmmInc -v Fakemet
#python plot.py -b -c ZmmInc -v MEt.pt
#python plot.py -b -c ZmmInc -v Lepton1.pt
#python plot.py -b -c ZmmInc -v Lepton2.pt
#python plot.py -b -c ZmmInc -v Lepton1.pfIso04
#python plot.py -b -c ZmmInc -v Lepton2.pfIso04
#python plot.py -b -c ZmmInc -v V.pt
#python plot.py -b -c ZmmInc -v V.eta
#python plot.py -b -c ZmmInc -v V.mass
#python plot.py -b -c ZmmInc -v nPV

#TCR
#python plot.py -b -c TCR -v Fakemet
#python plot.py -b -c TCR -v MEt.pt
#python plot.py -b -c TCR -v Lepton1.pt
#python plot.py -b -c TCR -v Lepton2.pt
#python plot.py -b -c TCR -v Lepton1.pfIso04
#python plot.py -b -c TCR -v Lepton2.pfIso04
#python plot.py -b -c TCR -v V.pt
#python plot.py -b -c TCR -v V.eta
#python plot.py -b -c TCR -v V.mass
#python plot.py -b -c TCR -v nPV

#TInc
#python plot.py -b -c TInc -v Fakemet
#python plot.py -b -c TInc -v MEt.pt
#python plot.py -b -c TInc -v Lepton1.pt
#python plot.py -b -c TInc -v Lepton2.pt
#python plot.py -b -c TInc -v Lepton1.pfIso04
#python plot.py -b -c TInc -v Lepton2.pfIso04
#python plot.py -b -c TInc -v V.pt
#python plot.py -b -c TInc -v V.eta
#python plot.py -b -c TInc -v V.mass
#python plot.py -b -c TInc -v nPV

#SR                                                                                                                                                   
#python plot.py -b -c SR -v MEt.pt
#python plot.py -b -B -c SR -v Fakemet
#python plot.py -b -c SR -v nJets
#python plot.py -b -c SR -v Jet1.pt
#python plot.py -b -c SR -v Jet1.eta
#python plot.py -b -c SR -v Jet1.dPhi_met
#python plot.py -b -c SR -v Jet1.CSV
#python plot.py -b -c SR -v Jet2.pt
#python plot.py -b -c SR -v Jet2.eta
#python plot.py -b -c SR -v Jet2.dPhi_met
#python plot.py -b -c SR -v Jet2.CSV
#python plot.py -b -c SR -v Jet3.pt
#python plot.py -b -c SR -v Jet3.eta
#python plot.py -b -c SR -v Jet3.dPhi_met
#python plot.py -b -c SR -v Jet3.CSV

#R="SR"

#for var in MEt.pt Fakemet nJets Jet1.pt Jet1.eta Jet1.dPhi_met Jet1.CSV Jet2.pt Jet2.eta Jet2.dPhi_met Jet2.CSV Jet3.pt Jet3.eta Jet3.dPhi_met Jet3.CSV
#for var in nElectrons nMuons nTightElectrons nTightMuons nLooseElectrons nLooseMuons
#do
#python plot.py -b -c $R -v ${var}
#done

#triggerMET
#python plot.py -b -c triggerMET -v MEt.pt
#python plot.py -b -c triggerMET -v Fakemet
#python plot.py -b -c triggerMET -v nJets
#python plot.py -b -c triggerMET -v Jet1.chf
#python plot.py -b -c triggerMET -v Jet1.nhf
#python plot.py -b -c triggerMET -v Jet1.pt
#python plot.py -b -c triggerMET -v Jet2.pt
#python plot.py -b -c triggerMET -v Jet3.pt
#python plot.py -b -c triggerMET -v Jet1.eta
#python plot.py -b -c triggerMET -v Jet2.eta
#python plot.py -b -c triggerMET -v Jet3.eta
#python plot.py -b -c triggerMET -v Jet1.CSV
#python plot.py -b -c triggerMET -v Jet2.CSV
#python plot.py -b -c triggerMET -v Jet3.CSV
#python plot.py -b -c triggerMET -v Jet1.dPhi_met
#python plot.py -b -c triggerMET -v Jet2.dPhi_met

#triggerEle
#python plot.py -b -c triggerEle -v nElectrons
#python plot.py -b -c triggerEle -v nMuons
#python plot.py -b -c triggerEle -v Lepton1.pt
#python plot.py -b -c triggerEle -v Lepton2.pt
#python plot.py -b -c triggerEle -v Lepton1.eta
#python plot.py -b -c triggerEle -v Lepton2.eta
#python plot.py -b -c triggerEle -v Lepton1.pfIso04
#python plot.py -b -c triggerEle -v Lepton2.pfIso04

#triggerIsoMuo20
#python plot.py -b -c triggerIsoMuo20 -v nElectrons
#python plot.py -b -c triggerIsoMuo20 -v nMuons
#python plot.py -b -c triggerIsoMuo20 -v Lepton1.pt
#python plot.py -b -c triggerIsoMuo20 -v Lepton2.pt
#python plot.py -b -c triggerIsoMuo20 -v Lepton1.eta
#python plot.py -b -c triggerIsoMuo20 -v Lepton2.eta
#python plot.py -b -c triggerIsoMuo20 -v Lepton1.pfIso04
#python plot.py -b -c triggerIsoMuo20 -v Lepton2.pfIso04

#state flag specific
#sra
#python plot.py -b -c sra -v MEt.pt
#python plot.py -b -c sra -v Fakemet
#python plot.py -b -c sra -v nJets
#python plot.py -b -c sra -v Jet1.chf
#python plot.py -b -c sra -v Jet1.nhf
#python plot.py -b -c sra -v Jet1.pt
#python plot.py -b -c sra -v Jet2.pt
#python plot.py -b -c sra -v Jet3.pt
#python plot.py -b -c sra -v Jet1.eta
#python plot.py -b -c sra -v Jet2.eta
#python plot.py -b -c sra -v Jet3.eta
#python plot.py -b -c sra -v nElectrons
#python plot.py -b -c sra -v nMuons
#python plot.py -b -c sra -v nTaus
#python plot.py -b -c sra -v nPhotons

#srb
#python plot.py -b -c srb -v MEt.pt
#python plot.py -b -c srb -v Fakemet
#python plot.py -b -c srb -v nJets
#python plot.py -b -c srb -v Jet1.chf
#python plot.py -b -c srb -v Jet1.nhf
#python plot.py -b -c srb -v Jet1.pt
#python plot.py -b -c srb -v Jet2.pt
#python plot.py -b -c srb -v Jet3.pt
#python plot.py -b -c srb -v Jet1.eta
#python plot.py -b -c srb -v Jet2.eta
#python plot.py -b -c srb -v Jet3.eta
#python plot.py -b -c srb -v nElectrons
#python plot.py -b -c srb -v nMuons
#python plot.py -b -c srb -v nTaus
#python plot.py -b -c srb -v nPhotons
#python plot.py -b -c srb -v nTightElectrons
#python plot.py -b -c srb -v nTightMuons
#python plot.py -b -c srb -v nLooseElectrons
#python plot.py -b -c srb -v nLooseMuons

#wecr
#python plot.py -b -c wecr -v MEt.pt
#python plot.py -b -c wecr -v Fakemet
#python plot.py -b -c wecr -v nElectrons
#python plot.py -b -c wecr -v nMuons
#python plot.py -b -c wecr -v Lepton1.pt
#python plot.py -b -c wecr -v Lepton2.pt
#python plot.py -b -c wecr -v Lepton1.eta
#python plot.py -b -c wecr -v Lepton2.eta
#python plot.py -b -c wecr -v Lepton1.pfIso04
#python plot.py -b -c wecr -v Lepton2.pfIso04
#python plot.py -b -c wecr -v nTightMuons
#python plot.py -b -c wecr -v nLooseElectrons
#python plot.py -b -c wecr -v nLooseMuons
#python plot.py -b -c wecr -v nTightElectrons

#wmcr
#python plot.py -b -c wmcr -v MEt.pt
#python plot.py -b -c wmcr -v Fakemet
#python plot.py -b -c wmcr -v nElectrons
#python plot.py -b -c wmcr -v nMuons
#python plot.py -b -c wmcr -v Lepton1.pt
#python plot.py -b -c wmcr -v Lepton2.pt
#python plot.py -b -c wmcr -v Lepton1.eta
#python plot.py -b -c wmcr -v Lepton2.eta
#python plot.py -b -c wmcr -v Lepton1.pfIso04
#python plot.py -b -c wmcr -v Lepton2.pfIso04
#python plot.py -b -c wmcr -v nTightElectrons
#python plot.py -b -c wmcr -v nTightMuons
#python plot.py -b -c wmcr -v nLooseElectrons
#python plot.py -b -c wmcr -v nLooseMuons

#zeecr
#python plot.py -b -c zeecr -v MEt.pt
#python plot.py -b -c zeecr -v Fakemet
#python plot.py -b -c zeecr -v nElectrons
#python plot.py -b -c zeecr -v nMuons
#python plot.py -b -c zeecr -v Lepton1.pt
#python plot.py -b -c zeecr -v Lepton2.pt
#python plot.py -b -c zeecr -v Lepton1.eta
#python plot.py -b -c zeecr -v Lepton2.eta
#python plot.py -b -c zeecr -v Lepton1.pfIso04
#python plot.py -b -c zeecr -v Lepton2.pfIso04
#python plot.py -b -c zeecr -v nTightElectrons
#python plot.py -b -c zeecr -v nTightMuons
#python plot.py -b -c zeecr -v nLooseElectrons
#python plot.py -b -c zeecr -v nLooseMuons

#zmmcr
#python plot.py -b -c zmmcr -v MEt.pt
#python plot.py -b -c zmmcr -v Fakemet
#python plot.py -b -c zmmcr -v nElectrons
#python plot.py -b -c zmmcr -v nMuons
#python plot.py -b -c zmmcr -v Lepton1.pt
#python plot.py -b -c zmmcr -v Lepton2.pt
#python plot.py -b -c zmmcr -v Lepton1.eta
#python plot.py -b -c zmmcr -v Lepton2.eta
#python plot.py -b -c zmmcr -v Lepton1.pfIso04
#python plot.py -b -c zmmcr -v Lepton2.pfIso04
#python plot.py -b -c zmmcr -v nTightElectrons
#python plot.py -b -c zmmcr -v nTightMuons
#python plot.py -b -c zmmcr -v nLooseElectrons
#python plot.py -b -c zmmcr -v nLooseMuons

#tcr
#python plot.py -b -c tcr -v MEt.pt
#python plot.py -b -c tcr -v Fakemet
#python plot.py -b -c tcr -v nElectrons
#python plot.py -b -c tcr -v nMuons
#python plot.py -b -c tcr -v Lepton1.pt
#python plot.py -b -c tcr -v Lepton2.pt
#python plot.py -b -c tcr -v Lepton1.eta
#python plot.py -b -c tcr -v Lepton2.eta
#python plot.py -b -c tcr -v Lepton1.pfIso04
#python plot.py -b -c tcr -v Lepton2.pfIso04
#python plot.py -b -c tcr -v nTightElectrons
#python plot.py -b -c tcr -v nTightMuons
#python plot.py -b -c tcr -v nLooseElectrons
#python plot.py -b -c tcr -v nLooseMuons
