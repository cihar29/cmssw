// -*- C++ -*-
//
// Class:      SiPixelPhase1Base
//
// Implementations of the class
//
// Original Author: Yi-Mu "Enoch" Chen

#include "DQM/SiPixelPhase1Common/interface/SiPixelPhase1Base.h"

// Constructor requires manually looping the trigger flag settings
// Since constructor of GenericTriggerEventFlag requires
// EDConsumerBase class protected member calls
SiPixelPhase1Base::SiPixelPhase1Base( const edm::ParameterSet& iConfig ) :
  DQMEDAnalyzer(),
  HistogramManagerHolder( iConfig )
{
  // Flags will default to empty vector if not specified in configuration file
  auto flags = iConfig.getUntrackedParameter<edm::VParameterSet>( "triggerflags" , {} );

  for( auto& flag : flags ){
    triggerlist.emplace_back( new GenericTriggerEventFlag(flag, consumesCollector(), *this) );
  }
}

// Booking histograms as required by the DQM
void
SiPixelPhase1Base::bookHistograms(
  DQMStore::IBooker&     iBooker,
  edm::Run const&        run,
  edm::EventSetup const& iSetup )
{
  for( HistogramManager& histoman : histo ){
    histoman.book( iBooker, iSetup );
  }

  // Running trigger flag initialization (per run)
  for( auto& trigger : triggerlist ){
    if( trigger->on() ){
      trigger->initRun( run, iSetup );
    }
  }
}

// trigger checking function
bool
SiPixelPhase1Base::checktrigger(
  const edm::Event&      iEvent,
  const edm::EventSetup& iSetup,
  const unsigned         trgidx ) const
{
  //no triggers loaded
  if (triggerlist.size() == 0) return true;

  // Always return true for MC
  if( !iEvent.isRealData() ) { return true; }

  if ( trgidx >= triggerlist.size() ) { cout << "Trigger index " << trgidx << " not found." << endl; return true; }

  // Always return true is flag is not on;
  if( !triggerlist.at(trgidx)->on() ) { return true; }

  return triggerlist.at(trgidx)->accept( iEvent, iSetup );
}
