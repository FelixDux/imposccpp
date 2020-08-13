#include "dynamics.hpp"

#include <math.h>

using namespace std;

namespace dynamics {

ChatterChecker::ChatterChecker(const Parameters &parameters, Velocity velocity_threshold, unsigned int count_threshold):
			v_threshold(velocity_threshold),
			c_threshold(count_threshold),
			impact_count(0),
			sticking(parameters)
{
	if (parameters.get_coefficient_of_restitution() < 1 && parameters.get_coefficient_of_restitution() >=0)
	{ 
		can_chatter = true;
		accumulation_time = [parameters] (const Impact &impact) 
		{
			return impact.get_time() - 2*impact.get_velocity() / (1-parameters.get_coefficient_of_restitution()) /
				(cos(impact.get_time() * parameters.get_forcing_frequency()) - parameters.get_obstacle_offset());
		};
	}
	else
	{
		can_chatter = false;
		accumulation_time = [parameters] (const Impact &impact)  {return impact.get_time();};
	}
}

ChatterChecker::ChatterResult ChatterChecker::operator() (const Impact &impact) const
{
	if (can_chatter && impact.get_velocity() < v_threshold)
	{
		if (++impact_count > c_threshold)
		{
			impact_count = 0;
			auto new_time = accumulation_time(impact);

			if (sticking.is_sticking_time(new_time))
			{
				return {.is_chatter = true, .accumulation_impact = Impact(sticking.converter(), new_time, 0)};
			}
		}
	}
	
	return {.is_chatter = false, .accumulation_impact = impact};
}

// Apply the map to an impact
Impact ImpactMap::apply(const Impact &impact) const
{
	vector<StateOfMotion> trajectory = motion.to_next_impact(impact);

	auto state_at_impact = trajectory.back();

	return Impact(motion.converter(), state_at_impact.t, state_at_impact.v);
}

// Iterate the map 
vector<Impact> ImpactMap::iterate(const Impact &impact, unsigned int num_iterations) const
{
	list<Impact> trajectory;

	trajectory.push_back(impact);

	for (unsigned int i=0; i < num_iterations; i++)
	{
		trajectory.push_back(apply(trajectory.back()));

		// Now check for chatter
		auto chatter_result = chatter_checker(trajectory.back());

		if (chatter_result.is_chatter)
		{
			trajectory.push_back(chatter_result.accumulation_impact);
		}
	}

	// We've grown the trajectory as a list but return it as a vector
	vector<Impact> result;
	result.reserve(trajectory.size());
	copy(begin(trajectory), end(trajectory), back_inserter(result));
	return result;
}

// Generate a singularity set
std::vector<Impact> ImpactMap::singularity_set(unsigned int num_points) const
{
	list<Impact> trajectory;

	Time delta_time = motion.converter().get_period()/num_points;

	Time starting_time = 0;

	for (int i=0; i < num_points; i++)
	{
		trajectory.push_back(apply(Impact(motion.converter(), starting_time, 0)));

		starting_time += delta_time;
	}

	// We've grown the trajectory as a list but return it as a vector
	vector<Impact> result;
	result.reserve(trajectory.size());
	copy(begin(trajectory), end(trajectory), back_inserter(result));
	return result;
}
}
