#include "Loader.h"
#include <fstream>
#include <iostream>

#define WORD_DELIMITER '='
#define KNOWN_WORD '!'
#define DEBUG 1

using namespace std;
using std::cout;

void loader::loadWords(vector<util::Word*>& wordList, const string filename) {
	ifstream file(filename);
	if (file.is_open()) {
		string line;
		while (getline(file, line)) {
			util::Word* word = new util::Word;

			// TODO int idx = line.find(WORD_DELIMITER);

			// get every word and its translation
			for (int i = 0; i < line.length(); i++) {
				if (line[i] == WORD_DELIMITER) {
					int offset = 0;

					// known word marker
					if (line[0] == KNOWN_WORD) {
						offset = 1;
						word->complexity = -1;
						word->age = -1;
					}
					word->value = line.substr(offset, i);
					word->translation = line.substr(i + 1, line.length() - i - 1 - offset);
					break;
				}
			}

			wordList.push_back(word);
		}
	}
	else {
		cout << "Unable to open file" << filename << endl;
	}
	file.close();
}

// takes word list and converts it to a map from 
void loader::wordListToMap(vector<util::Word*> wordList, map<string, util::Word*>& wordMap) {
	for (int i = 0; i < wordList.size(); i++) {
		wordMap[wordList[i]->value] = wordList[i];

		//cout << wordMap[wordList[i]->value]->value << endl;
	}
}

void savePhraseDependencies(util::Phrase* phrase_ptr, vector<util::Phrase*> phraseList) {
	// loop through all phrases to see if this phrase is a dependency
	for (auto& phrase : phraseList) {
		if (phrase == phrase_ptr) {
			continue;
		}

		// if word isn't in phrase, then it's not a dependency
		for (auto& word : phrase_ptr->words) {
			// find(word) == end() means word not found
			if (phrase->words.find(word) == phrase->words.end()) {
				goto next_phrase;
			}
		}
		phrase->dependencies.push(phrase_ptr);
	next_phrase:;
	}
}

void loader::addPhrases(vector<util::Phrase*>& phraseList, map<string, util::Word*> wordMap, string filename) {
	ifstream file(filename);
	if (file.is_open()) {
		string line;
		while (getline(file, line)) {
			util::Phrase* phrase = new util::Phrase;

			int numSpaces = 0;
			int prevSpaceIdx = -1;

			size_t ln = line.length();

			// separate phrase into words and translation
			for (size_t i = 0; i < ln; i++) {
				if (line[i] == WORD_DELIMITER) {
					phrase->value = line.substr(0, i);
					phrase->translation = line.substr(i + 1, line.length() - i - 1);
					break;
				}

				// get individual words
				if (line[i] == ' ' || line[i] == WORD_DELIMITER) {
					numSpaces++;

					string word = line.substr(prevSpaceIdx + 1, i - prevSpaceIdx - 1);

					if (wordMap.count(word) <= 0) {
						// cerr?
						cout << word << " not found in dictionary" << endl;
						return;
					}

					phrase->words.insert(wordMap[word]);
					//phrase->dependencies.push((util::Phrase*) wordMap[word]);

					prevSpaceIdx = (int) i;
				}
			}

			// number of words + 1
			phrase->complexity = numSpaces + 2;

			//cout << *phrase << endl;

			phraseList.push_back(phrase);
		}
	}
	else {
		cout << "Unable to open file " << filename << endl;
	}
	file.close();

	for (auto& phrase : phraseList) {
		savePhraseDependencies(phrase, phraseList);
	}

#ifdef DEBUG
	for (auto& phrase : phraseList) {
		util::Phrase p = *phrase;

		cout << "Phrase: " << p.value << endl;
		auto& pq = p.dependencies;
		cout << "Priority Queue: " << endl;
		while (!pq.empty()) {
			cout << *pq.top() << endl;
			pq.pop();
		}
		cout << endl;
	}
#endif
}

void loader::saveMemoryFile(vector<util::Phrase*> &phraseList, const string name) {

}

void loader::loadMemoryFile(vector<util::Phrase*> &phraseList, const string name) {

}