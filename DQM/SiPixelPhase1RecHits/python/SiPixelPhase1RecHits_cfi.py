import FWCore.ParameterSet.Config as cms
from DQMServices.Core.DQMEDHarvester import DQMEDHarvester
from DQM.SiPixelPhase1Common.HistogramManager_cfi import *

SiPixelPhase1RecHitsNRecHits = DefaultHistoTrack.clone(
  name = "rechits",
  title = "RecHits",
  range_min = 0, range_max = 30, range_nbins = 30,
  xlabel = "rechits",
  dimensions = 0,
  specs = VPSet(
   StandardSpecificationInclusive_Num,
   StandardSpecificationTrend_Num
   # StandardSpecification2DProfile_Num,
   # StandardSpecificationInclusive_Num,
   # StandardSpecifications1D_Num
  )
)

SiPixelPhase1RecHitsClustX = DefaultHistoTrack.clone(
  name = "rechitsize_x",
  title = "X size of RecHit clusters",
  range_min = 0, range_max = 50, range_nbins = 50,
  xlabel = "RecHit X-Size",
  dimensions = 1,
  specs = VPSet(
    StandardSpecification2DProfile
  )
)

SiPixelPhase1RecHitsClustY = SiPixelPhase1RecHitsClustX.clone(
  name = "rechitsize_y",
  title = "Y size of RecHit clusters",
  xlabel = "RecHit Y-Size"
)

SiPixelPhase1RecHitsErrorX = DefaultHistoTrack.clone(
  enabled=False,
  name = "rechiterror_x",
  title = "RecHit Error in X-direction",
  range_min = 0, range_max = 0.02, range_nbins = 100,
  xlabel = "X error",
  dimensions = 1,
  specs = VPSet(
    StandardSpecification2DProfile
  )
)

SiPixelPhase1RecHitsErrorY = SiPixelPhase1RecHitsErrorX.clone(
  enabled=False,
  name = "rechiterror_y",
  title = "RecHit Error in Y-direction",
  xlabel = "Y error"
)

SiPixelPhase1RecHitsPosition = DefaultHistoTrack.clone(
  enabled = False,
  name = "rechit_pos",
  title = "Position of RecHits on Module",
  range_min   = -1, range_max   = 1, range_nbins   = 100,
  range_y_min = -4, range_y_max = 4, range_y_nbins = 100,
  xlabel = "x offset",
  ylabel = "y offset",
  dimensions = 2,
  specs = VPSet(
    Specification(PerModule).groupBy("PXBarrel/PXLayer/DetId").save(),
    Specification(PerModule).groupBy("PXForward/PXDisk/DetId").save(),
  )
)

SiPixelPhase1RecHitsProb = DefaultHistoTrack.clone(
  name = "clusterprob",
  title = "Cluster Probability",
  xlabel = "log_10(Pr)",
  range_min = -10, range_max = 1, range_nbins = 50,
  dimensions = 1,
  specs = VPSet(
    StandardSpecifications1D
  )
)


SiPixelPhase1RecHitsConf = cms.VPSet(
  SiPixelPhase1RecHitsNRecHits,
  SiPixelPhase1RecHitsClustX,
  SiPixelPhase1RecHitsClustY,
  SiPixelPhase1RecHitsErrorX,
  SiPixelPhase1RecHitsErrorY,
  SiPixelPhase1RecHitsPosition,
  SiPixelPhase1RecHitsProb,
)

SiPixelPhase1RecHitsAnalyzerNoTrig = cms.EDAnalyzer("SiPixelPhase1RecHits",
        src = cms.InputTag("generalTracks"),
        histograms = SiPixelPhase1RecHitsConf,
        geometry = SiPixelPhase1Geometry,
        onlyValidHits = cms.bool(False)
)

SiPixelPhase1RecHitsHarvesterNoTrig = DQMEDHarvester("SiPixelPhase1Harvester",
        histograms = SiPixelPhase1RecHitsConf,
        geometry = SiPixelPhase1Geometry
)

#Trigger Analyzer
import DQM.SiPixelPhase1Common.TriggerEventFlag_cfi as trigger

SiPixelPhase1RecHitsConfHLT = cms.VPSet()
SiPixelPhase1RecHitsConfL1 = cms.VPSet()

for i in range( 0, len(SiPixelPhase1RecHitsConf) ):
  #if SiPixelPhase1RecHitsConf[i].getParameter("dimensions").value() == 2:
  #  continue
  if SiPixelPhase1RecHitsConf[i].getParameter("name").value() not in trigger.HLT_DontPlot:
    histHLT = SiPixelPhase1RecHitsConf[i].clone(
                topFolderName = cms.string( SiPixelPhase1RecHitsConf[i].topFolderName.value() + trigger.HLTfoldername.value() )
              )
    SiPixelPhase1RecHitsConfHLT.append( histHLT )
  if SiPixelPhase1RecHitsConf[i].getParameter("name").value() not in trigger.L1_DontPlot:
    histL1 = SiPixelPhase1RecHitsConf[i].clone(
                topFolderName = cms.string( SiPixelPhase1RecHitsConf[i].topFolderName.value() + trigger.L1foldername.value() )
              )
    SiPixelPhase1RecHitsConfL1.append( histL1 )

SiPixelPhase1RecHitsAnalyzerHLT = SiPixelPhase1RecHitsAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1RecHitsConfHLT,
        triggerflags = trigger.SiPixelPhase1TriggerHLT
)

SiPixelPhase1RecHitsHarvesterHLT = SiPixelPhase1RecHitsHarvesterNoTrig.clone(
        histograms = SiPixelPhase1RecHitsConfHLT
)

SiPixelPhase1RecHitsAnalyzerL1 = SiPixelPhase1RecHitsAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1RecHitsConfL1,
        triggerflags = trigger.SiPixelPhase1TriggerL1
)

SiPixelPhase1RecHitsHarvesterL1 = SiPixelPhase1RecHitsHarvesterNoTrig.clone(
        histograms = SiPixelPhase1RecHitsConfL1
)

SiPixelPhase1RecHitsAnalyzer = cms.Sequence(  SiPixelPhase1RecHitsAnalyzerNoTrig
                                            * SiPixelPhase1RecHitsAnalyzerHLT
                                            * SiPixelPhase1RecHitsAnalyzerL1
                                           )

SiPixelPhase1RecHitsHarvester = cms.Sequence(  SiPixelPhase1RecHitsHarvesterNoTrig
       	     	       	       	             * SiPixelPhase1RecHitsHarvesterHLT
                                             * SiPixelPhase1RecHitsHarvesterL1
       	      	       	       		    )
