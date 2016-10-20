#! /usr/bin/env python 

selection = {
    #dataset
    "triggerMET" : "(isMC?1:(HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v||HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v||HLT_PFMET170_NoiseCleaned_v||HLT_PFMET120_BTagCSV_p067_v))",
    "triggerEle" : "(isMC?1:HLT_Ele23_WPLoose_Gsf_v||HLT_Ele27_WPLoose_Gsf_v)",
    "triggerIsoMuo20" : "(isMC?1:(HLT_IsoMu20_v||HLT_IsoTkMu20_v))",
    "triggerIsoMuo24" : "(isMC?1:(HLT_IsoMu24_v||HLT_IsoTkMu24_v))",
    "triggerMuo45" : "(isMC?1:(HLT_Mu45_eta2p1_v))",
    "triggerMuo50" : "(isMC?1:(HLT_Mu50_v||HLT_TkMu50_v))",
    "triggerMET_bkp" : "(isMC?1:(HLT_PFMET120_BTagCSV_p067_v||HLT_PFMET170_NoiseCleaned_v))",
    "triggerLepton" : "triggerEle || triggerIsoMuo20",
    #cross check final product if ntuple with state flag
    #"sra" : "triggerMET && isSR ",
    #"srb" : "triggerMET && isZtoNN",
    #"wecr" : "triggerEle && isWtoEN && isWCR",
    #"wmcr" : "triggerIsoMuo20 && isWtoMN && isWCR",
    #"zeecr" : "triggerEle && isZtoEE && isZCR",
    #"zmmcr" : "triggerIsoMuo20 && isZtoMM && isZCR",
    #"tcr" : "triggerIsoMuo20 && Lepton1.isMuon!=Lepton2.isMuon && isTCR",

    #cat
    "cat1" : "( Jet1.pt>50 && Jet1.chf>0.1 && Jet1.nhf<0.8 && ( ( nJets==1 && Jet1.CSV>0.890 ) || ( nJets==2 && ( ( Jet1.CSV>0.890 ) + ( Jet2.CSV>0.890 ) )==1 ) ) ) && nTaus==0 && nPhotons==0",
    ##"cat1" : "Jet1.pt>50 && Jet1.chf>0.1 && Jet1.nhf<0.8 && (nJets==1||nJets==2) && nTaus==0 && nPhotons==0",
    "cat2" : "( Jet1.pt>50 && Jet1.chf>0.1 && Jet1.nhf<0.8 && Jet2.pt>50 && ( ( nJets==2 && ( ( Jet1.CSV>0.890 ) + ( Jet2.CSV>0.890 ) )==2 ) || ( nJets==3 && ( ( Jet1.CSV>0.890 ) + ( Jet2.CSV>0.890 ) + ( Jet3.CSV>0.890 ) )==2  ) ) ) && nTaus==0 && nPhotons==0",
    ##"cat2" : "Jet1.pt>50 && Jet1.chf>0.1 && Jet1.nhf<0.8 && Jet2.pt>50 && (nJets==2||nJets==3) && nTaus==0 && nPhotons==0",
    #SR                                                                                        
    "SR1" : "triggerMET && nLooseElectrons==0 && nLooseMuons==0 && MEt.pt>200 && MinJetMetDPhi>0.5 && cat1 && nBTagJets==1",
    "SR2" : "triggerMET && nLooseElectrons==0 && nLooseMuons==0 && MEt.pt>200 && MinJetMetDPhi>0.5 && cat2 && nBTagJets==2",
    "SR"  : "triggerMET && nLooseElectrons==0 && nLooseMuons==0 && MEt.pt>200 && MinJetMetDPhi>0.5 && (cat1 || cat2)",
    # W
    "WeInc" : "triggerEle && isWtoEN && nTightElectrons==1 && Lepton1.isElectron && Lepton1.isTight && Lepton1.pt>30 && V.tmass>50",
    "WmInc" : "triggerIsoMuo20 && isWtoMN && nTightMuons==1 && Lepton1.isMuon && Lepton1.isTight && Lepton1.pt>30 && Lepton1.pfIso04<0.15 && V.tmass>50",
    "WeCR" : "WeInc && Fakemet>200 && isWCR && V.tmass<160 && (cat1 || cat2)",
    "WmCR" : "WmInc && Fakemet>200 && isWCR && V.tmass<160 && (cat1 || cat2)",
    "WebCR" : "WeInc && Fakemet>200 && isWCR && V.tmass<160 && cat1 && nBTagJets==1",
    "WmbCR" : "WmInc && Fakemet>200 && isWCR && V.tmass<160 && cat1 && nBTagJets==1",
    "WebbCR" : "WeInc && && Fakemet>200 && isWCR && V.tmass<160 && cat2 && nBTagJets==2",
    "WmbbCR" : "WmInc && && Fakemet>200 && isWCR && V.tmass<160 && cat2 && nBTagJets==2",
    # Z                                                                                                                                                      
    "ZeeInc" : "triggerEle && isZtoEE && nTightElectrons==2 && Lepton1.isTight && Lepton1.pt>30 && Lepton2.isTight && Lepton2.pt>30 && V.mass>70 && V.mass<110",
    "ZmmInc" : "triggerIsoMuo20 && isZtoMM && nTightMuons==2 && Lepton1.isTight && Lepton1.pt>30 && Lepton1.pfIso04<0.15 && Lepton2.isTight && Lepton2.pt>30 && Lepton2.pfIso04<0.15 && V.mass>70 && V.mass<110",
    "ZeeCR" : "ZeeInc && Fakemet>200 && isZCR && (cat1 || cat2)",
    "ZmmCR" : "ZmmInc && Fakemet>200 && isZCR && (cat1 || cat2)",
    "ZeebCR" : "ZeeInc && Fakemet>200 && isZCR && cat1 && nBTagJets==1",
    "ZmmbCR" : "ZmmInc && Fakemet>200 && isZCR && cat1 && nBTagJets==1",
    "ZeebbCR" : "ZeeInc && Fakemet>200 && isZCR && cat2 && nBTagJets==2",
    "ZmmbbCR" : "ZmmInc && && Fakemet>200 && isZCR && cat2 && nBTagJets==2",
    # T                         
    "TInc" : "triggerIsoMuo20 && nTightElectrons==1 && nTightMuons==1 && Lepton1.isMuon!=Lepton2.isMuon && Lepton1.pt>30 && Lepton2.pt>30 && Lepton1.isTight && Lepton2.isTight && (Lepton1.isMuon ? Lepton1.pfIso04<0.15 : Lepton2.pfIso04<0.15)",
    "TCR" : "TInc && Fakemet>200 && (cat1 || cat2)",
    "TbCR" : "TInc && Fakemet>200 && cat1 && nBTagJets==1",
    "TbbCR" : "TInc && Fakemet>200 && cat2 && nBTagJets==2",

    }
