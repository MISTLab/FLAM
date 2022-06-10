#include "radiation_loop_functions.h"

#include <map>

#include <argos3/core/simulator/simulator.h>
#include <argos3/plugins/robots/kheperaiv/simulator/kheperaiv_entity.h>

#include "buzz_controller_drone_sim.h"

using buzz_drone_sim::CBuzzControllerDroneSim;

const std::string RADIATION_SOURCES_FILE = "data/radiation_sources";
const std::string RESULT_FILE = "results/result";

std::map<int, CBuzzControllerDroneSim*> CRadiationLoopFunctions::robots_;

/****************************************/
/****************************************/

CRadiationLoopFunctions::CRadiationLoopFunctions() : CLoopFunctions(), m_max_intensity_(0.0f) {
    // Find experiment number and file
    int experiment_number = -1;
    do
    {
        experiment_number++;
        result_file_name_ = RESULT_FILE + std::to_string(experiment_number) + ".csv";
    } while (std::ifstream(result_file_name_).good());
    radiation_file_name_ = RADIATION_SOURCES_FILE + std::to_string(experiment_number) + ".json";

    sources = this->ReadRadiationSources();
}

CRadiationLoopFunctions::~CRadiationLoopFunctions() {
}

void CRadiationLoopFunctions::Init(TConfigurationNode &t_node) {
    m_floor = &GetSpace().GetFloorEntity();
    try {
        /* Get the radius of radiation items from XML */
        TConfigurationNode &tRadiation = GetNode(t_node, "radiation");
        GetNodeAttribute(tRadiation, "radius", m_fRadiationRadius);

        for (auto source : this->sources) {
           AddRadiationCylinder(source);
        }
    } catch (CARGoSException &ex) {
        THROW_ARGOSEXCEPTION_NESTED("Error parsing loop functions!", ex);
    }

    // Store initialized robots
    CSpace::TMapPerType &robots = GetSpace().GetEntitiesByType("kheperaiv");
    for (CSpace::TMapPerType::iterator it = robots.begin();
        it != robots.end(); ++it) {
      CKheperaIVEntity *bot = any_cast<CKheperaIVEntity*>(it->second);
      CBuzzControllerDroneSim &controller =
        dynamic_cast<CBuzzControllerDroneSim&>(
            bot->GetControllableEntity().GetController()
        );
      robots_[controller.RobotIdStrToInt()] = &controller;
    }
}

CColor CRadiationLoopFunctions::GetFloorColor(const CVector2 &c_position_on_plane) {
  float intensity = 0.0f;
  for (int i = 0; i < sources.size(); ++i) {
    CVector3 sourceCoord = sources[i].GetCoordinates();
    CVector2 sourcePos(sourceCoord.GetX(), sourceCoord.GetY());
    intensity += sources[i].GetPerceivedIntensity(
        c_position_on_plane.GetX(),
        c_position_on_plane.GetY()
    );
  }
  if (intensity > m_max_intensity_) {
    m_max_intensity_ = intensity;
  }
  float ratio = intensity / m_max_intensity_;
  const CVector3 red(255, 0, 0);
  const CVector3 grey(128, 128, 128);
  CVector3 color = ratio * red + (1.0f - ratio) * grey;
  return CColor(color.GetX(), color.GetY(), color.GetZ());
}

const std::list<StructFVsSensed> &CRadiationLoopFunctions::RunCRM(int id) {
  return robots_[id]->RunCRM();
}

void CRadiationLoopFunctions::AddRadiationCylinder(RadiationSource source) {
    CCylinderEntity* cylinder = new CCylinderEntity("c" + source.ToString(),
                                                    source.GetCoordinates(),
                                                    CQuaternion(),
                                                    false,
                                                    m_fRadiationRadius,
                                                    1.0);

   AddEntity(*cylinder);
   m_floor->SetChanged();
}

std::vector<RadiationSource> CRadiationLoopFunctions::ReadRadiationSources() {
    Json::Value radiationValues;
    Json::Reader reader;
    std::ifstream radiationFile(radiation_file_name_);
    std::vector<RadiationSource> sources;

    reader.parse(radiationFile, radiationValues);
    if (radiationValues["sources"].size() <= 0) {
        throw JSON_USE_EXCEPTION;
    }

    for (auto source : radiationValues["sources"]) {
        sources.push_back(RadiationSource(source["x"].asFloat(), source["y"].asFloat(), source["intensity"].asFloat()));
    }

    return sources;
}

/****************************************/
/****************************************/

REGISTER_LOOP_FUNCTIONS(CRadiationLoopFunctions, "radiation_loop_functions")
