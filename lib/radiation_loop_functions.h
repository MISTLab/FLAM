#ifndef FORAGING_LOOP_FUNCTIONS_H
#define FORAGING_LOOP_FUNCTIONS_H

#include "radiation_source.h"

#include <argos3/core/simulator/loop_functions.h>
#include <argos3/core/simulator/simulator.h>
#include <argos3/core/simulator/entity/floor_entity.h>
#include <argos3/core/utility/math/range.h>
#include <argos3/core/utility/math/rng.h>
#include <argos3/plugins/simulator/entities/cylinder_entity.h>
#include <json/json.h>

#include "buzz_controller_drone_sim.h"

using buzz_drone_sim::RadiationSource;

class CRadiationLoopFunctions : public CLoopFunctions {

public:
    CRadiationLoopFunctions();
    virtual ~CRadiationLoopFunctions();
    virtual void Init(TConfigurationNode &t_tree);
    virtual CColor GetFloorColor(const CVector2 &c_position_on_plane);

    static const std::list<StructFVsSensed> &RunCRM(int id);

private:
    float m_max_intensity_;
    Real m_fRadiationRadius;
    std::vector<CCylinderEntity> m_cVisibleRadiation;
    CFloorEntity *m_floor;
    std::string radiation_file_name_;
    std::string result_file_name_;
    std::vector<RadiationSource> sources;

    static std::map<int, buzz_drone_sim::CBuzzControllerDroneSim*> robots_;

    std::vector<RadiationSource> ReadRadiationSources();
    void AddRadiationCylinder(const RadiationSource source);
};

#endif
