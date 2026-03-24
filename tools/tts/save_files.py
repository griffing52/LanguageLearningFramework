import tts
import os
import hashlib
import subprocess
from pydub import AudioSegment

# Hash function to avoid illegal filenames
def hash_text(text):
    return hashlib.sha1(text.encode()).hexdigest()

# Main processor
def process_lesson(lesson_file, output_file="final_lesson.wav"):
    audio_sequence = []
    
    with open(lesson_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip(): continue
            tag, content = line.strip().split("] ", 1)
            tag = tag[1:]  # Remove leading [

            if tag in ["NARRATION", "INTRO"]:
                fname = f"{hash_text(content)}.wav"
                path = f"audio_cache/prompts/{fname}"
                if not os.path.exists(path):
                    tts.generate_audio(content, path) # POTENTIALLY MAKE THIS GENERATION DIFFERENT (English)
                outpath = f"audio_sequence/{i:04d}_{tag}.wav"
                os.system(f'cp "{path}" "{outpath}"')
                audio_sequence.append(outpath)

            elif tag.startswith("WAIT") and tag[4:].isdigit():
                sec = int(tag[4:])
                pause_file = f"pauses/pause_{sec}s.wav"
                if not os.path.exists(pause_file):
                    AudioSegment.silent(duration=sec).export(pause_file, format="wav")
                os.system(f'cp "{pause_file}" "{outpath}"')
                audio_sequence.append(outpath)
                
            elif tag == "WORD":
                fname = f"{content}.wav"
                path = f"audio_cache/words/{fname}"
                if not os.path.exists(path):
                    tts.generate_audio(content, path) # Swiss German
                outpath = f"audio_sequence/{i:04d}_{tag}.wav"
                os.system(f'cp "{path}" "{outpath}"')
                audio_sequence.append(outpath)

            elif tag == "PHRASE":
                fname = f"{hash_text(content)}.wav"
                path = f"audio_cache/phrases/{fname}"
                if not os.path.exists(path):
                    tts.generate_audio(content, path) # Swiss German
                outpath = f"audio_sequence/{i:04d}_{tag}.wav"
                os.system(f'cp "{path}" "{outpath}"')
                audio_sequence.append(outpath)

            else:
                print(f"Unknown tag: {tag}")

    # Write list for ffmpeg
    with open("audio_list.txt", "w") as f:
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