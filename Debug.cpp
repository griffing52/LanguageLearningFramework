#include "Debug.h"
#include <iostream>


using namespace std;


namespace debug {
	void printPhraseList(vector<util::Phrase*> phraseList) {
		for (auto& phrase : phraseList) {
			cout << phrase->value << endl;
		}
	}

	void printPhrase(string phrase, vector<util::Phrase*> phraseList) {
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->value == phrase) {
				cout << *phrase_ptr << endl;
				return;
			}
		}
	}
	void printPhraseDependencies(string phrase, vector<util::Phrase*> phraseList) {
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->value == phrase) {
				printDependencies(phrase_ptr->dependencies);
				return;
			}
		}
	}

	void printPhraseFromTranslation(string translation, vector<util::Phrase*> phraseList) {
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->translation == translation) {
				cout << *phrase_ptr << endl;
				return;
			}
		}
	}
	void printPhraseDependenciesFromTranslation(string translation, vector<util::Phrase*> phraseList) {
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->translation == translation) {
				printDependencies(phrase_ptr->dependencies);
				return;
			}
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