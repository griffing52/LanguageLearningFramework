#pragma once
#include <string>
#include <queue>
#include <set>

using namespace std;

namespace util {
	struct Word {
		string value;
		string translation;
		int complexity = 0;
		int frequency = 0;
		int age = 0;

		bool operator()(Word* below, Word* above) {
			if (below->complexity > above->complexity) {
				return true;
			}
			else if (below->complexity == above->complexity) {
				if (below->frequency > above->frequency) {
					return true;
				}
				else if (below->frequency == above->frequency) {
					if (below->age < above->age) {
						return true;
					}
				}

			}

			return false;
		}
	};

	struct Phrase : public Word {
		set<Word*> words;
		priority_queue<Phrase*> dependencies;
		//priority_queue<Word*, vector<Word*>, Compare> dependencies;
		//Word* dependencies = nullptr;
	};

	class Compare {
	public:
		bool operator()(Word* below, Word* above)
		{
			if (below->complexity > above->complexity) {
				return true;
			} else if (below->complexity == above->complexity) {
				if (below->frequency > above->frequency) {
					return true;
				} else if (below->frequency == above->frequency) {
					if (below->age < above->age) {
						return true;
					}
				}
				
			}

			return false;
		}
	};

	ostream& operator<<(ostream& os, const Word& word);
}
