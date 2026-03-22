# Tooling

## Scraping helpers

Location: scraping/

| Script | Type | Output |
| --- | --- | --- |
| LessonScraper.js | Browser userscript | Per-lesson JSON and TXT files |
| dataCleaner.py | Local Python script | Flattened text output for downstream use |

- LessonScraper.js
  - Browser userscript intended for Swiss German lesson pages.
  - Collects phrase/translation pairs and writes JSON and TXT outputs.
- dataCleaner.py
  - Reads downloaded JSON files and emits cleaned lines to output.txt.

These scripts are utility tools and are not part of the C++ build.

## TTS helpers

Location: tts/

See also: [TTS Methods](tts-methods/index.md) for historical approaches and why the current model direction was chosen.

| Script | Purpose | Dependency highlights |
| --- | --- | --- |
| tts.py | Generate speech audio from text | transformers, torch, soundfile |
| helper.py | Normalize and clean text input | Python standard library |
| save_files.py | Concatenate lesson audio assets | ffmpeg, pydub |

- tts.py
  - Uses Hugging Face SpeechT5 model artifacts to synthesize audio.
- helper.py
  - Text normalization helpers including number and character conversions.
- save_files.py
  - Builds lesson audio tracks from tagged script files and ffmpeg concatenation.

## Notes

- Paths in tts.py currently include local absolute paths and may need environment-specific updates.
- tts/requirements.txt is present but currently empty.
- save_files.py assumes ffmpeg is available on PATH.

## Useful commands

```powershell
python scraping/dataCleaner.py
python tts/tts.py
python tts/save_files.py
```

!!! warning "Portability"
    Review hard-coded local paths before sharing scripts across machines.
