#include <fstream>
#include "Planner.h"
#include "json.hpp"
#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <cstdlib>
#include <sstream>

using namespace std;
using json = nlohmann::json;

namespace planner {

	const int neededReinforcement = 3;
	const int forgettingThreshold = 2;

	bool needsReview(util::Word* word, int currentCycle) {
		return word->frequency < neededReinforcement ||
			(currentCycle - word->age >= forgettingThreshold);
	}

	void reinforceWord(util::Word* word, int currentCycle) {
		word->frequency += 1;
		word->age = currentCycle;
	}

	void plan(const string& lessonName, vector<util::Phrase*>& currPhrases, map<string, util::Word*> wordMap) {
		unsigned int seed = 0;
		for (char c : lessonName) seed += c;
		srand(seed);
		int currentCycle = seed % 10000;

		set<util::Word*> newlyTaughtWords;
		set<util::Phrase*> plannedPhrases;
		vector<string> steps;

		steps.push_back("Lesson: " + lessonName);

		for (util::Phrase* phrase : currPhrases) {
			vector<util::Word*> needsTeaching;
			for (util::Word* word : phrase->words) {
				if (needsReview(word, currentCycle)) {
					needsTeaching.push_back(word);
				}
			}

			for (util::Phrase* dep : phrase->dependencies) {
				bool relevant = false;
				for (util::Word* w : dep->words) {
					if (needsReview(w, currentCycle)) {
						relevant = true;
						break;
					}
				}
				if (relevant && plannedPhrases.find(dep) == plannedPhrases.end()) {
					steps.push_back("Reinforce phrase: " + dep->value + " = " + dep->translation);
					for (util::Word* w : dep->words) {
						 reinforceWord(w, currentCycle);
						newlyTaughtWords.insert(w);
					}
					plannedPhrases.insert(dep);
				}
			}

			for (util::Word* word : needsTeaching) {
				if (newlyTaughtWords.find(word) == newlyTaughtWords.end()) {
					if (word->frequency == 0) {
						steps.push_back("Introduce new word: " + word->value + " = " + word->translation);
						steps.push_back("Repeat word: " + word->value);
						reinforceWord(word, currentCycle);
						reinforceWord(word, currentCycle);
					}
					else {
						steps.push_back("Review word: " + word->value + " = " + word->translation);
						reinforceWord(word, currentCycle);
					}
					newlyTaughtWords.insert(word);
				}
			}

			bool phraseReady = true;
			for (util::Word* word : phrase->words) {
				if (needsReview(word, currentCycle)) {
					phraseReady = false;
					break;
				}
			}
			if (phraseReady && plannedPhrases.find(phrase) == plannedPhrases.end()) {
				steps.push_back("Teach main phrase: " + phrase->value + " = " + phrase->translation);
				for (util::Word* w : phrase->words) {
					reinforceWord(w, currentCycle);
				}
				plannedPhrases.insert(phrase);
			}
		}

		// Save to JSON
		json j;
		j["lesson_name"] = lessonName;
		j["cycle"] = currentCycle;
		j["steps"] = steps;

		ofstream out("lesson_" + lessonName + ".json");
		out << j.dump(4);  // pretty print
		out.close();
	}

	//void printPlan(
}
