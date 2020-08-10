#include "sticking.hpp"


#include <cmath>

using namespace dynamics;

Sticking::Sticking(const Parameters &parameters):phase_converter(parameters.forcing_frequency)
{
	if (1 <= parameters.obstacle_offset)
	{
		// No sticking
		phase_in = 0;
		phase_out = 0;
	}
	else if (-1 >= parameters.obstacle_offset ||
			!phase_converter.is_valid()) // Traps case of forcing_frequency==0
	{
		// Sticking for all phases
		phase_in = 1;
		phase_out = 0;
	}
	else
	{ 
		// (OK to divide by forcing_frequency because zero case trapped above)
		auto angle = acos(parameters.obstacle_offset); 
		auto phase1 = angle/parameters.forcing_frequency; 
		auto phase2 = (2 * M_PI - angle)/parameters.forcing_frequency;

		if (sin(angle) < 0)
		{
			phase_in = phase1;
			phase_out = phase2;
		}
		else
		{
			phase_in = phase2;
			phase_out = phase1;
		}
	}
}

Sticking::ReleaseImpact Sticking::check_impact(const Impact &impact) const
{

	if (is_valid() && impact.get_velocity() == 0 && is_sticking(impact.get_phase()))
	{
		return {.new_impact = true, .impact = Impact(phase_converter, release_time(impact.get_time()), 0)};
	}
	else
	{
		return {.new_impact = false, .impact = impact};
	}
}
