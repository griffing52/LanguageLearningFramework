# C++ File Overview

This document describes what each C++ source and header file in this repository does.

## Main Program

### Main.cpp
- Entry point for the console application.
- Implements a command loop (`>`) that parses user commands and dispatches behavior.
- Owns in-memory containers:
  - `vector<util::Word*> wordList`
  - `map<string, util::Word*> wordMap`
  - `vector<util::Phrase*> phraseList`
- Handles commands such as:
  - `start`, `load`, `save`, `clear`, `print`, `set`, `help`, `exit`
- Uses `loader` namespace functions for loading/saving data and `debug` namespace functions for diagnostics and printing.

## Data Model and Utilities

### Util.h
- Defines core data structures in namespace `util`.
- `struct Word`:
  - Fields: `value`, `translation`, `complexity`, `frequency`, `age`.
  - Includes a comparator-style `operator()` used for priority ordering logic.
- `struct Phrase : public Word`:
  - Adds `set<Word*> words` (tokenized words in phrase).
  - Adds `set<Phrase*> dependencies` (phrases this phrase depends on).
- `class Compare`:
  - Comparator for ordering `Word*` by complexity/frequency/age.
- Declares stream output overload:
  - `ostream& operator<<(ostream& os, const Word& word);`

### Util.cpp
- Implements `util::operator<<` for `Word`.
- Prints a compact summary of a word, including translation and `C` (complexity), `A` (age), `F` (frequency).

## Loading and Persistence

### Loader.h
- Declares all file I/O and persistence-related functions in namespace `loader`.
- Core responsibilities:
  - Load dictionary words into list + lookup map.
  - Load phrase lessons and build dependency graph.
  - Save and restore phrase memory/state from disk.

### Loader.cpp
- Implements parsing and persistence logic.
- `loadWords(...)`:
  - Reads dictionary lines from file.
  - Parses forms like synonyms and translations using delimiters.
  - Supports markers:
    - `*` known word (reduced complexity, learned state)
    - `!` important word (boosted complexity/age)
  - Populates both `wordList` and `wordMap`.
- `wordListToMap(...)`:
  - Deprecated helper to build map from list.
- `addPhrases(...)`:
  - Parses phrase lines (`phrase=translation`).
  - Splits phrase into words and resolves each from `wordMap`.
  - Computes phrase complexity from component words.
  - Builds phrase dependency relationships after all phrases are loaded.
- Internal helper `savePhraseDependencies(...)`:
  - Marks phrase dependencies when one phrase's word set is contained in another phrase.
- `saveMemoryFile(...)`:
  - Writes phrase metadata and dependency indices to a memory file.
- `loadMemoryFile(...)`:
  - Reconstructs phrases, metadata, word references, and dependencies from memory file.

## Planning / Selection Logic

### Planner.h
- Declares selection/scoring functions in namespace `planner`.
- `chooseNext(Phrase* phrase)` returns the next target word/phrase dependency to practice.
- `calculateCost(Word* word)` computes a cost score used by planning heuristics.

### Planner.cpp
- Implements practice-selection heuristics.
- `chooseNext(...)`:
  - Early null check.
  - Uses randomized gating to avoid deterministic repetition.
  - Preference order:
    1. Lower-frequency words inside phrase under a threshold.
    2. Phrase dependencies when dependency effort condition is met.
    3. Remaining phrase words up to phrase complexity threshold.
  - Returns `nullptr` when no candidate should be selected.
- `calculateCost(...)`:
  - Returns 0 for known words (`complexity == 0`).
  - Computes score roughly proportional to complexity and inversely proportional to frequency and age.
  - Adds bounded random noise (`ALPHA`) for exploration.

## Debug / Inspection Helpers

### Debug.h
- Declares print and lookup helper functions in namespace `debug`.
- Supports:
  - Word lookup and print by string.
  - Phrase list printing.
  - Phrase/dependency printing by phrase text or translation.
  - Dumping dependencies for all phrases.

### Debug.cpp
- Implements the `debug` helper functions.
- Provides console-friendly diagnostics for interactive use from the command loop.
- Includes utility functions to:
  - Print one word from `wordMap`.
  - Print phrase summaries.
  - Print dependency sets and full dependency report.

## Timing Stub

### Timer.h
- Header placeholder with only `#pragma once`.
- Currently has no declarations.

### Timer.cpp
- Contains commented-out example code for timing execution with `std::chrono`.
- Not currently integrated into the active program flow.

## High-Level Interaction Between Files

- `Main.cpp` is the orchestrator.
- `Loader.cpp/.h` builds and persists the learning state.
- `Util.cpp/.h` defines shared data types and formatting.
- `Planner.cpp/.h` encapsulates next-item selection heuristics.
- `Debug.cpp/.h` provides inspection and diagnostics.
- `Timer.cpp/.h` is currently a scaffold for future performance measurement.
