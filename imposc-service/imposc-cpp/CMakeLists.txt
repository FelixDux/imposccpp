cmake_minimum_required(VERSION 3.10)

#set( CMAKE_VERBOSE_MAKEFILE on )

# set the project name and version
project(imposc VERSION 1.0.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Make libraries shared
set(BUILD_SHARED_LIBS True)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Specify the executable
add_executable (imposc main.cpp)

# Enable the thread library
set(THREADS_PREFER_PTHREAD_FLAG ON)
# set(CMAKE_FIND_LIBRARY_SUFFIXES ${CMAKE_STATIC_LIBRARY_SUFFIX})
find_package(Threads REQUIRED)
target_link_libraries(imposc PRIVATE Threads::Threads)

# dynamics
add_subdirectory (dynamics)
# target_link_libraries (imposc PUBLIC dynamics)

# charts
add_subdirectory (charts)
# target_link_libraries (imposc PUBLIC charts)

# Library for Python binding
add_subdirectory (imposcpy)
target_link_libraries (imposc PUBLIC imposcpy)

# Testing
set(CATCH_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/test/catch)
#add_library(Catch2::Catch IMPORTED INTERFACE)
#set_property(TEST Catch2::Catch PROPERTY INTERFACE_INCLUDE_DIRECTORIES "${CATCH_INCLUDE_DIR}")

enable_testing ()
add_subdirectory (test)

install(TARGETS imposcpy LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/libs)
install(TARGETS dynamics LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/libs)
install(TARGETS charts LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/libs)
install(FILES imposcpy/include/imposcpy.hpp DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/libs)

