#ifndef IMPOSC_CHARTS_DOA_PLOT_HPP
#define IMPOSC_CHARTS_DOA_PLOT_HPP

#include <vector>
#include <string>
#include <stdexcept>
#include <map>
#include <list>

#include "impact.hpp"
#include "dynamics.hpp"

namespace charts
{
	void plot_doa(const dynamics::Parameters &parameters, dynamics::Velocity max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, unsigned int n_iterations);

	class DOAClassifier
	{
		public:
			class DOARangeError : public std::domain_error
			{
				protected:
					DOARangeError(const std::string &msg):std::domain_error(msg) {};
			};

			class MaxVelocityError : public DOARangeError
			{
				public:
					MaxVelocityError():DOARangeError("Max velocity for DOA plot must be > 0"){};
			};

			class VelocityIncrementsError : public DOARangeError
			{
				public:
					VelocityIncrementsError():DOARangeError("Number of velocity increments for DOA plot must be > 0"){};
			};

			class PhaseIncrementsError : public DOARangeError
			{
				public:
					PhaseIncrementsError():DOARangeError("Number of phase increments for DOA plot must be > 0"){}
			};

			DOAClassifier(const dynamics::Parameters &params, dynamics::Velocity max_velocity, unsigned int n_v_increments, unsigned int n_phi_increments, unsigned int n_iterations);

			std::map< std::string, std::vector< dynamics::Impact > > operator() ();

		private:

			std::string classify_orbit(const dynamics::PhaseConverter &converter, const dynamics::IterationResult &impacts) const;

			std::pair<std::string, dynamics::Impact> classify_from_impact(dynamics::Phase phi, dynamics::Velocity v) const;

			std::map<std::string, std::list<dynamics::Impact> > classify_for_phase_range(unsigned int n_start_phi, unsigned int n_end_phi);

			dynamics::Parameters parameters;
			unsigned int num_iterations;
			unsigned int num_v;
			unsigned int num_phi;
			dynamics::Velocity max_v;
			dynamics::Velocity delta_v;
			dynamics::Phase delta_phi;

	};
}

#endif
