#pragma once

#include "Util.h"

using util::Word;
using util::Phrase;

namespace planner {
	void plan(const string lessonName, vector<util::Phrase*>& currPhrases, map<string, util::Word*> wordMap);
	Word* chooseNext(Phrase* phrase);
	float calculateCost(Word* word);
}