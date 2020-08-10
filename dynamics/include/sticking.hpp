#ifndef IMPOSC_DYNAMICS_STICKING_HPP
#define IMPOSC_DYNAMICS_STICKING_HPP

#include "types.hpp"
#include "parameters.hpp"
#include "forcing_phase.hpp"
#include "impact.hpp"

namespace dynamics
{
	class Sticking
	{
		public:
			struct ReleaseImpact
			{
				bool new_impact;
				Impact impact;
			};

			Sticking(const Parameters &parameters);

			bool never() const {return phase_in == phase_out;}

			bool always() const 
			{
				return 1==phase_in && 0==phase_out;
			}

			bool is_sticking(Phase phi) const
			{
				if (never()) return false;
				if (always()) return true;

				return (phi < phase_out) || (phi >= phase_in );
			}

			bool is_sticking_time(Time time) const
			{
				return is_sticking(
					phase_converter.time_to_phase(time)
					);
			}

			Time release_time(Time time) const
			{
				return phase_converter.forward_to_phase(
						time, phase_out);
			}

			ReleaseImpact check_impact(const Impact &impact) const;

			bool is_valid() const {return phase_converter.is_valid();}

			const PhaseConverter &converter() const {return phase_converter;}

		private:
			Phase phase_in;
			Phase phase_out;
			PhaseConverter phase_converter;
	};

}

#endif
