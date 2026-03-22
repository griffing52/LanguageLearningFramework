# Data Files

This project is data-first: most behavior depends on the structure and quality of text files.

## File summary

| File | Purpose | Loaded by |
| --- | --- | --- |
| words.txt | Dictionary entries and synonyms | load words / start |
| lesson1.txt | Phrase and translation pairs | load phrases |
| mem0 | Serialized study state and dependencies | load mem / start |

## Words file

Default file: words.txt

Expected line structure:

```text
word=translation
word1,word2,word3=translation
*word=translation
!word=translation
```

Notes:

- Synonyms map to the same Word object.
- *word marks a known word.
- !word marks an important word.

!!! tip "Safe authoring"
   Keep one entry per line and avoid trailing spaces around the = delimiter.

Markers affect initial metadata:

- \* sets low complexity and known/aged values.
- ! increases complexity and age for prioritization.

## Phrase lesson file

Default sample: lesson1.txt

Expected line structure:

```text
phrase text=translation
```

A phrase is split by spaces. Every token in the phrase must exist in the loaded word map.

If a token is missing from words, phrase loading stops with an error message.

### Phrase example

```text
ich bi neui da=i am new here
du bisch da=you are here
```

## Memory file

Default file: mem0

Saved memory format is line-based and includes:

1. Total phrase count.
2. For each phrase:
   - phrase value
   - phrase translation
   - frequency
   - age
   - dependency count
3. Dependency indices serialized after phrase records.

Example shape:

```text
<num_phrases>
<phrase_0_value>
<phrase_0_translation>
<phrase_0_frequency>
<phrase_0_age>
<phrase_0_dependency_count>
...
<dep_index_0>
<dep_index_1>
...
```

This format is designed for compact load/save between sessions.

## Validation checklist

- Every phrase token exists in loaded words.
- No blank value before or after =.
- Memory file phrase count matches actual serialized records.
- Files are UTF-8 encoded when non-ASCII text is used.

## Other data files in repository

- known_words.txt and known_phrases.txt for reference vocab sets.
- listArray.json and other helper files used by scripts/tools.
