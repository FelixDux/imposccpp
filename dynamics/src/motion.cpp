#include "motion.hpp"

#include <math.h>

using namespace dynamics;
using namespace std;

MotionAtTime::MotionAtTime(const Parameters &parameters) : 
		params(parameters), impact_time(0),cos_coefficient(0),sin_coefficient(0)
{
	if (0 != params.forcing_frequency)
	{
		gamma = 1.0/(1 - pow(params.forcing_frequency,2));
	}
	else
	{
		gamma = 1;
	}
}

void MotionAtTime::reset_impact(const Impact &impact) const
{
	impact_time = impact.get_time();

	cos_coefficient = params.obstacle_offset - gamma * cos(impact_time);
	
	sin_coefficient = -(params.coefficient_of_restitution * impact.get_velocity()) 
		- params.forcing_frequency * gamma * sin(impact_time); 
}
			
StateOfMotion MotionAtTime::operator() (Time time) const
{ 
	auto lambda = time - impact_time;

	auto cos_lambda = cos(lambda);
	auto sin_lambda = sin(lambda);

	return StateOfMotion {.t = time,
		.x = cos_coefficient * cos_lambda + 
			sin_coefficient * sin_lambda + 
			gamma * cos ( time * params.forcing_frequency),
		.v = sin_coefficient * cos_lambda - 
			cos_coefficient * sin_lambda - 
			params.forcing_frequency * gamma * sin ( time * params.forcing_frequency) 
	};
}
			
MotionBetweenImpacts &MotionBetweenImpacts::initialise_motion(const Impact &impact) const
{
	trajectory.clear();

	trajectory.push_back( {.t = impact.get_time(), .x = motion.parameters().obstacle_offset, .v = impact.get_velocity()});
	
	auto release_impact = sticking.check_impact(impact);

	if (motion.is_valid())
	{
		motion.reset_impact(release_impact.impact);

		if (release_impact.new_impact)
		{
			trajectory.push_back( {.t = release_impact.impact.get_time(), .x = motion.parameters().obstacle_offset, .v = impact.get_velocity()});
		}
	}
}

vector<StateOfMotion> MotionBetweenImpacts::to_next_impact(const Impact &impact) const
{
	initialise_motion(impact);

	auto step_size = search.initial_step_size;

	auto current_time = trajectory.back().t;

	while (fabs(step_size) > search.minimum_step_size)
	{
		current_time += step_size;

		auto current_state = motion(current_time);

		// Update step size - this is the bisection search algorithm
		if (current_state.x <= offset)
		{
			// only record the state if it is physical (i.e. non-penetrating)
			trajectory.push_back(current_state);

			if (step_size < 0)
			{
				step_size *= -0.5;
			}
		}
		else
		{
			if (step_size > 0)
			{
				step_size *= -0.5;
			}
		}
	}

	// We've grown the trajectory as a list but return it as a vector
	vector<StateOfMotion> result;
	result.reserve(trajectory.size());
	copy(begin(trajectory), end(trajectory), back_inserter(result));
	return result;
}
