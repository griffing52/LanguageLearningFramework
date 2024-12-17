#pragma once
#include "Util.h"
#include <vector>
#include <string>

using namespace std;

namespace loader {
	// binary tree for searching isntead of hashmap? maybe not since less than 10000 words
	void loadWords(vector<util::Word*> wordList, string filename);
	void addPhrases(vector<util::Phrase*> phraseList, string filename);

	void saveMemoryFile(vector<util::Phrase*> phraseList, string name);
	void loadMemoryFile(vector<util::Phrase*> phraseList, string name);
}