#include "dynamics.hpp"
#include "charts.hpp"
#include "doa_plot.hpp"

#include <iostream>

int main(int argc, char** argv)
{
	try
	{
		//dynamics::Parameters parameters(2, 0.8, -0.01);
		dynamics::Parameters parameters(5.2, 0.8, -0.01);

		dynamics::ImpactMap map(parameters);

		//charts::plot_impacts(map.iterate(0, 0, 10000));
		//charts::plot_impacts(map.singularity_set(1000)) 
		charts::plot_doa(parameters, 0.5, 100, 100, 500);
	}
	catch (const dynamics::ParameterError &e)
	{
		std::cerr << e.what() << std::endl;
	}

	return 0;
}
