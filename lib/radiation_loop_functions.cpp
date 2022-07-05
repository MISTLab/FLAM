#include "radiation_loop_functions.h"

#include <map>

#include <argos3/core/simulator/simulator.h>
#include <argos3/plugins/robots/kheperaiv/simulator/kheperaiv_entity.h>

const std::string RADIATION_SOURCES_FILE = "data/radiation_sources";
const std::string RESULT_FILE = "results/result";

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
}

CColor CRadiationLoopFunctions::GetFloorColor(const CVector2 &c_position_on_plane) {
  float x = c_position_on_plane.GetX();
  float y = c_position_on_plane.GetY();
  if (x < -4.0f && y > 6.0f) {
    return CColor(51, 122, 183);
  }
  float intensity = 0.0f;
  for (int i = 0; i < sources.size(); ++i) {
    CVector3 sourceCoord = sources[i].GetCoordinates();
    CVector2 sourcePos(sourceCoord.GetX(), sourceCoord.GetY());
    intensity += sources[i].GetPerceivedIntensity(x, y);
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
