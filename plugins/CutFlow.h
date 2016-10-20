// system include files                                                                                                                                 

#include <memory>

// user include files                                                                                                                                        
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//added header
//#include <sstream>
//#include <iomanip>
//#include <vector>

//#include <unordered_map>
//using std::unordered_map;
//root
#include "TTree.h"
#include "TVector3.h"
#include "TFile.h"
#include "TF1.h"
#include "TEnv.h"
#include "TString.h"
#include "TStopwatch.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2D.h"

//#include "/lustre/cmswork/hoh/CMSSW_8_0_12/src/Analysis/ALPHA/plugins/Dibottom.h"

// class declaration 

class CutFlow : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
 public:
  explicit CutFlow(const edm::ParameterSet&);
  ~CutFlow();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


 private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  // ----------member data ---------------------------                                                                                              

};

//                                                                                                                                                           
// constants, enums and typedefs                                                                                                                  
//                                                                                                                                                   
 
//                                                                                                                                                           
// static data member definitions                                                                                                                            
//                                                        


