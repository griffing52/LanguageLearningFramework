import re

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
            return f"{number_words[unit]}e{number_words[tens * 10]}"
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
    result = re.sub(r'\b\d+(?=\D)', replace, text)

    return result

replacements = [
    ("â", "a"),  # Long a
    ("ç", "ch"),  # Ch as in "chair"
    ("ğ", "gh"),  # Silent g or slight elongation of the preceding vowel
    ("ı", "i"),   # Dotless i
    ("î", "i"),   # Long i
    ("ö", "oe"),  # Similar to German ö
    ("ş", "sh"),  # Sh as in "shoe"
    ("ü", "ue"),  # Similar to German ü
    ("û", "u"),   # Long u
]

# Function to clean up text using the replacement pairs
def cleanup_text(text):
    for src, dst in replacements:
        text = text.replace(src, dst)
    return text

def normalize_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation (except apostrophes)
    text = re.sub(r'[^\w\s\']', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text

def format_text(text):
    converted_text = replace_numbers_with_words(text)
    cleaned_text = cleanup_text(converted_text)
    final_text = normalize_text(cleaned_text)
    return final_text