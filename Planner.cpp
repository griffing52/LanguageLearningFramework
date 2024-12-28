#include "Planner.h"
#include <iostream>
#include <cmath>    // For sqrt
#include <cstdlib>  // For rand
#include <ctime>    // For seeding random

#define ALPHA 0.1 // The range of the random number generated in calculateCost

using namespace std;

namespace planner {
	util::Word* chooseNext(util::Phrase* phrase) {

		if (phrase == nullptr) {
			cout << "Phrase is null" << endl;
		}

		return nullptr;
	}

	float calculateCost(util::Word* word) {
		// TODO: Implement this function
		if (word->complexity == 0) return 0;

		float C = word->complexity;
		float F = word->frequency;
		float A = word->age;

		// Generate a random number in the range [-alpha, alpha].
		double R = ((static_cast<float>(rand()) / RAND_MAX) * 2 * ALPHA) - ALPHA;

		// Perform the calculation.
		return (C / ((F + 1) * sqrt(A + 1))) * (1 + R);
	}
}