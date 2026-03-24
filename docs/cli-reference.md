# CLI Reference

The executable runs an interactive prompt. Enter commands after the > prompt.

## Command map

| Group | Goal |
| --- | --- |
| Lifecycle | Load, clear, save, and exit |
| Inspection | Print words, phrases, and dependencies |
| Mutation | Update word metadata fields |
| Help | Discover built-in commands |

## Lifecycle commands

```text
start
load
load words <file>
load phrases <file>
load mem <file>
load <file>
save <file>
save
clear words
clear phrases
exit
```

- start loads default words file data/seed/words.txt and default memory file data/state/mem0.
- load without args behaves like start.
- load <file> is treated as a memory file.

### Lifecycle example

```text
> start
> load phrases data/seed/lesson1.txt
> save data/state/mem0
```

## Inspection commands

```text
print words
print word <word>
print phrases
print phrase "PHRASE"
print phrase_deps "PHRASE"
print phrase_trans "TRANSLATION"
print phrase_trans_deps "TRANSLATION"
print deps
```

## Mutation commands

```text
set word "WORD" frequency <int>
set word "WORD" complexity <int>
set word "WORD" translation <string>
```

### Mutation example

```text
> set word "du" frequency 8
> set word "du" translation "you"
> print word du
```

## Help command

```text
help
```

- Prints built-in command usage summary.

## Placeholders

The following command groups currently exist in the parser but have no implementation:

```text
add
remove
list
```

!!! note "Current parser behavior"
    Placeholder commands are recognized but do not perform operations yet.
