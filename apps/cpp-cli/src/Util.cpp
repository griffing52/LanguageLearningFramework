#include "Util.h"
#include <iostream>

namespace util {
	ostream& operator<<(ostream& os, const Word& word) {
		os << word.value << '\t' << word.translation << '\t' << "C: " << word.complexity << ", A: " << word.age << ", F: " << word.frequency;
		return os;
	}
}