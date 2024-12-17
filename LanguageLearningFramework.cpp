// LanguageLearningFramework.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Loader.h"

using namespace std;

int main()
{
	vector<util::Word*> wordList;

	cout << sizeof(util::Word) << endl;

    string wordFile = "words.txt";
    //cout << "Please enter word file: \n";
    //cin >> wordFile;

    string phrasesFile = "lesson1.txt";
    //cout << "Please enter phrase file: \n";
    //cin >> phrasesFile;

	loader::loadWords(wordList, wordFile);
}