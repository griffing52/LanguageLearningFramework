#pragma once

#include <vector>
#include "Util.h"

using namespace std;

namespace debug {
	void printPhraseList(vector<util::Phrase*> phraseList);
	void printDependencies(set<util::Phrase*> dependencies);
	void printAllDependencies(vector<util::Phrase*> phraseList);
}