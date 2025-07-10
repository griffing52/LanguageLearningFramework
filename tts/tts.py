print("Loading SpeechT5 model and processor...")

from transformers import SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Processor
import soundfile as sf
import torch
from TTS.api import TTS

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
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
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

def generate_audio_gtts_en(text, path):
    """
    Generate speech from text using gTTS (Google Text-to-Speech).
    :param text: The input text to convert to speech.
    :return: The generated speech saved to a file.
    """
    # Generate 16kHz wav directly
    tts.tts_to_file(text=text, file_path=path, speaker_wav=None, language=None, sample_rate=16000)
