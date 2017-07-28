import FWCore.ParameterSet.Config as cms
from DQMServices.Core.DQMEDHarvester import DQMEDHarvester
from DQM.SiPixelPhase1Common.HistogramManager_cfi import *

SiPixelPhase1ClustersCharge = DefaultHistoDigiCluster.clone(
  name = "charge",
  title = "Cluster Charge",
  range_min = 0, range_max = 300e3, range_nbins = 150,
  xlabel = "Charge (electrons)",

  specs = VPSet(
    StandardSpecification2DProfile,
    StandardSpecificationPixelmapProfile,
    StandardSpecificationTrend,
    StandardSpecifications1D,
    StandardSpecificationTrend2D
  )
)

SiPixelPhase1ClustersSize = DefaultHistoDigiCluster.clone(
  name = "size",
  title = "Total Cluster Size",
  range_min = 0, range_max = 30, range_nbins = 30,
  xlabel = "size[pixels]",
  specs = VPSet(
    StandardSpecification2DProfile,
    StandardSpecificationPixelmapProfile,
    StandardSpecificationTrend,
    StandardSpecifications1D,
    StandardSpecificationTrend2D
  )
)

SiPixelPhase1ClustersSizeX = DefaultHistoDigiCluster.clone(
  name = "sizeX",
  title = "Cluster Size in X",
  range_min = 0, range_max = 30, range_nbins = 30,
  xlabel = "size[pixels]",
  specs = VPSet(
    #StandardSpecification2DProfile,
    #StandardSpecificationPixelmapProfile,
    #StandardSpecificationTrend,
    StandardSpecifications1D,
    #StandardSpecificationTrend2D
  )
)

SiPixelPhase1ClustersSizeY = DefaultHistoDigiCluster.clone(
  name = "sizeY",
  title = "Cluster Size in Y",
  range_min = 0, range_max = 30, range_nbins = 30,
  xlabel = "size[pixels]",
  specs = VPSet(
    #StandardSpecification2DProfile,
    #StandardSpecificationPixelmapProfile,
    #StandardSpecificationTrend,
    StandardSpecifications1D,
    #StandardSpecificationTrend2D
  )
)

SiPixelPhase1ClustersNClusters = DefaultHistoDigiCluster.clone(
  name = "clusters",
  title = "Clusters",
  range_min = 0, range_max = 30, range_nbins = 60,
  xlabel = "clusters",
  dimensions = 0,

  specs = VPSet(
    StandardSpecificationOccupancy,
    StandardSpecification2DProfile_Num,
    StandardSpecificationTrend_Num,
    StandardSpecifications1D_Num,

    Specification().groupBy("PXBarrel/PXLayer/Event") #this will produce inclusive counts per Layer/Disk
                             .reduce("COUNT")    
                             .groupBy("PXBarrel/PXLayer")
                             .save(nbins=100, xmin=0, xmax=20000),
    Specification().groupBy("PXForward/PXDisk/Event")
                             .reduce("COUNT")    
                             .groupBy("PXForward/PXDisk/")
                             .save(nbins=100, xmin=0, xmax=10000),
  )
)


SiPixelPhase1ClustersNClustersInclusive = DefaultHistoDigiCluster.clone(
  name = "clusters",
  title = "Clusters",
  range_min = 0, range_max = 30000, range_nbins = 150,
  xlabel = "clusters",
  dimensions = 0,
  specs = VPSet(
    StandardSpecificationInclusive_Num
  )
)


SiPixelPhase1ClustersEventrate = DefaultHistoDigiCluster.clone(
  name = "clustereventrate",
  title = "Number of Events with clusters",
  ylabel = "#Events",
  dimensions = 0,
  enabled=False,
  specs = VPSet(
    Specification().groupBy("Lumisection")
                   .groupBy("", "EXTEND_X").save(),
    Specification().groupBy("BX")
                   .groupBy("", "EXTEND_X").save()
    )

)


SiPixelPhase1ClustersPositionB = DefaultHistoDigiCluster.clone(
  name = "clusterposition_zphi",
  title = "Cluster Positions",
  range_min   =  -60, range_max   =  60, range_nbins   = 300,
  range_y_min = -3.2, range_y_max = 3.2, range_y_nbins = 200,
  xlabel = "Global Z", ylabel = "Global \phi",
  dimensions = 2,
  specs = VPSet(
    Specification().groupBy("PXBarrel/PXLayer").save(),
    Specification().groupBy("").save(),
  )
)

SiPixelPhase1ClustersPositionF = DefaultHistoDigiCluster.clone(
  name = "clusterposition_xy",
  title = "Cluster Positions",
  xlabel = "Global X", ylabel = "Global Y",
  range_min   = -20, range_max   = 20, range_nbins   = 200,
  range_y_min = -20, range_y_max = 20, range_y_nbins = 200,
  dimensions = 2,
  specs = VPSet(
    Specification().groupBy("PXForward/PXDisk").save(),
    Specification().groupBy("PXForward").save(),
    #Specification().groupBy("PXBarrel").save(),
  )
)

SiPixelPhase1ClustersPositionXZ = DefaultHistoDigiCluster.clone(
  enabled = False, # only for debugging geometry
  name = "clusterposition_xz",
  title = "Cluster Positions",
  xlabel = "Global X", ylabel = "Global Z",
  range_min   = -20, range_max   = 20, range_nbins   = 200,
  range_y_min = -60, range_y_max = 60, range_y_nbins = 1200,
  dimensions = 2,
  specs = VPSet(
  )
)

SiPixelPhase1ClustersPositionYZ = DefaultHistoDigiCluster.clone(
  enabled = False, # only for debugging geometry
  name = "clusterposition_yz",
  title = "Cluster Positions",
  xlabel = "Global Y", ylabel = "Global Z",
  range_min   = -20, range_max   = 20, range_nbins   = 200,
  range_y_min = -60, range_y_max = 60, range_y_nbins = 1200,
  dimensions = 2,
  specs = VPSet(
  )
)

SiPixelPhase1ClustersSizeVsEta = DefaultHistoDigiCluster.clone(
  name = "sizeyvseta",
  title = "Cluster Size along Beamline vs. Cluster position #eta",
  xlabel = "Cluster #eta",
  ylabel = "length [pixels]",
  range_min = -3.2, range_max  = 3.2, range_nbins   = 40,
  range_y_min =  0, range_y_max = 40, range_y_nbins = 40,
  dimensions = 2,
  specs = VPSet(
    Specification().groupBy("PXBarrel/PXLayer").save(),
    Specification().groupBy("PXBarrel").save()
  )
)

SiPixelPhase1ClustersReadoutCharge = DefaultHistoReadout.clone(
  name = "charge",
  title = "Cluster Charge",
  range_min = 0, range_max = 200e3, range_nbins = 200,
  xlabel = "Charge (electrons)",
  specs = VPSet(
    Specification(PerReadout).groupBy("PXBarrel/Shell/Sector").save(),
    Specification(PerReadout).groupBy("PXForward/HalfCylinder").save()

    #Specification(PerReadout).groupBy("PXBarrel/Shell/Sector/OnlineBlock")
    #                         .groupBy("PXBarrel/Shell/Sector", "EXTEND_Y").save(),
    #Specification(PerReadout).groupBy("PXForward/HalfCylinder/OnlineBlock")
    #                         .groupBy("PXForward/HalfCylinder", "EXTEND_Y").save(),
  )
)

SiPixelPhase1ClustersReadoutNClusters = DefaultHistoReadout.clone(
  name = "clusters",
  title = "Clusters",
  range_min = 0, range_max = 30, range_nbins = 30,
  xlabel = "clusters",
  dimensions = 0,
  specs = VPSet(
    Specification(PerReadout).groupBy("PXBarrel/Shell/Sector/DetId/Event").reduce("COUNT")
                             .groupBy("PXBarrel/Shell/Sector").save(),
    Specification(PerReadout).groupBy("PXForward/HalfCylinder/DetId/Event").reduce("COUNT")
                             .groupBy("PXForward/HalfCylinder").save(),

    Specification(PerReadout).groupBy("PXBarrel/Shell/Sector/DetId/Event").reduce("COUNT")
                             .groupBy("PXBarrel/Shell/Sector/Lumisection").reduce("MEAN")
                             .groupBy("PXBarrel/Shell/Sector", "EXTEND_X").save(),
    Specification(PerReadout).groupBy("PXForward/HalfCylinder/DetId/Event").reduce("COUNT")
                             .groupBy("PXForward/HalfCylinder/Lumisection").reduce("MEAN")
                             .groupBy("PXForward/HalfCylinder", "EXTEND_X").save(),
  )
)

SiPixelPhase1ClustersPixelToStripRatio = DefaultHistoDigiCluster.clone(
  name = "cluster_ratio",
  title = "Pixel to Strip clusters ratio",
  
  xlabel = "ratio",
  dimensions = 1,
  
  specs = VPSet(
    Specification().groupBy("PXAll").save(100, 0, 1), 
    Specification().groupBy("PXAll/Lumisection")
                   .reduce("MEAN") 
                   .groupBy("PXAll", "EXTEND_X")
                   .save(),
    Specification().groupBy("PXAll/BX")
                   .reduce("MEAN") 
                   .groupBy("PXAll", "EXTEND_X")
                   .save(),
  )
)

SiPixelPhase1ClustersConf = cms.VPSet(
  SiPixelPhase1ClustersCharge,
  SiPixelPhase1ClustersSize,
  SiPixelPhase1ClustersSizeX,
  SiPixelPhase1ClustersSizeY,
  SiPixelPhase1ClustersNClusters,
  SiPixelPhase1ClustersNClustersInclusive,
  SiPixelPhase1ClustersEventrate,
  SiPixelPhase1ClustersPositionB,
  SiPixelPhase1ClustersPositionF,
  SiPixelPhase1ClustersPositionXZ,
  SiPixelPhase1ClustersPositionYZ,
  SiPixelPhase1ClustersSizeVsEta,
  SiPixelPhase1ClustersReadoutCharge,
  SiPixelPhase1ClustersReadoutNClusters,
  SiPixelPhase1ClustersPixelToStripRatio
)

SiPixelPhase1ClustersAnalyzerNoTrig = cms.EDAnalyzer("SiPixelPhase1Clusters",
        pixelSrc = cms.InputTag("siPixelClusters"),
        stripSrc = cms.InputTag("siStripClusters"),
        histograms = SiPixelPhase1ClustersConf,
        geometry = SiPixelPhase1Geometry
)

SiPixelPhase1ClustersHarvesterNoTrig = DQMEDHarvester("SiPixelPhase1Harvester",
        histograms = SiPixelPhase1ClustersConf,
        geometry = SiPixelPhase1Geometry
)

#Trigger Analyzer
import DQM.SiPixelPhase1Common.TriggerEventFlag_cfi as trigger

SiPixelPhase1ClustersConfHLT = cms.VPSet()
SiPixelPhase1ClustersConfL1 = cms.VPSet()

for i in range( 0, len(SiPixelPhase1ClustersConf) ):
  #if SiPixelPhase1ClustersConf[i].getParameter("dimensions").value() == 2:
  #  continue
  if SiPixelPhase1ClustersConf[i].getParameter("name").value() not in trigger.HLT_DontPlot:
    histHLT = SiPixelPhase1ClustersConf[i].clone(
                topFolderName = cms.string( SiPixelPhase1ClustersConf[i].topFolderName.value() + trigger.HLTfoldername.value() )
              )
    SiPixelPhase1ClustersConfHLT.append( histHLT )
  if SiPixelPhase1ClustersConf[i].getParameter("name").value() not in trigger.L1_DontPlot:
    histL1 = SiPixelPhase1ClustersConf[i].clone(
                topFolderName = cms.string( SiPixelPhase1ClustersConf[i].topFolderName.value() + trigger.L1foldername.value() )
              )
    SiPixelPhase1ClustersConfL1.append( histL1 )

SiPixelPhase1ClustersAnalyzerHLT = SiPixelPhase1ClustersAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1ClustersConfHLT,
        triggerflags = trigger.SiPixelPhase1TriggerHLT
)

SiPixelPhase1ClustersHarvesterHLT = SiPixelPhase1ClustersHarvesterNoTrig.clone(
        histograms = SiPixelPhase1ClustersConfHLT
)

SiPixelPhase1ClustersAnalyzerL1 = SiPixelPhase1ClustersAnalyzerNoTrig.clone(
        histograms = SiPixelPhase1ClustersConfL1,
        triggerflags = trigger.SiPixelPhase1TriggerL1
)

SiPixelPhase1ClustersHarvesterL1 = SiPixelPhase1ClustersHarvesterNoTrig.clone(
        histograms = SiPixelPhase1ClustersConfL1
)

SiPixelPhase1ClustersAnalyzer = cms.Sequence(  SiPixelPhase1ClustersAnalyzerNoTrig
                                             * SiPixelPhase1ClustersAnalyzerHLT
                                             * SiPixelPhase1ClustersAnalyzerL1
                                            )

SiPixelPhase1ClustersHarvester = cms.Sequence(  SiPixelPhase1ClustersHarvesterNoTrig
       	       	       	       	       	      * SiPixelPhase1ClustersHarvesterHLT
                                              * SiPixelPhase1ClustersHarvesterL1
       	       	       	       	 	     )
