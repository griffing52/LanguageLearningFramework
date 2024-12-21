#include "Debug.h"
#include <iostream>


using namespace std;


namespace debug {
	void printPhraseList(vector<util::Phrase*> phraseList) {
		for (auto& phrase : phraseList) {
			cout << phrase->value << endl;
		}
	}

	void printDependencies(set<util::Phrase*> dependencies) {
		for (auto& phrase : dependencies) {
			cout << phrase->value << endl;
		}
	}

	void printAllDependencies(vector<util::Phrase*> phraseList) {
		for (auto& phrase : phraseList) {
			cout << phrase->value << " depends on:" << endl;
			printDependencies(phrase->dependencies);
			cout << endl;
		}
	}
}