#ifndef IMPOSC_CHARTS_GNUPLOT_IF_HPP
#define IMPOSC_CHARTS_GNUPLOT_IF_HPP

#include <stdlib.h>
#include <cstdio>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <vector>


#include <iostream>

#include "impact.hpp"

namespace charts
{
	std::string gnuplot_prefix(const std::string &outfile)
	{
		return "gnuplot -e \"set terminal png size 400,300; set output '" + outfile + "'; set key outside; ";
	};

	std::string prepare_plot(const std::vector<dynamics::Impact> &impacts, const std::string &title, const std::string &marker)
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
		
		return " '" + data_file + "' title '" + title + "' with " + marker;
	}


	int do_plot(const std::vector<std::string> &commands, const std::string &outfile)
	{
		std::stringstream command;
		command << gnuplot_prefix(outfile);

		bool first = true;

		for (const auto &cmd : commands)
		{
			if (!cmd.empty()){
			if (first)
			{
				first = false;
				command << " plot ";
			}
			else
			{
				command << ", ";
			}
			command << cmd;
			}
		}

		command << " \" ";

		std::cout << command.str() << std::endl;

		return system(command.str().c_str());
	};
}

#endif
