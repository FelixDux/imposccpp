#ifndef IMPOSC_IMPOSCPY_IMPOSCPY_HPP
#define IMPOSC_IMPOSCPY_IMPOSCPY_HPP

unsigned char map_impacts(double omega, double r, double sigma, unsigned int max_periods,
 double phi, double v, unsigned int num_iterations, const char* outfile, const char* logfile);

unsigned char map_singularity_set(double omega, double r, double sigma, unsigned int max_periods,
 unsigned int num_points, const char* outfile, const char* logfile);

unsigned char map_doa(double omega, double r, double sigma, unsigned int max_periods,
 double max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, 
 unsigned int n_iterations, const char* outfile, const char* logfile);

#endif
