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


# text = "Hesch du hüt am Morge öpper im Büro gseh."
text = "Du möchtisch öppis Schöns undernäh"

final_text = format_text(text)

inputs = processor(text=final_text, return_tensors="pt")


vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)


# Save the audio to a file (e.g., 'output.wav')
sf.write('output.wav', speech.numpy(), 16000)