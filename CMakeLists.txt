cmake_minimum_required(VERSION 3.10)

project(FLAM LANGUAGES CXX)

find_package(ARGoS REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(JSONCPP jsoncpp)

add_library(buzz_controller_drone STATIC
  lib/buzz_utils.h
  lib/buzz_controller_drone_sim.h
  lib/buzz_controller_drone_sim.cpp
  lib/buzz_closures_drone_sim.cpp
  lib/radiation_source.h
  lib/radiation_source.cpp
  lib/crm/celldatacontainers.h
  lib/crm/celldatacontainers.cpp
  lib/crm/crminrobotagent_optimised.h
  lib/crm/crminrobotagent_optimised.cpp
  lib/crm/propriofeaturevector.h
  lib/crm/propriofeaturevector.cpp
)

target_include_directories(buzz_controller_drone PRIVATE
  ${ARGOS_INCLUDE_DIRS}
  ${JSONCPP_INCLUDE_DIRS}
)

target_link_libraries(buzz_controller_drone PUBLIC
  ${ARGOS_LIBRARIES}
  ${JSONCPP_LIBRARIES}
)

if(ARGOS_BUILD_FOR STREQUAL "khiv")
  add_executable(FLAM ${ARGOS_INCLUDE_DIRS}/argos3/plugins/robots/kheperaiv/real_robot/main.cpp)
  target_include_directories(FLAM PUBLIC ${ARGOS_INCLUDE_DIRS} ${JSONCPP_INCLUDE_DIRS})
  target_link_directories(FLAM PUBLIC ${ARGOS_LIBRARY_DIR})
  target_link_libraries(FLAM PUBLIC
    khepera
    pthread
    dl
    -Wl,--whole-archive
    buzz_controller_drone
    -Wl,--no-whole-archive
    argos3plugin_khiv_kheperaiv
    argos3plugin_khiv_buzz
    argos3plugin_khiv_genericrobot
    argos3core_khiv
    buzzdbg
    buzz
  )
else(ARGOS_BUILD_FOR STREQUAL "khiv")
  # Loop functions for visualization
  add_library(flam_loop_functions SHARED
    lib/radiation_loop_functions.h
    lib/radiation_loop_functions.cpp
    lib/radiation_source.h
    lib/radiation_source.cpp
  )

  target_include_directories(flam_loop_functions PRIVATE
    ${ARGOS_INCLUDE_DIRS}
    ${JSONCPP_INCLUDE_DIRS}
  )

  target_link_libraries(flam_loop_functions PUBLIC
    ${ARGOS_LIBRARIES}
    ${JSONCPP_LIBRARIES}
  )
endif(ARGOS_BUILD_FOR STREQUAL "khiv")
