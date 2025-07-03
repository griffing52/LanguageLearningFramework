#include "Planner.h"
#include <iostream>
#include <map>
#include <cmath>    // For sqrt
#include <cstdlib>  // For rand
#include <ctime>    // For seeding random

#define ALPHA 0.1 // The range of the random number generated in calculateCost

using namespace std;

namespace planner {
	void plan(const string lessonName, vector<util::Phrase*>& currPhrases, map<string, util::Word*> wordMap) {
		// Seed the random number generator.
		unsigned int seed = 0;
		for (char c : lessonName) {
			seed += c;
		}
		srand(seed); // reproduceable random numbers

		// Iterate through the lesson plan.
		for (auto& phrase : currPhrases) {
			// Choose the next word.
			util::Word* nextWord = chooseNext(phrase);

			// If there is no next word, skip this phrase.
			if (nextWord == nullptr) {
				cout << "No next word found for phrase: " << phrase->value << endl;
				continue;
			}

			// Print the next word and its cost.
			cout << "Next word: " << nextWord->value << " Cost: " << cost << endl;
		}
	}


	util::Word* chooseNext(util::Phrase* phrase) {

		if (phrase == nullptr) {
			cout << "Phrase is null" << endl;
			return nullptr;
		}

		// Generate a random number in the range [0, 1).
		double randNum = (static_cast<float>(rand()) / RAND_MAX);

		// check if new-ish word frequency < phase complexity
		for (auto& word : phrase->words) {
			if (word->complexity == 0) continue;

			if (word->frequency < phrase->complexity - 2) {

				double prob = 1 / (0.15 * word->frequency + 1);

				if (randNum < prob) continue;

				return word;
			}
		}

		// go through dependencies
		for (auto& dep : phrase->dependencies) {
			if (dep->complexity * dep->frequency < dep->complexity + phrase->complexity) {

				double prob = 1 / (0.15 * dep->frequency + 1);

				if (randNum < prob) continue;

				return dep;
			}
		}

		// go through all words until word frequency == phrase complexity
		for (auto& word : phrase->words) {
			if (word->complexity == 0) continue;

			if (word->frequency <= phrase->complexity) {
				double prob = 1 / (0.15 * word->frequency + 1);

				if (randNum < prob) continue;

				return word;
			}
		}


		return nullptr;
	}

	// DEPRECATED
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