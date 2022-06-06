cmake_minimum_required(VERSION 3.10)

project(FLAM LANGUAGES CXX)

find_package(ARGoS REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(JSONCPP jsoncpp)

add_library(buzz_controller_drone SHARED
  lib/buzz_utils.h
  lib/buzz_controller_drone_sim.h
  lib/buzz_controller_drone_sim.cpp
  lib/buzz_closures_drone_sim.cpp
  lib/radiation_source.h
  lib/radiation_source.cpp
)

target_include_directories(buzz_controller_drone PRIVATE
  ${JSONCPP_INCLUDE_DIRS}
)

target_link_libraries(buzz_controller_drone PUBLIC
  ${ARGOS_LIBRARIES}
  ${JSONCPP_LIBRARIES}
)

# Loop functions for visualization
add_library(flam_loop_functions SHARED
  lib/radiation_loop_functions.h
  lib/radiation_loop_functions.cpp
  lib/radiation_source.h
  lib/radiation_source.cpp
)

target_include_directories(flam_loop_functions PRIVATE
  ${JSONCPP_INCLUDE_DIRS}
)

target_link_libraries(flam_loop_functions PUBLIC
  ${JSONCPP_LIBRARIES}
)
