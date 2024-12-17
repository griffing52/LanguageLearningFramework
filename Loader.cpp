#include "Loader.h"
#include <fstream>
#include <iostream>

#define WORD_DELIMITER '='

using namespace std;
using std::cout;

void loader::loadWords(vector<util::Word*> &wordList, const string filename) {
	ifstream file(filename);
	if (file.is_open()) {
		string line;
		while (getline(file, line)) {
			util::Word* word = new util::Word;

			//int idx = line.find(WORD_DELIMITER);

			for (int i = 0; i < line.length(); i++) {
				if (line[i] == WORD_DELIMITER) {
					int offset = 0;
					if (line[0] == '*') {
						offset = 1;
						word->complexity = -1;
						word->age = -1;
					}
					word->value = line.substr(offset, i);
					word->translation = line.substr(i + 1, line.length() - i - 1 - offset);
					break;
				}
			}
			//cout << *word << endl;

			wordList.push_back(word);
		}
	}
	else {
		cout << "Unable to open file" << filename << endl;
	}
	file.close();
}

void loader::wordListToMap(vector<util::Word*> wordList, map<string, util::Word*> &wordMap) {
	for (int i = 0; i < wordList.size(); i++) {
		wordMap[wordList[i]->value] = wordList[i];

		cout << wordMap[wordList[i]->value]->value << endl;
	}
}


void loader::addPhrases(vector<util::Phrase*> &phraseList, map<string, util::Word*> wordMap, string filename) {
	ifstream file(filename);
	if (file.is_open()) {
		string line;
		while (getline(file, line)) {
			util::Phrase* phrase = new util::Phrase;

			int numSpaces = 0;
			int prevSpaceIdx = -1;

			for (int i = 0; i < line.length(); i++) {
				if (line[i] == WORD_DELIMITER) {
					phrase->value = line.substr(0, i);
					phrase->translation = line.substr(i + 1, line.length() - i - 1);
					break;
				}
				else if (line[i] == ' ') {
					numSpaces++;

					string word = line.substr(prevSpaceIdx + 1, i - prevSpaceIdx - 1);

					if (wordMap.count(word) <= 0) {
						// cerr?
						cout << word << " not found in dictionary" << endl;
						return;
					}

					phrase->dependencies.push(wordMap[word]);

					prevSpaceIdx = i;
				}
			}

			phrase->complexity = numSpaces + 2;

			cout << *phrase << endl;
		}
	}
	else {
		cout << "Unable to open file " << filename << endl;
	}
	file.close();
}

void loader::saveMemoryFile(vector<util::Phrase*> &phraseList, const string name) {

}

void loader::loadMemoryFile(vector<util::Phrase*> &phraseList, const string name) {

}