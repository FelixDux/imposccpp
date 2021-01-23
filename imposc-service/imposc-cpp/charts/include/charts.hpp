#ifndef IMPOSC_CHARTS_CHARTS_HPP
#define IMPOSC_CHARTS_CHARTS_HPP

#include "impact.hpp"
#include "dynamics.hpp"

#include <vector>
#include <string>

namespace charts
{
	void plot_impacts(const std::vector<dynamics::Impact> &impacts, const std::string &outfile, const dynamics::Parameters &params);
}

#endif
