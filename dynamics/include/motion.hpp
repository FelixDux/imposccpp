#ifndef IMPOSC_DYNAMICS_MOTION_HPP
#define IMPOSC_DYNAMICS_MOTION_HPP

/*
 * Classes for time evolution of the system from one impact to the next
 */

#include "types.hpp"
#include "parameters.hpp"
#include "impact.hpp"
#include "sticking.hpp"

#include <vector>
#include <list>

namespace dynamics
{
	struct StateOfMotion 
	/* State and phase variables for the motion between impacts */
	{ 
		Time t; 
		Displacement x; 
		Velocity v;
	};

	typedef std::vector<StateOfMotion> Trajectory;

	class MotionAtTime
	{
		/*
		 * Coefficients for time evolution of 
		 * the system from one impact to the next 
		 */
		public:
			// Construction (rule of zero applies)
			MotionAtTime(const Parameters &parameters);

			void reset_impact(const Impact &impact) const;

			StateOfMotion operator() (Time time) const;

			bool is_valid() const {return params.forcing_frequency != 0;}

			const Parameters &parameters() const {return params;}

		private: 
			Scalar gamma;
			Parameters params;
			mutable Time impact_time;
			mutable Scalar cos_coefficient;
			mutable Scalar sin_coefficient;
	};

	struct SearchParameters
	{
		Time initial_step_size;
		Time minimum_step_size;
	};

	class MotionBetweenImpacts
	{
		/*
		 * Generates a trajectory from one impact to the next
		 */
		public:
			// Construction (rule of zero applies)
			MotionBetweenImpacts(const Parameters &parameters,
					SearchParameters search_parameters={.initial_step_size=0.1, .minimum_step_size=0.000001}):
					sticking(parameters),
					search(search_parameters),
					offset(parameters.obstacle_offset),
					motion(parameters) {};

			std::vector<StateOfMotion> to_next_impact(const Impact &impact) const;

			bool is_valid() const {return sticking.is_valid() && motion.is_valid();}

			const PhaseConverter& converter() const {return sticking.converter();}

		private:

			MotionBetweenImpacts &initialise_motion(const Impact &impact) const;

			MotionAtTime motion;
			Sticking sticking;
			SearchParameters search;
			Displacement offset;

			mutable std::list<StateOfMotion> trajectory;

	};

}

#endif

