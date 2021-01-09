# distutils: sources = ../../imposc-cpp/charts/src/charts.cpp  ../../imposc-cpp/dynamics/src/dynamics.cpp  ../../imposc-cpp/dynamics/src/motion.cpp  ../../imposc-cpp/imposcpy/src/imposcpy.cpp  ../../imposc-cpp/charts/src/doa_plot.cpp ../../imposc-cpp/dynamics/src/forcing_phase.cpp ../../imposc-cpp/dynamics/src/sticking.cpp
# distutils: include_dirs= ../../imposc-cpp/charts/include/  ../../imposc-cpp/dynamics/include/  ../../imposc-cpp/imposcpy/include/
# distutils: language = c++
# cython: language_level=3
# cython: extra_compile_args ="-std=c++17"

cdef extern from "imposcpy.hpp":
    unsigned char map_impacts(double omega, double r, double sigma, unsigned int max_periods, double phi, double v, unsigned int num_iterations, const char* outfile, const char* logfile)

def impacts(omega, r, sigma, max_periods, phi, v, num_iterations, outfile, logfile):
    return map_impacts(omega, r, sigma, max_periods, phi, v, num_iterations, outfile, logfile)

cdef extern from "imposcpy.hpp":
    unsigned char map_singularity_set(double omega, double r, double sigma, unsigned int max_periods,unsigned int num_points, const char* outfile, const char* logfile)

def singularity_set(omega, r, sigma, max_periods, num_points, outfile, logfile):
    return map_singularity_set(omega, r, sigma, max_periods, num_points, outfile, logfile)

cdef extern from "imposcpy.hpp":
    unsigned char map_doa(double omega, double r, double sigma, unsigned int max_periods, double max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, unsigned int n_iterations, const char* outfile, const char* logfile)

def doa(omega, r, sigma, max_periods, max_velocity, n_v_increments, n_phi_increments, n_iterations, outfile, logfile):
    return map_doa(omega, r, sigma, max_periods, max_velocity, n_v_increments, n_phi_increments, n_iterations, outfile, logfile)