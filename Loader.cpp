#include "Loader.h"
#include <fstream>
#include <iostream>

#define WORD_DELIMITER '='

using namespace std;

void loader::loadWords(vector<util::Word*> wordList, string filename) {
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
			cout << *word << endl;

			wordList.push_back(word);
		}
	}
	else {
		cout << "Unable to open file" << filename << endl;
	}
	file.close();
}

void loader::addPhrases(vector<util::Phrase*> phraseList, string filename) {
	ifstream file(filename);
	if (file.is_open()) {
		string line;
		while (getline(file, line)) {
			util::Phrase* phrase = new util::Phrase;

			int numSpaces = 0;

			for (int i = 0; i < line.length(); i++) {
				if (line[i] == WORD_DELIMITER) {
					phrase->value = line.substr(0, i);
					phrase->translation = line.substr(i + 1, line.length() - i - 1);
					break;
				}
				else if (line[i] == ' ') {
					numSpaces++;
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

void loader::saveMemoryFile(vector<util::Phrase*> phraseList, string name) {

}

void loader::loadMemoryFile(vector<util::Phrase*> phraseList, string name) {

}