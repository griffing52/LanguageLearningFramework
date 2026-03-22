# Concatenative Recordings

## Approach summary

Record a bank of individual word clips, then concatenate them into full phrases and lessons.

## Pipeline shape

```text
word list -> recorded wav clips -> lookup by token -> ordered clip list -> ffmpeg concat output
```

## Strengths

- High control over exact pronunciation per recorded token.
- Easy to understand and debug.
- Can work without model training.

## Limitations

- Requires many recordings to get broad coverage.
- Prosody is often unnatural at sentence boundaries.
- Coarticulation is missing because words are spoken in isolation.
- Out-of-vocabulary words require new recordings.

## Where this appears in the repo

The lesson stitching style is related to the batching/concat workflow described in [Tooling](../tooling.md), although the current script uses generated audio caches rather than purely human recordings.

## Best use cases

- Very small fixed phrase sets.
- Drill content with stable vocabulary.
- Early prototype audio for lesson flow testing.
