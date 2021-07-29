#ifndef FORAGING_LOOP_FUNCTIONS_H
#define FORAGING_LOOP_FUNCTIONS_H

#include "../../../controller/src/argos/radiation_source.h"

#include <argos3/core/simulator/loop_functions.h>
#include <argos3/core/simulator/simulator.h>
#include <argos3/core/utility/math/range.h>
#include <argos3/core/utility/math/rng.h>
#include <argos3/plugins/simulator/entities/cylinder_entity.h>
#include <json/json.h>

using namespace argos;
using namespace buzz_drone_sim;

class CRadiationLoopFunctions : public CLoopFunctions {

public:
    CRadiationLoopFunctions();
    virtual ~CRadiationLoopFunctions();
    virtual void Init(TConfigurationNode &t_tree);

private:
    Real m_fRadiationRadius;
    std::vector<CCylinderEntity> m_cVisibleRadiation;
    std::string radiation_file_name_;
    std::string result_file_name_;
    std::vector<RadiationSource> sources;

    std::vector<RadiationSource> ReadRadiationSources();
    void AddRadiationCylinder(const RadiationSource source);
};

#endif