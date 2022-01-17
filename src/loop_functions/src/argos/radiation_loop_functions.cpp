#include "radiation_loop_functions.h"

const std::string RADIATION_SOURCES_FILE = "data/radiation_sources";
const std::string RESULT_FILE = "results/result";

/****************************************/
/****************************************/

CRadiationLoopFunctions::CRadiationLoopFunctions() : CLoopFunctions() {
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

void CRadiationLoopFunctions::AddRadiationCylinder(RadiationSource source) {
    CCylinderEntity* cylinder = new CCylinderEntity("c" + source.ToString(),
                                                    source.GetCoordinates(),
                                                    CQuaternion(),
                                                    false,
                                                    m_fRadiationRadius,
                                                    1.0);

   AddEntity(*cylinder);
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