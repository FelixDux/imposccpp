#ifndef IMPOSC_DYNAMICS_IMPACT_MAP_HPP
#define IMPOSC_DYNAMICS_IMPACT_MAP_HPP

#include "impact.hpp"
#include "parameters.hpp"
#include "motion.hpp"
#include "forcing_phase.hpp"


#include <list>
#include <vector>
#include <functional>

namespace dynamics
{
	class ChatterChecker
	{
		/* 
		 * Detects and numerically approximates 'Chatter', which is when an infinite sequence of impacts accumulates 
		 * in a finite time on a 'sticking' impact. It is the analogue in this system to a real-world situation in 
		 * which the mass judders against the stop. To handle it numerically it is necessary to detect when it is 
		 * happening and then extrapolate forward to the accumulation point.
		 */
		public:
			struct ChatterResult
			{
				bool is_chatter;
				Impact accumulation_impact;
			};

			ChatterChecker(const Parameters &parameters, Velocity velocity_threshold=0.05, unsigned int count_threshold=10);

			ChatterResult operator() (const Impact &impact) const;

		private:
			Velocity v_threshold;
			unsigned int c_threshold;
			Sticking sticking;
			std::function<Time(const Impact&)> accumulation_time;
			bool can_chatter;

			mutable unsigned int impact_count;
	};

	class ImpactMap
	{
		/*
		 * Transformation of the impact surface (an infinite half cylinder parametrised by phase and velocity)
		 * which maps impacts to impacts
		 */

		public:
			// Construction (rule of zero applies)
			ImpactMap(const Parameters &parameters):motion(parameters),chatter_checker(parameters) {}

			// Apply the map to an impact
			Impact apply(const Impact &impact) const;

			// Iterate the map 
			std::vector<Impact> iterate(const Impact &impact, unsigned int num_iterations) const;
			// Convenient overload
			std::vector<Impact> iterate(Phase phi, Velocity v, unsigned int num_iterations) const
			{
				auto t = motion.converter().time_into_cycle(phi);
				Impact impact(motion.converter(), t, v);
				return iterate(impact, num_iterations);
			};

			// Generate a singularity set
			std::vector<Impact> singularity_set(unsigned int num_points) const;

			// Accessors
			bool is_valid() const {return motion.is_valid();}

			PhaseConverter converter() const {return motion.converter();}

		private:
			MotionBetweenImpacts motion;
			ChatterChecker chatter_checker;
	};
}

#endif
