#include "buzz_controller_drone_sim.h"
#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include <algorithm>
#include <cmath>
#include <json/json.h>

#include "crm/crminrobotagent_optimised.h"

CProprioceptiveFeatureVector::RobotData CProprioceptiveFeatureVector::m_sRobotData;

namespace buzz_drone_sim {

const std::string RESULT_FILE = "results/result";
const std::string RADIATION_SOURCES_FILE = "data/radiation_sources";
const std::string DATA_TRANSMITTED_FILE = "results/data_transmitted";

/****************************************/
/****************************************/

CBuzzControllerDroneSim::CBuzzControllerDroneSim() : CBuzzControllerKheperaIV(),
  timer_(0), crminAgent_(nullptr) {
   std::chrono::high_resolution_clock::time_point previous = 
      std::chrono::high_resolution_clock::now();
   usleep(10);
   std::chrono::high_resolution_clock::duration duration(
      std::chrono::high_resolution_clock::now() -  previous);

   // Find experiment number and file
   int experiment_number = -1;
   std::string file_name;
   do {
      experiment_number++;
      result_file_name_ = RESULT_FILE + std::to_string( experiment_number ) + ".csv";
   } while( std::ifstream(result_file_name_).good() );
   data_transmitted_file_name_ = DATA_TRANSMITTED_FILE + std::to_string(experiment_number) + ".csv";
   radiation_file_name_ = RADIATION_SOURCES_FILE + std::to_string(experiment_number) + ".json";
}

/****************************************/
/****************************************/

CBuzzControllerDroneSim::~CBuzzControllerDroneSim() {
}

/****************************************/
/****************************************/

void CBuzzControllerDroneSim::Init(TConfigurationNode& t_node) {
   GetNode(*t_node.Parent()->Parent()->Parent()->FirstChildElement(), "experiment")
     .GetAttributeOrDefault("random_seed", &seed_, 907998);


   random_engine_.seed(1168202547 + RobotIdStrToInt());

   crminAgent_ =  new CRMinRobotAgentOptimised(
       RobotIdStrToInt(),
       CProprioceptiveFeatureVector::NUMBER_OF_FEATURES
   );

   CBuzzControllerKheperaIV::Init(t_node);
}

void CBuzzControllerDroneSim::ControlStep() {
  CBuzzControllerKheperaIV::ControlStep();
  ++timer_;
  featureVectors_.erase(featureVectors_.begin(), featureVectors_.end());
}

void CBuzzControllerDroneSim::UpdateFV(int i, unsigned int value) {
  bool ok = false;
  for (auto it = featureVectors_.begin(); it != featureVectors_.end(); ++it) {
    if (it->uFV == value) {
      it->fRobots += 0.1f;
      ok = true;
      break;
    }
  }
  if (!ok && value != 0) {
    featureVectors_.emplace_back(value, 1.0f);
  }
}

const std::list<StructFVsSensed> &CBuzzControllerDroneSim::RunCRM() {
  if (featureVectors_.size() > 0) {
    crminAgent_->SimulationStepUpdatePosition(timer_, &featureVectors_);
  }
  return featureVectors_;
}


/****************************************/
/****************************************/

size_t CBuzzControllerDroneSim::HashString(const std::string data) {
   std::hash<std::string> hashed_string;

   return hashed_string(data);
}

/****************************************/
/****************************************/

bool CBuzzControllerDroneSim::HasReached(const CVector2& position, const float& delta) {
   float difference = std::sqrt(
      std::pow(m_pcPos->GetReading().Position.GetX() - position.GetX(),2)+
      std::pow(m_pcPos->GetReading().Position.GetY() - position.GetY(),2));

   return difference < delta;   
}

/****************************************/
/****************************************/

std::string CBuzzControllerDroneSim::GetCurrentKey(){
   int x = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetX()));
   int y = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetY()));
   std::string key = std::to_string(x) + '_' + std::to_string(y);
   return key;
}

/****************************************/
/****************************************/

float CBuzzControllerDroneSim::GetRadiationIntensity(const int& experimentNumber){
   Json::Value radiationValues;
   Json::Reader reader;
   std::ifstream radiationFile(RADIATION_SOURCES_FILE + std::to_string(experimentNumber) + ".json");

   reader.parse(radiationFile, radiationValues);

   if (radiationValues["sources"].size() <= 0){
      throw JSON_USE_EXCEPTION;
   }
   
   int x = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetX()));
   int y = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetY()));
   
   float totalRadiationIntensity = 0.0;

   for (auto source : radiationValues["sources"]){
      RadiationSource radiation = RadiationSource(source["x"].asFloat(), source["y"].asFloat(), source["intensity"].asFloat());
      totalRadiationIntensity += radiation.GetPerceivedIntensity(x, y);
   }

   // Compute belief elem [0,1]
   float radiation_belief = totalRadiationIntensity; // + noise;
   if (radiation_belief < 0.0) {
      radiation_belief = 0.0;
   } else if (radiation_belief > 1.0) {
      radiation_belief = 1.0;
   }

   return radiation_belief;
}

/****************************************/
/****************************************/

void CBuzzControllerDroneSim::LogDatum(const std::string& key, const float& data, const int& step){
   std::string parsed_key = key;
   std::replace(parsed_key.begin(), parsed_key.end(), '_', ' ');
   std::stringstream ss(parsed_key);
   int x, y;
   ss >> x >> y;

   std::ofstream result_file;
   result_file.open(result_file_name_, std::ios::out | std::ios::app);

   float weight = 1.0;
   result_file << x << "," << y << "," << data << "," << weight << "," << step << "," << m_unRobotId << std::endl;
}

/****************************************/
/****************************************/

void CBuzzControllerDroneSim::LogDataSize(const int& total_data, const int& step){
   
   std::ofstream result_file;
   result_file.open(data_transmitted_file_name_, std::ios::out | std::ios::app);

   result_file << total_data << "," << step << "," << m_unRobotId << std::endl;
}

unsigned CBuzzControllerDroneSim::RobotIdStrToInt() {
  std::string id = GetId();
  id.erase(0, 2);
  std::string::size_type size = 0;
  unsigned outId = std::stoi(id, &size);
  return outId;
}

}
