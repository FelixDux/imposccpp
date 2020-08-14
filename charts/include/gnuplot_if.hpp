#ifndef IMPOSC_CHARTS_GNUPLOT_IF_HPP
#define IMPOSC_CHARTS_GNUPLOT_IF_HPP

#include <stdlib.h>
#include <cstdio>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <vector>

#include "impact.hpp"

namespace charts
{
	std::string gnuplot_prefix(const std::string &outfile)
	{
		return "gnuplot -e \"set terminal png size 400,300; set output '" + outfile + "';";
	};

	std::string prepare_scatter_plot(const std::vector<dynamics::Impact> &impacts, const std::string &title)
	{
		std::string data_file = tmpnam(nullptr);

		{
			std::ofstream outfile(data_file); 
			
			for_each(impacts.begin(), impacts.end(), 
					[&outfile] (const dynamics::Impact& impact)
					{ outfile << impact.get_phase() 
					<< "\t" << impact.get_velocity()
					<< std::endl;}
					);
		}
		
		return "plot '" + data_file + "' with dots title '" + title + "'; ";
	}


	int do_plot(const std::vector<std::string> &commands, const std::string &outfile)
	{
		auto command = gnuplot_prefix(outfile);

		for (const auto &cmd : commands)
		{
			command += cmd;
		}

		command += " \" ";

		return system(command.c_str());
	};
}

#endif
