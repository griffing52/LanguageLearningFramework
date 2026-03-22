# IPA Pipeline

## Approach summary

Convert normalized text into phonetic symbols (IPA or IPA-like representation), then synthesize speech from that phonetic sequence.

## Pipeline shape

```text
raw text -> normalization -> grapheme-to-phoneme (IPA) -> phoneme-level synthesis -> wav output
```

## Why this was explored

Swiss German spelling varies heavily by dialect and writer. A phoneme-focused representation can improve pronunciation consistency relative to direct grapheme-based synthesis.

## Strengths

- Better pronunciation control for non-standard orthography.
- Can reduce ambiguity in text-to-sound mapping.
- Potentially easier cross-dialect adaptation with explicit phonemes.

## Limitations

- Requires reliable grapheme-to-phoneme conversion for dialect text.
- IPA inventory and stress handling can become complex.
- End-to-end quality still depends on synthesis backend quality.
- Adds preprocessing complexity and maintenance overhead.

## Practical note

If this method is revisited, keep a versioned pronunciation lexicon and include regression samples to catch pronunciation drift.
