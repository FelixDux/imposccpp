#include "charts.hpp"
#include "forcing_phase.hpp"
#include "gnuplot_if.hpp"

using namespace dynamics;
	
namespace charts
{

	void plot_impacts(const std::vector<Impact> &impacts, const std::string &outfile)
	{ 
		do_plot( {prepare_plot(impacts, "", "dots")}, outfile);
	}
}
