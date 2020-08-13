#include "doa_plot.hpp"

namespace charts

	std::string classify_orbit(const PhaseConverter &converter, const std::vector<dynamics::Impact> &impacts)
	{ 
		auto rit = impacts.crbegin();

		const Impact &comparator = *rit;

		unsigned int num_impacts = 1;

		unsigned int num_periods = 0;

		bool chatter = false;

		bool found = false;

		std::stringstream result_str;

		for (; rit != impacts.crend() && found; ++rit)
		{
			if (0 == rit->get_velocity())
			{
				chatter = true;
			}

			if (rit->almost_equal(comparator))
			{
				found = true;
				num_periods = converter.difference_in_periods(comparator.get_time(), rit->get_time());
			}
			else
			{
				num_impacts++;
			}
		}

		if (found)
		{
			if (chatter)
			{
				result_str << "(∞," << num_periods << ")";
			}
			else
			{
				result_str << "(" << num_impacts << "," << num_periods << ")";
			}
		}
		else
		{
			result_str << "(∞,∞)";
		}

		return result_str.str();
	}
}
