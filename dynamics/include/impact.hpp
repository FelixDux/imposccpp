#ifndef IMPOSC_DYNAMICS_IMPACT_HPP
#define IMPOSC_DYNAMICS_IMPACT_HPP

/*
 *
 * Each impact is uniquely specified by two parameters:
 * `:phi`: the phase (time modulo and scaled by the forcing period) at
 * which the impact occurs
 * `:v`: the velocity of the impact, which cannot be negative
 *
 * In addition, we also record the actual time `:t`.
 *
 * Because `:phi` is periodic and `:v` non-negative, the surface on which
 * impacts are defined is a half-cylinder. Whether a zero-velocity impact
 * is physically meaningful depends on the value of `:phi` and on `sigma`
 * the offset of the obstacle from the centre of motion.
 */

#include "types.hpp"
#include "forcing_phase.hpp"

namespace dynamics
{
	class Impact
	{
		public:
			// Construction (rule of zero applies)
			Impact(const PhaseConverter &converter,
				Time time, Velocity velocity):
				t(time), v(velocity)
				{
					phi = converter.time_to_phase(t);
				}

			// Accessors
			Phase get_phase() const {return phi;}
			Time get_time() const {return t;}
			Velocity get_velocity() const {return v;}

		private:
			Phase phi;
			Time t;
			Velocity v;
	};
}

#endif
