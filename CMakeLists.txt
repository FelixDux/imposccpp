cmake_minimum_required(VERSION 3.10)

#set( CMAKE_VERBOSE_MAKEFILE on )

# set the project name and version
project(imposc VERSION 1.0.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Specify the executable
add_executable (imposc main.cpp)

# dynamics
add_subdirectory (dynamics)
target_link_libraries (imposc PUBLIC dynamics)

# charts
add_subdirectory (charts)
target_link_libraries (imposc PUBLIC charts)

# Testing
set(CATCH_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/test/catch)
#add_library(Catch2::Catch IMPORTED INTERFACE)
#set_property(TEST Catch2::Catch PROPERTY INTERFACE_INCLUDE_DIRECTORIES "${CATCH_INCLUDE_DIR}")

enable_testing ()
add_subdirectory (test)

