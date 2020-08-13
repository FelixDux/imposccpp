#ifndef IMPOSC_CHARTS_CHARTS_HPP
#define IMPOSC_CHARTS_CHARTS_HPP

#include "impact.hpp"

#include <vector>
#include <string>

namespace charts
{
	void plot_impacts(const std::vector<dynamics::Impact> &impacts);

	std::string classify_orbit(const std::vector<dynamics::Impact> &impacts);
}

#endif
