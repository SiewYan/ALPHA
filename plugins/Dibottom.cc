// -*- C++ -*-
//
//Package:    Analysis/dibottom
// Class:      dibottom
// 
/**\class dibottom dibottom.cc Analysis/dibottom/plugins/dibottom.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Siew Yan Hoh
//         Created:  Wed, 20 Jul 2016 13:46:29 GMT
//
//

#include "Dibottom.h"

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
Dibottom::Dibottom(const edm::ParameterSet& iConfig):
    GenPSet(iConfig.getParameter<edm::ParameterSet>("genSet")),
    PileupPSet(iConfig.getParameter<edm::ParameterSet>("pileupSet")),
    TriggerPSet(iConfig.getParameter<edm::ParameterSet>("triggerSet")),
    ElectronPSet(iConfig.getParameter<edm::ParameterSet>("electronSet")),
    MuonPSet(iConfig.getParameter<edm::ParameterSet>("muonSet")),
    TauPSet(iConfig.getParameter<edm::ParameterSet>("tauSet")),
    PhotonPSet(iConfig.getParameter<edm::ParameterSet>("photonSet")),
    JetPSet(iConfig.getParameter<edm::ParameterSet>("jetSet")),
    //BTagAlgo(iConfig.getParameter<std::string>("bTagAlgo")),
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
    //theBTagAnalyzer     = new BTagInterface(BTagAlgo);
    
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

    std::vector<std::string> labels={"All", "Trigger", "nJets #leq 4", "Jet cut", "Leptoncut", "V Cand", "Reco V"};
    
    int nbins;
    float min, max;
    std::string name, title, opt;
    
    ifstream histFile(HistFile);
    if(!histFile.is_open()) {
        throw cms::Exception("Dibottom Analyzer", HistFile + " file not found");
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
	    if(name=="a_PrenEvents") for(unsigned int i=0; i<labels.size(); i++) Hist[name]->GetXaxis()->SetBinLabel(i+1,labels[i].c_str());
        }
    }
    histFile.close();

    nevent=0;
    SR_counter = SR1_counter = SR2_counter = ZCR_counter = WCR_counter = TCR_counter = Preselected_counter = 0;

    std::cout << "---------- STARTING ----------" << std::endl;

}


Dibottom::~Dibottom()
{
 
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
float Dibottom::createFakeMETpt_e(std::vector<pat::Electron>& el, pat::MET& met){
  
  pat::MET* fakemet= met.clone();

  float px = met.px();
  float py = met.py();

  for (unsigned int i=0; i< el.size(); i++){
    px += el[i].px();
    py += el[i].py();
  }
  fakemet->setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py) ));

  return fakemet->pt();
}

float Dibottom::createFakeMETpt_m(std::vector<pat::Muon>& mu, pat::MET& met){

  pat::MET* fakemet= met.clone();

  float px = met.px();
  float py = met.py();

  for (unsigned int i=0; i< mu.size(); i++){
    px += mu[i].px();
    py += mu[i].py();
  }
  fakemet->setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py) ));

  return fakemet->pt();
}

// ------------ method called for each event  ------------
void
Dibottom::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  if (Verbose){
    std::cout<<std::endl;
    std::cout<<"###########################################################"<<std::endl;
    std::cout << " --- Event n. " << iEvent.id().event() << ", lumi " << iEvent.luminosityBlock() << ", run " << iEvent.id().run() << ", weight " << EventWeight << std::endl;  
    std::cout<<std::endl;
  }
  nevent++;

  //variables for identification
  isSR = isSR1 = isSR2 = isZCR = isWCR = isTCR = false;
  
  isMC = !iEvent.isRealData();
  EventNumber = iEvent.id().event();
  LumiNumber = iEvent.luminosityBlock();
  RunNumber = iEvent.id().run();
    
  //
  EventWeight = StitchWeight = ZewkWeight = WewkWeight = PUWeight = TriggerWeight = LeptonWeight = 1.;
  FacWeightUp = FacWeightDown = RenWeightUp = RenWeightDown = ScaleWeightUp = ScaleWeightDown = 1.;
  isZtoEE = isZtoMM = isTtoEM = isWtoEN = isWtoMN = isZtoNN = false;
  nPV = nElectrons = nMuons = nTaus = nPhotons = nJets = nBTagJets = 0;
  nTightElectrons = nTightMuons = 0;
  MaxJetBTag = -1.;
  MinJetMetDPhi = 10.;

  AddFourMomenta addP4;

  //fakemet
  Fakemet=0;
  Zpt=0;
  Zmass=0;
  Zeta=0;
  nPVZ=0;

  Wpt=0;
  Wmass=0;
  Weta=0;
  nPVW=0;
  
  // Initialize types 
  // please refer to Objects.h (declared the struct of particle) and ObjectsFormat.h/.cc (declare the method to manipulate objects)
  for(int i = 0; i < WriteNElectrons; i++) ObjectsFormat::ResetLeptonType(Electrons[i]);
  for(int i = 0; i < WriteNMuons; i++) ObjectsFormat::ResetLeptonType(Muons[i]);
  for(int i = 0; i < WriteNLeptons; i++) ObjectsFormat::ResetLeptonType(Leptons[i]);
  for(int i = 0; i < WriteNTaus; i++) ObjectsFormat::ResetTauType(Taus[i]);
  for(int i = 0; i < WriteNPhotons; i++) ObjectsFormat::ResetPhotonType(Photons[i]);
  for(int i = 0; i < WriteNJets; i++) ObjectsFormat::ResetJetType(Jets[i]);
  ObjectsFormat::ResetMEtType(MEt);
  ObjectsFormat::ResetCandidateType(V);

  Hist["a_PrenEvents"]->Fill(1., EventWeight);  
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

  if (Verbose){
    std::cout<<"***********************************************************"<<std::endl;
    std::cout<<" -- Read Physics Objects -- "<<std::endl;
    std::cout<<"***********************************************************"<<std::endl;
    std::cout<<"Event number = "<<nevent<<std::endl;
    std::cout<<std::endl;
  }

  // Muons 
  std::vector<pat::Muon> MuonVect = theMuonAnalyzer->FillMuonVector(iEvent);
  nMuons = MuonVect.size();
  //std::vector<pat::Muon> LooseMuonVect;                                                                                                              
  std::vector<pat::Muon> TightMuonVect;

  if (Verbose){
    std::cout<<" Number of Muon = "<<MuonVect.size()<<std::endl;
    std::cout<<"--------------------"<<std::endl;
    for(unsigned int i =0; i<MuonVect.size(); i++){

      std::cout<<i<<"th number of MuonVect, pt = "<<MuonVect.at(i).pt()
	       <<" , eta = "<<MuonVect.at(i).eta()
	       <<" , charge = "<<MuonVect.at(i).charge()
	       <<" , TightId = "<<MuonVect.at(i).userInt("isTight")
	       <<" , LooseId = "<<MuonVect.at(i).userInt("isLoose")
	       <<" , MediumId = "<<MuonVect.at(i).userInt("isMedium")
	       <<" , pfIso04 = "<< (MuonVect.at(i).userFloat("pfIso04"))
	       <<std::endl;
    }
    std::cout<<std::endl;
  }

  // Electrons
  std::vector<pat::Electron> ElecVect = theElectronAnalyzer->FillElectronVector(iEvent);
  nElectrons = ElecVect.size();
  //std::vector<pat::Electron> LooseElecVect;
  std::vector<pat::Electron> TightElecVect;
  
  if (Verbose){
    std::cout<<" Number of Electron = "<<ElecVect.size()<<std::endl;
    std::cout<<"--------------------"<<std::endl;
      for(unsigned int i =0; i<ElecVect.size(); i++){
	std::cout<<i<<"th number of ElecVect, pt = "<<ElecVect.at(i).pt()
		 <<" , eta = "<<ElecVect.at(i).eta()
		 <<" , charge = "<<ElecVect.at(i).charge()
		 <<" , TightId = "<<ElecVect.at(i).userInt("isTight")
		 <<" , LooseId = "<<ElecVect.at(i).userInt("isLoose")
		 <<" , MediumId = "<<ElecVect.at(i).userInt("isMedium")
		 <<" , VetoId = "<<ElecVect.at(i).userInt("isVeto")
		 <<" , pfIso04 = "<<(ElecVect.at(i).userFloat("pfIso04"))
		 <<std::endl;
      }
      std::cout<<std::endl;
  }
    
  // Taus
  std::vector<pat::Tau> TauVect = theTauAnalyzer->FillTauVector(iEvent);
  theTauAnalyzer->CleanTausFromMuons(TauVect, MuonVect, 0.4); //attention
  theTauAnalyzer->CleanTausFromElectrons(TauVect, ElecVect, 0.4); //attention
  nTaus = TauVect.size();
  
  // Photons
  std::vector<pat::Photon> PhotonVect = thePhotonAnalyzer->FillPhotonVector(iEvent);
  nPhotons = PhotonVect.size();
  
  // Jets
  std::vector<pat::Jet> JetsVect = theJetAnalyzer->FillJetVector(iEvent);
  //sort jet in ascending pt order
  sort(JetsVect.begin(), JetsVect.end(), jetComparator);
  theJetAnalyzer->CleanJetsFromMuons(JetsVect, MuonVect, 0.4);
  theJetAnalyzer->CleanJetsFromElectrons(JetsVect, ElecVect, 0.4);
  nJets = JetsVect.size();
  
  //btagjet 
  nBTagJets = theJetAnalyzer->GetNBJets(JetsVect);
  
  //theBTagAnalyzer->FillBTagVector(iEvent,JetsVect);
  
  // Missing Energy
  pat::MET MET = theJetAnalyzer->FillMetVector(iEvent);
  //pat::MET Neutrino(MET);

  // -----------------------------------
  //           GEN LEVEL
  // -----------------------------------
  
  // Gen weights
  std::map<std::string, float> GenWeight = theGenAnalyzer->FillWeightsMap(iEvent);
  EventWeight *= GenWeight["event"];
  
  //product id
  if(GenWeight.find("2") != GenWeight.end()) FacWeightUp     = GenWeight["2"];
  if(GenWeight.find("3") != GenWeight.end()) FacWeightDown   = GenWeight["3"];
  if(GenWeight.find("4") != GenWeight.end()) RenWeightUp     = GenWeight["4"];
  if(GenWeight.find("7") != GenWeight.end()) RenWeightDown   = GenWeight["7"];
  if(GenWeight.find("5") != GenWeight.end()) ScaleWeightUp   = GenWeight["5"];
  if(GenWeight.find("9") != GenWeight.end()) ScaleWeightDown = GenWeight["9"];
  
  // Lhe Particles
  // reading LHE event content and prepare it in Map format std::map<std::string, float>
  std::map<std::string, float> LheMap = theGenAnalyzer->FillLheMap(iEvent);
  
  Hist["g_nPartons"]->Fill(LheMap["lhePartons"]);
  Hist["g_nBPartons"]->Fill(LheMap["lheBPartons"]);
  Hist["g_lheHT"]->Fill(LheMap["lheHT"]);
  Hist["g_lhePtZ"]->Fill(LheMap["lhePtZ"]);
  Hist["g_lhePtW"]->Fill(LheMap["lhePtW"]);
  
  // Mc Stitching
  StitchWeight = theGenAnalyzer->GetStitchWeight(LheMap);
  //EventWeight *= StitchWeight; // Not yet
  
  // Gen Particles
  std::vector<reco::GenParticle> GenPVect = theGenAnalyzer->FillGenVector(iEvent); //serve as a carrier
  
  // Gen candidates
  reco::Candidate* theGenZ = theGenAnalyzer->FindGenParticle(GenPVect, 23);
  reco::Candidate* theGenW = theGenAnalyzer->FindGenParticle(GenPVect, 24);
  
  // EWK corrections
  if(theGenZ) ZewkWeight = theGenAnalyzer->GetZewkWeight(theGenZ->pt());
  if(theGenW) WewkWeight = theGenAnalyzer->GetWewkWeight(theGenW->pt());
  
  //    if(LheMap.find("lhePtZ")!=LheMap.end()) ZewkWeight = theGenAnalyzer->GetZewkWeight(LheMap["lhePtZ"]);
  //    if(LheMap.find("lhePtW")!=LheMap.end()) WewkWeight = theGenAnalyzer->GetWewkWeight(LheMap["lhePtW"]);
  
  EventWeight *= ZewkWeight * WewkWeight;
  
  // ---------- Trigger selections ----------
  // Dummy trigger
  //TriggerWeight*=theElectronAnalyzer->GetDoubleElectronTriggerSF(ElecVect.at(0), ElecVect.at(1));
  //TriggerWeight*=theMuonAnalyzer->GetDoubleMuonTriggerSF(MuonVect.at(0), MuonVect.at(1));

  Hist["a_PrenEvents"]->Fill(2., EventWeight);
  Hist["a_nEvents"]->Fill(2., EventWeight);
  Hist["e_nEvents"]->Fill(2., EventWeight);
  Hist["m_nEvents"]->Fill(2., EventWeight);


  //Preselection
  //nJets <=4
  if (JetsVect.size() == 0){if (Verbose)std::cout<<"EXIT :jet.size==0"<<std::endl; return;}
  if (JetsVect.size() > 4){if (Verbose) std::cout<<"EXIT :jet.size>4"<<std::endl; return;}

  Hist["a_PrenEvents"]->Fill(3., EventWeight);
  
  for (unsigned int j = 0; j < JetsVect.size(); j++){

    if(j==0){
      if(JetsVect.at(j).pt() < 50.){if (Verbose) std::cout<<"EXIT :jets "<<j<<" pt < 50 GeV"<<std::endl;return;}
      if(abs(JetsVect.at(j).eta()) > 2.5){if (Verbose) std::cout<<"EXIT :jets "<<j<<" eta > 2.5"<<std::endl;return;}
    }
    else{
      if(JetsVect.at(j).pt() < 20.){if (Verbose) std::cout<<"EXIT :jets "<<j<<" pt < 20 GeV"<<std::endl;return;}
      if(abs(JetsVect.at(j).eta()) > 2.5){if (Verbose) std::cout<<"EXIT :jets "<<j<<" eta > 2.5"<<std::endl;return;}
    }
  }
  
  Hist["a_PrenEvents"]->Fill(4., EventWeight); //jetcut1

  //tauIdByMuonRejection->loose; photonid->loose; //move to offline cut******
  //if ( nTaus > 0 ) {if (Verbose) std::cout<<"EXIT :nTaus>0"<<std::endl; return;}
  //if ( nPhotons > 0 ) {if (Verbose) std::cout<<"EXIT :nPhotons>0"<<std::endl; return;}

  //Tight electron/muon selection
  for ( unsigned int m = 0; m < MuonVect.size() ; m++){
    if(MuonVect.at(m).pt() < 30) continue;
    if(abs(MuonVect.at(m).eta()) > 2.4 ) continue;
    if(MuonVect.at(m).userInt("isTight")!=1) continue;
    TightMuonVect.push_back(MuonVect.at(m));  
  }
  sort(TightMuonVect.begin(),TightMuonVect.end(),muonComparator);
  nTightMuons = TightMuonVect.size();

  for ( unsigned int e = 0; e < ElecVect.size() ; e++){
    if(ElecVect.at(e).pt() < 30) continue;
    if(abs(ElecVect.at(e).eta()) > 2.5 ) continue;
    if(ElecVect.at(e).userInt("isTight")!=1) continue;
    TightElecVect.push_back(ElecVect.at(e));
  }
  sort(TightElecVect.begin(),TightElecVect.end(),elecComparator);
  nTightElectrons = TightElecVect.size();
  
  Hist["a_PrenEvents"]->Fill(5., EventWeight); // suppose to be lepton cut.
   
  Preselected_counter++;

  if(Verbose){
    std::cout<<"***********************************************************"<<std::endl;
    std::cout<<" -- Online Preselection result -- "<<std::endl;
    std::cout<<"***********************************************************"<<std::endl;
    std::cout<<" Number of preselected jet = "<<JetsVect.size()<<std::endl;
    std::cout<<"------------------------------------"<<std::endl;
    for ( unsigned int j = 0; j < JetsVect.size(); j++){
      std::cout<<j<<"th Jet pt = "<<JetsVect.at(j).pt()<<" GeV , eta = "<<JetsVect.at(j).eta()
	       <<" , isLoose = "<<JetsVect.at(j).userInt("isLoose")
	       <<std::endl;
    }
    std::cout<<std::endl;
    std::cout<<" Number of preselected Tight Muon = "<<TightMuonVect.size()<<std::endl;
    std::cout<<"------------------------------------"<<std::endl;
    if(TightMuonVect.size()>0){
      std::cout<<"TightMuonVect"<<std::endl;
      for (unsigned int i=0; i<TightMuonVect.size(); i++){
	std::cout<<i<<"th number of TightMuonVect, pt = "<<TightMuonVect.at(i).pt()
		 <<" , eta = "<<TightMuonVect.at(i).eta()
		 <<" , charge = "<<TightMuonVect.at(i).charge()
		 <<" , TightId = "<<TightMuonVect.at(i).userInt("isTight")
		 <<" , LooseId = "<<TightMuonVect.at(i).userInt("isLoose")
		 <<" , MediumId = "<<TightMuonVect.at(i).userInt("isMedium")
		 <<" , pfIso04 = "<< (TightMuonVect.at(i).userFloat("pfIso04"))
		 <<std::endl;
      }
    }
    std::cout<<std::endl;
    std::cout<<" Number of preselected Tight Electrons = "<<TightElecVect.size()<<std::endl;
    std::cout<<"------------------------------------"<<std::endl;
    if(TightElecVect.size()>0){
      std::cout<<"TightElecVect"<<std::endl;
      for (unsigned int i=0; i<TightElecVect.size(); i++){
	std::cout<<i<<"th number of TightElecVect, pt = "<<TightElecVect.at(i).pt()
		 <<" , eta = "<<TightElecVect.at(i).eta()
		 <<" , charge = "<<TightElecVect.at(i).charge()
		 <<" , TightId = "<<TightElecVect.at(i).userInt("isTight")
		 <<" , LooseId = "<<TightElecVect.at(i).userInt("isLoose")
                 <<" , MediumId = "<<TightElecVect.at(i).userInt("isMedium")
		 <<" , VetoId = "<<TightElecVect.at(i).userInt("isVeto") 
		 <<" , pfIso04 = "<<(TightElecVect.at(i).userFloat("pfIso04"))
		 <<std::endl;
      }
    }
    std::cout<<std::endl;
    std::cout<<"***********************************************************"<<std::endl;
  }
  
  // -----------------------------------
  //           VECTOR BOSON
  // -----------------------------------
  if (Verbose){
    std::cout<<" -- Categorization depending on the number of leptons --"<<std::endl;
    std::cout<<"***********************************************************"<<std::endl;
  }
  // Categorization depending on the number of leptons
  // the flag state can only happen once in one event loop; except the SR and the ZtoNN
  
  // ---------- Z TO LEPTONS ----------
  if ( TightMuonVect.size()>=2 || TightElecVect.size()>=2 ) {
    
    if(TightMuonVect.size()>=2 && TightElecVect.size()>=2) {
      if(TightMuonVect.at(0).pt() > TightElecVect.at(0).pt()) isZtoMM=true;
      else isZtoEE=true;
    }

    if(TightElecVect.size()>=2) isZtoEE=true;
    else if(TightMuonVect.size()>=2) isZtoMM=true;
    else {if(Verbose) std::cout << "EXIT :No Iso Same Flavor Leptons" << std::endl;}
  }
  // ---------- W TO LEPTON and NEUTRINO ----------
  else if ( TightMuonVect.size()==1 || TightElecVect.size()==1 ) {
    if(TightMuonVect.size()==1 && TightElecVect.size()==1){isTtoEM = true;}
    else if(TightElecVect.size()==1) isWtoEN=true;
    else if(TightMuonVect.size()==1) isWtoMN=true;
    else {if(Verbose) std::cout << "EXIT :No Iso Lepton" << std::endl;}
  }

  // ----------- Z TO NEUTRINOS -------------------
  else if ( ElecVect.size() == 0 && MuonVect.size() == 0 ){
    
    if(Verbose) std::cout << " - No charged leptons" << std::endl;
    
    isZtoNN=true;
    
  }
  else {if(Verbose)std::cout<<" The loose leptons exist. It does not enter any region "<<std::endl;}

  if(Verbose){
    std::cout<<"isZtoEE = "<<isZtoEE<<std::endl;
    std::cout<<"isZtoMM = "<<isZtoMM<<std::endl;
    std::cout<<"isWtoEN = "<<isWtoEN<<std::endl;
    std::cout<<"isWtoMN = "<<isWtoMN<<std::endl;
    std::cout<<"isTtoEM = "<<isTtoEM<<std::endl;
    std::cout<<"isZtoNN = "<<isZtoNN<<std::endl;
    if ( TightMuonVect.size() > 2 ){std::cout<<" -- NOTE -- "<<std::endl;
      std::cout<<"TightMuonVect has more then 2 lepton, which is "<<TightMuonVect.size()<<" Tight Muons"<<std::endl;}
    if ( TightElecVect.size() > 2 ){std::cout<<" -- NOTE -- "<<std::endl;
      std::cout<<"TightElecVect has more then 2 lepton, which is "<<TightElecVect.size()<<" Tight Electrons"<<std::endl;}
    std::cout<<std::endl;
    std::cout<<"***********************************************************"<<std::endl;
  }

  if(not(isZtoEE || isZtoMM || isZtoNN || isWtoEN || isWtoMN || isTtoEM ) ) {
    if(Verbose) std::cout << "EXIT - No V candidate" << std::endl;
    return;
  }
  
  Hist["a_PrenEvents"]->Fill(6., EventWeight);
  Hist["a_nEvents"]->Fill(3., EventWeight);
  Hist["m_nEvents"]->Fill(8., EventWeight);
  
  if(isZtoEE) Hist["e_nEvents"]->Fill(3., EventWeight);
  if(isZtoMM) Hist["m_nEvents"]->Fill(3., EventWeight);
  
  // ---------- Reconstruct V Candidate --------------- //
  if(Verbose){
    std::cout<<" - Reconstructing V Candidate - "<<std::endl;
    std::cout<<"***********************************************************"<<std::endl;
  }

  pat::CompositeCandidate theV;
  
  if(isZtoMM) {
    if(Verbose) std::cout << " - Try to reconstruct Z -> mm" << std::endl;
    // Indentify leptons
    float maxZpt(-1.);
    
    if ( TightMuonVect[0].charge() != TightMuonVect[1].charge() ){
      
      if(Verbose){std::cout <<" has opposite charge tight 0th muon and 1th muon "<< std::endl;}

      //fakemet test, computed from the selected tight leptons
      float fk = createFakeMETpt_m(TightMuonVect,MET);
      if(Verbose){std::cout<<"Calculated FakeMET (from member function) = "<<fk<<std::endl;}
      if (fk < 100) {if(Verbose) std::cout<<"EXIT :fakemet < 100 GeV"<<std::endl; return;}
      
      float mZpt = (TightMuonVect[0].p4() + TightMuonVect[1].p4()).pt();
      float mZmass = (TightMuonVect[0].p4() + TightMuonVect[1].p4()).mass();

      if (Verbose){
	std::cout<<"The Calculated Zmass = "<<mZmass<<std::endl;
      }
      
      if(mZmass > 70. && mZmass < 110. && mZpt > maxZpt){if(Verbose) std::cout<<"Its a Z Control Region"<<std::endl; isZCR=true;}

      theV.addDaughter(TightMuonVect.at(0));
      theV.addDaughter(TightMuonVect.at(1));
      addP4.set(theV);

      if (Verbose){std::cout<<"The Reconstructed V mass = "<<theV.mass()<<std::endl;}
      
      Fakemet= fk;
      Zpt = mZpt;
      Zmass = mZmass;
      nPVZ = thePileupAnalyzer->GetPV(iEvent);
      
      // SF
      if(isMC) {                
      /// FIXME -> APPLYING THE SF FOR Mu45eta2p1 HADRCODED <- FIXME ///
	LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFMu45eta2p1(TightMuonVect.at(0)); //include lepton trigger weight
	LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFIsoMu22(TightMuonVect.at(0)); //added

	LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(TightMuonVect.at(0));
	LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(TightMuonVect.at(1));
	
	//0: tracker high pt muon id, 1: loose, 2: medium, 3: tight, 4: high pt 
	//0: trk iso (<0.1), 1: loose (<0.25), 2: tight (<0.15) (pfIso in cone 0.4)
	LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(TightMuonVect.at(0), 3);
	LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(TightMuonVect.at(1), 3);
	LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(TightMuonVect.at(0), 2);
	LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(TightMuonVect.at(1), 2);
      }
    }
    else {if(Verbose) std::cout<< "EXIT - has NO opposite charge tight 0th muon and 1th muon" <<std::endl; return; }
  }
  else if(isZtoEE) {
    if(Verbose) std::cout << " - Try to reconstruct Z -> ee" << std::endl;
   
    float maxZpt(-1.);

    if ( TightElecVect[0].charge() != TightElecVect[1].charge() ){

      if(Verbose) std::cout <<" has opposite charge tight 0th electron and 1th electron "<< std::endl;
      //fakemet test, computed from the selected tight leptons                                                                                           
      float fk = createFakeMETpt_e(TightElecVect, MET );
      if(Verbose){std::cout<<"Calculated FakeMET = "<<fk<<std::endl;}
      if (fk < 100) {if(Verbose) std::cout<<"EXIT :fakemet < 100 GeV"<<std::endl; return;}

      float mZpt = (TightElecVect[0].p4() + TightElecVect[1].p4()).pt();
      float mZmass = (TightElecVect[0].p4() + TightElecVect[1].p4()).mass();

      if (Verbose){
	std::cout<<"The Calculated Zmass = "<<mZmass<<std::endl;
      }

      if(mZmass > 70. && mZmass < 110. && mZpt > maxZpt){if(Verbose) std::cout<<"Its a Z Control Region"<<std::endl;isZCR=true;}
      
      theV.addDaughter(TightElecVect.at(0));
      theV.addDaughter(TightElecVect.at(1));
      addP4.set(theV);
      
      if (Verbose){std::cout<<"The Reconstructed V mass = "<<theV.mass()<<std::endl;}
      
      Fakemet= fk;
      Zpt = mZpt;
      Zmass = mZmass;
      nPVZ = thePileupAnalyzer->GetPV(iEvent);

      // SF
      if(isMC) {
	/// FIXME -> APPLYING THE SF FOR Ele105 HADRCODED <- FIXME ///
	//LeptonWeight *= theElectronAnalyzer->GetElectronTriggerSFEle105(TightElecVect.at(0));
	
	//0: veto, 1: loose, 2: medium, 3: tight, 4: HEEP, 5: MVA medium nonTrig, 6: MVA tight nonTrig, 7: MVA medium Trig, 8: MVA tight Trig
	LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(TightElecVect.at(0), 3);
        LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(TightElecVect.at(1), 3);
  
	LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(TightElecVect.at(0));
	LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(TightElecVect.at(1));
      }
    }
    else { if(Verbose) std::cout << "EXIT : has NO opposite charge tight 0th electron and 1th electron" << std::endl; return; }
  }
  else if(isTtoEM) {
    if(Verbose) std::cout << " - Try to reconstruct TT -> enmn" << std::endl;
    
    if (TightElecVect[0].charge() != -(TightMuonVect[1].charge())){
      if(Verbose) std::cout << "TT has one tight electron and tight muon with opposite sign" << std::endl;
      pat::MET* fakemet = MET.clone();
      float px = MET.px() + (TightElecVect[0].p4() + TightMuonVect[0].p4()).px();
      float py = MET.py() + (TightElecVect[0].p4() + TightMuonVect[0].p4()).py();
      
      fakemet->setP4(reco::Particle::LorentzVector(px, py, 0, sqrt(px*px + py*py)));

      if(Verbose){std::cout<<"Calculated FakeMET = "<<fakemet->pt()<<std::endl;}
      if (fakemet->pt() < 100) {if(Verbose) std::cout<<"EXIT :fakemet < 100 GeV"<<std::endl; return;}
      
      Fakemet= fakemet->pt();
      isTCR=true;
      
      theV.addDaughter(TightMuonVect.at(0));
      theV.addDaughter(TightElecVect.at(0));
      addP4.set(theV);

      if (Verbose){
	std::cout<<"The Reconstructed V mass = "<<theV.mass()<<std::endl;
      }
      
      if(isMC){
	//Muon
	//ADD TRIGGER SF                                                                                                                              
	LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFMu45eta2p1(TightMuonVect.at(0));
	LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFIsoMu22(TightMuonVect.at(0)); //added

	LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(TightMuonVect.at(0));

	//0: tracker high pt muon id, 1: loose, 2: medium, 3: tight, 4: high pt                                          
	//0: trk iso (<0.1), 1: loose (<0.25), 2: tight (<0.15) (pfIso in cone 0.4)
	LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(TightMuonVect.at(0), 3);
	LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(TightMuonVect.at(0), 2);

	//Electron
	//ADD TRIGGER SF                                                                                                                   
	//LeptonWeight *= theElectronAnalyzer->GetElectronTriggerSFEle105(TightElecVect.at(0));

	//0: veto, 1: loose, 2: medium, 3: tight, 4: HEEP, 5: MVA medium nonTrig, 6: MVA tight nonTrig, 7: MVA medium Trig, 8: MVA tight Trig
	LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(TightElecVect.at(0), 3);
	LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(TightElecVect.at(0));

      }
      
    }
    else{if(Verbose) std::cout << "EXIT : has NO opposite sign in tight electrons and tight muons" << std::endl; return;}
 
  }
  else if(isWtoMN) {
    if(Verbose) std::cout << " - Try to reconstruct W -> mn" << std::endl;

    float fk = createFakeMETpt_m(TightMuonVect,MET);

    if(Verbose){std::cout<<"Calculated FakeMET = "<<fk<<std::endl;}
    if (fk < 100) {if(Verbose) std::cout<<"EXIT :fakemet < 100 GeV"<<std::endl; return;}

    float W_mT = sqrt(2.*TightMuonVect.at(0).et()*MET.pt()*(1.-cos(deltaPhi(TightMuonVect.at(0).phi(),MET.phi()))));

    if (Verbose){
      std::cout<<"The Calculated W Transverse Mass = "<<W_mT<<std::endl;
    }
    
    //question, should we save it??
    if(W_mT > 50. && W_mT < 160. ){if(Verbose) std::cout<<"Its a W Control Region"<<std::endl; isWCR=true;}
    
    theV.addDaughter(TightMuonVect.at(0));
    theV.addDaughter(MET);
    addP4.set(theV);
    
    Fakemet= fk;
    Wmass = W_mT;
    nPVW = thePileupAnalyzer->GetPV(iEvent);
    
    // SF
    if(isMC) {
      
      //ADD TRIGGER SF
      LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFMu45eta2p1(TightMuonVect.at(0)); 
      LeptonWeight *= theMuonAnalyzer->GetMuonTriggerSFIsoMu22(TightMuonVect.at(0)); //added
      
      LeptonWeight *= theMuonAnalyzer->GetMuonTrkSF(TightMuonVect.at(0));
      
      //0: tracker high pt muon id, 1: loose, 2: medium, 3: tight, 4: high pt                                                                               
      //0: trk iso (<0.1), 1: loose (<0.25), 2: tight (<0.15) (pfIso in cone 0.4)
      LeptonWeight *= theMuonAnalyzer->GetMuonIdSF(TightMuonVect.at(0), 3);
      LeptonWeight *= theMuonAnalyzer->GetMuonIsoSF(TightMuonVect.at(0), 2);
    }

  }
  else if(isWtoEN) {
    if(Verbose) std::cout << " - Try to reconstruct W -> en" << std::endl;

    float fk = createFakeMETpt_e(TightElecVect,MET);

    if(Verbose){std::cout<<"Calculated FakeMET = "<<fk<<std::endl;}
    if (fk < 100) {if(Verbose) std::cout<<"EXIT :fakemet < 100 GeV"<<std::endl; return;}

    float W_mT = sqrt(2.*TightElecVect.at(0).et()*MET.pt()*(1.-cos(deltaPhi(TightElecVect.at(0).phi(),MET.phi()))));

    if (Verbose){
      std::cout<<"The Calculated W Transverse Mass = "<<W_mT<<std::endl;
    }
    
    if(W_mT > 50. && W_mT < 160. ){if(Verbose) std::cout<<"Its a W Control Region"<<std::endl; isWCR=true;}
      
    theV.addDaughter(TightElecVect.at(0));
    theV.addDaughter(MET);
    addP4.set(theV);
    
    Fakemet= fk;
    nPVZ = thePileupAnalyzer->GetPV(iEvent);
    Wmass = W_mT;
    
    // SF
    if(isMC) {
      //ADD TRIGGER SF
      //LeptonWeight *= theElectronAnalyzer->GetElectronTriggerSFEle105(TightElecVect.at(0));
      
      //0: veto, 1: loose, 2: medium, 3: tight, 4: HEEP, 5: MVA medium nonTrig, 6: MVA tight nonTrig, 7: MVA medium Trig, 8: MVA tight Trig  
      LeptonWeight *= theElectronAnalyzer->GetElectronIdSF(TightElecVect.at(0), 3);
      LeptonWeight *= theElectronAnalyzer->GetElectronRecoEffSF(TightElecVect.at(0));
    }
    
  }
  else if(isZtoNN) {
    if(Verbose) std::cout << " - Try to reconstruct Z -> nn" << std::endl;
    if(Verbose){std::cout<<"Type-1 MET pt in signal region (0 leptons) = "<<MET.pt()<<std::endl;}
    if(MET.pt() < 100){if(Verbose)std::cout<<"EXIT : MET < 100 GeV"<<std::endl;return;}
    theV.addDaughter(MET);
    addP4.set(theV);
    isSR=true; //signal region flagged!
    SR_counter++;
  }
  
  else { if(Verbose) std::cout << "EXIT - No reconstructible V candidate / or none of the event enter CR" << std::endl; return; }

  if (Verbose) {
    std::cout<<std::endl;
    std::cout<<"***********************************************************"<<std::endl;
  }

  // Update event weight with lepton selections
  EventWeight *= LeptonWeight;
  
  Hist["a_PrenEvents"]->Fill(7., EventWeight); //Reconstructed V candidate

  Hist["a_nEvents"]->Fill(4., EventWeight);
  Hist["m_nEvents"]->Fill(9., EventWeight);
  if(isZtoEE) Hist["e_nEvents"]->Fill(4., EventWeight);
  if(isZtoMM) Hist["m_nEvents"]->Fill(4., EventWeight);
  
  if(isZtoEE) {
    Hist["e_Zmass"]->Fill(theV.mass(), EventWeight);
    if(TightElecVect.at(0).isEB() && TightElecVect.at(1).isEB()) Hist["e_ZmassBB"]->Fill(theV.mass(), EventWeight);
    if(TightElecVect.at(0).isEE() && TightElecVect.at(1).isEB()) Hist["e_ZmassEB"]->Fill(theV.mass(), EventWeight);
    if(TightElecVect.at(0).isEB() && TightElecVect.at(1).isEE()) Hist["e_ZmassBE"]->Fill(theV.mass(), EventWeight);
    if(TightElecVect.at(0).isEE() && TightElecVect.at(1).isEE()) Hist["e_ZmassEE"]->Fill(theV.mass(), EventWeight);
  }
  if(isZtoMM) {
    Hist["m_Zmass"]->Fill(theV.mass(), EventWeight);
    if(abs(TightMuonVect.at(0).eta())<1.1 && abs(TightMuonVect.at(1).eta())<1.1) Hist["m_ZmassBB"]->Fill(theV.mass(), EventWeight);
    if(abs(TightMuonVect.at(0).eta())>1.1 && abs(TightMuonVect.at(1).eta())<1.1) Hist["m_ZmassEB"]->Fill(theV.mass(), EventWeight);
    if(abs(TightMuonVect.at(0).eta())<1.1 && abs(TightMuonVect.at(1).eta())>1.1) Hist["m_ZmassBE"]->Fill(theV.mass(), EventWeight);
    if(abs(TightMuonVect.at(0).eta())>1.1 && abs(TightMuonVect.at(1).eta())>1.1) Hist["m_ZmassEE"]->Fill(theV.mass(), EventWeight);
  }
  
  if(Verbose) std::cout << " - Candidate built" << std::endl;
  
  // ---------- Event Variables ----------
  
  // Max b-tagged jet in the event
  for(unsigned int i = 2; i < JetsVect.size(); i++) if(JetsVect[i].bDiscriminator(JetPSet.getParameter<std::string>("btag")) > MaxJetBTag) MaxJetBTag = JetsVect[i].bDiscriminator(JetPSet.getParameter<std::string>("btag"));
  
  for(unsigned int i = 0; i < JetsVect.size(); i++) if(fabs(reco::deltaPhi(JetsVect[i].phi(), MET.phi())) < MinJetMetDPhi) MinJetMetDPhi = fabs(reco::deltaPhi(JetsVect[i].phi(), MET.phi()));
  
  // Jet variables
  theJetAnalyzer->AddVariables(JetsVect, MET);
  theElectronAnalyzer->AddVariables(TightElecVect, MET);
  theMuonAnalyzer->AddVariables(TightMuonVect, MET);
  
  // ---------- Print Summary ----------
  if(Verbose) {
    std::cout<<std::endl;
    std::cout<<" ----- Print Summary ----- "<<std::endl;
    //std::cout << " --- Event n. " << iEvent.id().event() << ", lumi " << iEvent.luminosityBlock() << ", run " << iEvent.id().run() << ", weight " << EventWeight << std::endl;

    std::cout << "number of Tight electrons: " << TightElecVect.size() << std::endl;
    for(unsigned int i = 0; i < TightElecVect.size(); i++) std::cout << "  electron [" << i << "]\tpt: " << TightElecVect[i].pt() << "\teta: " << TightElecVect[i].eta() << "\tphi: " << TightElecVect[i].phi() << "\tmass: " << TightElecVect[i].mass() << "\tcharge: " << TightElecVect[i].charge() << std::endl;

    std::cout << "number of Tight muons:     " << TightMuonVect.size() << std::endl;
    for(unsigned int i = 0; i < TightMuonVect.size(); i++) std::cout << "  muon     [" << i << "]\tpt: " << TightMuonVect[i].pt() << "\teta: " << TightMuonVect[i].eta() << "\tphi: " << TightMuonVect[i].phi() << "\tmass: " << TightMuonVect[i].mass() << "\tcharge: " << TightMuonVect[i].charge() << std::endl;

    std::cout << "number of taus:  " << TauVect.size() << std::endl;
    for(unsigned int i = 0; i < TauVect.size(); i++) std::cout << "  tau  [" << i << "]\tpt: " << TauVect[i].pt() << "\teta: " << TauVect[i].eta() << "\tphi: " << TauVect[i].phi() << std::endl;

    std::cout << "number of photons:  " << PhotonVect.size() << std::endl;
    for(unsigned int i = 0; i < PhotonVect.size(); i++) std::cout << "  photon  [" << i << "]\tpt: " << PhotonVect[i].pt() << "\teta: " << PhotonVect[i].eta() << "\tphi: " << PhotonVect[i].phi() << std::endl;

    std::cout << "number of AK4 jets:  " << JetsVect.size() << std::endl;    
    for(unsigned int i = 0; i < JetsVect.size(); i++) std::cout << "  AK4 jet  [" << i << "]\tpt: " << JetsVect[i].pt() << "\teta: " << JetsVect[i].eta() << "\tphi: " << JetsVect[i].phi() << "\tmass: " << JetsVect[i].mass() << "\tBtag" <<JetsVect[i].bDiscriminator(JetPSet.getParameter<std::string>("btag")) << std::endl;

    std::cout << "Missing energy:      " << MET.pt() << std::endl;
    std::cout << "V leptonic mass:     " << theV.mass() << std::endl;
    std::cout<<std::endl;
  }
  
  
  // ---------- Fill objects ----------
  if(Verbose) std::cout << " - Filling objects" << std::endl;
  
  //** saving only the tight lepton.
  if(isZtoEE || isWtoEN) 
    for(unsigned int i = 0; i < Leptons.size() && i < TightElecVect.size(); i++) ObjectsFormat::FillElectronType(Leptons[i], &TightElecVect[i], isMC);
  else if(isZtoMM || isWtoMN) 
    for(unsigned int i = 0; i < Leptons.size() && i < TightMuonVect.size(); i++) ObjectsFormat::FillMuonType(Leptons[i], &TightMuonVect[i], isMC);
  else if(isTtoEM && Leptons.size() >= 2) {
    if(TightElecVect[0].pt() > TightMuonVect[0].pt()) {
      ObjectsFormat::FillElectronType(Leptons[0], &TightElecVect[0], isMC);
      ObjectsFormat::FillMuonType(Leptons[1], &TightMuonVect[0], isMC);
    }
    else {
      ObjectsFormat::FillMuonType(Leptons[0], &TightMuonVect[0], isMC);
      ObjectsFormat::FillElectronType(Leptons[1], &TightElecVect[0], isMC);
    }
  }
 
  for(unsigned int i = 0; i < Taus.size() && i < TauVect.size(); i++) ObjectsFormat::FillTauType(Taus[i], &TauVect[i], isMC);
  for(unsigned int i = 0; i < Photons.size() && i < PhotonVect.size(); i++) ObjectsFormat::FillPhotonType(Photons[i], &PhotonVect[i], isMC);
  for(unsigned int i = 0; i < Jets.size() && i < JetsVect.size(); i++) ObjectsFormat::FillJetType(Jets[i], &JetsVect[i], isMC);
  
  ObjectsFormat::FillMEtType(MEt, &MET, isMC);
  ObjectsFormat::FillCandidateType(V, &theV, isMC); // V is the reconstructed boson

  if ( (isZtoEE || isZtoMM) && isZCR ) ZCR_counter++;
  if ( (isWtoEN || isWtoMN) && isWCR ) WCR_counter++;
  if ( isTtoEM && isTCR ) TCR_counter++;

  //checking overlapping of flag state
  if (isSR && isZtoNN){if(isZtoEE || isZtoMM || isWtoEN || isWtoMN || isTtoEM) if(Verbose)std::cout<<"EXIT = TROUBLE, SR overlap with CR"<<std::endl;}
  if (isWtoEN && isWtoMN){if(Verbose)std::cout<<"WCR conflict"<<std::endl;}
  if (isZtoEE && isZtoMM){if(Verbose)std::cout<<"ZCR conflict"<<std::endl;}
  if ( (isWtoEN || isWtoMN) && (isZtoEE || isZtoMM) ){if(Verbose)std::cout<<"WCR and ZCR overlap"<<std::endl;}
  if ( ( (isZtoEE || isZtoMM) || (isWtoEN || isWtoMN) ) && isTCR ){if(Verbose)std::cout<<"WCR and ZCR overlap TCR"<<std::endl;}

  
  if (Verbose){

    std::cout<<"==========================================================="<<std::endl;
    std::cout<<"Inspecting all the flag state"<<std::endl;
    std::cout<<"==========================================================="<<std::endl;
    std::cout<<"isZtoEE = "<<isZtoEE<<std::endl;
    std::cout<<"isZtoMM = "<<isZtoMM<<std::endl;
    std::cout<<"isTtoEM = "<<isTtoEM<<std::endl;
    std::cout<<"isWtoEN = "<<isWtoEN<<std::endl;
    std::cout<<"isWtoMN = "<<isWtoMN<<std::endl;
    std::cout<<"isZtoNN = "<<isZtoNN<<std::endl;
    std::cout<<"isSR = "<<isSR<<std::endl;
    std::cout<<"isSR1 = "<<isSR1<<std::endl;
    std::cout<<"isSR2 = "<<isSR2<<std::endl;
    std::cout<<"isZCR = "<<isZCR<<std::endl;
    std::cout<<"isWCR = "<<isWCR<<std::endl;
    std::cout<<"isTCR = "<<isTCR<<std::endl;
    std::cout<<"==========================================================="<<std::endl;
    std::cout<<std::endl;
  }
  
  // Fill tree
  tree->Fill();
  
}


// ------------ method called once each job just before starting event loop  ------------
void 
Dibottom::beginJob()
{
  
  // Object objects are created only one in the begin job. The reference passed to the branch has to be the same
  for(int i = 0; i < WriteNElectrons; i++) Electrons.push_back( LeptonType() );
  for(int i = 0; i < WriteNMuons; i++) Muons.push_back( LeptonType() );
  for(int i = 0; i < WriteNLeptons; i++) Leptons.push_back( LeptonType() );
  for(int i = 0; i < WriteNTaus; i++) Taus.push_back( TauType() );
  for(int i = 0; i < WriteNPhotons; i++) Photons.push_back( PhotonType() );
  for(int i = 0; i < WriteNJets; i++) Jets.push_back( JetType() );
  
  // Create Tree and set Branches
  //Global
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
  tree->Branch("isSR", &isSR, "isSR/O");
  tree->Branch("isSR1", &isSR1, "isSR1/O");
  tree->Branch("isSR2", &isSR2, "isSR2/O");
  tree->Branch("isZCR", &isZCR, "isZCR/O");
  tree->Branch("isWCR", &isWCR, "isWCR/O");
  tree->Branch("isTCR", &isTCR, "isTCR/O");
  //added
  tree->Branch("Fakemet", &Fakemet, "Fakemet/F");
  tree->Branch("Zpt", &Zpt, "Zpt/F");
  tree->Branch("Zmass", &Zmass, "Zmass/F");
  tree->Branch("Zeta", &Zeta, "Zeta/F");
  tree->Branch("nPVZ", &nPVZ, "nPVZ/I");

  tree->Branch("Wpt", &Wpt, "Wpt/F");
  tree->Branch("Wmass", &Wmass, "Wmass/F");
  tree->Branch("Weta", &Weta, "Weta/F");
  tree->Branch("nPVW", &nPVW, "nPVW/I");
  
  tree->Branch("nPV", &nPV, "nPV/I");
  tree->Branch("nElectrons", &nElectrons, "nElectrons/I");
  tree->Branch("nMuons", &nMuons, "nMuons/I");
  tree->Branch("nTightElectrons", &nTightElectrons, "nTightElectrons/I");
  tree->Branch("nTightMuons", &nTightMuons, "nTightMuons/I");
  tree->Branch("nTaus", &nTaus, "nTaus/I");
  tree->Branch("nPhotons", &nPhotons, "nPhotons/I");
  tree->Branch("nJets", &nJets, "nJets/I");
  tree->Branch("nBTagJets", &nBTagJets, "nBTagJets/I");
  
  tree->Branch("MaxJetBTag", &MaxJetBTag, "MaxJetBTag/F");
  tree->Branch("MinJetMetDPhi", &MinJetMetDPhi, "MinJetMetDPhi/F");
  
  // Set Branches for objects
  for(int i = 0; i < WriteNElectrons; i++) tree->Branch(("Electron"+std::to_string(i+1)).c_str(), &(Electrons[i].pt), ObjectsFormat::ListLeptonType().c_str());
  for(int i = 0; i < WriteNMuons; i++) tree->Branch(("Muon"+std::to_string(i+1)).c_str(), &(Muons[i].pt), ObjectsFormat::ListLeptonType().c_str());
  for(int i = 0; i < WriteNLeptons; i++) tree->Branch(("Lepton"+std::to_string(i+1)).c_str(), &(Leptons[i].pt), ObjectsFormat::ListLeptonType().c_str());
  for(int i = 0; i < WriteNTaus; i++) tree->Branch(("Tau"+std::to_string(i+1)).c_str(), &(Taus[i].pt), ObjectsFormat::ListTauType().c_str());
  for(int i = 0; i < WriteNPhotons; i++) tree->Branch(("Photon"+std::to_string(i+1)).c_str(), &(Photons[i].pt), ObjectsFormat::ListPhotonType().c_str());
  for(int i = 0; i < WriteNJets; i++) tree->Branch(("Jet"+std::to_string(i+1)).c_str(), &(Jets[i].pt), ObjectsFormat::ListJetType().c_str());
  
  tree->Branch("MEt", &MEt.pt, ObjectsFormat::ListMEtType().c_str());
  tree->Branch("V", &V.pt, ObjectsFormat::ListCandidateType().c_str());

  //tree declaration for catagorization
  users=fs->make<TTree>("users","users");
  users->Branch("SR_counter", &SR_counter , "SR_counter/I");
  users->Branch("ZCR_counter", &ZCR_counter , "ZCR_counter/I");
  users->Branch("WCR_counter", &WCR_counter , "WCR_counter/I");
  users->Branch("TCR_counter", &ZCR_counter , "TCR_counter/I");
  users->Branch("Preselected_counter", &Preselected_counter , "Preselected_counter/I");

}

// ------------ method called once each job just after ending the event loop  ------------
void 
Dibottom::endJob() 
{
  users->Fill();
  if (Verbose){
    std::cout<<"**************** Internal Variables *********************"<<std::endl;
    std::cout<<"Total number of event = "<<nevent<<std::endl;
    std::cout<<"Total number of preselected event = "<<Preselected_counter<<std::endl;
    std::cout<<"Total number of event entering SR = "<<SR_counter<<std::endl;
    std::cout<<"Total number of event entering ZCR = "<<ZCR_counter<<std::endl;
    std::cout<<"Total number of event entering WCR = "<<WCR_counter<<std::endl;
    std::cout<<"Total number of event entring TCR = "<<TCR_counter<<std::endl;
  }
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
Dibottom::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Dibottom);
