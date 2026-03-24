# Architecture

This page describes how data moves through the C++ core and where responsibilities live.

## Core domain model

The model is defined in Util.h.

- Word
  - value, translation, complexity, frequency, age.
- Phrase (inherits Word)
  - words: set of Word pointers used in the phrase.
  - dependencies: set of Phrase pointers derived from overlap logic.

## Core modules

| Module | Responsibility |
| --- | --- |
| apps/cpp-cli/src/Main.cpp | Command parsing and dispatch |
| apps/cpp-cli/src/Loader.cpp | File parsing and serialization |
| apps/cpp-cli/src/Debug.cpp | Lookup and print helpers |
| apps/cpp-cli/src/Planner.cpp | Study-target selection heuristics |
| apps/cpp-cli/src/Timer.cpp | Time-related utilities |

- apps/cpp-cli/src/Main.cpp
  - Interactive command loop and command dispatch.
- apps/cpp-cli/src/Loader.cpp
  - Parsing words and phrases, dependency inference, memory save/load.
- apps/cpp-cli/src/Debug.cpp
  - Print and lookup helpers for inspection commands.
- apps/cpp-cli/src/Planner.cpp
  - Selection and cost heuristics for next learning target.
- apps/cpp-cli/src/Timer.cpp
  - Timing-related utilities.

## High-level data flow

1. Load words from dictionary file into list + map.
2. Load or add phrases, linking phrase tokens to words.
3. Compute phrase dependencies from phrase word-set containment.
4. Inspect or mutate objects from CLI commands.
5. Save phrase memory back to disk.

```text
data/seed/words.txt ---> Loader ---> Word list/map -------+
                                          |
data/seed/lesson1.txt -> Loader -> Phrase list -----+--> Debug/Planner/Main
                                          |
data/state/mem0 -------> Loader ----------------------+--> save/load cycle
```

## Dependency inference behavior

A phrase A is considered a dependency of phrase B when all words in A are present in B.
This is implemented as set inclusion against phrase word sets after phrases are loaded.

## Current constraints

- Data is primarily pointer-based and mutable in-memory.
- Input validation is basic and command argument checks are uneven.
- Some parser branches are duplicated or incomplete and may need cleanup.

!!! note "Design tradeoff"
    Pointer-based objects keep updates simple during one session but require careful ownership/memory management if the project grows.
