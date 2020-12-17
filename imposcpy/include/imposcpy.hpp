#ifndef IMPOSC_IMPOSCPY_IMPOSCPY_HPP
#define IMPOSC_IMPOSCPY_IMPOSCPY_HPP

#include "types.hpp"

#include <fstream>

bool map_impacts(dynamics::Frequency omega, dynamics::Scalar r, dynamics::Displacement sigma, unsigned int max_periods,
 dynamics::Phase phi, dynamics::Velocity v, unsigned int num_iterations, const char* outfile, const char* logfile);

bool map_singularity_set(dynamics::Frequency omega, dynamics::Scalar r, dynamics::Displacement sigma, unsigned int max_periods,
 unsigned int num_points, const char* outfile, const char* logfile);

bool map_doa(dynamics::Frequency omega, dynamics::Scalar r, dynamics::Displacement sigma, unsigned int max_periods,
 dynamics::Velocity max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, 
 unsigned int n_iterations, const char* outfile, const char* logfile);

class ErrorLogger
{
    public:

    ErrorLogger(const char* logfile):logger(logfile) {}

    void log(const std::string &message)
    {
        logger << message << std::endl;
    }

    private:
        std::ofstream logger;
};

#endif
