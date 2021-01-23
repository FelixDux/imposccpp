#include "doa_plot.hpp"
#include "gnuplot_if.hpp"
#include <thread>
#include <future>
#include <iostream>

using namespace dynamics;

namespace charts
{
	DOAClassifier::DOAClassifier(const Parameters &params, Velocity max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, unsigned int n_iterations):
		num_iterations(n_iterations), num_v(n_v_increments), num_phi(n_phi_increments), max_v(max_velocity),parameters(params)
	{
		if (max_velocity <= 0)
		{
			throw MaxVelocityError();
		}

		if (num_v == 0)
		{
			throw VelocityIncrementsError();
		}

		if (num_phi == 0)
		{
			throw PhaseIncrementsError();
		}

		delta_phi = 1.0 / num_phi;
		delta_v = max_v / num_v;
	}

	std::string DOAClassifier::classify_orbit( const PhaseConverter &converter, const IterationResult &impacts) const
	{ 

		auto rit = impacts.impacts.crbegin();

		const Impact &comparator = *rit;

		unsigned int num_impacts = 1;

		unsigned int num_periods = 0;

		bool chatter = false;

		bool found = false;

		std::stringstream result_str;

		if (impacts.long_excursions)
		{
			result_str << "long excursions";
		}
		else
		{			
			for (++rit; rit != impacts.impacts.crend() && !found; ++rit)
			{
				if (0 == rit->get_velocity())
				{
					chatter = true;
				}

				if (rit->almost_equal(comparator))
				{
					num_periods = converter.difference_in_periods(comparator.get_time(), rit->get_time());
					found = (num_periods > 0);

					//if (0==num_periods) std::cout << num_periods << " between " << comparator.get_time() << " and " << rit->get_time() << std::endl;
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
					result_str << "chatter"; //"(∞," << num_periods << ")";
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
		}

		return result_str.str();
	}

	std::pair<std::string, Impact> DOAClassifier::classify_from_impact(Phase phi, Velocity v) const
	{
		ImpactMap impact_map(parameters);

		auto impacts = impact_map.iterate(phi, v, num_iterations);

		return std::pair<std::string, Impact>(classify_orbit(impact_map.converter(), impacts), impacts.impacts.front());
	}

	std::map<std::string, std::list<Impact> > DOAClassifier::classify_for_phase_range(unsigned int n_start_phi, unsigned int n_end_phi)
	{
		std::map<std::string, std::list<Impact> > result;

		Phase phi = delta_phi * n_start_phi;

		for (auto n_phi = n_start_phi; n_phi < n_end_phi; ++n_phi)
		{
			Velocity v = max_v;
			
			for (auto n_v = 0; n_v < num_v; ++n_v)
			{
				auto classification = classify_from_impact(phi, v);

				result[classification.first].push_back(classification.second);

				v -= delta_v;

				if (v < 0)
				{
					v = 0;
				}
			}

			phi += delta_phi;
		}


		return result;
	}

	std::map< std::string, std::vector< Impact > > DOAClassifier::operator() ()
	{
		std::map< std::string, std::vector< Impact > > result;

		// #if !defined(NDEBUG)
		// unsigned int num_tasks = 1;
		// #else
		auto num_tasks = std::thread::hardware_concurrency();

		if (num_tasks <= 0)
		{
			num_tasks = 1;
		}
		// #endif

		std::vector< std::future < std::map <std::string, std::list<Impact> > > >  tasks(num_tasks);

		unsigned int n_phi_per_task = num_phi / num_tasks;

		unsigned int n_start_phi = 0;

		for (unsigned int n_task = 0; n_task < num_tasks; ++n_task)
		{
			unsigned int n_end_phi = n_start_phi + n_phi_per_task;

			if (n_task + 1 == num_tasks)
			{
				n_end_phi = num_phi;
			}

			tasks[n_task] = std::async([n_start_phi, n_end_phi, this]() {return this->classify_for_phase_range(n_start_phi, n_end_phi);});

			n_start_phi = n_end_phi;
		}

		for (auto &task : tasks)
		{
			auto result_map = task.get();

			// Marshall results
			for (const auto &classification : result_map)
			{
				auto &target_vector = result[classification.first];

				for (const auto &impact : classification.second)
				{
					target_vector.push_back(impact);
				}
			}
		}

		return result;
	}

	void plot_doa(const Parameters &parameters, Velocity max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, unsigned int n_iterations, const std::string &outfile)
	{
		DOAClassifier classifier(parameters, max_velocity, n_v_increments, n_phi_increments, n_iterations);

		auto doa_data = classifier();

		std::vector < std::string > commands(doa_data.size());

		for (const auto &orbit : doa_data)
		{
			commands.push_back(prepare_plot(orbit.second, orbit.first, "points pointtype 5 pointsize 1"));

			std::cout << orbit.first << std::endl;
		}

		int mult = 10;
		float aspect_ratio = 0.75;
		int sizeX = 0;

		if (n_phi_increments > n_v_increments)
		{
			sizeX = mult*n_phi_increments;
		}
		else
		{
			sizeX = mult*n_v_increments;
		}

		do_plot(commands, outfile, parameters, true, sizeX, sizeX*aspect_ratio);

	}
}
