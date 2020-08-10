#ifndef IMPOSC_DYNAMICS_PARAMETERS_HPP
#define IMPOSC_DYNAMICS_PARAMETERS_HPP

/*
 * parameters which define a 1-d impact oscillator system with no damping 
 * between impacts
 *
 */

#include "types.hpp"

namespace dynamics
{
	struct Parameters
	{
		Frequency forcing_frequency;
		Scalar coefficient_of_restitution;
		Displacement obstacle_offset;
	};
}

#endif
