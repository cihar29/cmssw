import FWCore.ParameterSet.Config as cms
from DQMServices.Core.DQMEDHarvester import DQMEDHarvester
from DQM.SiPixelPhase1Common.HistogramManager_cfi import *


SiPixelPhase1RawDataNErrors = DefaultHisto.clone(
topFolderName = DefaultHisto.topFolderName.value() +"/FED",
  name = "errors",
  title = "Errors",
  xlabel = "errors",
  range_min = 0, range_max = 30, range_nbins = 30,
  dimensions = 0,
  specs = VPSet(
    Specification().groupBy("FED/FED/Event")
                   .reduce("COUNT")
                   .groupBy("FED/FED").save(),
    Specification().groupBy("FED/FED/LinkInFed")
                   .groupBy("FED/FED", "EXTEND_X")
                   .save(),
    Specification().groupBy("FED/LinkInFed")
                   .groupBy("FED", "EXTEND_X")
                   .groupBy("", "EXTEND_Y")
                   .save(),
    Specification().groupBy("FED/FED/Lumisection")
    .groupBy("FED/FED","EXTEND_X")
    .save()
    .groupBy("")
    .save()
  )
)

SiPixelPhase1RawDataFIFOFull = DefaultHisto.clone(
    topFolderName = DefaultHisto.topFolderName.value() +"/FED", 
    name = "fifofull",
    title = "Type of FIFO full",
    xlabel = "FIFO (data bit #)",
    range_min = -0.5, range_max = 7.5, range_nbins = 8,
    dimensions = 1,
    specs = VPSet(
        Specification().groupBy("FED/FED").save(),
    )
)

SiPixelPhase1RawDataTBMMessage = DefaultHisto.clone(
  topFolderName = DefaultHisto.topFolderName.value() +"/FED",
  name = "tbmmessage",
  title = "TBM trailer message",
  xlabel = "TBM message (data bit #)",
  range_min = -0.5, range_max = 7.5, range_nbins = 8,
  dimensions = 1,
  specs = VPSet(
    Specification().groupBy("FED/FED").save(),
  )
)

SiPixelPhase1RawDataTBMType = DefaultHisto.clone(
  topFolderName = DefaultHisto.topFolderName.value() +"/FED",
  name = "tbmtype",
  title = "Type of TBM trailer",
  xlabel = "TBM type",
  range_min = -0.5, range_max = 4.5, range_nbins = 5,
  dimensions = 1,
  specs = VPSet(
    Specification().groupBy("FED/FED").save(),
  )
)

SiPixelPhase1RawDataTypeNErrors = DefaultHisto.clone(
  topFolderName = DefaultHisto.topFolderName.value() +"/FED",
  name = "nerrors_per_type",
  title = "Number of Errors per Type",
  xlabel = "Error Type",
  range_min = 24.5, range_max = 40.5, range_nbins = 16,
  dimensions = 1,
  specs = VPSet(
    Specification().groupBy("FED/FED").save(),
    Specification().groupBy("FED")
                   .groupBy("", "EXTEND_Y").save(),
    Specification().groupBy("FED/FED/LinkInFed")
                   .groupBy("FED/FED","EXTEND_Y").save()                  

  )
)

SiPixelPhase1RawDataConf = cms.VPSet(
  SiPixelPhase1RawDataNErrors,
  SiPixelPhase1RawDataFIFOFull,
  SiPixelPhase1RawDataTBMMessage,
  SiPixelPhase1RawDataTBMType,
  SiPixelPhase1RawDataTypeNErrors,
)

SiPixelPhase1RawDataAnalyzerNoTrig = cms.EDAnalyzer("SiPixelPhase1RawData",
        src = cms.InputTag("siPixelDigis"),
        histograms = SiPixelPhase1RawDataConf,
        geometry = SiPixelPhase1Geometry
)

SiPixelPhase1RawDataHarvesterNoTrig = DQMEDHarvester("SiPixelPhase1Harvester",
        histograms = SiPixelPhase1RawDataConf,
        geometry = SiPixelPhase1Geometry
)

#Trigger Analyzer
import DQM.SiPixelPhase1Common.TriggerEventFlag_cfi as trigger

SiPixelPhase1RawDataConfHLT = cms.VPSet()
SiPixelPhase1RawDataConfL1 = cms.VPSet()

for i in range( 0, len(SiPixelPhase1RawDataConf) ):
  histHLT = SiPixelPhase1RawDataConf[i].clone(
              topFolderName = cms.string( SiPixelPhase1RawDataConf[i].topFolderName.value() + trigger.HLTfoldername.value() )
            )
  SiPixelPhase1RawDataConfHLT.append( histHLT )
  histL1 = SiPixelPhase1RawDataConf[i].clone(
              topFolderName = cms.string( SiPixelPhase1RawDataConf[i].topFolderName.value() + trigger.L1foldername.value() )
            )
  SiPixelPhase1RawDataConfL1.append( histL1 )

SiPixelPhase1RawDataAnalyzerHLT = SiPixelPhase1RawDataAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1RawDataConfHLT,
        triggerflags = trigger.SiPixelPhase1TriggerHLT
)

SiPixelPhase1RawDataHarvesterHLT = SiPixelPhase1RawDataHarvesterNoTrig.clone(
        histograms = SiPixelPhase1RawDataConfHLT
)

SiPixelPhase1RawDataAnalyzerL1 = SiPixelPhase1RawDataAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1RawDataConfL1,
        triggerflags = trigger.SiPixelPhase1TriggerL1
)

SiPixelPhase1RawDataHarvesterL1 = SiPixelPhase1RawDataHarvesterNoTrig.clone(
        histograms = SiPixelPhase1RawDataConfL1
)

SiPixelPhase1RawDataAnalyzer = cms.Sequence( SiPixelPhase1RawDataAnalyzerNoTrig
                                           * SiPixelPhase1RawDataAnalyzerHLT
                                           * SiPixelPhase1RawDataAnalyzerL1
                                           )

SiPixelPhase1RawDataHarvester = cms.Sequence( SiPixelPhase1RawDataHarvesterNoTrig
       	       	       	       	       	    * SiPixelPhase1RawDataHarvesterHLT
                                            * SiPixelPhase1RawDataHarvesterL1
       	       	       	       	 	    )
