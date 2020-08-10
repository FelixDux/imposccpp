cmake_minimum_required(VERSION 3.10)

# set the project name and version
project(imposc VERSION 1.0.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Specify the executable
add_executable (imposc main.cpp)

# dynamics
add_subdirectory (dynamics)
target_link_libraries (imposc LINK_PUBLIC dynamics)
