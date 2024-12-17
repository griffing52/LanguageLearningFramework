// LanguageLearningFramework.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Loader.h"

using namespace std;

int main()
{
    vector<util::Word*> wordList;
    map<string, util::Word*> wordMap;
    vector<util::Phrase*> phraseList;

    string wordFile = "words.txt";
    //cout << "Please enter word file: \n";
    //cin >> wordFile;

    string phraseFile = "lesson1.txt";
    //cout << "Please enter phrase file: \n";
    //cin >> phrasesFile;

	string saveFile = "memory.txt";

	loader::loadWords(wordList, wordFile);
    loader::wordListToMap(wordList, wordMap);

    //loader::loadMemoryFile(phraseList, saveFile);
    loader::addPhrases(phraseList, wordMap, phraseFile);
	//loader::saveMemoryFile(phraseList, saveFile);
}