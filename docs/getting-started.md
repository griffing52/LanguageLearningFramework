# Getting Started

This page covers the fastest path to run docs and the C++ app locally.

## Prerequisites

- Windows with Visual Studio (C++ Desktop workload) for the C++ solution.
- Python 3.10+ for scripting and docs tooling.
- Optional: Node.js if you plan to modify browser scraping scripts.

## Repository layout

- C++ core: root-level .cpp/.h files and the Visual Studio solution.
- Scraping helper: scraping/.
- TTS helper scripts: tts/.
- Documentation site: docs/ plus mkdocs.yml.

## Build and run the C++ app

1. Open LanguageLearningFramework.sln in Visual Studio.
2. Build the solution in Debug or Release.
3. Run the executable from Visual Studio or terminal.

## First-session CLI flow

```text
> start
> print words
> print phrases
> help
```

## Build docs locally

Install docs dependencies:

```powershell
pip install -r requirements-docs.txt
```

Serve docs locally:

```powershell
mkdocs serve
```

Build a static site:

```powershell
mkdocs build
```

The generated static site is written to the site/ folder.

## Common issues

| Issue | Likely cause | Fix |
| --- | --- | --- |
| mkdocs not found | Scripts path not on PATH | Run python -m mkdocs serve |
| Empty phrase load | words not loaded first | Run start or load words <file> before load phrases <file> |
| Missing TTS output | model assets not available | Check local model paths in tts/tts.py |

!!! tip "Recommended workflow"
    Keep one terminal for mkdocs serve and another terminal for CLI app testing.
