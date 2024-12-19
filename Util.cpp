#include "Util.h"
#include <iostream>

namespace util {
	ostream& operator<<(ostream& os, const Word& word) {
		os << word.value << '\t' << word.translation << '\t' << "C: " << word.complexity << ", A: " << word.age << ", F: " << word.frequency;
		return os;
	}

	bool Compare::operator()(Word* below, Word* above)
	{
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
}