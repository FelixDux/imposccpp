#include "imposcpy.hpp"

#include <iostream>

int main(int argc, char** argv)
{
	map_impacts(5.2, 0.8, -0.63, 100, 0.5, 2, 4000, "impact-map.png");

	return 0;
}
