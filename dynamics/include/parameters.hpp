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

				str << "Value " << value << " of parameter " << parameter << " is invalid";

				if (!reason.empty())
				{
					str << " because " << reason;
				}

				return str.str();
			}

			ParameterError(const std::string &parameter, double value, const std::string &reason) : std::domain_error(what_message(parameter, value, reason)) {}
	};

	struct Parameters
	{
		Frequency forcing_frequency;
		Scalar coefficient_of_restitution;
		Displacement obstacle_offset;

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
		};
	};
}

#endif
