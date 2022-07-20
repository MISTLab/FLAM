#ifndef BUZZ_CONTROLLER_DRONE_SIM_H
#define BUZZ_CONTROLLER_DRONE_SIM_H

#include <argos3/plugins/robots/kheperaiv/control_interface/buzz_controller_kheperaiv.h>

#include <random>
#include <chrono>
#include <vector>
#include <list>

#include "crm/featurevectorsinrobotagent.h"

#include "radiation_source.h"

class CRMinRobotAgentOptimised;

namespace buzz_drone_sim {

/*
* Buzz controller
*/
class CBuzzControllerDroneSim : public CBuzzControllerKheperaIV {

public:

   CBuzzControllerDroneSim();
   
   virtual ~CBuzzControllerDroneSim();

   virtual void Init(TConfigurationNode& t_node);

   virtual void ControlStep();

   void UpdateFV(int i, unsigned int value);

   const std::list<StructFVsSensed> &RunCRM();

   // Control functions

   std::default_random_engine& GetRandomEngine()
   {
      return random_engine_;
   }

   size_t HashString(std::string data);

#if 0
   bool HasReached(const CVector2& position, const float& delta);

   std::string GetCurrentKey();

   float GetRadiationIntensity(const int& experimentNumber);
#endif

   void LogDatum(const std::string& key, const float& data, const int& step);
   
   void LogDataSize(const int& total_data, const int& step);

   unsigned RobotIdStrToInt();

protected:

   virtual buzzvm_state RegisterFunctions();

private:

   // Fault detection and robot classification data
   unsigned int timer_;
   CRMinRobotAgentOptimised *crminAgent_;
   std::list<StructFVsSensed> featureVectors_;

   // Radiation source data

   int seed_;
   std::default_random_engine random_engine_;

   std::string result_file_name_, data_transmitted_file_name_, radiation_file_name_;

};
}
#endif
