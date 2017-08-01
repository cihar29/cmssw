import FWCore.ParameterSet.Config as cms
from DQMServices.Core.DQMEDHarvester import DQMEDHarvester
from DQM.SiPixelPhase1Common.HistogramManager_cfi import *

SiPixelPhase1TrackResidualsResidualsX = DefaultHistoTrack.clone(
  name = "residual_x",
  title = "Track Residuals X",
  range_min = -0.15, range_max = 0.15, range_nbins = 150,
  xlabel = "(x_rec - x_pred) [cm]",
  dimensions = 1,
  specs = VPSet(
    StandardSpecification2DProfile,
    StandardSpecifications1D
  )
)

SiPixelPhase1TrackResidualsResidualsY = SiPixelPhase1TrackResidualsResidualsX.clone(
  name = "residual_y",
  title = "Track Residuals Y",
  xlabel = "(y_rec - y_pred) [cm]",
)

SiPixelPhase1TrackResidualsConf = cms.VPSet(
  SiPixelPhase1TrackResidualsResidualsX,
  SiPixelPhase1TrackResidualsResidualsY
)

SiPixelPhase1TrackResidualsAnalyzerNoTrig = cms.EDAnalyzer("SiPixelPhase1TrackResiduals",
        trajectoryInput = cms.string("generalTracks"),
        Tracks        = cms.InputTag("generalTracks"),
        histograms = SiPixelPhase1TrackResidualsConf,
        geometry = SiPixelPhase1Geometry
)

SiPixelPhase1TrackResidualsHarvesterNoTrig = DQMEDHarvester("SiPixelPhase1Harvester",
        histograms = SiPixelPhase1TrackResidualsConf,
        geometry = SiPixelPhase1Geometry
)

#Trigger Analyzer
import DQM.SiPixelPhase1Common.TriggerEventFlag_cfi as trigger

SiPixelPhase1TrackResidualsConfHLT = cms.VPSet()
SiPixelPhase1TrackResidualsConfL1 = cms.VPSet()

for i in range( 0, len(SiPixelPhase1TrackResidualsConf) ):
  histHLT = SiPixelPhase1TrackResidualsConf[i].clone(
              topFolderName = cms.string( SiPixelPhase1TrackResidualsConf[i].topFolderName.value() + trigger.HLTfoldername.value() )
            )
  histL1 = SiPixelPhase1TrackResidualsConf[i].clone(
              topFolderName = cms.string( SiPixelPhase1TrackResidualsConf[i].topFolderName.value() + trigger.L1foldername.value() )
            )
  name = SiPixelPhase1TrackResidualsConf[i].getParameter("name").value()
  if SiPixelPhase1TrackResidualsConf[i].getParameter("dimensions").value() == 2:
    histHLT.enabled = False
    histL1.enabled = False
  elif name in trigger.HLT_DontPlot: histHLT.enabled = False
  elif name in trigger.L1_DontPlot: histL1.enabled = False
  else :
    newspecs = [spec for spec in SiPixelPhase1TrackResidualsConf[i].specs if (spec not in StandardSpecification2DProfile
                                                                    and spec not in StandardSpecificationTrend2D
                                                                    and spec not in StandardSpecification2DOccupancy
                                                                    and spec not in StandardSpecification2DProfile_Num)]
    histHLT.specs = newspecs
    histL1.specs = newspecs
  SiPixelPhase1TrackResidualsConfHLT.append( histHLT )
  SiPixelPhase1TrackResidualsConfL1.append( histL1 )

SiPixelPhase1TrackResidualsAnalyzerHLT = SiPixelPhase1TrackResidualsAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1TrackResidualsConfHLT,
        triggerflags = trigger.SiPixelPhase1TriggerHLT
)

SiPixelPhase1TrackResidualsHarvesterHLT = SiPixelPhase1TrackResidualsHarvesterNoTrig.clone(
        histograms = SiPixelPhase1TrackResidualsConfHLT
)

SiPixelPhase1TrackResidualsAnalyzerL1 = SiPixelPhase1TrackResidualsAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1TrackResidualsConfL1,
        triggerflags = trigger.SiPixelPhase1TriggerL1
)

SiPixelPhase1TrackResidualsHarvesterL1 = SiPixelPhase1TrackResidualsHarvesterNoTrig.clone(
        histograms = SiPixelPhase1TrackResidualsConfL1
)

SiPixelPhase1TrackResidualsAnalyzer = cms.Sequence(  SiPixelPhase1TrackResidualsAnalyzerNoTrig
                                                   * SiPixelPhase1TrackResidualsAnalyzerHLT
                                                   * SiPixelPhase1TrackResidualsAnalyzerL1
                                                  )

SiPixelPhase1TrackResidualsHarvester = cms.Sequence(  SiPixelPhase1TrackResidualsHarvesterNoTrig
       	       	       	       	         	    * SiPixelPhase1TrackResidualsHarvesterHLT
                                                    * SiPixelPhase1TrackResidualsHarvesterL1
       	       	       	       	 	           )
