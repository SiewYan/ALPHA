#! /usr/bin/env python 

selection = {
    #dataset
    "triggerMET" : "(isMC?1:(HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v||HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v))",
    "triggerEle" : "(isMC?1:HLT_Ele27_WPLoose_Gsf_v)",
    "triggerIsoMuo20" : "(isMC?1:(HLT_IsoMu20_v||HLT_IsoTkMu20_v))",
    "triggerIsoMuo22" : "(isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))",
    "triggerIsoMuo24" : "(isMC?1:(HLT_IsoMu24_v||HLT_IsoTkMu24_v))",
    "triggerMuo45" : "(isMC?1:(HLT_Mu45_eta2p1_v))",
    "triggerMuo50" : "(isMC?1:(HLT_Mu50_v||HLT_TkMu50_v))",
    "triggerMET_bkp" : "(isMC?1:(HLT_PFMET120_BTagCSV_p067_v||HLT_PFMET170_NoiseCleaned_v))",
    "triggerLepton" : "triggerEle || triggerIsoMuo20",
    # Cat
    "cat1" : "( Jet1.pt>50 && Jet1.chf>0.1 && Jet1.nhf<0.8 && ( ( nJets==1 && Jet1.CSV>0.890 ) || ( nJets==2 && ( ( Jet1.CSV>0.890 ) + ( Jet2.CSV>0.890 ) )==1 ) ) ) && nTaus==0 ",
    "cat2" : "( Jet1.pt>50 && Jet1.chf>0.1 && Jet1.nhf<0.8 && Jet2.pt>50 && ( ( nJets==2 && ( ( Jet1.CSV>0.890 ) + ( Jet2.CSV>0.890 ) )==2 ) || ( nJets==3 && ( ( Jet1.CSV>0.890 ) + ( Jet2.CSV>0.890 ) + ( Jet3.CSV>0.890 ) )==2  ) ) ) && nTaus==0 ",
    # SR
    #v1 selection
    #'ZeeCR' : 'triggerEle && isZtoEE && isZCR && Lepton1.pt>30',
    #'ZmmCR' : 'triggerIsoMuo22 && isZtoMM && isZCR && Lepton1.pt>30',
    #'WenCR' : 'triggerEle && isWtoEN && isWCR && Lepton1.pt>30',
    #'WmnCR' : 'triggerIsoMuo22 && isWtoMN && isWCR && Lepton1.pt>30',
    #'TemCR' : 'triggerIsoMuo22 && isTtoEM && isTCR && Lepton1.pt>30',
    #'Signal' : 'triggerMET && isZtoNN && isSR && MEt.pt>200',
    #v2 selection
    #'ZeeCR' : 'triggerEle && isZtoEE && isZCR && Lepton1.pt>30 && Lepton2.pt>30 && nPhotons==0 && nTaus==0',
    #'ZmmCR' : 'triggerIsoMuo22 && isZtoMM && isZCR && Lepton1.pt>30 && Lepton2.pt>30 && nPhotons==0 && nTaus==0',
    #'WenCR' : 'triggerEle && isWtoEN && isWCR && Lepton1.pt>30 && nPhotons==0 && nTaus==0',
    #'WmnCR' : 'triggerIsoMuo22 && isWtoMN && isWCR && Lepton1.pt>30 && nPhotons==0 && nTaus==0',
    #'TemCR' : 'triggerIsoMuo22 && isTtoEM && isTCR && Lepton1.pt>30 && nPhotons==0 && nTaus==0',
    #'Signal' : 'triggerMET && isZtoNN && isSR && MEt.pt>200 && nPhotons==0 && nTaus==0',
    #v3 selection
    #'ZeeCR' : 'triggerEle && isZtoEE && Lepton1.pt>30',
    #'ZmmCR' : 'triggerIsoMuo22 && isZtoMM && Lepton1.pt>30',
    #'WenCR' : 'triggerEle && isWtoEN && Lepton1.pt>30',
    #'WmnCR' : 'triggerIsoMuo22 && isWtoMN && Lepton1.pt>30',
    #'TemCR' : 'triggerIsoMuo22 && isTtoEM && Lepton1.pt>30',
    #'Signal' : 'triggerMET && isZtoNN && MEt.pt>200',
    ##inclusive sample selection, electron no isolation
    'SR1' : "triggerMET && nElectrons==0 && nMuons==0 && MEt.pt>200 && MinJetMetDPhi>0.5 && cat1 && nBTagJets==1",
    'SR2' : "triggerMET && nElectrons==0 && nMuons==0 && MEt.pt>200 && MinJetMetDPhi>0.5 && cat2 && nBTagJets==2",
    'ZmmCR' : "triggerIsoMuo22 && isZtoMM && hadronicRecoil.pt>200 && Lepton1.isMuon && Lepton2.isMuon && MinJetMetDPhi>0.5 && ((Lepton1.pt>30 && Lepton1.isTight && Lepton1.pfIso04<0.15 && Lepton2.pt>10 && Lepton2.isLoose && Lepton2.pfIso04<0.25)||(Lepton1.pt>10 && Lepton1.isLoose && Lepton1.pfIso04<0.25 && Lepton2.pt>30 && Lepton2.isTight && Lepton2.pfIso04<0.15)) && V.mass > 70 && V.mass<110 ",
    'ZeeCR' : "triggerEle && isZtoEE && hadronicRecoil.pt>200 && Lepton1.isElectron && Lepton2.isElectron && MinJetMetDPhi>0.5 && ((Lepton1.pt>30 && Lepton1.isTight && Lepton2.pt>10 && Lepton2.isLoose)||(Lepton1.pt>10 && Lepton1.isLoose && Lepton2.pt>30 && Lepton2.isTight)) && V.mass > 70 && V.mass<110 ",
    'WmnCR' : "triggerIsoMuo22 && isWtoMN && hadronicRecoil.pt>200 && Lepton1.isMuon && Lepton1.pt>30 && Lepton1.isTight && Lepton1.pfIso04<0.15 && V.tmass>50 && V.tmass<160 && MinJetMetDPhi>0.5 ",
    'WenCR' : "triggerEle && isWtoEN && hadronicRecoil.pt>200 && Lepton1.isElectron && Lepton1.pt>30 && Lepton1.isTight && V.tmass>50 && V.tmass<160 && MinJetMetDPhi>0.5 ",
    'TemCR' : "triggerIsoMuo22 && isTtoEM && hadronicRecoil.pt>200 && ((Lepton1.isMuon && Lepton1.pt>30 && Lepton1.isTight && Lepton1.pfIso04<0.15 && Lepton2.isElectron && Lepton2.pt>30 && Lepton2.isTight)||(Lepton1.isElectron && Lepton1.pt>30 && Lepton1.isTight && Lepton2.isMuon && Lepton2.pt>30 && Lepton2.isTight && Lepton2.pfIso04<0.15)) && MinJetMetDPhi>0.5 ",
    ##first catagory
    'ZmmbCR' : "ZmmCR && cat1 && nBTagJets==1",
    'ZeebCR' : "ZeeCR && cat1 && nBTagJets==1",
    'WmnbCR' : "WmnCR && cat1 && nBTagJets==1",
    'WenbCR' : "WenCR && cat1 && nBTagJets==1",
    'TembCR' : "TemCR && cat1 && nBTagJets==1",
    ##second catagory
    #'ZmmbCR' : "ZmmCR && cat2 && nBTagJets==2",
    #'ZeebCR' : "ZeeCR && cat2 && nBTagJets==2",
    #'WmnbCR' : "WmnCR && cat2 && nBTagJets==2",
    #'WenbCR' : "WenCR && cat2 && nBTagJets==2",
    #'TembCR' : "TemCR && cat2 && nBTagJets==2",
}
