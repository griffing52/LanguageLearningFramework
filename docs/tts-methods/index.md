# TTS Methods

This section documents different text-to-speech approaches explored for this project.

## Why this exists

The Swiss German use case makes TTS quality and pronunciation control especially important. Different methods were tested with different tradeoffs in quality, effort, and flexibility.

## Methods covered

| Method | Main idea | Current status |
| --- | --- | --- |
| Concatenative recordings | Record many words and stitch clips to build phrases | Prototyped |
| IPA-based synthesis | Convert text to IPA and synthesize from phonetic forms | Investigated |
| Fine-tuned SpeechT5 | Start from a pretrained German-capable model and fine-tune on SwissDial | Current direction |

## Recommended read order

1. [Concatenative Recordings](concatenative-word-recordings.md)
2. [IPA Pipeline](ipa-phoneme-pipeline.md)
3. [Fine-tuned SpeechT5](finetuned-speecht5.md)
4. [Method Comparison](comparison.md)

!!! tip "Scope"
    This section is focused on engineering decisions and practical tradeoffs, not only model theory.
