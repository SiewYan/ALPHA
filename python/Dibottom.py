import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import os

options = VarParsing ('analysis')
options.parseArguments()

# Determine sample name for MC stitching
sample = (options.inputFiles[0]).split('/')[-1].replace('.txt', '') if len(options.inputFiles) > 0 else ''
if sample=='list': sample = (options.inputFiles[0]).split('/')[-3]

process = cms.Process('ALPHA')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.threshold = 'ERROR'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# input
# default: if no filelist from command line, run on specified samples

if len(options.inputFiles) == 0:
    process.source = cms.Source('PoolSource',
        fileNames = cms.untracked.vstring(
        	#'root://cmsxrootd.fnal.gov//store/mc/RunIISpring16MiniAODv2/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/10000/AC51B7C5-7829-E611-AF89-6CC2173DA9E0.root',
        	'root://cmsxrootd.fnal.gov//store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/275/001/00000/E8366493-E034-E611-8A7E-02163E0146AE.root'
        )
    )
# production: read externally provided filelist
else:
    filelist = open(options.inputFiles[0], 'r').readlines()
    process.source = cms.Source ('PoolSource', fileNames = cms.untracked.vstring(filelist) )

#output
process.TFileService = cms.Service('TFileService',
    fileName = cms.string('output.root' if len(options.outputFile) == 0 else options.outputFile),
    closeFileFast = cms.untracked.bool(True)
)

# Determine whether we are running on data or MC
isData = ('/store/data/' in process.source.fileNames[0])
isCustom = ('GluGluToAToZhToLLBB' in process.source.fileNames[0])
isReHLT = ('_reHLT_' in process.source.fileNames[0])
print 'Running on', ('data' if isData else 'MC'), ', sample is', (
	'Default dataset' if len(options.inputFiles) == 0 else sample)
if isReHLT: print '-> re-HLT sample'
#isData = False
######################
# Filter
# EDMAnalyzer
# Ntupler

#-----------------------#
#        FILTERS        #
#-----------------------#

# JSON filter
import FWCore.PythonUtilities.LumiList as LumiList
if isData:
    #process.source.lumisToProcess = LumiList.LumiList(filename = '%s/src/Analysis/ALPHA/data/JSON/Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt' % os.environ['CMSSW_BASE']).getVLuminosityBlockRange() #4.34
    process.source.lumisToProcess = LumiList.LumiList(filename = '%s/src/Analysis/ALPHA/data/JSON/Cert_271036-275783_13TeV_PromptReco_Collisions16_JSON.txt' % os.environ['CMSSW_BASE']).getVLuminosityBlockRange() #6.26


process.counter = cms.EDAnalyzer('CounterAnalyzer',
    lheProduct = cms.InputTag('externalLHEProducer' if not isCustom else 'source'),
)

# Trigger filter
import HLTrigger.HLTfilters.hltHighLevel_cfi
triggerTag = 'HLT2' if isReHLT else 'HLT'
process.HLTFilter = cms.EDFilter('HLTHighLevel',
    TriggerResultsTag = cms.InputTag('TriggerResults', '', triggerTag),
    HLTPaths = cms.vstring(
        #'HLT_Mu45_eta2p1_v*',
        #'HLT_Mu50_v*',
        #'HLT_TkMu50_v*',
        'HLT_IsoMu20_v*',
        'HLT_IsoTkMu20_v*',
        #'HLT_IsoMu24_v*',
        #'HLT_IsoTkMu24_v*',
        #'HLT_Mu27_TkMu8_v*',
        #'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*',
        #'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*',
        #'HLT_Ele105_CaloIdVT_GsfTrkIdT_v*',
        #'HLT_Ele115_CaloIdVT_GsfTrkIdT_v*',
        'HLT_Ele23_WPLoose_Gsf_v*',
        'HLT_Ele27_WPLoose_Gsf_v*',
        #'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*',
        #'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v*',
        'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*',
        'HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v*',
        'HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v*',
        'HLT_PFMET120_BTagCSV_p067_v*',
        'HLT_PFMET170_NoiseCleaned_v*',
        #'HLT_DoublePhoton60_v*',
    ),
    eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key
    andOr = cms.bool(True),    # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
    throw = cms.bool(False)    # throw exception on unknown path names
)

#process.load('RecoMET.METFilters.metFilters_cff')

process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.BadPFMuonFilter.muons = cms.InputTag('slimmedMuons')
process.BadPFMuonFilter.PFCandidates = cms.InputTag('packedPFCandidates')

process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.BadChargedCandidateFilter.muons = cms.InputTag('slimmedMuons')
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag('packedPFCandidates')

process.METFilter = cms.EDFilter('HLTHighLevel',
    TriggerResultsTag = cms.InputTag('TriggerResults', '', 'RECO'),
    HLTPaths = cms.vstring(
        #'Flag_HBHENoiseFilter',
        'Flag_HBHENoiseIsoFilter',
        #'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_goodVertices',
        'Flag_eeBadScFilter',
        #'Flag_globalTightHalo2016Filter',
    ),
    eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key
    andOr = cms.bool(True),    # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
    throw = cms.bool(False)    # throw exception on unknown path names
)

# Primary vertex
import RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi
process.primaryVertexFilter = cms.EDFilter('GoodVertexFilter',
    vertexCollection = cms.InputTag('offlineSlimmedPrimaryVertices'),
    minimumNDOF = cms.uint32(4) ,
    maxAbsZ = cms.double(24), 
    maxd0 = cms.double(2) 
)

#-----------------------#
#        OBJECTS        #
#-----------------------#

#electrons upstream modules
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
ele_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',
                 'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff',
                 'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',
                 'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff']
for ele_idmod in ele_id_modules:
    setupAllVIDIdsInModule(process,ele_idmod,setupVIDElectronSelection)

######################
if isData:
    process.seq = cms.Sequence(
        process.counter *
        process.HLTFilter *

        process.METFilter *
        process.BadPFMuonFilter *
        process.BadChargedCandidateFilter
        
#        process.primaryVertexFilter *
#        process.egmGsfElectronIDSequence *
#        process.calibratedPatElectrons *
#        process.egmPhotonIDSequence *
#        process.cleanedMuons *
#        process.ak4PFL2L3ResidualCorrectorChain *
#        process.QGTagger *
#        process.ntuple
    )
else:
    process.seq = cms.Sequence(
        process.counter *

        process.BadPFMuonFilter *
        process.BadChargedCandidateFilter
        
#        process.primaryVertexFilter *
#        process.egmGsfElectronIDSequence *
#        process.calibratedPatElectrons *
#        process.egmPhotonIDSequence *
#        process.cleanedMuons *
#        process.ak4PFL2L3ResidualCorrectorChain *
#        process.QGTagger *
#        process.ntuple
    )

process.p = cms.Path(process.seq)