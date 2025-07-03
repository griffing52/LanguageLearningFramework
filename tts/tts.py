from transformers import SpeechT5Processor, SpeechT5HifiGan
import soundfile as sf
import torch

model = SpeechT5ForTextToSpeech.from_pretrained(
    "griffing52/speecht5_finetuned_emirhan_tr"
)

example = dataset["test"][104]
speaker_embeddings = torch.tensor(example["speaker_embeddings"]).unsqueeze(0)

# text = "Hesch du hüt am Morge öpper im Büro gseh."
text = "Du möchtisch öppis Schöns undernäh"

number_words = {
    0: "null", 1: "eis", 2: "zwöi", 3: "drü", 4: "vier", 5: "füf", 6: "sächs", 7: "sibe", 8: "acht", 9: "nün",
    10: "zäh", 11: "elf", 12: "zwölf", 13: "drüzäh", 14: "vierzäh", 15: "füfzäh", 16: "sächzäh",
    17: "sibezäh", 18: "achtzäh", 19: "nünzäh", 20: "zwänzg", 30: "dryssg", 40: "vierzg",
    50: "füfzg", 60: "sächzg", 70: "sibezg", 80: "achtzg", 90: "nünzg", 100: "hundert", 1000: "tusig"
}

def number_to_words(number):
    if number < 20:
        return number_words[number]
    elif number < 100:
        tens, unit = divmod(number, 10)
        if unit == 0:
            return number_words[tens * 10]
        else:
            return f"{number_words[unit]}-e-{number_words[tens * 10]}"
    elif number < 1000:
        hundreds, remainder = divmod(number, 100)
        result = "hundert" if hundreds == 1 else f"{number_words[hundreds]} hundert"
        return result + (f" {number_to_words(remainder)}" if remainder else "")
    elif number < 1_000_000:
        thousands, remainder = divmod(number, 1000)
        result = "tusig" if thousands == 1 else f"{number_to_words(thousands)} tusig"
        return result + (f" {number_to_words(remainder)}" if remainder else "")
    else:
        return str(number)

def replace_numbers_with_words(text):

    def replace(match):
        number = int(match.group())
        return number_to_words(number)

    # Find the numbers and change with words.
    result = re.sub(r'\b\d+\b', replace, text)

    return result

# Function to clean up text using the replacement pairs
def cleanup_text(text):
    for src, dst in replacements:
        text = text.replace(src, dst)
    return text

converted_text = replace_numbers_with_words(text)
cleaned_text = cleanup_text(converted_text)
final_text = normalize_text(cleaned_text)

inputs = processor(text=final_text, return_tensors="pt")


vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)


# Save the audio to a file (e.g., 'output.wav')
sf.write('output.wav', speech.numpy(), 16000)