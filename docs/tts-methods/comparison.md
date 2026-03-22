# Method Comparison

## Side-by-side view

| Criterion | Concatenative recordings | IPA pipeline | Fine-tuned SpeechT5 |
| --- | --- | --- | --- |
| Setup complexity | Low to medium | Medium to high | High |
| Data requirement | Recording effort | Pronunciation resources + synthesis data | Labeled training audio/text |
| Pronunciation control | High per recorded token | High if G2P quality is strong | Medium to high via model behavior |
| Naturalness | Low to medium | Medium | Medium to high |
| Scalability | Low | Medium | High |
| Best fit | Small fixed phrase sets | Pronunciation-focused research | Production-like lesson generation |

## Decision outcome

The project direction moved to a fine-tuned SpeechT5 approach (pretrained baseline, then SwissDial-oriented fine-tuning) because it balances naturalness and scalability better than earlier approaches.

!!! note "Not final forever"
    The methods are complementary. Concatenative and IPA workflows may still be useful for constrained drills, pronunciation experiments, or fallback generation.

## Suggested evaluation dimensions

```text
- Intelligibility on held-out lesson phrases
- Dialect pronunciation fidelity
- Naturalness/prosody across sentence boundaries
- Inference speed for lesson batch generation
- Out-of-vocabulary robustness
```
