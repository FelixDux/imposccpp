
#include "imposcpy.hpp"
#include "dynamics.hpp"
#include "charts.hpp"
#include "doa_plot.hpp"

using namespace dynamics;
using namespace charts;

bool map_impacts(Frequency omega, Scalar r, Displacement sigma, unsigned int max_periods,
 Phase phi, Velocity v, unsigned int num_iterations, const char* outfile)
{
	try
	{
        Parameters parameters(omega, r, sigma, max_periods);
        
        ImpactMap map(parameters);
        
        plot_impacts(map.iterate(phi, v, num_iterations).impacts, outfile);
	}
	catch (const dynamics::ParameterError &e)
	{
		return false;
	}

    return true;
}

bool map_singularity_set(Frequency omega, Scalar r, Displacement sigma, unsigned int max_periods,
 unsigned int num_points, const char* outfile)
{
	try
	{
        Parameters parameters(omega, r, sigma, max_periods);
        
        ImpactMap map(parameters);
        
        plot_impacts(map.singularity_set(num_points), outfile);
	}
	catch (const dynamics::ParameterError &e)
	{
		return false;
	}

    return true;
}

bool map_doa(Frequency omega, Scalar r, Displacement sigma, unsigned int max_periods,
 Velocity max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, 
 unsigned int n_iterations, const char* outfile)
{
	try
	{
        Parameters parameters(omega, r, sigma, max_periods);

        charts::plot_doa(parameters, max_velocity, n_v_increments, n_phi_increments, n_iterations, outfile);
	}
	catch (const dynamics::ParameterError &e)
	{
		return false;
	}

    return true;
}