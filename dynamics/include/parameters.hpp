#ifndef IMPOSC_DYNAMICS_PARAMETERS_HPP
#define IMPOSC_DYNAMICS_PARAMETERS_HPP

/*
 * parameters which define a 1-d impact oscillator system with no damping 
 * between impacts
 *
 */
#include <stdexcept>
#include <string>
#include <sstream>

#include "types.hpp"

namespace dynamics
{

	class ParameterError : public std::domain_error
	{
		public:
			static std::string what_message(const std::string &parameter, double value, const std::string & reason) 
			{
				std::stringstream str;

				str << "ERROR: value " << value << " of " << parameter << " is invalid";

				if (!reason.empty())
				{
					str << " because " << reason;
				}

				return str.str();
			}

			ParameterError(const std::string &parameter, double value, const std::string &reason) : std::domain_error(what_message(parameter, value, reason)) {}
	};

	class Parameters
	{
		public:
			Parameters(Frequency omega, Scalar r, Displacement sigma, unsigned int N=100) : forcing_frequency(omega), coefficient_of_restitution(r), obstacle_offset(sigma),
																							maximum_periods(N)
			{
				validate();
			};

			Frequency get_forcing_frequency() const {return forcing_frequency;}
			Scalar get_coefficient_of_restitution() const {return coefficient_of_restitution;}
			Displacement get_obstacle_offset() const {return obstacle_offset;}
			unsigned int get_maximum_periods() const {return maximum_periods;}

		private:

			void validate()
			{
				if (forcing_frequency == 0)
				{
					throw ParameterError("forcing frequency", forcing_frequency, "the model cannot cope with constant (non-periodic) forcing");
				}
				if (forcing_frequency < 0)
				{
					throw ParameterError("forcing frequency", forcing_frequency, "the model cannot cope with negative forcing frequencies");
				}
				if (forcing_frequency == 1)
				{
					throw ParameterError("forcing frequency", forcing_frequency, "this is a resonant case with unbounded solutions");
				}
				if (coefficient_of_restitution > 1)
				{
					throw ParameterError("coefficient of restitution", coefficient_of_restitution, "values > 1 generate unbounded solutions");
				}
				if (coefficient_of_restitution < 0)
				{
					throw ParameterError("coefficient of restitution", coefficient_of_restitution, "negative values generate unphysical solutions");
				}
				if (maximum_periods==0)
				{
					throw ParameterError("maximum forcing periods to detect impact", maximum_periods, "must be > 0");
				}
			};

			Frequency forcing_frequency;
			Scalar coefficient_of_restitution;
			Displacement obstacle_offset;
			unsigned int maximum_periods;
	};
}

#endif
