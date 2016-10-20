// -*- C++ -*-
//
// Package:    Analysis/dibottom
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
#ifndef DIBOTTOM_H
#define DIBOTTOM_H

// system include files
#include <memory>
#include <utility>
#include <algorithm>
#include <math.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"

// Consumes
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

// miniAOD
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
// Pat
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/PatCandidates/interface/Conversion.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"
#include "DataFormats/PatCandidates/interface/PFParticle.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "PhysicsTools/CandUtils/interface/EventShapeVariables.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
// Vertex
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
// PU
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
// Trigger
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
// Gen Info
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHECommonBlocks.h"
// dR and dPhi
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "TTree.h"
#include "TH2.h"
#include "TH1.h"

#include "Objects.h"
#include "ObjectsFormat.h"
#include "GenAnalyzer.h"
#include "PileupAnalyzer.h"
#include "TriggerAnalyzer.h"
#include "ElectronAnalyzer.h"
#include "MuonAnalyzer.h"
#include "TauAnalyzer.h"
#include "PhotonAnalyzer.h"
#include "TauAnalyzer.h"
#include "JetAnalyzer.h"
//#include "BTagInterface.h"
#include "Utilities.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class Dibottom : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit Dibottom(const edm::ParameterSet&);
  ~Dibottom();
  
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  float createFakeMETpt_e(std::vector<pat::Electron>& el, pat::MET& met);
  float createFakeMETpt_m(std::vector<pat::Muon>& mu, pat::MET& met);
  
private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;
  
  // ----------member data ---------------------------
  
  edm::ParameterSet GenPSet;
  edm::ParameterSet PileupPSet;
  edm::ParameterSet TriggerPSet;
  edm::ParameterSet ElectronPSet;
  edm::ParameterSet MuonPSet;
  edm::ParameterSet TauPSet;
  edm::ParameterSet PhotonPSet;
  edm::ParameterSet JetPSet;
  //std::string BTagAlgo;        
  boost::shared_ptr<FactorizedJetCorrector> jecAK8_;
  
  int WriteNElectrons, WriteNMuons, WriteNLeptons, WriteNTaus, WriteNPhotons, WriteNJets; 
  
  std::string HistFile;
  bool Verbose;
  
  GenAnalyzer* theGenAnalyzer;
  PileupAnalyzer* thePileupAnalyzer;
  TriggerAnalyzer* theTriggerAnalyzer;
  ElectronAnalyzer* theElectronAnalyzer;
  MuonAnalyzer* theMuonAnalyzer;
  TauAnalyzer* theTauAnalyzer;
  PhotonAnalyzer* thePhotonAnalyzer;
  JetAnalyzer* theJetAnalyzer;
  //BTagInterface* theBTagAnalyzer;
  
  std::map<std::string, bool> TriggerMap;
  std::map<std::string, TH1F*> Hist;
  
  edm::Service<TFileService> fs;
  TTree* tree;
  
  bool isMC, isZtoEE, isZtoMM, isTtoEM, isWtoEN, isWtoMN, isZtoNN;
  long int EventNumber, RunNumber, LumiNumber;
  float EventWeight, StitchWeight, ZewkWeight, WewkWeight, PUWeight, TriggerWeight, LeptonWeight;
  float FacWeightUp, FacWeightDown, RenWeightUp, RenWeightDown, ScaleWeightUp, ScaleWeightDown;
  int nPV, nElectrons, nMuons, nTaus, nPhotons, nJets, nBTagJets;
  int nTightElectrons, nTightMuons;
  float MaxJetBTag, MinJetMetDPhi, Chi2;
  
  //Objects declared in Objects.h (constum struct type)
  std::vector<LeptonType> Electrons;
  std::vector<LeptonType> Muons;
  std::vector<LeptonType> Leptons;
  std::vector<TauType> Taus;
  std::vector<PhotonType> Photons;
  std::vector<JetType> Jets;
  
  MEtType MEt;
  CandidateType V;
  
  int nevent;
  bool isSR, isZCR, isWCR, isTCR;
  bool isSR1, isSR2;

  //TTree* SR;
  //TTree* ZCR;
  //TTree* WCR;
  //TTree* TCR;

  TTree* users;

  //user variable
  float Fakemet;
  float Zpt;
  float Zmass;
  float Zeta;
  int nPVZ;

  float Wpt;
  float Wmass;
  float Weta;
  int nPVW;
  
  int SR_counter,SR1_counter,SR2_counter,ZCR_counter,WCR_counter,TCR_counter,Preselected_counter;

  struct JetIndexByPt{
    const Bool_t operator() (const pat::Jet& j1, const pat::Jet& j2) {return ( (j1.pt()) > (j2.pt()) );}
  };

  struct MuonIndexByPt{
    const Bool_t operator() (const pat::Muon& m1, const pat::Muon& m2) {return ( (m1.pt()) > (m2.pt()) );}
  };

  struct ElecIndexByPt{
    const Bool_t operator() (const pat::Electron& e1, const pat::Electron& e2) {return ( (e1.pt()) > (e2.pt()) );}
  };

  JetIndexByPt jetComparator;  
  MuonIndexByPt muonComparator;
  ElecIndexByPt elecComparator;
  
};

#endif
