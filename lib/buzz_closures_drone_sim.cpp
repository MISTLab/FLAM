#include "buzz_controller_drone_sim.h"

#include "buzz_utils.h"
#if 0
#include "radiation_loop_functions.h"
#endif

using namespace buzz_utils;

namespace buzz_drone_sim {

/****************************************/
/****************************************/

static int BuzzRandUniform(buzzvm_t vm){

   buzzvm_lload(vm, 1);
   buzzvm_lload(vm, 2);
   buzzobj_t buzz_range_lowest = buzzvm_stack_at(vm, 2);
   buzzobj_t buzz_range_highest = buzzvm_stack_at(vm, 1);
   float range_lowest, range_highest;

   if(buzz_range_lowest->o.type == BUZZTYPE_FLOAT) range_lowest = buzz_range_lowest->f.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "uniform(x,y): expected %s, got %s in first argument",
                      buzztype_desc[BUZZTYPE_FLOAT],
                      buzztype_desc[buzz_range_lowest->o.type]
         );
      return vm->state;
   } 
   if(buzz_range_highest->o.type == BUZZTYPE_FLOAT) range_highest = buzz_range_highest->f.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "uniform(x,y): expected %s, got %s in first argument",
                      buzztype_desc[BUZZTYPE_FLOAT],
                      buzztype_desc[buzz_range_highest->o.type]
         );
      return vm->state;
   } 

   std::uniform_real_distribution<float> distribution(range_lowest, range_highest);

   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);
   
   /* Call function */
   float random_value = distribution(
      reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->GetRandomEngine());

   buzzvm_pushf(vm, random_value);

   return buzzvm_ret1(vm);
}

/****************************************/
/****************************************/

static int BuzzRandGauss(buzzvm_t vm){

   buzzvm_lload(vm, 1);
   buzzvm_lload(vm, 2);
   buzzobj_t buzz_mean = buzzvm_stack_at(vm, 2);
   buzzobj_t buzz_stdev = buzzvm_stack_at(vm, 1);
   int mean, stdev;

   if(buzz_mean->o.type == BUZZTYPE_INT) mean = buzz_mean->i.value;
   else if(buzz_mean->o.type == BUZZTYPE_FLOAT) mean = (int)buzz_mean->f.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "gauss(x,y): expected %s, got %s in first argument",
                      buzztype_desc[BUZZTYPE_INT],
                      buzztype_desc[buzz_mean->o.type]
         );
      return vm->state;
   } 
   if(buzz_stdev->o.type == BUZZTYPE_INT) stdev = buzz_stdev->i.value;
   else if(buzz_stdev->o.type == BUZZTYPE_FLOAT) stdev = (int)buzz_stdev->f.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "gauss(x,y): expected %s, got %s in first argument",
                      buzztype_desc[BUZZTYPE_INT],
                      buzztype_desc[buzz_stdev->o.type]
         );
      return vm->state;
   } 
   std::normal_distribution<float> distribution(mean, stdev);
   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);
   /* Call function */
   float random_value = distribution(
      reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->GetRandomEngine());

   buzzvm_pushf(vm, random_value);

   return buzzvm_ret1(vm);
}

/****************************************/
/****************************************/

static int BuzzHashString(buzzvm_t vm){
   /* Push the string */
   buzzvm_lload(vm, 1);

   /* Create the string */
   std::string data_string = buzzvm_stack_at(vm, 1)->s.value.str;

   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);

   /* Call function */
   size_t hashed_string = 
      reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->HashString(data_string);
   
   buzzvm_pushi(vm, hashed_string);

   return buzzvm_ret1(vm);
}

/****************************************/
/****************************************/

#if 0
static int BuzzHasReached(buzzvm_t vm) {
   /* Push the vector components */
   buzzvm_lload(vm, 1);
   buzzvm_lload(vm, 2);
   buzzvm_lload(vm, 3);
   /* Create a new vector with that */
   CVector2 position;
   float delta;
   buzzobj_t tX = buzzvm_stack_at(vm, 3);
   buzzobj_t tY = buzzvm_stack_at(vm, 2);
   buzzobj_t tDelta = buzzvm_stack_at(vm, 1);
   if(tX->o.type == BUZZTYPE_FLOAT) position.SetX(tX->f.value);
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "goto_abs(x,y): expected %s, got %s in first argument",
                      buzztype_desc[BUZZTYPE_FLOAT],
                      buzztype_desc[tX->o.type]
         );
      return vm->state;
   }      
   if(tY->o.type == BUZZTYPE_FLOAT) position.SetY(tY->f.value);
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "goto_abs(x,y): expected %s, got %s in second argument",
                      buzztype_desc[BUZZTYPE_FLOAT],
                      buzztype_desc[tY->o.type]
         );
      return vm->state;
   }
   if(tDelta->o.type == BUZZTYPE_FLOAT) delta = tDelta->f.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "goto_abs(x,y): expected %s, got %s in second argument",
                      buzztype_desc[BUZZTYPE_FLOAT],
                      buzztype_desc[tDelta->o.type]
         );
      return vm->state;
   }
   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);
   /* Call function */
   bool has_reached = 
      reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->HasReached(position, delta);
   
   buzzvm_pushi(vm, (int) has_reached);

   return buzzvm_ret1(vm);
}
#endif

/****************************************/
/****************************************/

#if 0
static int BuzzGetCurrentKey(buzzvm_t vm){
   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);
   /* Call function */
   std::string key_value =
      reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->GetCurrentKey();

   buzzvm_pushs(vm, buzzvm_string_register(vm, key_value.c_str(), 1));

   return buzzvm_ret1(vm);
}
#endif

/****************************************/
/****************************************/

#if 0
static int BuzzGetRadiationIntensity(buzzvm_t vm){
   /* Get experiment number */
   buzzvm_lload(vm, 1);
   buzzobj_t buzzExperimentNumber = buzzvm_stack_at(vm, 1);
   int experimentNumber = buzzExperimentNumber->i.value;

   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);
   /* Call function */
   float radiationIntensity = 
      reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->GetRadiationIntensity(experimentNumber);
   
   buzzvm_pushf(vm, radiationIntensity);

   return buzzvm_ret1(vm);
}
#endif

/****************************************/
/****************************************/

static int BuzzLogDatum(buzzvm_t vm){
   /* Push the vector components */
   buzzvm_lload(vm, 1);
   buzzvm_lload(vm, 2);
   buzzvm_lload(vm, 3);
   /* Create a new vector with that */
   std::string key;
   float data;
   int step;
   buzzobj_t tkey = buzzvm_stack_at(vm, 3);
   buzzobj_t tdata = buzzvm_stack_at(vm, 2);
   buzzobj_t tstep = buzzvm_stack_at(vm, 1);
   if(tkey->o.type == BUZZTYPE_STRING) key = tkey->s.value.str;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "log_datum(key,data,step): expected %s, got %s in first argument",
                      buzztype_desc[BUZZTYPE_STRING],
                      buzztype_desc[tkey->o.type]
         );
      return vm->state;
   }      
   if(tdata->o.type == BUZZTYPE_FLOAT) data = tdata->f.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "log_datum(key,data,step): expected %s, got %s in second argument",
                      buzztype_desc[BUZZTYPE_FLOAT],
                      buzztype_desc[tdata->o.type]
         );
      return vm->state;
   }
   if(tstep->o.type == BUZZTYPE_INT) step = tstep->i.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "log_datum(key,data,step): expected %s, got %s in second argument",
                      buzztype_desc[BUZZTYPE_INT],
                      buzztype_desc[tstep->o.type]
         );
      return vm->state;
   }

   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);
   /* Call function */
   reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->LogDatum(key, data, step);

   return buzzvm_ret0(vm);
}

/****************************************/
/****************************************/

static int BuzzLogDataSize(buzzvm_t vm){
   /* Push the vector components */
   buzzvm_lload(vm, 1);
   buzzvm_lload(vm, 2);
   /* Create a new vector with that */
   std::string key;
   float data;
   int step;
   int total_data;
   buzzobj_t ttotal = buzzvm_stack_at(vm, 2);
   buzzobj_t tstep = buzzvm_stack_at(vm, 1);
   if(tstep->o.type == BUZZTYPE_INT) step = tstep->i.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "log_datum(key,data,step): expected %s, got %s in second argument",
                      buzztype_desc[BUZZTYPE_INT],
                      buzztype_desc[tstep->o.type]
         );
      return vm->state;
   }
   if(ttotal->o.type == BUZZTYPE_INT) total_data = ttotal->i.value;
   else {
      buzzvm_seterror(vm,
                      BUZZVM_ERROR_TYPE,
                      "log_datum(key,data,step): expected %s, got %s in second argument",
                      buzztype_desc[BUZZTYPE_INT],
                      buzztype_desc[ttotal->o.type]
         );
      return vm->state;
   }

   /* Get pointer to the controller */
   buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
   buzzvm_gload(vm);
   /* Call function */
   reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value)->LogDataSize(total_data, step);

   return buzzvm_ret0(vm);
}

static int BuzzUpdateFV(buzzvm_t vm) {
  buzzvm_lload(vm, 1);

  buzzobj_t inputValues = buzzvm_stack_at(vm, 1);
  if (inputValues->o.type != BUZZTYPE_TABLE) {
    buzzvm_seterror(vm,
                    BUZZVM_ERROR_TYPE,
                    "update_fv(values): expected %s, got %s in first argument",
                    buzztype_desc[BUZZTYPE_TABLE],
                    buzztype_desc[inputValues->o.type]
    );
    return vm->state;
  }

  buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
  buzzvm_gload(vm);
  CBuzzControllerDroneSim *controller = reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value);

  int i = 0;
  buzzvm_push(vm, inputValues);
  buzzvm_pushi(vm, i);
  buzzvm_tget(vm);
  while (!buzzobj_isnil(buzzvm_stack_at(vm, 1))) {
    int value = buzzvm_stack_at(vm, 1)->i.value;
    controller->UpdateFV(i++, static_cast<unsigned int>(value));
    buzzvm_push(vm, inputValues);
    buzzvm_pushi(vm, i);
    buzzvm_tget(vm);
  }

  return buzzvm_ret0(vm);
}

static int BuzzRunCRM(buzzvm_t vm) {
  buzzvm_pushs(vm, buzzvm_string_register(vm, "controller", 1));
  buzzvm_gload(vm);

  CBuzzControllerDroneSim *controller = reinterpret_cast<CBuzzControllerDroneSim*>(buzzvm_stack_at(vm, 1)->u.value);
  const std::list<StructFVsSensed> &featureVectors = controller->RunCRM();

  buzzobj_t result = buzzheap_newobj(vm, BUZZTYPE_TABLE);

  for (auto it = featureVectors.cbegin(); it != featureVectors.cend(); ++it) {
    buzzvm_push(vm, result);
    buzzvm_pushi(vm, it->uFV);
    buzzvm_pushi(vm, it->uMostWantedState);
    buzzvm_tput(vm);
  }

  buzzvm_push(vm, result);
  return buzzvm_ret1(vm);
}

/****************************************/
/************ Registration **************/
/****************************************/

buzzvm_state CBuzzControllerDroneSim::RegisterFunctions() {
   CBuzzControllerKheperaIV::RegisterFunctions();

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "FLAM_SEED", 1));
   buzzvm_pushi(m_tBuzzVM, seed_);
   buzzvm_gstore(m_tBuzzVM);

#if ARGOS_BUILD_FOR == "khiv"
   // Initialize sensor variables
   buzzobj_t position = buzzheap_newobj(m_tBuzzVM, BUZZTYPE_TABLE);

   buzzvm_push(m_tBuzzVM, position);
   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "x", 1));
   buzzvm_pushf(m_tBuzzVM, 0.0);
   buzzvm_tput(m_tBuzzVM);

   buzzvm_push(m_tBuzzVM, position);
   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "y", 1));
   buzzvm_pushf(m_tBuzzVM, 0.0);
   buzzvm_tput(m_tBuzzVM);

   buzzobj_t orientation = buzzheap_newobj(m_tBuzzVM, BUZZTYPE_TABLE);

   buzzvm_push(m_tBuzzVM, orientation);
   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "yaw", 1));
   buzzvm_pushf(m_tBuzzVM, 0.0);
   buzzvm_tput(m_tBuzzVM);

   buzzobj_t pose = buzzheap_newobj(m_tBuzzVM, BUZZTYPE_TABLE);
   buzzvm_push(m_tBuzzVM, pose);
   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "position", 1));
   buzzvm_push(m_tBuzzVM, position);
   buzzvm_tput(m_tBuzzVM);

   buzzvm_push(m_tBuzzVM, pose);
   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "orientation", 1));
   buzzvm_push(m_tBuzzVM, orientation);
   buzzvm_tput(m_tBuzzVM);

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "pose", 1));
   buzzvm_push(m_tBuzzVM, pose);
   buzzvm_gstore(m_tBuzzVM);
#endif

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "uniform", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzRandUniform));
   buzzvm_gstore(m_tBuzzVM);

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "gauss", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzRandGauss));
   buzzvm_gstore(m_tBuzzVM);

#if 0
   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "has_reached", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzHasReached));
   buzzvm_gstore(m_tBuzzVM);
#endif

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "hash_string", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzHashString));
   buzzvm_gstore(m_tBuzzVM);

#if 0
   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "get_current_key", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzGetCurrentKey));
   buzzvm_gstore(m_tBuzzVM);

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "get_radiation_intensity", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzGetRadiationIntensity));
   buzzvm_gstore(m_tBuzzVM);
#endif

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "log_datum", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzLogDatum));
   buzzvm_gstore(m_tBuzzVM);

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "log_datasize", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzLogDataSize));
   buzzvm_gstore(m_tBuzzVM);

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "update_fv", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzUpdateFV));
   buzzvm_gstore(m_tBuzzVM);

   buzzvm_pushs(m_tBuzzVM, buzzvm_string_register(m_tBuzzVM, "run_crm", 1));
   buzzvm_pushcc(m_tBuzzVM, buzzvm_function_register(m_tBuzzVM, BuzzRunCRM));
   buzzvm_gstore(m_tBuzzVM);

   return m_tBuzzVM->state;
}

/****************************************/
/****************************************/

REGISTER_CONTROLLER(CBuzzControllerDroneSim, "buzz_controller_drone_sim");

}
