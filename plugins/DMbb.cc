// -*- C++ -*-
//
// Package:    Analysis/DMbb
// Class:      DMbb
// 
/**\class DMbb DMbb.cc Analysis/DMbb/plugins/DMbb.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Alberto Zucchetta
//         Created:  Thu, 28 Apr 2016 08:28:54 GMT
//
//

#include "DMbb.h"

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
DMbb::DMbb(const edm::ParameterSet& iConfig):
    GenPSet(iConfig.getParameter<edm::ParameterSet>("genSet")),
    PileupPSet(iConfig.getParameter<edm::ParameterSet>("pileupSet")),
    TriggerPSet(iConfig.getParameter<edm::ParameterSet>("triggerSet")),
    ElectronPSet(iConfig.getParameter<edm::ParameterSet>("electronSet")),
    MuonPSet(iConfig.getParameter<edm::ParameterSet>("muonSet")),
    TauPSet(iConfig.getParameter<edm::ParameterSet>("tauSet")),
    PhotonPSet(iConfig.getParameter<edm::ParameterSet>("photonSet")),
    JetPSet(iConfig.getParameter<edm::ParameterSet>("jetSet")),
    WriteNElectrons(iConfig.getParameter<int>("writeNElectrons")),
    WriteNMuons(iConfig.getParameter<int>("writeNMuons")),
    WriteNLeptons(iConfig.getParameter<int>("writeNLeptons")),
    WriteNTaus(iConfig.getParameter<int>("writeNTaus")),
    WriteNPhotons(iConfig.getParameter<int>("writeNPhotons")),
    WriteNJets(iConfig.getParameter<int>("writeNJets")),
    HistFile(iConfig.getParameter<std::string>("histFile")),
    Verbose(iConfig.getParameter<bool>("verbose"))
{
    //now do what ever initialization is needed
    usesResource("TFileService");
    
    // Initialize Objects
    theGenAnalyzer      = new GenAnalyzer(GenPSet, consumesCollector());
    thePileupAnalyzer   = new PileupAnalyzer(PileupPSet, consumesCollector());
    theTriggerAnalyzer  = new TriggerAnalyzer(TriggerPSet, consumesCollector());
    theElectronAnalyzer = new ElectronAnalyzer(ElectronPSet, consumesCollector());
    theMuonAnalyzer     = new MuonAnalyzer(MuonPSet, consumesCollector());
    theTauAnalyzer      = new TauAnalyzer(TauPSet, consumesCollector());
    thePhotonAnalyzer   = new PhotonAnalyzer(PhotonPSet, consumesCollector());
    theJetAnalyzer      = new JetAnalyzer(JetPSet, consumesCollector());
    //theBTagAnalyzer     = new BTagAnalyzer(BTagAlgo);

    theUtilities        = new Utilities();
    
    std::vector<std::string> TriggerList(TriggerPSet.getParameter<std::vector<std::string> >("paths"));
    for(unsigned int i = 0; i < TriggerList.size(); i++) TriggerMap[ TriggerList[i] ] = false;
        
    // ---------- Plots Initialization ----------
    TFileDirectory allDir=fs->mkdir("All/");
    TFileDirectory genDir=fs->mkdir("Gen/");
    TFileDirectory eleDir=fs->mkdir("Electrons/");
    TFileDirectory muoDir=fs->mkdir("Muons/");
    TFileDirectory tauDir=fs->mkdir("Taus/");
    TFileDirectory phoDir=fs->mkdir("Photons/");
    TFileDirectory jetDir=fs->mkdir("Jets/");
    TFileDirectory kinDir=fs->mkdir("Kin/");
    
    // Make TH1F
    std::vector<std::string> nLabels={"All", "Trigger", "Iso Lep #geq 2", "Z cand ", "Jets #geq 2", "Z mass ", "h mass ", "Top veto", "bJets #geq 1", "bJets #geq 2"};
    
    int nbins;
    float min, max;
    std::string name, title, opt;
    
    ifstream histFile(HistFile);
    if(!histFile.is_open()) {
        throw cms::Exception("DMbb Analyzer", HistFile + " file not found");
    }
    while(histFile >> name >> title >> nbins >> min >> max >> opt) {
        if(name.find('#')==std::string::npos) {
            while(title.find("~")!=std::string::npos) title=title.replace(title.find("~"), 1, " "); // Remove ~
            if(name.substr(0, 2)=="a_") Hist[name] = allDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max); //.substr(2)
            if(name.substr(0, 2)=="g_") Hist[name] = genDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max);
            if(name.substr(0, 2)=="e_") Hist[name] = eleDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max);
            if(name.substr(0, 2)=="m_") Hist[name] = muoDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max);
            if(name.substr(0, 2)=="t_") Hist[name] = tauDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max);
            if(name.substr(0, 2)=="p_") Hist[name] = phoDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max);
            if(name.substr(0, 2)=="j_") Hist[name] = jetDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max);
            if(name.substr(0, 2)=="k_") Hist[name] = kinDir.make<TH1F>(name.c_str(), title.c_str(), nbins, min, max);
            Hist[name]->Sumw2();
            Hist[name]->SetOption(opt.c_str());
            // Particular histograms
            if(name=="a_nEvents" || name=="e_nEvents" || name=="m_nEvents") for(unsigned int i=0; i<nLabels.size(); i++) Hist[name]->GetXaxis()->SetBinLabel(i+1, nLabels[i].c_str());
        }
    }
    histFile.close();
    
    std::cout << "---------- STARTING ----------" << std::endl;
}


DMbb::~DMbb() {
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
    std::cout << "---------- ENDING  ----------" << std::endl;
    
    
    delete theGenAnalyzer;
    delete thePileupAnalyzer;
    delete theTriggerAnalyzer;
    delete theElectronAnalyzer;
    delete theMuonAnalyzer;
    delete theTauAnalyzer;
    delete thePhotonAnalyzer;
    delete theJetAnalyzer;
    //delete theBTagAnalyzer;
    
}


//
// member functions
//

// ------------ method called for each event  ------------
void DMbb::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

    isMC = !iEvent.isRealData();
    EventNumber = iEvent.id().event();
    LumiNumber = iEvent.luminosityBlock();
    RunNumber = iEvent.id().run();
    
    EventWeight = StitchWeight = ZewkWeight = WewkWeight = TopPtWeight = PUWeight = TriggerWeight = LeptonWeight = 1.;
    FacWeightUp = FacWeightDown = RenWeightUp = RenWeightDown = ScaleWeightUp = ScaleWeightDown = 1.;
    isZtoEE = isZtoMM = isTtoEM = isWtoEN = isWtoMN = isZtoNN = false;
    nPV = nElectrons = nMuons = nTaus = nPhotons = nJets = nBTagJets = 1;
    nVetoElectrons = nLooseMuons = nLooseElectrons = nTightMuons = nTightElectrons = 0;
    MaxJetBTag = Chi2 = -1.;
    MinJetMetDPhi = 10.;
    massRecoilFormula = -1.;
    AddFourMomenta addP4;
    
    // Initialize types
    for(int i = 0; i < WriteNElectrons; i++) ObjectsFormat::ResetLeptonType(Electrons[i]);
    for(int i = 0; i < WriteNMuons; i++) ObjectsFormat::ResetLeptonType(Muons[i]);
    for(int i = 0; i < WriteNLeptons; i++) ObjectsFormat::ResetLeptonType(Leptons[i]);
    for(int i = 0; i < WriteNTaus; i++) ObjectsFormat::ResetTauType(Taus[i]);
    for(int i = 0; i < WriteNPhotons; i++) ObjectsFormat::ResetPhotonType(Photons[i]);
    for(int i = 0; i < WriteNJets; i++) ObjectsFormat::ResetJetType(Jets[i]);

    ObjectsFormat::ResetMEtType(MEt);
    ObjectsFormat::ResetMEtType(hadronicRecoil);
    
    ObjectsFormat::ResetCandidateType(V);
    ObjectsFormat::ResetCandidateType(X);
    
    Hist["a_nEvents"]->Fill(1., EventWeight);
    Hist["e_nEvents"]->Fill(1., EventWeight);
    Hist["m_nEvents"]->Fill(1., EventWeight);

    // -----------------------------------
    //           READ OBJECTS
    // -----------------------------------
    
    // Pu weight
    PUWeight = thePileupAnalyzer->GetPUWeight(iEvent);
    nPV = thePileupAnalyzer->GetPV(iEvent);
    Hist["a_nPVNoWeight"]->Fill(nPV, EventWeight);
    EventWeight *= PUWeight;
    Hist["a_nPVReWeight"]->Fill(nPV, EventWeight);
    
    // Trigger
    theTriggerAnalyzer->FillTriggerMap(iEvent, TriggerMap);
    EventWeight *= TriggerWeight;
    
    // Electrons
    std::vector<pat::Electron> ElecVect = theElectronAnalyzer->FillElectronVector(iEvent);
    nElectrons = ElecVect.size();
    std::vector<pat::Electron> TightElecVect;
    for(unsigned int i =0; i<ElecVect.size(); i++){
        if(ElecVect.at(i).userInt("isTight")==1) {
            TightElecVect.push_back(ElecVect.at(i));
            nTightElectrons++;
        }
    }
    // Muons
    std::vector<pat::Muon> MuonVect = theMuonAnalyzer->FillMuonVector(iEvent);
    nMuons = MuonVect.size();
    std::vector<pat::Muon> TightMuonVect;
    for(unsigned int i =0; i<MuonVect.size(); i++){
        if(MuonVect.at(i).userInt("isTight")==1){
            TightMuonVect.push_back(MuonVect.at(i));
            nTightMuons++;
        }
    }
    // Taus
    std::vector<pat::Tau> TauVect = theTauAnalyzer->FillTauVector(iEvent);
    theTauAnalyzer->CleanTausFromMuons(TauVect, MuonVect, 0.4);
    theTauAnalyzer->CleanTausFromElectrons(TauVect, ElecVect, 0.4);
    nTaus = TauVect.size();
    // Photons
    std::vector<pat::Photon> PhotonVect = thePhotonAnalyzer->FillPhotonVector(iEvent);
    thePhotonAnalyzer->CleanPhotonsFromMuons(PhotonVect, MuonVect, 0.4);
    thePhotonAnalyzer->CleanPhotonsFromElectrons(PhotonVect, ElecVect, 0.4);
    nPhotons = PhotonVect.size();
    // Jets
    std::vector<pat::Jet> JetsVect = theJetAnalyzer->FillJetVector(iEvent);
    theJetAnalyzer->CleanJetsFromMuons(JetsVect, MuonVect, 0.4);
    theJetAnalyzer->CleanJetsFromElectrons(JetsVect, ElecVect, 0.4);
    nJets = JetsVect.size();
    nBTagJets = theJetAnalyzer->GetNBJets(JetsVect);
    // Fat Jets
    // Missing Energy
    pat::MET MET = theJetAnalyzer->FillMetVector(iEvent);
    pat::MET hadRecoil(MET);
    
    //theJetAnalyzer->ApplyRecoilCorrections(MET, &MET.genMET()->p4(), &theV.p4(), 0);
    
    
    // -----------------------------------
    //           GEN LEVEL
    // -----------------------------------
    
    // Gen weights
    std::map<std::string, float> GenWeight = theGenAnalyzer->FillWeightsMap(iEvent);
    EventWeight *= GenWeight["event"];
    if(GenWeight.find("2") != GenWeight.end()) FacWeightUp     = GenWeight["2"];
    if(GenWeight.find("3") != GenWeight.end()) FacWeightDown   = GenWeight["3"];
    if(GenWeight.find("4") != GenWeight.end()) RenWeightUp     = GenWeight["4"];
    if(GenWeight.find("7") != GenWeight.end()) RenWeightDown   = GenWeight["7"];
    if(GenWeight.find("5") != GenWeight.end()) ScaleWeightUp   = GenWeight["5"];
    if(GenWeight.find("9") != GenWeight.end()) ScaleWeightDown = GenWeight["9"];
    // Lhe Particles
    std::map<std::string, float> LheMap = theGenAnalyzer->FillLheMap(iEvent);
    // Mc Stitching
    StitchWeight = theGenAnalyzer->GetStitchWeight(LheMap);
    //EventWeight *= StitchWeight; // Not yet
    // Gen Particles
    std::vector<reco::GenParticle> GenPVect = theGenAnalyzer->FillGenVector(iEvent);
    // Gen candidates
    reco::Candidate* theGenZ = theGenAnalyzer->FindGenParticle(GenPVect, 23);
    reco::Candidate* theGenW = theGenAnalyzer->FindGenParticle(GenPVect, 24);
    reco::Candidate* theGenTop     = theGenAnalyzer->FindGenParticle(GenPVect, 6);
    reco::Candidate* theGenAntiTop = theGenAnalyzer->FindGenParticle(GenPVect, -6);
    // EWK corrections
    if(theGenZ) ZewkWeight = theGenAnalyzer->GetZewkWeight(theGenZ->pt());
    if(theGenW) WewkWeight = theGenAnalyzer->GetWewkWeight(theGenW->pt());
    // TopPtReweighting corrections
    if(theGenTop && theGenAntiTop) TopPtWeight = theGenAnalyzer->GetTopPtWeight(theGenTop->pt())*theGenAnalyzer->GetTopPtWeight(theGenAntiTop->pt());
    
    EventWeight *= ZewkWeight * WewkWeight * TopPtWeight;
    
    std::vector<int> LepIds = {11,13,15,-11,-13,-15};
    std::vector<int> NeuIds = {12,14,16,-12,-14,-16};
    std::vector<int> HadIds = {1,2,3,4,5,-1,-2,-3,-4,-5};
//     std::vector<int> BquIds = {5,-5};
    reco::GenParticle* theGenLep = theGenAnalyzer->FindGenParticleGenByIds(GenPVect, LepIds);
    reco::GenParticle* theGenNeu = theGenAnalyzer->FindGenParticleGenByIds(GenPVect, NeuIds);
    reco::GenParticle* theGenHad = theGenAnalyzer->FindGenParticleGenByIds(GenPVect, HadIds);
//     reco::GenParticle* theGenBqu = theGenAnalyzer->FindGenParticleGenByIds(GenPVect, BquIds);
    
    if(theGenZ){
        Hist["g_Zmass"]->Fill(theGenZ->mass(), EventWeight);
        Hist["g_Zpt"]->Fill(theGenZ->pt(), EventWeight);
        Hist["g_Zeta"]->Fill(theGenZ->eta(), EventWeight);
        Hist["g_Zphi"]->Fill(theGenZ->phi(), EventWeight);
    }
    
    if(theGenW){
        Hist["g_Wmass"]->Fill(theGenW->mass(), EventWeight);
        Hist["g_Wpt"]->Fill(theGenW->pt(), EventWeight);
        Hist["g_Weta"]->Fill(theGenW->eta(), EventWeight);
        Hist["g_Wphi"]->Fill(theGenW->phi(), EventWeight);
    }

//     if(theGenBqu!=NULL){
//         float dR_GenB = -1;
//         float dPhi_GenB = -1;
//         for(unsigned int b = 0; b<=theGenBqu->size(); b++) {
//             if(b<2){
//                 Hist[Form("g_b%dpt",b+1)]->Fill(theGenBqu[b]->pt(), EventWeight);
//                 Hist[Form("g_b%deta",b+1)]->Fill(theGenBqu[b]->eta(), EventWeight);
//                 Hist[Form("g_b%dphi",b+1)]->Fill(theGenBqu[b]->phi(), EventWeight);
//             }
//         }
//         if(theGenBqu->size()>1){
//             dR_GenB = reco::deltaR(theGenBqu[0]->eta(),theGenBqu[0]->phi(),theGenBqu[0]->eta(),theGenBqu[0]->phi());
//             dPhi_GenB = reco::deltaPhi(theGenBqu[0]->phi(),theGenBqu[0]->phi());
//             Hist["g_bdR"]->Fill(dR_GenB, EventWeight);
//             Hist["g_bdPhi"]->Fill(dPhi_GenB, EventWeight);
//         }
//     }
   
    
//     reco::Candidate* theGenX = theGenAnalyzer->FindGenParticleByIdAndStatus(GenPVect, 39, 62);
//     if(!theGenX) theGenX = theGenAnalyzer->FindGenParticleByIdAndStatus(GenPVect, 36, 62);
//     if(theGenX!=NULL && theGenLep!=NULL && theGenHad!=NULL && isGenZZ){
//         Hist["g_XMass"]->Fill(theGenX->mass(), EventWeight);
//         Hist["g_XMT"]->Fill(theGenX->mt(), EventWeight);
//         Hist["g_XPt"]->Fill(theGenX->pt(), EventWeight);
//         Hist["g_XRapidity"]->Fill(theGenX->rapidity(), EventWeight);
//         //GenXMass = theGenX->mass();
//     }
        
    // -----------------------------------
    //           VECTOR BOSON
    // -----------------------------------
    
    // Categorization depending on the number of leptons
    
    // ---------- Z TO LEPTONS ----------
    if(MuonVect.size()>=2 || ElecVect.size()>=2) {
        if(MuonVect.size()>=2 && ElecVect.size()>=2) {
            if(MuonVect.at(0).pt() > ElecVect.at(0).pt()) isZtoMM=true;
            else isZtoEE=true;
        }
        else if(ElecVect.size()>=2) isZtoEE=true;
        else if(MuonVect.size()>=2) isZtoMM=true;
        else {if(Verbose) std::cout << " - No Iso SF OS Leptons" << std::endl;}
    }
    // ---------- W TO LEPTON and NEUTRINO ----------
    else if(MuonVect.size()==1 || ElecVect.size()==1) {
        if(MuonVect.size()==1 && ElecVect.size()==1) isTtoEM = true;
        else if(ElecVect.size()==1) isWtoEN=true;
        else if(MuonVect.size()==1) isWtoMN=true;
        else {if(Verbose) std::cout << " - No Iso Leptons" << std::endl;}
    }
    // ----------- Z TO NEUTRINOS ---------------
    else if(MuonVect.size()==0 && ElecVect.size()==0) {
        isZtoNN=true;
        if(Verbose) std::cout << " - No charged leptons" << std::endl;
    }
    else {if(Verbose) std::cout << " - No leptons and not enough MET to have Z->inv" << std::endl; return;}
    
    if(isTtoEM) {if(Verbose) std::cout << " - ttbar(lep) candidate" << std::endl; }
    else if(isZtoEE || isZtoMM) {if(Verbose) std::cout << " - Z->ll candidate" << std::endl; }
    else if(isWtoEN || isWtoMN) {if(Verbose) std::cout << " - W->lnu candidate" << std::endl; }
    else if(isZtoNN) {if(Verbose) std::cout << " - Z->inv candidate" << std::endl; }
//     else if(not(isZtoEE || isZtoMM || isZtoNN || isWtoEN || isWtoMN)) {if(Verbose) std::cout << " - No V candidate" << std::endl; return;}
    
    Hist["a_nEvents"]->Fill(3., EventWeight);
    Hist["m_nEvents"]->Fill(8., EventWeight);
//    if(isZtoEE) Hist["e_nEvents"]->Fill(3., EventWeight);
//    if(isZtoMM) Hist["m_nEvents"]->Fill(3., EventWeight);


    // ---------- Reconstruct V candidate ----------
    
    pat::CompositeCandidate theV;

    if(isZtoMM) {
        if(Verbose) std::cout << " - Try to reconstruct Z -> mm" << std::endl;
        // Indentify leptons
        int m1(-1), m2(-1);
        float maxZpt(-1.);
        for(unsigned int i = 0; i < MuonVect.size(); i++) {
            for(unsigned int j = 1; j < MuonVect.size(); j++) {
                if(i==j) continue;
                if(MuonVect[i].charge() == MuonVect[j].charge()) continue;
                float Zpt = (MuonVect[i].p4() + MuonVect[j].p4()).pt();
                float Zmass = (MuonVect[i].p4() + MuonVect[j].p4()).mass();
                if(Zmass > 70. && Zmass < 110. && Zpt > maxZpt) {m1 = i; m2 = j; maxZpt = Zpt;}
            }
        }
        // Build candidate
        if(m1 >= 0 && m2 >= 0) {
            theV.addDaughter(MuonVect.at(m1).charge() < 0 ? MuonVect.at(m1) : MuonVect.at(m2));
            theV.addDaughter(MuonVect.at(m1).charge() < 0 ? MuonVect.at(m2) : MuonVect.at(m1));
            addP4.set(theV);
            // SF
            if(isMC) {
                LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(MuonVect.at(m1));
                LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(MuonVect.at(m2));
                if (MuonVect.at(m1).pt() > MuonVect.at(m2).pt() ) {
                    /// FIXME -> APPLYING THE SF FOR IsoMu22 HADRCODED <- FIXME ///
//                     LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFIsoMu22(MuonVect.at(m1));
                    LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(MuonVect.at(m1), 3); // TightID
                    LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(MuonVect.at(m1), 2);// TightIso
                    LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(MuonVect.at(m2), 1); // LooseID
                    LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(MuonVect.at(m2), 1);// LooseIso
                }
                else {
                    /// FIXME -> APPLYING THE SF FOR IsoMu22 HADRCODED <- FIXME ///
//                     LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFIsoMu22(MuonVect.at(m2));
                    LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(MuonVect.at(m2), 3); // TightID
                    LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(MuonVect.at(m2), 2);// TightIso
                    LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(MuonVect.at(m1), 1); // LooseID
                    LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(MuonVect.at(m1), 1);// LooseIso
                }
            }
        }
        else { if(Verbose) std::cout << " - No OS muons" << std::endl; return; }
        // Clean-up muon collection
        pat::Muon Mu1 = MuonVect.at(m1), Mu2 = MuonVect.at(m2);
        MuonVect.clear();
        if(Mu1.pt() > Mu2.pt()) {MuonVect.push_back(Mu1); MuonVect.push_back(Mu2);}
        else {MuonVect.push_back(Mu2); MuonVect.push_back(Mu1);}

        float px = MET.px() + Mu1.px() + Mu2.px();
        float py = MET.py() + Mu1.py() + Mu2.py();      
        hadRecoil.setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py) ));
    }
    else if(isZtoEE) {
        if(Verbose) std::cout << " - Try to reconstruct Z -> ee" << std::endl;
        // Indentify leptons
        int e1(-1), e2(-1);
        float maxZpt(-1.);
        for(unsigned int i = 0; i < ElecVect.size(); i++) {
            for(unsigned int j = 1; j < ElecVect.size(); j++) {
                if(i==j) continue;
                if(ElecVect[i].charge() == ElecVect[j].charge()) continue;
                float Zpt = (ElecVect[i].p4() + ElecVect[j].p4()).pt();
                float Zmass = (ElecVect[i].p4() + ElecVect[j].p4()).mass();
                if(Zmass > 70. && Zmass < 110. && Zpt > maxZpt) {e1 = i; e2 = j; maxZpt = Zpt;}
            }
        }
        // Build candidate
        if(e1 >= 0 && e2 >= 0) {
            theV.addDaughter(ElecVect.at(e1).charge() ? ElecVect.at(e1) : ElecVect.at(e2));
            theV.addDaughter(ElecVect.at(e1).charge() ? ElecVect.at(e2) : ElecVect.at(e1));
            addP4.set(theV);
            // SF
            if(isMC) {
                LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(ElecVect.at(e1));
                LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(ElecVect.at(e2));
                if (ElecVect.at(e1).pt() > ElecVect.at(e2).pt() ) {
                /// FIXME -> APPLYING THE SF FOR Ele27 HADRCODED <- FIXME ///
                    LeptonWeight *= theElectronAnalyzer->GetElectronTriggerSFEle27Tight(ElecVect.at(e1));
                    LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(ElecVect.at(e1), 3);// TightID
                    LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(ElecVect.at(e2), 1);// LooseID
                }
                else {
                /// FIXME -> APPLYING THE SF FOR Ele27 HADRCODED <- FIXME ///
                    LeptonWeight *= theElectronAnalyzer->GetElectronTriggerSFEle27Tight(ElecVect.at(e2));                
                    LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(ElecVect.at(e2), 3);// TightID
                    LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(ElecVect.at(e1), 1);// LooseID
                }
            }        
        }
        else { if(Verbose) std::cout << " - No OS electrons" << std::endl; return; }
        // Clean-up electron collection
        pat::Electron Ele1 = ElecVect.at(e1), Ele2 = ElecVect.at(e2);
        ElecVect.clear();
        if(Ele1.pt() > Ele2.pt()) {ElecVect.push_back(Ele1); ElecVect.push_back(Ele2);}
        else {ElecVect.push_back(Ele2); ElecVect.push_back(Ele1);}

        float px = MET.px() + Ele1.px() + Ele2.px();
        float py = MET.py() + Ele1.py() + Ele2.py();      
        hadRecoil.setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py) ));
    }
    else if(isTtoEM) {
        if(Verbose) std::cout << " - Try to reconstruct TT -> enmn" << std::endl;
        theV.addDaughter(MuonVect.at(0));
        theV.addDaughter(ElecVect.at(0));
        addP4.set(theV);
        // SF
        if(isMC) {
            ///Mu
            LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(MuonVect.at(0));
            LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(MuonVect.at(0), 3); //TightID
            LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(MuonVect.at(0), 2);//TightIso
            ///Ele
            /// FIXME -> APPLYING THE SF FOR Ele27 HADRCODED <- FIXME ///
            LeptonWeight *= theElectronAnalyzer->GetElectronTriggerSFEle27Tight(ElecVect.at(0));
            LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(ElecVect.at(0));
            LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(ElecVect.at(0), 3);// TightID
        }

        float px = MET.px() + MuonVect.at(0).px() + ElecVect.at(0).px();
        float py = MET.py() + MuonVect.at(0).py() + ElecVect.at(0).py();      
        hadRecoil.setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py) ));
    }
    else if(isWtoMN) {
        if(Verbose) std::cout << " - Try to reconstruct W -> mn" << std::endl;
        // W kinematic reconstruction
//         float pz = theUtilities->RecoverNeutrinoPz(&MuonVect.at(0).p4(), &MET.p4());
//         Neutrino.setP4(reco::Particle::LorentzVector(MET.px(), MET.py(), pz, sqrt(MET.pt()*MET.pt() + pz*pz) ));
        theV.addDaughter(MuonVect.at(0));
        theV.addDaughter(MET);
        addP4.set(theV);
        // SF
        if(isMC) {
            /// FIXME -> APPLYING THE SF FOR IsoMu22 HADRCODED <- FIXME ///
//             LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFIsoMu22(MuonVect.at(0));
            LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(MuonVect.at(0));
            LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(MuonVect.at(0), 3); //TightID
            LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(MuonVect.at(0), 2);//TightIso
        }

        float px = MET.px() + MuonVect.at(0).px();
        float py = MET.py() + MuonVect.at(0).py();      
        hadRecoil.setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py) ));
    }
    else if(isWtoEN) {
        if(Verbose) std::cout << " - Try to reconstruct W -> em" << std::endl;
        // W kinematic reconstruction
//         float pz = theUtilities->RecoverNeutrinoPz(&ElecVect.at(0).p4(), &MET.p4());
//         Neutrino.setP4(reco::Particle::LorentzVector(MET.px(), MET.py(), pz, sqrt(MET.pt()*MET.pt() + pz*pz) ));
        theV.addDaughter(ElecVect.at(0));
        theV.addDaughter(MET);
        addP4.set(theV);
        // SF
        if(isMC) {
            /// FIXME -> APPLYING THE SF FOR Ele27 HADRCODED <- FIXME ///
            LeptonWeight *= theElectronAnalyzer->GetElectronTriggerSFEle27Tight(ElecVect.at(0));
            LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(ElecVect.at(0), 3); //TightID
            LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(ElecVect.at(0));
        }

        float px = MET.px() + ElecVect.at(0).px();
        float py = MET.py() + ElecVect.at(0).py();      
        hadRecoil.setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py) ));
    }
    else if(isZtoNN) {
        if(Verbose) std::cout << " - Try to reconstruct Z -> nn" << std::endl;
        theV.addDaughter(MET);
        addP4.set(theV);
    }
    
    else { if(Verbose) std::cout << " - No reconstructible V candidate" << std::endl; return; }
    // Update event weight with lepton selections
    EventWeight *= LeptonWeight;
    
    Hist["a_nEvents"]->Fill(4., EventWeight);
    Hist["m_nEvents"]->Fill(9., EventWeight);
//    if(isZtoEE) Hist["e_nEvents"]->Fill(4., EventWeight);
//    if(isZtoMM) Hist["m_nEvents"]->Fill(4., EventWeight);
    
    if(isZtoEE) {
        Hist["e_Zmass"]->Fill(theV.mass(), EventWeight);
        if(ElecVect.at(0).isEB() && ElecVect.at(1).isEB()) Hist["e_ZmassBB"]->Fill(theV.mass(), EventWeight);
        if(ElecVect.at(0).isEE() && ElecVect.at(1).isEB()) Hist["e_ZmassEB"]->Fill(theV.mass(), EventWeight);
        if(ElecVect.at(0).isEB() && ElecVect.at(1).isEE()) Hist["e_ZmassBE"]->Fill(theV.mass(), EventWeight);
        if(ElecVect.at(0).isEE() && ElecVect.at(1).isEE()) Hist["e_ZmassEE"]->Fill(theV.mass(), EventWeight);
    }
    if(isZtoMM) {
        Hist["m_Zmass"]->Fill(theV.mass(), EventWeight);
        if(abs(MuonVect.at(0).eta())<1.1 && abs(MuonVect.at(1).eta())<1.1) Hist["m_ZmassBB"]->Fill(theV.mass(), EventWeight);
        if(abs(MuonVect.at(0).eta())>1.1 && abs(MuonVect.at(1).eta())<1.1) Hist["m_ZmassEB"]->Fill(theV.mass(), EventWeight);
        if(abs(MuonVect.at(0).eta())<1.1 && abs(MuonVect.at(1).eta())>1.1) Hist["m_ZmassBE"]->Fill(theV.mass(), EventWeight);
        if(abs(MuonVect.at(0).eta())>1.1 && abs(MuonVect.at(1).eta())>1.1) Hist["m_ZmassEE"]->Fill(theV.mass(), EventWeight);
    }
    
    
    // ---------- Event Variables ----------
    
    // Max b-tagged jet in the event
    for(unsigned int i = 2; i < JetsVect.size(); i++) if(JetsVect[i].bDiscriminator(JetPSet.getParameter<std::string>("btag")) > MaxJetBTag) MaxJetBTag = JetsVect[i].bDiscriminator(JetPSet.getParameter<std::string>("btag"));

    for(unsigned int i = 0; i < JetsVect.size(); i++) if(fabs(reco::deltaPhi(JetsVect[i].phi(), MET.phi())) < MinJetMetDPhi) MinJetMetDPhi = fabs(reco::deltaPhi(JetsVect[i].phi(), MET.phi()));
    
    // Jet variables
    theJetAnalyzer->AddVariables(JetsVect, MET);
    // Leptons
    theElectronAnalyzer->AddVariables(ElecVect, MET);
    theMuonAnalyzer->AddVariables(MuonVect, MET);
    
    // Highest CSV bjet in the event

    // ---------- Print Summary ----------
    if(Verbose) {
        std::cout << " --- Event n. " << iEvent.id().event() << ", lumi " << iEvent.luminosityBlock() << ", run " << iEvent.id().run() << ", weight " << EventWeight << std::endl;
        std::cout << "number of electrons: " << ElecVect.size() << std::endl;
        for(unsigned int i = 0; i < ElecVect.size(); i++) std::cout << "  electron [" << i << "]\tpt: " << ElecVect[i].pt() << "\teta: " << ElecVect[i].eta() << "\tphi: " << ElecVect[i].phi() << "\tmass: " << ElecVect[i].mass() << "\tcharge: " << ElecVect[i].charge() << std::endl;
        std::cout << "number of muons:     " << MuonVect.size() << std::endl;
        for(unsigned int i = 0; i < MuonVect.size(); i++) std::cout << "  muon     [" << i << "]\tpt: " << MuonVect[i].pt() << "\teta: " << MuonVect[i].eta() << "\tphi: " << MuonVect[i].phi() << "\tmass: " << MuonVect[i].mass() << "\tcharge: " << MuonVect[i].charge() << std::endl;
        std::cout << "number of taus:  " << TauVect.size() << std::endl;
        for(unsigned int i = 0; i < TauVect.size(); i++) std::cout << "  tau  [" << i << "]\tpt: " << TauVect[i].pt() << "\teta: " << TauVect[i].eta() << "\tphi: " << TauVect[i].phi() << std::endl;
        std::cout << "number of photons:  " << PhotonVect.size() << std::endl;
        for(unsigned int i = 0; i < PhotonVect.size(); i++) std::cout << "  photon  [" << i << "]\tpt: " << PhotonVect[i].pt() << "\teta: " << PhotonVect[i].eta() << "\tphi: " << PhotonVect[i].phi() << std::endl;
        std::cout << "number of AK4 jets:  " << JetsVect.size() << std::endl;
        for(unsigned int i = 0; i < JetsVect.size(); i++) std::cout << "  AK4 jet  [" << i << "]\tpt: " << JetsVect[i].pt() << "\teta: " << JetsVect[i].eta() << "\tphi: " << JetsVect[i].phi() << "\tmass: " << JetsVect[i].mass() << "\tCSV: " << JetsVect[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") << std::endl;
        std::cout << "Missing energy:      " << MET.pt() << std::endl;
        std::cout << "Hadronic recoil:     " << hadRecoil.pt() << std::endl;
        std::cout << "V leptonic mass:     " << theV.mass() << std::endl;
//        std::cout << "Z merged hadronic mass:     " << theHMerged.mass() << ", generated: " << GenZHadMass << std::endl;
//        std::cout << "X merged candidate mass:    " << theXMerged.mass() << ", generated: " << GenXMass << std::endl;
//        std::cout << "Z resolved hadronic mass:     " << theHResolved.mass() << ", generated: " << GenZHadMass << std::endl;
//        std::cout << "X resolved candidate mass:    " << theXResolved.mass() << ", generated: " << GenXMass << std::endl;
    }

    
    // ---------- Fill objects ----------
    if(Verbose) std::cout << " - Filling objects" << std::endl;
    if(isZtoEE || isWtoEN) for(unsigned int i = 0; i < Leptons.size() && i < ElecVect.size(); i++) ObjectsFormat::FillElectronType(Leptons[i], &ElecVect[i], isMC);
    else if(isZtoMM || isWtoMN) for(unsigned int i = 0; i < Leptons.size() && i < MuonVect.size(); i++) ObjectsFormat::FillMuonType(Leptons[i], &MuonVect[i], isMC);
    else if(isTtoEM && Leptons.size() >= 2) {
        if(ElecVect[0].pt() > MuonVect[0].pt()) {
            ObjectsFormat::FillElectronType(Leptons[0], &ElecVect[0], isMC);
            ObjectsFormat::FillMuonType(Leptons[1], &MuonVect[0], isMC);
        }
        else {
            ObjectsFormat::FillMuonType(Leptons[0], &MuonVect[0], isMC);
            ObjectsFormat::FillElectronType(Leptons[1], &ElecVect[0], isMC);
        }
    }
    for(unsigned int i = 0; i < Taus.size() && i < TauVect.size(); i++) ObjectsFormat::FillTauType(Taus[i], &TauVect[i], isMC);
    for(unsigned int i = 0; i < Photons.size() && i < PhotonVect.size(); i++) ObjectsFormat::FillPhotonType(Photons[i], &PhotonVect[i], isMC);
    for(unsigned int i = 0; i < Jets.size() && i < JetsVect.size(); i++) ObjectsFormat::FillJetType(Jets[i], &JetsVect[i], isMC);
    ObjectsFormat::FillMEtType(MEt, &MET, isMC);
    ObjectsFormat::FillMEtType(hadronicRecoil, &hadRecoil, isMC);
    ObjectsFormat::FillCandidateType(V, &theV, isMC);
    
    if (Verbose) {
        std::cout << "isZtoEE | isZtoMM | isZtoNN | isWtoEN | isWtoMN | isTtoEM\n"; 
        std::cout << Form("      %d |       %d |       %d |       %d |       %d |       %d\n",isZtoEE,isZtoMM,isZtoNN,isWtoEN,isWtoMN,isTtoEM); 
    }
    
    if( !isZtoEE && !isZtoMM && !isZtoNN && !isWtoEN && !isWtoMN && !isTtoEM ) return;
    
    // Fill tree
    tree->Fill();

    
}    

// ------------ method called once each job just before starting event loop  ------------
void DMbb::beginJob() {
    
    // Object objects are created only one in the begin job. The reference passed to the branch has to be the same
    for(int i = 0; i < WriteNElectrons; i++) Electrons.push_back( LeptonType() );
    for(int i = 0; i < WriteNMuons; i++) Muons.push_back( LeptonType() );
    for(int i = 0; i < WriteNLeptons; i++) Leptons.push_back( LeptonType() );
    for(int i = 0; i < WriteNTaus; i++) Taus.push_back( TauType() );
    for(int i = 0; i < WriteNPhotons; i++) Photons.push_back( PhotonType() );
    for(int i = 0; i < WriteNJets; i++) Jets.push_back( JetType() );
    
    // Create Tree and set Branches
    tree=fs->make<TTree>("tree", "tree");
    tree->Branch("isMC", &isMC, "isMC/O");
    tree->Branch("EventNumber", &EventNumber, "EventNumber/L");
    tree->Branch("LumiNumber", &LumiNumber, "LumiNumber/L");
    tree->Branch("RunNumber", &RunNumber, "RunNumber/L");
    tree->Branch("EventWeight", &EventWeight, "EventWeight/F");
    tree->Branch("FacWeightUp", &FacWeightUp, "FacWeightUp/F");
    tree->Branch("FacWeightDown", &FacWeightDown, "FacWeightDown/F");
    tree->Branch("RenWeightUp", &RenWeightUp, "RenWeightUp/F");
    tree->Branch("RenWeightDown", &RenWeightDown, "RenWeightDown/F");
    tree->Branch("ScaleWeightUp", &ScaleWeightUp, "ScaleWeightUp/F");
    tree->Branch("ScaleWeightDown", &ScaleWeightDown, "ScaleWeightDown/F");
    tree->Branch("StitchWeight", &StitchWeight, "StitchWeight/F");
    tree->Branch("ZewkWeight", &ZewkWeight, "ZewkWeight/F");
    tree->Branch("WewkWeight", &WewkWeight, "WewkWeight/F");
    tree->Branch("TopPtWeight", &TopPtWeight, "TopPtWeight/F");
    tree->Branch("PUWeight", &PUWeight, "PUWeight/F");
    tree->Branch("TriggerWeight", &TriggerWeight, "TriggerWeight/F");
    tree->Branch("LeptonWeight", &LeptonWeight, "LeptonWeight/F");
    
    // Set trigger branches
    for(auto it = TriggerMap.begin(); it != TriggerMap.end(); it++) tree->Branch(it->first.c_str(), &(it->second), (it->first+"/O").c_str());
    
    // Analysis variables
    tree->Branch("isZtoEE", &isZtoEE, "isZtoEE/O");
    tree->Branch("isZtoMM", &isZtoMM, "isZtoMM/O");
    tree->Branch("isTtoEM", &isTtoEM, "isTtoEM/O");
    tree->Branch("isWtoEN", &isWtoEN, "isWtoEN/O");
    tree->Branch("isWtoMN", &isWtoMN, "isWtoMN/O");
    tree->Branch("isZtoNN", &isZtoNN, "isZtoNN/O");
    tree->Branch("isMerged", &isMerged, "isMerged/O");
    tree->Branch("isResolved", &isResolved, "isResolved/O");
    
    // Objects
    tree->Branch("nPV", &nPV, "nPV/I");
    tree->Branch("nElectrons", &nElectrons, "nElectrons/I");
    tree->Branch("nVetoElectrons", &nVetoElectrons, "nVetoElectrons/I");
    tree->Branch("nTightElectrons", &nTightElectrons, "nTightElectrons/I");
    tree->Branch("nMuons", &nMuons, "nMuons/I");
    tree->Branch("nLooseMuons", &nLooseMuons, "nLooseMuons/I");
    tree->Branch("nTightMuons", &nTightMuons, "nTightMuons/I");
    tree->Branch("nTaus", &nTaus, "nTaus/I");
    tree->Branch("nPhotons", &nPhotons, "nPhotons/I");
    tree->Branch("nJets", &nJets, "nJets/I");
    tree->Branch("nBTagJets", &nBTagJets, "nBTagJets/I");
    
    tree->Branch("MaxJetBTag", &MaxJetBTag, "MaxJetBTag/F");
    tree->Branch("MinJetMetDPhi", &MinJetMetDPhi, "MinJetMetDPhi/F");
    tree->Branch("Chi2", &Chi2, "Chi2/F");
    // Angular variables
    tree->Branch("CosThetaStar", &CosThetaStar, "CosThetaStar/F");
    tree->Branch("CosTheta1", &CosTheta1, "CosTheta1/F");
    tree->Branch("CosTheta2", &CosTheta2, "CosTheta2/F");
    tree->Branch("Phi", &Phi, "Phi/F");
    tree->Branch("Phi1", &Phi1, "Phi1/F");
    // Mass recoil formula
    tree->Branch("massRecoilFormula", &massRecoilFormula, "massRecoilFormula/F");
  
    // Set Branches for objects
    for(int i = 0; i < WriteNElectrons; i++) tree->Branch(("Electron"+std::to_string(i+1)).c_str(), &(Electrons[i].pt), ObjectsFormat::ListLeptonType().c_str());
    for(int i = 0; i < WriteNMuons; i++) tree->Branch(("Muon"+std::to_string(i+1)).c_str(), &(Muons[i].pt), ObjectsFormat::ListLeptonType().c_str());
    for(int i = 0; i < WriteNLeptons; i++) tree->Branch(("Lepton"+std::to_string(i+1)).c_str(), &(Leptons[i].pt), ObjectsFormat::ListLeptonType().c_str());
    for(int i = 0; i < WriteNTaus; i++) tree->Branch(("Tau"+std::to_string(i+1)).c_str(), &(Taus[i].pt), ObjectsFormat::ListTauType().c_str());
    for(int i = 0; i < WriteNPhotons; i++) tree->Branch(("Photon"+std::to_string(i+1)).c_str(), &(Photons[i].pt), ObjectsFormat::ListPhotonType().c_str());
    for(int i = 0; i < WriteNJets; i++) tree->Branch(("Jet"+std::to_string(i+1)).c_str(), &(Jets[i].pt), ObjectsFormat::ListJetType().c_str());
    tree->Branch("MEt", &MEt.pt, ObjectsFormat::ListMEtType().c_str());
    tree->Branch("hadronicRecoil", &hadronicRecoil.pt, ObjectsFormat::ListMEtType().c_str());
    tree->Branch("V", &V.pt, ObjectsFormat::ListCandidateType().c_str());

}

// ------------ method called once each job just after ending the event loop  ------------
void DMbb::endJob() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void DMbb::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DMbb);
