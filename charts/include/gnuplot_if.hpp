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
		return "gnuplot -e \"set terminal png size 400,300; set output '" + outfile + "'; set key below box; set yrange [0:]; set xrange [0 : 1]; set xtics ('0' 0, '{/Symbol p}/{/Symbol w}' 0.5, '2{/Symbol p}/{/Symbol w}' 1) ; set xlabel '{/Symbol f}'; set ylabel 'v'; ";
	};

	std::pair<std::ofstream, std::string> temp_file_stream()
	{
		char tmpname[] = "tmp.XXXXXX";
		auto fd = mkstemp(tmpname);
		return {std::ofstream(tmpname), std::string(tmpname)};
	}

	std::string prepare_plot(const std::vector<dynamics::Impact> &impacts, const std::string &title, const std::string &marker)
	{
		auto outpair = temp_file_stream();

		std::ofstream &outfile = outpair.first;

		std::string &data_file = outpair.second;
		
		for_each(impacts.begin(), impacts.end(), 
				[&outfile] (const dynamics::Impact& impact)
				{ outfile << impact.get_phase() 
				<< "\t" << impact.get_velocity()
				<< std::endl;}
				);
		
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
