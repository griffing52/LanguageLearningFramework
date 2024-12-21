// LanguageLearningFramework.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Loader.h"
#include "Debug.h"

#define DEFAULT_WORD_FILE "words.txt"
#define DEFAULT_MEM_FILE "mem0"

using namespace std;

int main()
{
    vector<util::Word*> wordList;
    map<string, util::Word*> wordMap;
    vector<util::Phrase*> phraseList;


	while (true) {
		cout << ">";
		string line;
		getline(cin, line);
		//cin >> line;

		vector<string> args;
		size_t ln = line.length();
		int prevSpace = -1;
		for (size_t i = 0; i <= ln; i++) {
			if (line[i] == '\"') {
				i++;

				int start = i;

				while (line[i] != '\"') {
					i++;
				};

				string arg = line.substr(start, i - start);
				args.push_back(arg);
				prevSpace = ++i;
				continue;
			}

			if (i == ln || line[i] == ' ') {
				string arg = line.substr(prevSpace + 1, i - prevSpace - 1);
				args.push_back(arg);
				prevSpace = i;
			}
		}
		
		if (args.size() == 0) {
			continue;
		}

		if (args[0] == "exit") {
			exit(0);
		}
		else if (args[0] == "start") {
			loader::loadWords(wordList, DEFAULT_WORD_FILE);
			loader::wordListToMap(wordList, wordMap);

			loader::loadMemoryFile(phraseList, wordMap, DEFAULT_MEM_FILE);
		}
		else if (args[0] == "print") {
			if (args.size() == 1) {
				cout << "Missing arguments\n";
				continue;
			}

			if (args[1] == "words") {
				for (auto& word : wordList) {
					cout << word->value << " " << word->translation << endl;
				}
			}
			else if (args[1] == "phrases") {
				for (auto& phrase : phraseList) {
					cout << phrase->value << " " << phrase->translation << endl;
				}
			}
			/*
			printPhrase(string phrase, vector<util::Phrase*> phraseList);
			printPhraseDependencies(string phrase, vector<util::Phrase*> phraseList);
			printPhraseFromTranslation(string tranlsation, vector<util::Phrase*> phraseList);
			printPhraseDependenciesFromTranslation(string tranlsation, vector<util::Phrase*> phraseList);
			*/
			// TODO ADD SIZE CHECK AND ADD TO HELP MENU
			else if (args[1] == "phrase") {
				debug::printPhrase(args[2], phraseList);
			}
			else if (args[1] == "phrase_deps") {
				debug::printPhraseDependencies(args[2], phraseList);
			}
			else if (args[1] == "phrase_trans") {
				debug::printPhraseFromTranslation(args[2], phraseList);
			} 
			else if (args[1] == "phrase_trans_deps") {
				debug::printPhraseDependenciesFromTranslation(args[2], phraseList);
			}
			else if (args[1] == "deps") {
				debug::printAllDependencies(phraseList);
			}
			else {
				cout << '>' << "Invalid argument " << args[1] << endl;
			}
		}
		else if (args[0] == "load") {
			if (args.size() == 1) {
				loader::loadWords(wordList, DEFAULT_WORD_FILE);
				loader::wordListToMap(wordList, wordMap);

				loader::loadMemoryFile(phraseList, wordMap, DEFAULT_MEM_FILE);
				continue;
			}

			if (args[1] == "words") {
				loader::loadWords(wordList, args[2]);
				loader::wordListToMap(wordList, wordMap);
			}
			else if (args[1] == "phrases") {
				loader::addPhrases(phraseList, wordMap, args[2]);
			}
			else if (args[1] == "mem") {
				loader::loadMemoryFile(phraseList, wordMap, args[2]);
			}
			else {
				loader::loadMemoryFile(phraseList, wordMap, args[1]);
			}
		}
		else if (args[0] == "save") {
			if (args.size() == 2) {
				loader::saveMemoryFile(phraseList, args[1]);
				continue;
			}

			else loader::saveMemoryFile(phraseList, DEFAULT_MEM_FILE);
		}
		else if (args[0] == "clear") {
			if (args.size() == 1) {
				cout << "Missing arguments\n";
				continue;
			}

			if (args[1] == "words") {
				wordList.clear();
				wordMap.clear();
			}
			else if (args[1] == "phrases") {
				phraseList.clear();
			}
			else {
				cout << "Invalid argument\n";
			}
		}
		else if (args[0] == "add") {

		}
		else if (args[0] == "remove") {

		}
		else if (args[0] == "list") {

		}
		else if (args[0] == "help") {
			cout << '\t' << "exit" << endl;
			cout << '\t' << "print" << endl;
			cout << '\t' << '\t' << "words" << endl;
			cout << '\t' << '\t' << "phrases" << endl;
			cout << '\t' << '\t' << "phrase \"PHRASE\" " << endl;
			cout << '\t' << '\t' << "phrase_deps \"PHRASE\" " << endl;
			cout << '\t' << '\t' << "phrase_trans \"TRANSLATION\" " << endl;
			cout << '\t' << '\t' << "phrase_trans_deps \"TRANSLATION\" " << endl;
			cout << '\t' << "load" << endl;
			cout << '\t' << '\t' << "words <word file>" << endl;
			cout << '\t' << '\t' << "phrases <phrase file>" << endl;
			cout << '\t' << '\t' << "mem <memory file>" << endl;
			cout << '\t' << '\t' << "<memory file>" << endl;
			cout << '\t' << "clear" << endl;
			cout << '\t' << '\t' << "words" << endl;
			cout << '\t' << '\t' << "phrases" << endl;
			cout << '\t' << "save <memory file name>" << endl;
			cout << '\t' << "add" << endl;
			cout << '\t' << "remove" << endl;
			cout << '\t' << "list" << endl;
			cout << '\t' << "help" << endl;
		}
		else {
			cout << "Invalid command\n";
		}
	}
    
    //string wordFile = "words.txt";
    //cout << "Please enter word file: \n";
    //cin >> wordFile;

    //string phraseFile = "lesson1.txt";
    //cout << "Please enter phrase file: \n";
    //cin >> phrasesFile;

	//string saveFile = "memory.txt";

	/*loader::loadWords(wordList, wordFile);
    loader::wordListToMap(wordList, wordMap);

    loader::loadMemoryFile(phraseList, wordMap, saveFile);
    loader::addPhrases(phraseList, wordMap, phraseFile);*/
	//loader::saveMemoryFile(phraseList, saveFile);
}