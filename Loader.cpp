#include "Loader.h"
#include "Debug.h"
#include <fstream>
#include <iostream>

#define WORD_DELIMITER '='
#define SYNONYM_DELIMITER ','
#define KNOWN_WORD '!'
#define DEBUG 1

using namespace std;
using std::cout;

void loader::loadWords(vector<util::Word*> &wordList, map<string, util::Word*> &wordMap, const string filename) {
	ifstream file(filename);
	if (file.is_open()) {
		string line;
		while (getline(file, line)) {
			util::Word* word = new util::Word;

			// TODO int idx = line.find(WORD_DELIMITER);

			int offset = 0;

			// known word marker
			if (line[0] == KNOWN_WORD) {
				offset = 1;
				word->complexity = 0;
				word->age = -1;
			}

			int prevSeperator = -1 + offset;
			// get every word and its translation
			for (int i = offset; i < line.length(); i++) {
				if (line[i] == SYNONYM_DELIMITER) {
					string synonym = line.substr(prevSeperator + 1, i - offset);
					prevSeperator = i;
					wordMap[synonym] = word;
				}
				else if (line[i] == WORD_DELIMITER) {
					word->value = line.substr(prevSeperator + 1, i - prevSeperator - 1);
					word->translation = line.substr(i + 1, line.length() - i - 1 - offset);
					break;
				}
			}

			wordList.push_back(word);
			wordMap[word->value] = word;
		}
	}
	else {
		cout << "Unable to open file" << filename << endl;
	}
	file.close();
}

// DEPRECATED
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
		phrase->dependencies.insert(phrase_ptr);
	next_phrase:;
	}
}

void loader::addPhrases(vector<util::Phrase*>& phraseList, map<string, util::Word*> wordMap, string filename) {
	ifstream file(filename);
	if (file.is_open()) {
		string line;
		while (getline(file, line)) {
			util::Phrase* phrase = new util::Phrase;

			//int numSpaces = 0;
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
					//numSpaces++;

					string word = line.substr(prevSpaceIdx + 1, i - prevSpaceIdx - 1);

					if (wordMap.count(word) <= 0) {
						// cerr?
						cout << word << " not found in dictionary" << endl;
						return;
					}

					util::Word* w = wordMap[word];

					phrase->words.insert(w);
					phrase->complexity += w->complexity;
					//phrase->dependencies.push((util::Phrase*) wordMap[word]);

					prevSpaceIdx = (int) i;
				}
			}

			// number of words + 1
			//phrase->complexity = numSpaces + 2;

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

}

void loader::saveMemoryFile(vector<util::Phrase*> &phraseList, const string name) {
	ofstream fout(name);

	fout << phraseList.size() << endl;

	for (auto& phrase : phraseList) {
		fout << phrase->value << endl;
		fout << phrase->translation << endl;
		fout << phrase->complexity << endl;
		fout << phrase->frequency << endl;
		fout << phrase->age << endl;
		fout << phrase->dependencies.size() << endl;
		/*for (auto& dep : phrase->dependencies) {
			fout << dep->value << endl;
		}*/
	}

	for (auto& phrase : phraseList) {

		//fout << "Test: " << phrase->value << endl;
		for (auto& dep : phrase->dependencies) {
			auto it = find(phraseList.begin(), phraseList.end(), dep);
			if (it == phraseList.end()) {
				cout << "Error finding dependency " << dep->value << " in phrase list" << endl;
				return;
			}

			size_t index = it - phraseList.begin();

			fout << index << endl;
		}
	}

	fout.close();
}

void loader::loadMemoryFile(vector<util::Phrase*>& phraseList, map<string, util::Word*> wordMap, const string name) {
	ifstream fin(name);

	if (!fin.is_open()) {
		cout << "Unable to open file " << name << endl;
		return;
	}

	size_t numPhrases;
	fin >> numPhrases;

	struct PhraseLoadData {
		util::Phrase* ptr;
	};

	size_t* numOfDependencies = new size_t[numPhrases];
	//util::Phrase** idxToPhrase = new util::Phrase*[numPhrases];
	for (size_t i = 0; i < numPhrases; i++) {
		util::Phrase* phrase = new util::Phrase;

		fin.ignore(1);

		string line;

		getline(fin, line);
		phrase->value = line;

		getline(fin, line);
		phrase->translation = line;

		fin >> phrase->complexity;
		fin >> phrase->frequency;
		fin >> phrase->age;

		fin >> numOfDependencies[i];

		//idxToPhrase[i] = phrase;

		// phrase words
		size_t ln = phrase->value.length();

		int prevSpaceIdx = -1;
		// separate phrase into words and translation
		for (size_t i = 0; i <= ln; i++) {
		//	// get individual words
			if (i == ln || phrase->value[i] == ' ') {

				string word = phrase->value.substr(prevSpaceIdx + 1, i - prevSpaceIdx - 1);

				if (wordMap.count(word) <= 0) {
					// cerr?
					cout << word << " not found in dictionary" << endl;
					return;
				}

				util::Word* w = wordMap[word];

				phrase->words.insert(w);
				phrase->complexity += w->complexity;
				//phrase->dependencies.push((util::Phrase*) wordMap[word]);

				prevSpaceIdx = (int)i;
			}
		}

		phraseList.push_back(phrase);
	}

	for (size_t i = 0; i < numPhrases; i++) {
		// phrase dependencies
		for (size_t j = 0; j < numOfDependencies[i]; j++) {
			size_t depIdx;
			fin >> depIdx;

			phraseList[i]->dependencies.insert(phraseList[depIdx]);
		}
	}

	// TODO

	fin.close();
}