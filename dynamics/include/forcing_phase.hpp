#ifndef IMPOSC_DYNAMICS_FORCING_PHASE_HPP
#define IMPOSC_DYNAMICS_FORCING_PHASE_HPP

/*
 * Functions and classes for converting between simulated time and
 * phase relative to a forcing cycle, which define as:
 *
 * phase = (time / forcing_period) mod 1
 *
 */

#include "types.hpp"

namespace dynamics
{
	class PhaseConverter
	{
		public:
			// Validity
			enum class Validity
			{
				valid,
				negative_frequency,
				zero_frequency
			};

			// Construction ("rule of zero" applies)
			PhaseConverter(Frequency omega);


			// Accessors
			bool is_valid() const {return (validity == Validity::valid);}
			Validity get_validity() const {return validity;}
			Frequency get_frequency() const {return frequency;}
			Time get_period() const {return period;}

			// Conversions
			Phase time_to_phase(Time time) const;
			Time time_into_cycle(Phase phase) const;

			// Get next time corresponding to a phase
			Time forward_to_phase(Time time, Phase phase) const;

		private:
			Frequency frequency;
			Time period;
			Validity validity;
	};
}

#endif
