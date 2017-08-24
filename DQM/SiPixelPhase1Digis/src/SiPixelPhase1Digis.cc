// -*- C++ -*-
//
// Package:    SiPixelPhase1Digis
// Class:      SiPixelPhase1Digis
//

// Original Author: Marcel Schneider

#include "DQM/SiPixelPhase1Digis/interface/SiPixelPhase1Digis.h"

// C++ stuff
#include <iostream>

// CMSSW stuff
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

// DQM Stuff
#include "DQMServices/Core/interface/MonitorElement.h"

SiPixelPhase1Digis::SiPixelPhase1Digis(const edm::ParameterSet& iConfig) :
  SiPixelPhase1Base(iConfig)
{
  srcToken_ = consumes<edm::DetSetVector<PixelDigi>>(iConfig.getParameter<edm::InputTag>("src"));
} 

void SiPixelPhase1Digis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  updateTriggers(iEvent,iSetup);

  edm::Handle<edm::DetSetVector<PixelDigi>> input;
  iEvent.getByToken(srcToken_, input);
  if (!input.isValid()) return; 
  bool hasDigis=false;

  edm::DetSetVector<PixelDigi>::const_iterator it;
  for (it = input->begin(); it != input->end(); ++it) {
    DetId id = DetId(it->detId());

    for(PixelDigi const& digi : *it) {
      hasDigis=true;
      histo[ADC]            .fill((double) digi.adc(), id, triggers_pass, &iEvent, digi.column(), digi.row());
      histo[MAP]            .fill(id, triggers_pass, &iEvent, digi.column(), digi.row()); 
      histo[OCCUPANCY]      .fill(id, triggers_pass, &iEvent, digi.column(), digi.row()); 
      histo[NDIGIS]         .fill(id, triggers_pass, &iEvent); // count
      histo[NDIGISINCLUSIVE].fill(id, triggers_pass, &iEvent); // count
      histo[NDIGIS_FED]     .fill(id, triggers_pass, &iEvent); 
      histo[NDIGIS_FEDtrend].fill(id, triggers_pass, &iEvent);  
    }
  }
  if (hasDigis) histo[EVENT].fill(DetId(0), triggers_pass, &iEvent);
  histo[NDIGIS]         .executePerEventHarvesting(&iEvent);
  histo[NDIGISINCLUSIVE].executePerEventHarvesting(&iEvent);
  histo[NDIGIS_FED]     .executePerEventHarvesting(&iEvent); 
  histo[NDIGIS_FEDtrend].executePerEventHarvesting(&iEvent);
}

DEFINE_FWK_MODULE(SiPixelPhase1Digis);

