print("Loading SpeechT5 model and processor...")

from transformers import SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Processor
import soundfile as sf
import torch
# from gtts import gTTS
import pyttsx3 
import tempfile
import librosa

from helper import format_text


checkpoint = "microsoft/speecht5_tts"
processor = SpeechT5Processor.from_pretrained(checkpoint)

# load my finetuned SpeechT5 model
model = SpeechT5ForTextToSpeech.from_pretrained(
    "griffing52/speecht5_finetuned_griffin_ch_lu"
)

speaker_embeddings = torch.load("C:/Users/griff/source/repos/LanguageLearningFramework/tts/speaker_embeddings.pt")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

print("Model and processor loaded successfully.")

# Load a pre-trained English TTS model
print("Loading English TTS model...")
# tts = gTTS(text=text, lang='en')
# tts.save("test.mp3")
engine = pyttsx3.init(driverName='sapi5')
print("English TTS model loaded successfully.")

# print(speaker_embeddings.shape)


# Example text inputs for testing
# text = "Hesch du hüt am Morge öpper im Büro gseh."
# text = "Du möchtisch öppis Schöns undernäh"
# text = "Ich bi 19i"
# text = "This is a test to see if the TTS model can generate speech in a different language."

def generate_audio(text, path):
    """ 
    Generate speech from text using the SpeechT5 model.
    :param text: The input text to convert to speech.
    :return: The generated speech as a tensor.
    """
    final_text = format_text(text)

    inputs = processor(text=final_text, return_tensors="pt")
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    # Save the audio to a file (e.g., 'output.wav')
    sf.write(path, speech.numpy(), 16000)

# def generate_audio_gtts_en(text, path):
#     """
#     Generate speech from text using gTTS (Google Text-to-Speech).
#     :param text: The input text to convert to speech.
#     :return: The generated speech saved to a file.
#     """

#     tts = gTTS(text=text, lang='en')
#     tts.save(path)

# def generate_audio_coqui_tts(text, path):
    # Generate 16kHz wav directly
    # coqui TTS
    # tts.tts_to_file(text=text, file_path=path, speaker_wav=None, language=None, sample_rate=16000)

def generate_wav_pyttsx3(text, output_path):
    engine.save_to_file(text, output_path)

    # Resample if needed
    # y, sr = librosa.load(temp_path, sr=None)
    # if sr != sample_rate:
        # y = librosa.resample(y, orig_sr=sr, target_sr=sample_rate)
    # sf.write(output_path, y, sample_rate)


def generate_all_pyttsx3():
    engine.runAndWait()
    

def resample(sample_rate, path):
    """ Resample an audio file to a target sample rate. """
    # Resample if needed
    y, sr = librosa.load(path, sr=None)
    if sr != sample_rate:
        y = librosa.resample(y, orig_sr=sr, target_sr=sample_rate)
    sf.write(path, y, sample_rate)