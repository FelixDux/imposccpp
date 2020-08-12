#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"

#include "forcing_phase.hpp"

#include <cmath>
#include <vector>
#include <math.h>

TEST_CASE( "Phase converter handles invalid values", "[phase]" ) {
	dynamics::PhaseConverter zero_freq(0);
    	REQUIRE( !zero_freq.is_valid() );
    	REQUIRE( zero_freq.get_validity() == dynamics::PhaseConverter::Validity::zero_frequency );

	dynamics::PhaseConverter negative_freq(-3);
    	REQUIRE( !negative_freq.is_valid() );
    	REQUIRE( negative_freq.get_validity() == dynamics::PhaseConverter::Validity::negative_frequency );
}

TEST_CASE( "Phase converter generates correct period", "[phase]" ) {
	std::vector<unsigned int> ints = {1, 2, 4, 5, 16};

	for (auto i : ints)
	{
		dynamics::PhaseConverter converter( 2 * M_PI / i );

		REQUIRE(converter.is_valid());
		REQUIRE(converter.get_period() == i);
	}

}

TEST_CASE( "Phase converter converts consistently in both directions", "[phase]" ) {
	std::vector<unsigned int> ints = {1, 2, 4, 5, 16};

	dynamics::PhaseConverter converter( 4.89 );

	REQUIRE(converter.is_valid());

	double start_time = 0.02;

	for (auto i : ints)
	{
		double new_time = converter.time_into_cycle(converter.time_to_phase(i * converter.get_period() + start_time));

		REQUIRE(fabs(new_time - start_time) < 1e-6);
	}

}

TEST_CASE( "Phase converter runs forward to specified phase correctly", "[phase]" ) {
	std::vector<unsigned int> ints = {1, 2, 4, 5, 16};
	dynamics::PhaseConverter converter(2.76) ;

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
