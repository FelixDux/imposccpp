#include "dynamics.hpp"
#include "charts.hpp"
#include "doa_plot.hpp"

#include <iostream>

int main(int argc, char** argv)
{
	try
	{
		//dynamics::Parameters parameters(2, 0.8, -0.01);
		dynamics::Parameters parameters(5.2, 0.8, -0.63);

		dynamics::ImpactMap map(parameters);

		//charts::plot_impacts(map.iterate(0, 0, 10000));
		//charts::plot_impacts(map.singularity_set(1000)) 
		charts::plot_doa(parameters, 4, 100, 100, 1000);
	}
	catch (const dynamics::ParameterError &e)
	{
		std::cerr << e.what() << std::endl;
	}

	return 0;
}
