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

