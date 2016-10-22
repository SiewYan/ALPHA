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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

# input
# default: if no filelist from command line, run on specified samples

if len(options.inputFiles) == 0:
    process.source = cms.Source('PoolSource',
        fileNames = cms.untracked.vstring(
            #DYJetsToLL
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/00000/10D44CB0-4E1A-E611-8EDF-0CC47A4F1D16.root',
            #ZJetsToNuNu
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/ZJetsToNuNu_HT-100To200_13TeV-madgraph/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/20000/04AC8065-D533-E611-B38A-0026B92785F6.root',
            #WJetsToLNu
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/00000/12E2F3B2-681E-E611-BBCD-0025907DC9C4.root',
            #TTbar inclusive
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext4-v1/00000/044031F9-D528-E611-BA6E-78E7D121E458.root',
            #Single Top
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/30000/3E960D48-6A1A-E611-BC02-3417EBE7009F.root',
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/50000/6068FBF2-D21F-E611-8D69-00259073E3A0.root',
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/40000/3865EFB2-F226-E611-984D-001E673D23F9.root',
            #VV Inclusive
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/50000/3C6B0B1B-111B-E611-9977-008CFA0646D4.root',
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/60000/4EDC509B-861B-E611-B919-842B2B019EA1.root',
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/50000/3420D4BA-E21A-E611-AD91-3417EBE64B5B.root',
            #QCD
            'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring16MiniAODv2/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/70000/0CEFB979-053E-E611-8508-0025904C51F2.root',
            #MET
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/data/Run2016C/MET/MINIAOD/PromptReco-v2/000/275/657/00000/420FBE99-833B-E611-A4B6-02163E011EAB.root',
            #singleElectron
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/data/Run2016C/SingleElectron/MINIAOD/PromptReco-v2/000/275/657/00000/38744E53-893B-E611-9978-02163E011EE1.root',
            #singleMuon
            #'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/data/Run2016C/SingleMuon/MINIAOD/PromptReco-v2/000/275/657/00000/AA1E9DFA-6C3B-E611-9C0C-02163E014549.root',
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
isDibosonInclusive = (True if (sample=='WW_TuneCUETP8M1_13TeV-pythia8_v1' or sample=='WZ_TuneCUETP8M1_13TeV-pythia8_v1' or sample=='ZZ_TuneCUETP8M1_13TeV-pythia8_v1') else False)
if isDibosonInclusive: print '-> Pythia LO sample'
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
    #process.source.lumisToProcess = LumiList.LumiList(filename = '%s/src/Analysis/ALPHA/data/JSON/Cert_271036-275783_13TeV_PromptReco_Collisions16_JSON.txt' % os.environ['CMSSW_BASE']).getVLuminosityBlockRange() #6.26
    process.source.lumisToProcess = LumiList.LumiList(filename = '%s/src/Analysis/ALPHA/data/JSON/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt' % os.environ['CMSSW_BASE']).getVLuminosityBlockRange() #12.9


process.counter = cms.EDAnalyzer('CounterAnalyzer',
    lheProduct = cms.InputTag('externalLHEProducer' if not isCustom else 'source'),
    pythiaLOSample = cms.bool(True if isDibosonInclusive else False),
)

# Trigger filter
import HLTrigger.HLTfilters.hltHighLevel_cfi
triggerTag = 'HLT2' if isReHLT else 'HLT'
process.HLTFilter = cms.EDFilter('HLTHighLevel',
    TriggerResultsTag = cms.InputTag('TriggerResults', '', triggerTag),
    HLTPaths = cms.vstring(
        'HLT_Mu45_eta2p1_v*',
        'HLT_Mu50_v*',
        'HLT_TkMu50_v*',
        'HLT_IsoMu20_v*',
        'HLT_IsoTkMu20_v*',
        'HLT_IsoMu22_v*',
        'HLT_IsoTkMu22_v*',
        'HLT_IsoMu24_v*',
        'HLT_IsoTkMu24_v*',
        'HLT_Ele23_WPLoose_Gsf_v*',
        'HLT_Ele27_WPLoose_Gsf_v*',
        'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*',
        'HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v*',
        'HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v*',
        'HLT_PFMET120_BTagCSV_p067_v*',
        'HLT_PFMET170_NoiseCleaned_v*',
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
        'Flag_HBHENoiseFilter',
        'Flag_HBHENoiseIsoFilter',
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_goodVertices',
        'Flag_eeBadScFilter',
        'Flag_globalTightHalo2016Filter',
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

#photons upstream modules
switchOnVIDPhotonIdProducer(process, DataFormat.MiniAOD)
ph_id_modules = ['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring15_25ns_V1_cff',
                'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Spring15_25ns_nonTrig_V2_cff']
for ph_idmod in ph_id_modules:
    setupAllVIDIdsInModule(process,ph_idmod,setupVIDPhotonSelection)

#muons upstream modules
process.cleanedMuons = cms.EDProducer('PATMuonCleanerBySegments',
    src = cms.InputTag('slimmedMuons'),#('calibratedMuons'),
    preselection = cms.string('track.isNonnull'),
    passthrough = cms.string('isGlobalMuon && numberOfMatches >= 2'),
    fractionOfSharedSegments = cms.double(0.499)
)

# Jet corrector https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CorrOnTheFly
process.load('JetMETCorrections.Configuration.JetCorrectors_cff')


#quark gluon likelihood upstream modules
qgDatabaseVersion = 'v2b' # check https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGDataBaseVersion
from CondCore.DBCommon.CondDBSetup_cfi import *
QGPoolDBESSource = cms.ESSource('PoolDBESSource',
      CondDBSetup,
      toGet = cms.VPSet(),
      connect = cms.string('frontier://FrontierProd/CMS_COND_PAT_000'),
)
for type in ['AK4PFchs','AK4PFchs_antib']:
    QGPoolDBESSource.toGet.extend(cms.VPSet(cms.PSet(
        record = cms.string('QGLikelihoodRcd'),
        tag    = cms.string('QGLikelihoodObject_'+qgDatabaseVersion+'_'+type),
        label  = cms.untracked.string('QGL_'+type)
    )))
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets = cms.InputTag('slimmedJets') # Could be reco::PFJetCollection or pat::JetCollection (both AOD and miniAOD)
process.QGTagger.jetsLabel = cms.string('QGL_AK4PFchs') # Other options: see https://twiki.cern.ch/twiki/bin/viewauth/CMS/QGDataBaseVersion

#https://twiki.cern.ch/twiki/bin/view/CMS/EGMSmearer#ECAL_scale_and_resolution_correc
process.load('EgammaAnalysis.ElectronTools.calibratedElectronsRun2_cfi')
#process.selectedElectrons = cms.EDFilter('PATElectronSelector', 
                                         #src = cms.InputTag('slimmedElectrons'), 
                                         #cut = cms.string('pt > 5 && abs(eta)<2.5') 
                                         #)
calibratedPatElectrons = cms.EDProducer('CalibratedPatElectronProducerRun2',
                                        # input collections
                                        electrons = cms.InputTag('slimmedElectrons'),
                                        gbrForestName = cms.string('gedelectron_p4combination_25ns'),
                                        # data or MC corrections
                                        # if isMC is false, data corrections are applied
                                        isMC = cms.bool(False) if isData else cms.bool(True),
                                        # set to True to get special 'fake' smearing for synchronization. Use JUST in case of synchronization
                                        isSynchronization = cms.bool(False),
                                        correctionFile = cms.string('80X_DCS05July_plus_Golden22')
                                        )


#-----------------------#
#        NTUPLE         #
#-----------------------#

process.ntuple = cms.EDAnalyzer('Dibottom',
    genSet = cms.PSet(
        genProduct = cms.InputTag('generator'),
        lheProduct = cms.InputTag('externalLHEProducer' if not isCustom else 'source'),
        genParticles = cms.InputTag('prunedGenParticles'),
        pdgId = cms.vint32(1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 21, 23, 24, 25, 36, 39, 1000022, 9100000, 9000001, 9000002, 9100012, 9100022, 9900032, 1023), # 9100000 ->LO mediator ; 9100022 -> chi
        samplesDYJetsToLL = cms.vstring(
            'DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
            'DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
            'DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
            'DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
            'DYBBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
            'DYBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
            'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
            'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
            'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
            'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
            'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
            'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        ),
        samplesZJetsToNuNu = cms.vstring(),
        samplesWJetsToLNu = cms.vstring(),
        samplesDir = cms.string('%s/src/Analysis/ALPHA/data/Stitch/' % os.environ['CMSSW_BASE']),
        sample = cms.string( sample ),
        ewkFile = cms.string('%s/src/Analysis/ALPHA/data/scalefactors_v4.root' % os.environ['CMSSW_BASE']),
        applyEWK = cms.bool(True if sample.startswith('DYJets') or sample.startswith('WJets') else False),
        pythiaLOSample = cms.bool(True if isDibosonInclusive else False),
    ),
    pileupSet = cms.PSet(
        pileup = cms.InputTag('slimmedAddPileupInfo'),
        vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
        dataFileName = cms.string('%s/src/Analysis/ALPHA/data/PU_71300.root' % os.environ['CMSSW_BASE']), #change to the latest
#        dataFileName = cms.string('%s/src/Analysis/ALPHA/data/Prod6.root' % os.environ['CMSSW_BASE']),
        mcFileName = cms.string('%s/src/Analysis/ALPHA/data/PU_MC.root' % os.environ['CMSSW_BASE']),
        dataName = cms.string('pileup'),
        mcName = cms.string('2016_25ns_SpringMC_PUScenarioV1'),
    ),
    triggerSet = cms.PSet(
        trigger = cms.InputTag('TriggerResults', '', triggerTag),
        paths = cms.vstring(
        'HLT_Mu45_eta2p1_v',
        'HLT_Mu50_v',
        'HLT_TkMu50_v',
        'HLT_IsoMu20_v',
        'HLT_IsoTkMu20_v',
        'HLT_IsoMu22_v',
        'HLT_IsoTkMu22_v',
        'HLT_IsoMu24_v',
        'HLT_IsoTkMu24_v',
        'HLT_Ele23_WPLoose_Gsf_v',
        'HLT_Ele27_WPLoose_Gsf_v',
        'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v',
        'HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v',
        'HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v',
        'HLT_PFMET120_BTagCSV_p067_v',
        'HLT_PFMET170_NoiseCleaned_v',),
    ),
    electronSet = cms.PSet(
        #electrons = cms.InputTag('selectedElectrons'),
        electrons = cms.InputTag('slimmedElectrons'),
        vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
        eleVetoIdMap = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'),
        eleLooseIdMap = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'),
        eleMediumIdMap = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
        eleTightIdMap = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'),
        eleHEEPIdMap = cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
        eleMVANonTrigMediumIdMap = cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'),
        eleMVANonTrigTightIdMap = cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'),
        eleMVATrigMediumIdMap = cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp90'),
        eleMVATrigTightIdMap = cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp80'),
        eleSingleTriggerFileName = cms.string('%s/src/Analysis/ALPHA/data/SingleEleTriggerEff.root' % os.environ['CMSSW_BASE']),
        eleVetoIdFileName = cms.string('%s/src/Analysis/ALPHA/data/runB_p2_passingVeto_egammaEffi_txt_SF2D.root' % os.environ['CMSSW_BASE']),
        eleLooseIdFileName = cms.string('%s/src/Analysis/ALPHA/data/runB_p2_passingLoose_egammaEffi_txt_SF2D.root' % os.environ['CMSSW_BASE']),
        eleMediumIdFileName = cms.string('%s/src/Analysis/ALPHA/data/runB_p2_passingMedium_egammaEffi_txt_SF2D.root' % os.environ['CMSSW_BASE']),
        eleTightIdFileName = cms.string('%s/src/Analysis/ALPHA/data/runB_p2_passingTight_egammaEffi_txt_SF2D.root' % os.environ['CMSSW_BASE']),
        eleMVATrigMediumIdFileName = cms.string('%s/src/Analysis/ALPHA/data/ScaleFactor_GsfElectronToRECO_passingTrigWP90.txt.egamma_SF2D.root' % os.environ['CMSSW_BASE']),
        eleMVATrigTightIdFileName = cms.string('%s/src/Analysis/ALPHA/data/ScaleFactor_GsfElectronToRECO_passingTrigWP80.txt.egamma_SF2D.root' % os.environ['CMSSW_BASE']),
        eleRecoEffFileName = cms.string('%s/src/Analysis/ALPHA/data/eleRECO.txt.egamma_SF2D.root' % os.environ['CMSSW_BASE']),
        electron1id = cms.int32(1), # 0: veto, 1: loose, 2: medium, 3: tight, 4: HEEP, 5: MVA medium nonTrig, 6: MVA tight nonTrig, 7: MVA medium Trig, 8: MVA tight Trig
        electron2id = cms.int32(1),
        electron1pt = cms.double(10.),
        electron2pt = cms.double(10.),
    ),
    muonSet = cms.PSet(
        muons = cms.InputTag('cleanedMuons'),#('slimmedMuons'),
        vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
        muonTrkFileName = cms.string('%s/src/Analysis/ALPHA/data/TrkEff.root' % os.environ['CMSSW_BASE']),
        muonIdFileName = cms.string('%s/src/Analysis/ALPHA/data/MuonID_Z_RunBCD_prompt80X_7p65.root' % os.environ['CMSSW_BASE']),
        muonIsoFileName = cms.string('%s/src/Analysis/ALPHA/data/MuonIso_Z_RunBCD_prompt80X_7p65.root' % os.environ['CMSSW_BASE']),
        muonTrkHighptFileName = cms.string('%s/src/Analysis/ALPHA/data/trackHighPtID_effSF_80X.root' % os.environ['CMSSW_BASE']),
        muonTriggerFileName = cms.string('%s/src/Analysis/ALPHA/data/SingleMuonTrigger_Z_RunBCD_prompt80X_7p65.root' % os.environ['CMSSW_BASE']),
        doubleMuonTriggerFileName = cms.string('%s/src/Analysis/ALPHA/data/MuHLTEfficiencies_Run_2012ABCD_53X_DR03-2.root' % os.environ['CMSSW_BASE']),#obsolete
        muon1id = cms.int32(1), # 0: tracker high pt muon id, 1: loose, 2: medium, 3: tight, 4: high pt
        muon2id = cms.int32(1),
        muon1iso = cms.int32(1), # 0: trk iso (<0.1), 1: loose (<0.25), 2: tight (<0.15) (pfIso in cone 0.4)
        muon2iso = cms.int32(1),
        muon1pt = cms.double(10.),
        muon2pt = cms.double(10.),
        useTuneP = cms.bool(True),
        doRochester = cms.bool(False),
    ),
    tauSet = cms.PSet(
        taus = cms.InputTag('slimmedTaus'),
        vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
        taupt = cms.double(20.),
        taueta = cms.double(2.3),
        tauIdByDecayMode = cms.int32(0),# 0: not set, 1: old, 2: new
        tauIdByDeltaBetaIso = cms.int32(0),# 0: not set, 1: loose, 2: medium, 3: tight
        tauIdByMVAIso = cms.int32(0),# 0: not set, 1: V loose, 2: loose, 3: medium, 4: tight, 5: V tight
        tauIdByMuonRejection = cms.int32(0),# 0: not set, 1: loose, 2: tight
        tauIdByElectronRejection = cms.int32(0),# 0: not set, 1: V loose, 2: loose, 3: medium, 4: tight
    ),
    photonSet = cms.PSet(
        photons = cms.InputTag('slimmedPhotons'),
        vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
        phoLooseIdMap = cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring15-25ns-V1-standalone-loose'),
        phoMediumIdMap = cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring15-25ns-V1-standalone-medium'),
        phoTightIdMap = cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring15-25ns-V1-standalone-tight'),
        phoMVANonTrigMediumIdMap = cms.InputTag('egmPhotonIDs:mvaPhoID-Spring15-25ns-nonTrig-V2-wp90'),
        phoLooseIdFileName = cms.string('%s/src/Analysis/ALPHA/data/Loosenumbers.txt.egamma_SF2D.root' % os.environ['CMSSW_BASE']),
        phoMediumIdFileName = cms.string('%s/src/Analysis/ALPHA/data/Mediumnumbers.txt.egamma_SF2D.root' % os.environ['CMSSW_BASE']),
        phoTightIdFileName = cms.string('%s/src/Analysis/ALPHA/data/Tightnumbers.txt.egamma_SF2D.root' % os.environ['CMSSW_BASE']),
        phoMVANonTrigMediumIdFileName = cms.string('%s/src/Analysis/ALPHA/data/MVAnumbers.txt.egamma_SF2D.root' % os.environ['CMSSW_BASE']),
        photonid = cms.int32(1), # 1: loose, 2: medium, 3: tight, 4:MVA NonTrig medium
        photonpt = cms.double(20.),
    ),
    jetSet = cms.PSet(
        jets = cms.InputTag('slimmedJets'),#('slimmedJetsAK8'), #selectedPatJetsAK8PFCHSPrunedPacked
        jetid = cms.int32(1), # 0: no selection, 1: loose, 2: medium, 3: tight
        jet1pt = cms.double(50.),
        jet2pt = cms.double(20.),
        jeteta = cms.double(2.5),
        addQGdiscriminator = cms.bool(True),
        recalibrateJets = cms.bool(True),
        recalibrateMass = cms.bool(False),
        recalibratePuppiMass = cms.bool(False),
        vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
        rho = cms.InputTag('fixedGridRhoFastjetAll'),        
        jecUncertaintyDATA = cms.string('%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_Uncertainty_AK4PFchs.txt' % os.environ['CMSSW_BASE']),
        jecUncertaintyMC = cms.string('%s/src/Analysis/ALPHA/data/Spring16_25nsV6_MC/Spring16_25nsV6_MC_Uncertainty_AK4PFchs.txt' % os.environ['CMSSW_BASE']),
        jecCorrectorDATA = cms.vstring(
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_L1FastJet_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_L2Relative_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_L3Absolute_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_L2L3Residual_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
        ),
        jecCorrectorMC = cms.vstring(
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_MC/Spring16_25nsV6_MC_L1FastJet_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_MC/Spring16_25nsV6_MC_L2Relative_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_MC/Spring16_25nsV6_MC_L3Absolute_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
        ),
        massCorrectorDATA = cms.vstring(
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_L2Relative_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_L3Absolute_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA_L2L3Residual_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
        ),
        massCorrectorMC = cms.vstring(
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_MC/Spring16_25nsV6_MC_L2Relative_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
            '%s/src/Analysis/ALPHA/data/Spring16_25nsV6_MC/Spring16_25nsV6_MC_L3Absolute_AK4PFchs.txt' % os.environ['CMSSW_BASE'],
        ),
        massCorrectorPuppi = cms.string('%s/src/Analysis/ALPHA/data/puppiJecCorr.root' % os.environ['CMSSW_BASE']),
        reshapeBTag = cms.bool(True),
        btag = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
        btagDB = cms.string('%s/src/Analysis/ALPHA/data/CSVv2.csv' % os.environ['CMSSW_BASE']),
        jet1btag = cms.int32(0), # 0: no selection, 1: loose, 2: medium, 3: tight
        jet2btag = cms.int32(0),
        met = cms.InputTag('slimmedMETs'),
        metRecoil = cms.bool(False),
        metRecoilMC = cms.string('%s/src/Analysis/ALPHA/data/recoilfit_gjetsMC_Zu1_pf_v5.root' % os.environ['CMSSW_BASE']),
        metRecoilData = cms.string('%s/src/Analysis/ALPHA/data/recoilfit_gjetsData_Zu1_pf_v5.root' % os.environ['CMSSW_BASE']),
    ),
#    bTagAlgo = cms.string('combinedSecondaryVertexBJetTags'),
    writeNElectrons = cms.int32(2),
    writeNMuons = cms.int32(2),
    writeNLeptons = cms.int32(2),
    writeNTaus = cms.int32(0),
    writeNPhotons = cms.int32(0),
    writeNJets = cms.int32(4),
    #writeNFatJets = cms.int32(1),
    histFile = cms.string('%s/src/Analysis/ALPHA/data/HistList_bb.dat' % os.environ['CMSSW_BASE']),
    verbose  = cms.bool(True),
)



######################
if isData:
    process.seq = cms.Sequence(
        process.counter *
        process.HLTFilter *

        process.METFilter *
        process.BadPFMuonFilter *
        process.BadChargedCandidateFilter *
        
        process.primaryVertexFilter *
        process.egmGsfElectronIDSequence *
        process.calibratedPatElectrons *
        process.egmPhotonIDSequence *
        process.cleanedMuons *
#        process.ak4PFL2L3ResidualCorrectorChain *
        process.QGTagger *
        process.ntuple
    )
else:
    process.seq = cms.Sequence(
        process.counter *

        process.BadPFMuonFilter *
        process.BadChargedCandidateFilter *
        
        process.primaryVertexFilter *
        process.egmGsfElectronIDSequence *
        process.calibratedPatElectrons *
        process.egmPhotonIDSequence *
        process.cleanedMuons *
#        process.ak4PFL2L3ResidualCorrectorChain *
        process.QGTagger *
        process.ntuple
    )

process.p = cms.Path(process.seq)
