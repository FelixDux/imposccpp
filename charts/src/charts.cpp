#include "charts.hpp"
#include "forcing_phase.hpp"

#include <algorithm>
#include <stdlib.h>
#include <cstdio>
#include <fstream>
#include <string>
#include <sstream>

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
