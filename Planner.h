#pragma once

#include "Util.h"
#include <map>

using util::Word;
using util::Phrase;

namespace planner {
	void plan(const string& lessonName, vector<util::Phrase*>& currPhrases, map<string, util::Word*> wordMap);
}