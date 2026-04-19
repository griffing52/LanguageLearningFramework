import hashlib
import os
import subprocess
import shutil
from pathlib import Path

from pydub import AudioSegment

from backends import is_local_method, load_local_backend, normalize_method

# Hash function to avoid illegal filenames
def hash_text(text):
    return hashlib.sha1(text.encode()).hexdigest()

def _copy_file(source_path, destination_path):
    destination = Path(destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination)


def _generate_audio(content, output_path, tts_method, tts_options):
    backend = load_local_backend(tts_method)
    return backend.generate_audio(content, output_path=output_path, **tts_options)


# Main processor
def process_lesson(lesson_file, output_file="final_lesson.wav", tts_method="speecht5", tts_options=None):
    audio_sequence = []
    selected_method = normalize_method(tts_method)
    if not is_local_method(selected_method):
        raise ValueError("Lesson assembly currently supports only local TTS methods: speecht5, legacy_stitched, or orpheus_lora")

    tts_options = dict(tts_options or {})

    Path("audio_cache/prompts").mkdir(parents=True, exist_ok=True)
    Path("audio_cache/words").mkdir(parents=True, exist_ok=True)
    Path("audio_cache/phrases").mkdir(parents=True, exist_ok=True)
    Path("audio_sequence").mkdir(parents=True, exist_ok=True)
    Path("pauses").mkdir(parents=True, exist_ok=True)

    with open(lesson_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            tag, content = line.strip().split("] ", 1)
            tag = tag[1:]  # Remove leading [

            if tag in ["NARRATION", "INTRO"]:
                fname = f"{hash_text(content)}.wav"
                path = Path("audio_cache/prompts") / fname
                if not path.exists():
                    _generate_audio(content, str(path), selected_method, tts_options)
                outpath = Path("audio_sequence") / f"{i:04d}_{tag}.wav"
                _copy_file(path, outpath)
                audio_sequence.append(str(outpath))

            elif tag.startswith("WAIT") and tag[4:].isdigit():
                sec = int(tag[4:])
                pause_file = Path("pauses") / f"pause_{sec}s.wav"
                if not pause_file.exists():
                    AudioSegment.silent(duration=sec).export(pause_file, format="wav")
                outpath = Path("audio_sequence") / f"{i:04d}_{tag}.wav"
                _copy_file(pause_file, outpath)
                audio_sequence.append(str(outpath))

            elif tag == "WORD":
                fname = f"{content}.wav"
                path = Path("audio_cache/words") / fname
                if not path.exists():
                    _generate_audio(content, str(path), selected_method, tts_options)
                outpath = Path("audio_sequence") / f"{i:04d}_{tag}.wav"
                _copy_file(path, outpath)
                audio_sequence.append(str(outpath))

            elif tag == "PHRASE":
                fname = f"{hash_text(content)}.wav"
                path = Path("audio_cache/phrases") / fname
                if not path.exists():
                    _generate_audio(content, str(path), selected_method, tts_options)
                outpath = Path("audio_sequence") / f"{i:04d}_{tag}.wav"
                _copy_file(path, outpath)
                audio_sequence.append(str(outpath))

            else:
                print(f"Unknown tag: {tag}")

    # Write list for ffmpeg
    with open("audio_list.txt", "w", encoding="utf-8") as f:
        for path in audio_sequence:
            f.write(f"file '{path}'\n")

    # 🧵 Stitch audio together
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "audio_list.txt",
        "-c", "copy",
        output_file
    ])
    print(f"✅ Lesson built: {output_file}")

# Example usage
# process_lesson("lesson_italie.txt")