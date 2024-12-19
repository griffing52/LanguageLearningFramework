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


	class Compare {
	public:
		bool operator()(Word* below, Word* above);
	};

	template <typename T>
	class queue_set : public set<T> {
	public:
		const T& front() const {
			return *this->begin();
		}

		void pop_back() {
			this->erase(--this->end());
		}

		void push_back(const T& value) {
			this->insert(value);
		}
	};

	struct Phrase : public Word {
		set<Word*> words;
		//priority_queue<Phrase*> dependencies;
		priority_queue<Word*, queue_set<Word*>, Compare> dependencies;
		//Word* dependencies = nullptr;
	};


	ostream& operator<<(ostream& os, const Word& word);
}
