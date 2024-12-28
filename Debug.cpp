#include "Debug.h"
#include <iostream>

using namespace std;

namespace debug {
	void printWordFromString(string word, map<string, util::Word*> wordMap) {
		cout << "Searching for word: \"" << word << '\"' << endl;
		if (wordMap.find(word) != wordMap.end()) {
			cout << *wordMap[word] << endl;
		}
		else {
			cout << "No valid word found" << endl;
		}
	}

	void printPhraseList(vector<util::Phrase*> phraseList) {
		for (auto& phrase : phraseList) {
			cout << phrase->value << endl;
		}
	}

	void printPhrase(string phrase, vector<util::Phrase*> phraseList) {
		cout << "Searching for phrase: \"" << phrase << '\"' << endl;
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->value == phrase) {
				cout << *phrase_ptr << endl;
				return;
			}
		}
		cout << "No valid phrase found" << endl;
	}
	void printPhraseDependencies(string phrase, vector<util::Phrase*> phraseList) {
		cout << "Searching for dependencies of phrase: \"" << phrase << '\"' << endl;
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->value == phrase) {
				printDependencies(phrase_ptr->dependencies);
				return;
			}
		}
		cout << "No valid phrase found" << endl;
	}

	void printPhraseFromTranslation(string translation, vector<util::Phrase*> phraseList) {
		cout << "Searching for translation: \"" << translation << '\"' << endl;
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->translation == translation) {
				cout << *phrase_ptr << endl;
				return;
			}
		}
		cout << "No valid phrase found" << endl;
	}
	void printPhraseDependenciesFromTranslation(string translation, vector<util::Phrase*> phraseList) {
		cout << "Searching for dependencies of translation: \"" << translation << '\"' << endl;
		for (auto& phrase_ptr : phraseList) {
			if (phrase_ptr->translation == translation) {
				printDependencies(phrase_ptr->dependencies);
				return;
			}
		}
		cout << "No valid phrase found" << endl;
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