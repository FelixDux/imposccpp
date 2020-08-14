#include "charts.hpp"
#include "forcing_phase.hpp"
#include "gnuplot_if.hpp"

using namespace dynamics;
	
namespace charts
{

	void plot_impacts(const std::vector<Impact> &impacts)
	{ 
		do_plot( {prepare_plot(impacts, "impact map", "dots")}, "scatter.png");
	}
}
