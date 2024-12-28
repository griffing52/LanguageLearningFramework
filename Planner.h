#pragma once

#include "Util.h"

using util::Word;
using util::Phrase;

namespace planner {
	Word* chooseNext(Phrase* phrase);
	float calculateCost(Word* word);
}