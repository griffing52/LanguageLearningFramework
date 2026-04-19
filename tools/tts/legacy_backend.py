"""Adapter for the legacy stitched-audio backend.

The backend is expected to live in a Git submodule rooted at
tools/tts/SwissGermanLanguage unless overridden by options or environment.
"""

from __future__ import annotations

import inspect
import os
import sys
from pathlib import Path
from typing import Any, Callable

from pydub import AudioSegment


DEFAULT_LEGACY_ROOT = Path(os.getenv("TTS_LEGACY_ROOT", Path(__file__).resolve().parent / "SwissGermanLanguage"))
DEFAULT_LEGACY_FUNCTIONS = (
    "generate_audio",
    "synthesize",
    "build_audio",
    "render_audio",
    "process_lesson",
)


def _ensure_legacy_path(legacy_root: Path) -> None:
    legacy_root_str = str(legacy_root)
    if legacy_root_str not in sys.path:
        sys.path.insert(0, legacy_root_str)


def _load_legacy_module(legacy_root: Path):
    if not legacy_root.exists():
        raise FileNotFoundError(
            f"Legacy TTS submodule not found at {legacy_root}. Add the SwissGermanLanguage submodule first."
        )

    _ensure_legacy_path(legacy_root)
    return None


def _call_candidate(function: Callable[..., Any], text: str, output_path: Path, options: dict[str, Any]) -> Any:
    signature = inspect.signature(function)
    parameters = signature.parameters

    if "output_path" in parameters:
        return function(text, output_path=str(output_path), **options)
    if len(parameters) >= 2:
        return function(text, str(output_path), **options)
    return function(text, **options)


def generate_audio(
    text: str,
    output_path: str | os.PathLike[str] = "output.wav",
    *,
    legacy_root: str | os.PathLike[str] | None = None,
    legacy_function: str | None = None,
    **options: Any,
) -> str:
    """Generate audio using the legacy backend and normalize the output path."""
    resolved_root = Path(legacy_root) if legacy_root else DEFAULT_LEGACY_ROOT
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    _load_legacy_module(resolved_root)

    import util

    util.audioDir = str(resolved_root / "audio") + os.sep
    Path(util.audioDir).mkdir(parents=True, exist_ok=True)
    Path(util.audioDir, "generated").mkdir(parents=True, exist_ok=True)

    legacy_mode = str(options.pop("mode", "stitched")).lower()
    source_audio_path = None

    if legacy_mode == "stitched":
        normalized_phrase = options.pop("phrase_key", text.strip()).strip().replace(" ", "-")
        try:
            util.mp3FromPhrase(normalized_phrase)
            source_audio_path = Path(util.audioDir) / "generated" / f"{normalized_phrase}.mp3"
        except Exception:
            legacy_mode = "speech"

    if legacy_mode != "stitched":
        generated_name = options.pop("file_name", output_file.stem)
        util.textToSpeech(text, generated_name)
        source_audio_path = Path(util.audioDir) / "generated" / f"{generated_name}.mp3"

    if source_audio_path is None or not source_audio_path.exists():
        raise FileNotFoundError("Legacy backend did not create an audio file")

    if output_file.suffix.lower() == ".mp3":
        if source_audio_path != output_file:
            output_file.write_bytes(source_audio_path.read_bytes())
        return str(output_file)

    audio = AudioSegment.from_mp3(source_audio_path)
    audio.export(output_file, format=output_file.suffix.lstrip(".") or "wav")
    return str(output_file)

