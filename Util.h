#pragma once
#include <string>

using namespace std;

namespace util {
	struct Word {
		string value;
		string translation;
		int complexity = 0;
		int frequency = 0;
		int age = 0;
	};

	struct Phrase : public Word {
		Word* dependencies = nullptr;
	};

	ostream& operator<<(ostream& os, const Word& word);
}
