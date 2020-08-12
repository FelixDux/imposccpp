#include "charts.hpp"

#include <algorithm>
#include <stdlib.h>
#include <cstdio>
#include <fstream>
#include <string>

using namespace dynamics;
	
namespace charts
{

void plot_impacts(const std::vector<Impact> &impacts)
{
	struct Accumulator
	{
		std::vector<double> v;
		std::vector<double> phi;
		unsigned int idx;

		Accumulator(unsigned int n):idx(0),v(n),phi(n)
		{
		};

		void operator() (const Impact& impact)
		{
			v[idx] = impact.get_velocity();
			phi[idx] = impact.get_phase();
			++idx;
		}
	} accumulator(impacts.size());

	std::string data_file = tmpnam(nullptr);

	{
		std::ofstream outfile(data_file); 
		
		for_each(impacts.begin(), impacts.end(), 
				[&outfile] (const Impact& impact)
				{ outfile << impact.get_phase() 
				<< "\t" << impact.get_velocity()
				<< std::endl;}
				);
	}

	//for_each(impacts.begin(), impacts.end(), accumulator);

	//plt::plot(accumulator.phi, accumulator.v, marker='.');
	
	std::string command = "gnuplot -e \"set terminal png size 400,300; set output 'scatter.png'; plot '" + data_file + "' with dots \" ";
	
	system(command.c_str());
}
}
