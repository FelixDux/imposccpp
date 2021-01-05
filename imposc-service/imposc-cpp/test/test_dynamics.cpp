#include "catch.hpp"

#include "parameters.hpp"
#include "forcing_phase.hpp"
#include "impact.hpp"

#include <cmath>
#include <vector>
#include <math.h>

using namespace dynamics;

SCENARIO( "Parameters class raises exception when incorrectly initialised ", "[parameters]") {
	Frequency good_frequency = 2.8;
	Scalar good_r = 0.8;
	Displacement good_offset = 0;

	GIVEN("A zero frequency") {
		Frequency f = 0;

		WHEN("A set of parameters is initialised") 
		{
			bool exception_happened = false;
			try {
				Parameters p(f, good_r, good_offset);
			}
			catch (const ParameterError &e) {
				THEN("An exception is raised") {
					exception_happened = true;
					REQUIRE_THAT(e.what(), Catch::Contains("forcing frequency"));
				}
			}
			REQUIRE( exception_happened );
		}
	}

	GIVEN("A negative frequency") {
		Frequency f = -3.7;

		WHEN("A set of parameters is initialised") 
		{
			bool exception_happened = false;
			try {
				Parameters p(f, good_r, good_offset);
			}
			catch (const ParameterError &e) {
				THEN("An exception is raised") {
					exception_happened = true;
					REQUIRE_THAT(e.what(), Catch::Contains("forcing frequency"));
				}
			}
			REQUIRE( exception_happened );
		}
	}

	GIVEN("A frequency of 1") {
		Frequency f = 1;

		WHEN("A set of parameters is initialised") 
		{
			bool exception_happened = false;
			try {
				Parameters p(f, good_r, good_offset);
			}
			catch (const ParameterError &e) {
				THEN("An exception is raised") {
					exception_happened = true;
					REQUIRE_THAT(e.what(), Catch::Contains("forcing frequency"));
				}
			}
			REQUIRE( exception_happened );
		}
	}

	GIVEN("A coefficient of restitution greater than 1") {
		Scalar r = 1.1;

		WHEN("A set of parameters is initialised") 
		{
			bool exception_happened = false;
			try {
				Parameters p(good_frequency, r, good_offset);
			}
			catch (const ParameterError &e) {
				THEN("An exception is raised") {
					exception_happened = true;
					REQUIRE_THAT(e.what(), Catch::Contains("coefficient of restitution"));
				}
			}
			REQUIRE( exception_happened );
		}
	}

	GIVEN("A coefficient of restitution less than 0") {
		Scalar r = -1.1;

		WHEN("A set of parameters is initialised") 
		{
			bool exception_happened = false;
			try {
				Parameters p(good_frequency, r, good_offset);
			}
			catch (const ParameterError &e) {
				THEN("An exception is raised") {
					exception_happened = true;
					REQUIRE_THAT(e.what(), Catch::Contains("coefficient of restitution"));
				}
			}
			REQUIRE( exception_happened );
		}
	}

	GIVEN("A valid set of parameter values") {

		WHEN("A set of parameters is initialised") 
		{
			bool exception_happened = false;
			try {
				Parameters p(good_frequency, good_r, good_offset);
			}
			catch ( ... ) {
				exception_happened = true;
			}
			THEN("No exception is raised") {
				REQUIRE( !exception_happened );
			}
		}
	}
}

SCENARIO( "Phase converter handles invalid values", "[phase]" ) {
	GIVEN("A zero frequency") {
		double f = 0;
		WHEN ("A phase converter is initialised") { 
			PhaseConverter zero_freq(f);

			THEN("It is flagged as invalid") { 
				REQUIRE( !zero_freq.is_valid() ); 
				REQUIRE( zero_freq.get_validity() == PhaseConverter::Validity::zero_frequency );
			}
		}
	}

	GIVEN("A negative frequency") {
		double f = -3.4;
		WHEN ("A phase converter is initialised") { 
			PhaseConverter negative_freq(f);

			THEN("It is flagged as invalid") { 
				REQUIRE( !negative_freq.is_valid() ); 
				REQUIRE( negative_freq.get_validity() == PhaseConverter::Validity::negative_frequency );
			}
		}
	}
}

TEST_CASE( "Phase converter generates correct period", "[phase]" ) {
	std::vector<unsigned int> ints = {1, 2, 4, 5, 16};

	for (auto i : ints)
	{
		PhaseConverter converter( 2 * M_PI / i );

		REQUIRE(converter.is_valid());
		REQUIRE(converter.get_period() == i);
	}

}

TEST_CASE( "Phase converter converts consistently in both directions", "[phase]" ) {
	std::vector<unsigned int> ints = {1, 2, 4, 5, 16};

	PhaseConverter converter( 4.89 );

	REQUIRE(converter.is_valid());

	double start_time = 0.02;

	for (auto i : ints)
	{
		double new_time = converter.time_into_cycle(converter.time_to_phase(i * converter.get_period() + start_time));

		REQUIRE(fabs(new_time - start_time) < 1e-6);
	}

}

TEST_CASE( "Phase converter returns correct number of periods between times", "[phase]" ) {
	std::vector<unsigned int> ints = {1, 2, 4, 5, 16};

	PhaseConverter converter( 4.89 );

	REQUIRE(converter.is_valid());

	double start_time = 0.02;

	for (auto i : ints)
	{
		double new_time = start_time + i*converter.get_period();

		REQUIRE(i == converter.difference_in_periods(start_time, new_time));
	}

}

TEST_CASE( "Phase converter runs forward to specified phase correctly", "[phase]" ) {
	std::vector<unsigned int> ints = {1, 2, 4, 5, 16};
	PhaseConverter converter(2.76) ;

	double phase = 0.6;

	double small_time = 0.2, big_time = 0.8;

	for (auto i : ints)
	{
		auto new_small = converter.forward_to_phase(small_time+i*converter.get_period(), phase);

		REQUIRE(1e-6 < fabs(small_time + (i+phase)*converter.get_period() - new_small));

		auto new_big = converter.forward_to_phase(big_time+i*converter.get_period(), phase);

		REQUIRE(1e-6 < fabs(big_time + (i+1+phase)*converter.get_period() - new_big));
	}

}

TEST_CASE( "Test for near equality of impacts works correctly ", "[impact]") {
	PhaseConverter converter(2);

	Impact impact1(converter, 0, 1);
	Impact impact2(converter, 0.0001, 1.0001);
	Impact impact3(converter, 0.3, 0.2);
	Impact impact4(converter, 1.0000001*converter.get_period(), 1);
	Impact impact5(converter, 0.99999*converter.get_period(), 1);

	REQUIRE(impact1.almost_equal(impact2));

	REQUIRE(!impact3.almost_equal(impact2));

	REQUIRE(impact1.almost_equal(impact4));

	REQUIRE(impact1.almost_equal(impact5));
}

