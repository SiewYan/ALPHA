#! /usr/bin/env python 

selection = {
    #dataset
    "triggerMET" : "(isMC?1:(HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v||HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v))",
    "triggerEle" : "(isMC?1:HLT_Ele27_WPTight_Gsf_v)",
    "triggerIsoMuo20" : "(isMC?1:(HLT_IsoMu20_v||HLT_IsoTkMu20_v))",
    "triggerIsoMuo22" : "(isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))",
    "triggerIsoMuo24" : "(isMC?1:(HLT_IsoMu24_v||HLT_IsoTkMu24_v))",
    "triggerMuo45" : "(isMC?1:(HLT_Mu45_eta2p1_v))",
    "triggerMuo50" : "(isMC?1:(HLT_Mu50_v||HLT_TkMu50_v))",
    "triggerMET_bkp" : "(isMC?1:(HLT_PFMET120_BTagCSV_p067_v||HLT_PFMET170_NoiseCleaned_v))",
    "triggerLepton" : "triggerEle || triggerIsoMuo20",
    # Cat
    "cat1" : "( Jet1.pt>50 && ( ( nJets==1 && Jet1.CSV>0.800 ) || ( nJets==2 && ( ( Jet1.CSV>0.800 ) + ( Jet2.CSV>0.800 ) )==1 ) ) )",
    "cat2" : "( Jet1.pt>50 && Jet2.pt>50 && ( ( nJets==2 && ( ( Jet1.CSV>0.800 ) + ( Jet2.CSV>0.800 ) )==2 ) || ( nJets==3 && ( ( Jet1.CSV>0.800 ) + ( Jet2.CSV>0.800 ) + ( Jet3.CSV>0.800 ) )==2  ) ) )",
    #SR #MinJetMetDPhi>1.0 && Jet1.isLoose && Jet2.isLoose && nBTagJets
    'SR' : "triggerMET && isZtoNN && MEt.pt>200 && nJets<4 && Jet1.pt>50 && abs(Jet1.eta)<2.5 && Jet2.pt>30 && abs(Jet2.eta)<2.5 && MinJetMetDPhi>0.5 && nElectrons==0 && nMuons==0 && nTaus==0 && nPhotons==0",
    'SR1' : "triggerMET && isZtoNN && MEt.pt>200 && nJets<4 && Jet1.pt>50 && abs(Jet1.eta)<2.5 && Jet2.pt>30 && abs(Jet2.eta)<2.5 && MinJetMetDPhi>0.5 && nElectrons==0 && nMuons==0 && nTaus==0 && nPhotons==0 && cat1",
    'SR2' : "triggerMET && isZtoNN && MEt.pt>200 && nJets<4 && Jet1.pt>50 && abs(Jet1.eta)<2.5 && Jet2.pt>30 && abs(Jet2.eta)<2.5 && MinJetMetDPhi>0.5 && nElectrons==0 && nMuons==0 && nTaus==0 && nPhotons==0 && cat2",
    #inclusive
    'ZmmINC' : "triggerMET && isZtoMM && Lepton1.isMuon && Lepton2.isMuon && ((Lepton1.pt>30 && Lepton1.isTight && Lepton1.pfIso04<0.15 && Lepton2.pt>10 && Lepton2.isLoose && Lepton2.pfIso04<0.25)||(Lepton1.pt>10 && Lepton1.isLoose && Lepton1.pfIso04<0.25 && Lepton2.pt>30 && Lepton2.isTight && Lepton2.pfIso04<0.15)) && V.mass > 70 && V.mass<110",
    'ZeeINC' : "triggerEle && isZtoEE && Lepton1.isElectron && Lepton2.isElectron && ((Lepton1.pt>30 && Lepton1.isTight && Lepton2.pt>10 && Lepton2.isLoose)||(Lepton1.pt>10 && Lepton1.isLoose && Lepton2.pt>30 && Lepton2.isTight)) && V.mass > 70 && V.mass<110",
    'WmnINC' : "triggerMET && isWtoMN && Lepton1.isMuon && Lepton1.pt>30 && Lepton1.isTight && Lepton1.pfIso04<0.15 && V.tmass>50",
    'WenINC' : "triggerEle && isWtoEN && Lepton1.isElectron && Lepton1.pt>30 && Lepton1.isTight && V.tmass>50",
    'TemINC' : "triggerEle && Lepton1.isTight && Lepton2.isTight && Lepton1.pt>30 && Lepton2.pt>30 && ((Lepton1.isMuon && Lepton1.pfIso04<0.15 && Lepton2.isElectron)||(Lepton2.isMuon && Lepton2.pfIso04<0.15 && Lepton1.isElectron)) && ((Lepton1.charge>0 && Lepton2.charge<0)||(Lepton2.charge>0 && Lepton1.charge<0))",
    #CR
    'ZmmCR' : "ZmmINC && hadronicRecoil.pt>200 && nElectrons==0 && nMuons==2 && nJets<4 && nTaus==0 && nPhotons==0 && Jet1.isLoose && Jet1.pt>50",
    'ZeeCR' : "ZeeINC && hadronicRecoil.pt>200 && nElectrons==2 && nMuons==0 && nJets<4 && nTaus==0 && nPhotons==0 && Jet1.isLoose && Jet1.pt>50",
    'WmnCR' : "WmnINC && hadronicRecoil.pt>200 && nElectrons==0 && nMuons==1 && nJets<4 && nTaus==0 && nPhotons==0 && Jet1.isLoose && Jet1.pt>50 && V.tmass>50 && V.tmass<160",
    'WenCR' : "WenINC && hadronicRecoil.pt>200 && nElectrons==1 && nMuons==0 && nJets<4 && nTaus==0 && nPhotons==0 && Jet1.isLoose && Jet1.pt>50 && V.tmass>50 && V.tmass<160 && MEt.pt>60",
    'TemCR' : "TemINC && hadronicRecoil.pt>200 && nElectrons==1 && nMuons==1 && nJets<4 && nTaus==0 && nPhotons==0 && Jet1.isLoose && Jet1.pt>50",
    ##first catagory
    'ZmmbCR' : "ZmmCR && cat1",
    'ZeebCR' : "ZeeCR && cat1",
    'WmnbCR' : "WmnCR && cat1",
    'WenbCR' : "WenCR && cat1",
    'TembCR' : "TemCR && cat1",
    ##second catagory
    'ZmmbbCR' : "ZmmCR && cat2",
    'ZeebbCR' : "ZeeCR && cat2",
    'WmnbbCR' : "WmnCR && cat2",
    'WenbbCR' : "WenCR && cat2",
    'TembbCR' : "TemCR && cat2",
}
