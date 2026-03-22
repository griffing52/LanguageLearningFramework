# Fine-tuned SpeechT5 (Current Direction)

## Approach summary

Use a pretrained SpeechT5 text-to-speech model, then fine-tune it toward Swiss German speech characteristics.

## Current implementation context

The current repository uses:

```python
checkpoint = "microsoft/speecht5_tts"
model = SpeechT5ForTextToSpeech.from_pretrained(
    "griffing52/speecht5_finetuned_griffin_ch_lu"
)
```

It also applies text normalization in the workflow described in [Tooling](../tooling.md) before synthesis.

## Training/data direction

The approach described for this project is:

- Base model pretrained on German-capable speech data.
- Fine-tuned for Swiss German style using SwissDial data.

## Why this became the primary path

- Produces more natural phrase-level speech than simple concatenation.
- Better generalization to unseen words than fixed recording banks.
- Keeps an extensible ML workflow for future quality improvements.

## Known constraints in current code

- Local absolute path is used for speaker embeddings.
- Vocoder is loaded inside generation flow, which may increase latency.
- Output is currently written to output.wav in the function.

## Next improvement ideas

```text
- Externalize model/embedding paths to config.
- Cache or preload vocoder/model objects once per session.
- Add small evaluation set for pronunciation and intelligibility checks.
- Support output path parameter in generate_audio.
```
