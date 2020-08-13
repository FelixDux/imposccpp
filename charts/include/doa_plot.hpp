#ifndef IMPOSC_CHARTS_DOA_PLOT_HPP
#define IMPOSC_CHARTS_DOA_PLOT_HPP

#include <vector>
#include <string>
#include <memory>

#include "impacts.hpp"
#include "dynamics.hpp"

namespace charts
{

	std::string classify_orbit(const PhaseConverter &converter, const std::vector<dynamics::Impact> &impacts);

	std::string classify_from_impact(const ImpactMap &iterator, Phase phi, Velocity v, unsigned int num_iterations);

	class DOAClassifier
	{
		public:
			DOAClassifier(const ImpactMap &iterator, Velocity max_velocity, unsigned int num_v_increments, unsigned int num_phi_increments, unsigned int num_iterations);


		private:
			std::shared_ptr<ImpactMap> = impact_map;
			unsigned int n_iterations;

	};
}

#endif
