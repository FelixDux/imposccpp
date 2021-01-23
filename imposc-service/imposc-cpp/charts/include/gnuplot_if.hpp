#ifndef IMPOSC_CHARTS_GNUPLOT_IF_HPP
#define IMPOSC_CHARTS_GNUPLOT_IF_HPP

#include <stdlib.h>
#include <string.h>
#include <cstdio>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <vector>
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

#include "impact.hpp"

namespace charts
{
	inline std::string gnuplot_prefix(const std::string &outfile, bool withKey=false, int sizeX=1000, int sizeY=750)
	{
		std::string result = "gnuplot -e \"set terminal png size " + std::to_string(sizeX) + "," + std::to_string(sizeY) + "; set output '" + outfile + "'; set yrange [0:]; set xrange [0 : 1]; set xtics ('0' 0, '{/Symbol p}/{/Symbol w}' 0.5, '2{/Symbol p}/{/Symbol w}' 1) ; set xlabel '{/Symbol f}'; set ylabel 'v'; ";

		if (withKey)
		{
			result += " set key below box;";
		}		

		return result;
	};

	inline std::pair<std::ofstream, std::string> temp_file_stream()
	{
		auto tmp_path = fs::temp_directory_path() / "tmp.XXXXXX";

		char tmpname[1 + strlen(tmp_path.c_str())] = "";

		sprintf(tmpname, "%s", tmp_path.c_str());

		auto fd = mkstemp(tmpname);
		return {std::ofstream(tmpname), std::string(tmpname)};
	}

	inline std::string prepare_plot(const std::vector<dynamics::Impact> &impacts, const std::string &title, const std::string &marker)
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


	inline int do_plot(const std::vector<std::string> &commands, const std::string &outfile, bool withKey=false, int sizeX=1000, int sizeY=750)
	{
		std::stringstream command;
		command << gnuplot_prefix(outfile, withKey, sizeX, sizeY);

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
