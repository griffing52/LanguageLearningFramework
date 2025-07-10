import tts
import os
import hashlib
import subprocess
from pydub import AudioSegment
from tqdm import tqdm

# Hash function to avoid illegal filenames
def hash_text(text):
    return hashlib.sha1(text.encode()).hexdigest()
    # return text

# Main processor
def process_lesson(lesson_file, output_file="final_lesson.wav"):
    audio_sequence = []
    lessonName = lesson_file.split("/")[-1].split(".")[0]
    print(f"Processing lesson: {lessonName}")
    
    with open(lesson_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip(): continue
            tag, content = line.strip().split("] ", 1)
            tag = tag[1:]  # Remove leading [

            if tag in ["NARRATION", "INTRO"]:
                fname = f"{hash_text(content)}.mp3"
                path = f"audio_cache/prompts/{fname}" 
                if not os.path.exists(path):
                    tts.generate_audio_gtts_en(content, path) 
                # outpath = f"audio_sequence/{i:04d}_{tag}.wav"
                # os.system(f'cp "{path}" "{outpath}"')
                audio_sequence.append(path)

            elif tag == "WAIT":
                sec = int(content)
                pause_file = f"audio_cache/pauses/pause_{sec}s.wav"
                if not os.path.exists(pause_file):
                    AudioSegment.silent(duration=sec * 1000).export(pause_file, format="wav")
                # os.system(f'cp "{pause_file}" "{outpath}"')
                audio_sequence.append(pause_file)
                
            elif tag == "WORD":
                fname = f"{hash_text(content)}.wav"
                path = f"audio_cache/words/{fname}"
                if not os.path.exists(path):
                    tts.generate_audio(content, path) # Swiss German
                # outpath = f"audio_sequence/{i:04d}_{tag}.wav"
                # os.system(f'cp "{path}" "{outpath}"')
                audio_sequence.append(path)

            elif tag == "PHRASE":
                fname = f"{hash_text(content)}.wav"
                path = f"audio_cache/phrases/{fname}"
                if not os.path.exists(path):
                    tts.generate_audio(content, path) # Swiss German
                # outpath = f"audio_sequence/{i:04d}_{tag}.wav"
                # os.system(f'cp "{path}" "{outpath}"')
                audio_sequence.append(path)

            else:
                print(f"Unknown tag: {tag}")

    # Write list for ffmpeg
    with open("audio_list.txt", "w") as f:
        for path in audio_sequence:
            f.write(f"file '{path}'\n")

    # Stitch audio together
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "audio_list.txt",
        "-ar", "16000",  # Set audio sample rate
        "-ac", "1",       # Set audio channels to mono
        "-c:a", "pcm_s16le",  # WAV format
        output_file
    ])
    print(f"Lesson built: {output_file}")

# Example usage
process_lesson("lessons/lesson_1.txt")