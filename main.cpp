#include "dynamics.hpp"
#include "charts.hpp"

int main(int argc, char** argv)
{
	dynamics::Parameters parameters = 
	{
		.forcing_frequency=4.85, 
		.coefficient_of_restitution=0.8,
		.obstacle_offset=0.01
	};
	dynamics::ImpactMap map(parameters);

	charts::plot_impacts(map.iterate(0, 0, 10000));
	//charts::plot_impacts(map.singularity_set(1000)) 

	return 0;
}
