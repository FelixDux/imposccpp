/*
 * Functions and classes for converting between simulated time and
 * phase relative to a forcing cycle, which define as:
 *
 * phase = (time / forcing_period) mod 1
 *
 */

#include "forcing_phase.hpp"

#include <math.h>
#include <cmath>

namespace dynamics {

// Construction
PhaseConverter::PhaseConverter(Frequency omega):frequency(omega)
{
	if (frequency > 0)
	{
		period = 2 * M_PI / frequency;
		validity = Validity::valid;
	}
	else if (frequency == 0)
	{
		validity = Validity::zero_frequency;
	}
	else
	{
		validity = Validity::negative_frequency;
	}
};

// Conversions
Phase PhaseConverter::time_to_phase(Time time) const
{
	auto scaled_time = time/period;

	return scaled_time - floor(scaled_time);
}

Time PhaseConverter::time_into_cycle(Phase phase) const
{
	return phase * period;
}

// Get next time corresponding to a phase
Time PhaseConverter::forward_to_phase(Time time, Phase phase) const
{
	Phase starting_phase = time_to_phase(time);

	Phase phase_change = phase - starting_phase;

	if (phase_change < 0)
	{
		phase_change += 1;
	}

	return time + period * phase_change;
}

unsigned int PhaseConverter::difference_in_periods(Time t1, Time t2) const
{
	auto delta_time = fabs(t1 - t2);

	auto delta_periods = delta_time/period;

	return (unsigned int) round(delta_periods);
}

}
