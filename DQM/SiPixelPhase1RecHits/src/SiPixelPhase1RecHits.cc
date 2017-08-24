// -*- C++ -*-
//
// Package:     SiPixelPhase1RecHits
// Class:       SiPixelPhase1RecHits
//

// Original Author: Marcel Schneider

#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/GeometryVector/interface/LocalPoint.h"

#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetUnit.h"
#include "Geometry/CommonTopologies/interface/PixelTopology.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"

#include "DataFormats/SiPixelDetId/interface/PixelSubdetector.h"

#include "DataFormats/TrackReco/interface/Track.h"

#include "DataFormats/TrackerRecHit2D/interface/SiPixelRecHit.h"

#include "DQM/SiPixelPhase1RecHits/interface/SiPixelPhase1RecHits.h"

SiPixelPhase1RecHits::SiPixelPhase1RecHits(const edm::ParameterSet& iConfig) :
  SiPixelPhase1Base(iConfig) 
{
  srcToken_ = consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("src"));
  onlyValid_=iConfig.getParameter<bool>("onlyValidHits");
}

void SiPixelPhase1RecHits::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  updateTriggers(iEvent,iSetup);

  edm::ESHandle<TrackerGeometry> tracker;
  iSetup.get<TrackerDigiGeometryRecord>().get(tracker);
  assert(tracker.isValid());

  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken( srcToken_, tracks);
  if (!tracks.isValid()) return;

  for (auto const & track : *tracks) {

    bool isBpixtrack = false, isFpixtrack = false;

    auto const & trajParams = track.extra()->trajParams();
    auto hb = track.recHitsBegin();
    for(unsigned int h=0;h<track.recHitsSize();h++){
     
      auto hit = *(hb+h);
      if(!hit->isValid()) continue;
      
      DetId id = hit->geographicalId();
      uint32_t subdetid = (id.subdetId());

      if (subdetid == PixelSubdetector::PixelBarrel) isBpixtrack = true;
      if (subdetid == PixelSubdetector::PixelEndcap) isFpixtrack = true;
    }

    if (!isBpixtrack && !isFpixtrack) continue;

    // then, look at each hit
    for(unsigned int h=0;h<track.recHitsSize();h++){
      auto rechit = *(hb+h);
    
      if(!rechit->isValid()) continue;

      //continue if not a Pixel recHit
      DetId id = rechit->geographicalId();
      uint32_t subdetid = (id.subdetId());

      if (   subdetid != PixelSubdetector::PixelBarrel 
	     && subdetid != PixelSubdetector::PixelEndcap) continue;

      bool isHitValid   = rechit->getType()==TrackingRecHit::valid;
      if (onlyValid_ && !isHitValid) continue; //useful to run on cosmics where the TrackEfficiency plugin is not used

      const SiPixelRecHit* prechit = dynamic_cast<const SiPixelRecHit*>(rechit);//to be used to get the associated cluster and the cluster probability      

      int sizeX=0, sizeY=0;

      if (isHitValid){
	SiPixelRecHit::ClusterRef const& clust = prechit->cluster();
	sizeX = (*clust).sizeX();
	sizeY = (*clust).sizeY();
      }

      const PixelGeomDetUnit* geomdetunit = dynamic_cast<const PixelGeomDetUnit*> ( tracker->idToDet(id) );
      const PixelTopology& topol = geomdetunit->specificTopology();

      LocalPoint lp = trajParams[h].position();
      MeasurementPoint mp = topol.measurementPosition(lp);
      
      int row = (int) mp.x();
      int col = (int) mp.y();
      
      float rechit_x = lp.x();
      float rechit_y = lp.y();
      
      LocalError lerr = rechit->localPositionError();
      float lerr_x = sqrt(lerr.xx());
      float lerr_y = sqrt(lerr.yy());

      histo[NRECHITS].fill(id, triggers_pass, &iEvent, col, row); //in general a inclusive counter of missing/valid/inactive hits

      if (isHitValid){
	histo[CLUST_X].fill(sizeX, id, triggers_pass, &iEvent, col, row);
	histo[CLUST_Y].fill(sizeY, id, triggers_pass, &iEvent, col, row);
      }

      histo[ERROR_X].fill(lerr_x, id, triggers_pass, &iEvent);
      histo[ERROR_Y].fill(lerr_y, id, triggers_pass, &iEvent);

      histo[POS].fill(rechit_x, rechit_y, id, triggers_pass, &iEvent);
      
      if (isHitValid){
	double clusterProbability= prechit->clusterProbability(0);
	if (clusterProbability > 0)
	  histo[CLUSTER_PROB].fill(log10(clusterProbability), id, triggers_pass, &iEvent);
      }
    }
  }

  histo[NRECHITS].executePerEventHarvesting(&iEvent);
}

DEFINE_FWK_MODULE(SiPixelPhase1RecHits);

