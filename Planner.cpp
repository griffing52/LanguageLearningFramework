#include <fstream>
#include "Planner.h"
#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <cstdlib>
#include <sstream>

using namespace std;

namespace planner {

	const int neededReinforcement = 3;
	const int forgettingThreshold = 4;

	vector<string> intros = {
	"Listen to the way you say",
	"Let's learn how to say",
	"Listen and repeat the following which means"
	};

	vector<string> starters = {
		"How do you say",
		"Let's hear you say"
	};

	string chooseIntro() {
		return intros[rand() % intros.size()];
	}

	string chooseStarter() {
		return starters[rand() % starters.size()];
	}

	bool needsReview(util::Word* word, int currentCycle) {
		return word->complexity != 0 && 
			(word->frequency < neededReinforcement ||
			(currentCycle - word->age >= forgettingThreshold));
	}

	void reinforceWord(util::Word* word, int currentCycle) {
		word->frequency += 1;
		word->age = currentCycle;
	}

	void reinforcePhraseWords(util::Phrase* phrase, int currentCycle) {
		for (util::Word* word : phrase->words) {
			reinforceWord(word, currentCycle);
		}
	}

	void addWaitTime(util::Word* word, ofstream& out) {
		out << "[WAIT] " << max(word->complexity, 2) << endl;
	}

	void introducePhraseInPlan(util::Word* phrase, int currentCycle, ofstream &out) {
		out << "[INTRO] " << chooseIntro() << endl;
		out << "[NARRATION] " << phrase->translation << endl;
		out << "[PHRASE] " << phrase->value << endl;
		addWaitTime(phrase, out);
		reinforceWord(phrase, currentCycle);
	}

	void usePhraseInPlan(util::Word* phrase, string identifier, int currentCycle, ofstream& out) {
		out << "[NARRATION] " << chooseStarter() << endl;
		out << "[NARRATION] " << phrase->translation << endl;
		addWaitTime(phrase, out);
		out << "[PHRASE] " << phrase->value << endl;
		addWaitTime(phrase, out);
		reinforceWord(phrase, currentCycle);
	}

	void introduceWordInPlan(util::Word* word, int currentCycle, ofstream& out) {
		out << "[INTRO] " << chooseIntro() << endl;
		out << "[NARRATION] " << word->translation << endl;
		out << "[WORD] " << word->value << endl;
		reinforceWord(word, currentCycle);
	}

	void useWordInPlan(util::Word* word, int currentCycle, ofstream& out) {
		out << "[NARRATION] " << chooseStarter() << endl;
		out << "[NARRATION] " << word->translation << endl;
		addWaitTime(word, out);
		out << "[WORD] " << word->value << endl;
		reinforceWord(word, currentCycle);
	}

	void plan(const string& lessonName, vector<util::Phrase*>& currPhrases, map<string, util::Word*> wordMap, int &currentCycle) {
		unsigned int seed = 0;
		for (char c : lessonName) seed += c;
		srand(seed);

		ofstream out("lessons/lesson_" + lessonName + ".txt");
		set<util::Phrase*> plannedPhrases;

		//steps.push_back("[LESSON]: " + lessonName);

		for (util::Phrase* phrase : currPhrases) {
			if (phrase->frequency == 0) {
				introducePhraseInPlan(phrase, currentCycle, out);
			}
			for (util::Word* word : phrase->words) {
				if (needsReview(word, currentCycle))
				{
					// TODO ADD RANDOMNESS? AND MAKE SURE ALL WORDS DON"T NEED REVIEW BEFORE MOVING ON OR CHECK IF THE WORDS ARE KNOWN ENOUGH TO USE DEPENDENCY PHRASE
					if (word->frequency == 0) {
						introduceWordInPlan(word, currentCycle, out);
					}
					useWordInPlan(word, currentCycle, out);
				}
			}
			// TODO
			for (util::Phrase* dep : phrase->dependencies) {
				if (plannedPhrases.find(dep) != plannedPhrases.end()) continue;

				if (phrase->complexity < dep->complexity * dep->frequency) {
					plannedPhrases.insert(dep);
				}
				else {
					for (util::Word* w : dep->words) {
						if (needsReview(w, currentCycle)) {
							plannedPhrases.insert(dep);
							break;
						}
					}
				}
			}


			if (!plannedPhrases.empty()) {
				auto first = *plannedPhrases.begin();
				if (first->frequency == 0) {
					introducePhraseInPlan(first, currentCycle, out);
				}
				usePhraseInPlan(first, "PHRASE", currentCycle, out);
				if (plannedPhrases.size() > 1) {
					usePhraseInPlan(*(--plannedPhrases.end()), "PHRASE", currentCycle, out);
				}
			}

			usePhraseInPlan(phrase, "PHRASE", currentCycle, out);
		}

		currentCycle++;

		/*for (int i = 0; i < steps.size(); i++) {
			out << steps[i] << endl;
			cout << steps[i] << endl;
		}*/

		  
		// Save to JSON
		//json j;
		//j["lesson_name"] = lessonName;
		//j["cycle"] = currentCycle;
		//j["steps"] = steps;


		//out << j.dump(4);  // pretty print
		out.close();
	}

	//void printPlan(
}
