from transformers import SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Processor
import soundfile as sf
import torch

from helper import format_text

checkpoint = "microsoft/speecht5_tts"
processor = SpeechT5Processor.from_pretrained(checkpoint)

model = SpeechT5ForTextToSpeech.from_pretrained(
    "griffing52/speecht5_finetuned_griffin_ch_lu"
)

speaker_embeddings = torch.load("C:/Users/griff/source/repos/LanguageLearningFramework/tts/speaker_embeddings.pt")
# print(speaker_embeddings.shape)

# Example text inputs for testing
# text = "Hesch du hüt am Morge öpper im Büro gseh."
# text = "Du möchtisch öppis Schöns undernäh"
# text = "Ich bi 19i"
# text = "This is a test to see if the TTS model can generate speech in a different language."

def generate_audio(text):
    """ 
    Generate speech from text using the SpeechT5 model.
    :param text: The input text to convert to speech.
    :return: The generated speech as a tensor.
    """
    final_text = format_text(text)

    inputs = processor(text=final_text, return_tensors="pt")


    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    # Save the audio to a file (e.g., 'output.wav')
    sf.write('output.wav', speech.numpy(), 16000)
