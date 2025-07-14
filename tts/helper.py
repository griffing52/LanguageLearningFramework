import os
import json
from cleaner import format_text, cleanup_text
import numpy as np

def clean_raw_data(directory_path):
    if not os.path.exists("data"):
        os.makedirs("data")
    items_in_directory = os.listdir(directory_path)

    for item_name in items_in_directory:
        full_path = os.path.join(directory_path, item_name)

        if os.path.isfile(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as file:  # 'r' for read mode, 'rb' for binary files
                    # open json files 
                    if item_name.endswith('.json'):
                        data = json.load(file)
                        print(f"Contents of {item_name}:")

                        with open(f"data/{item_name.replace('.json', '.txt').replace('_','')}", 'w', encoding='utf-8') as outfile:
                            for entry in data:
                                outfile.write(f"{format_text(entry['phrase'])}={entry['translation']}\n")
            except Exception as e:
                print(f"Error opening or reading {item_name}: {e}")

def clean_formatted_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        with open(path.replace(".txt", "_cleaned.txt"), "w", encoding="utf-8") as fo:
            for line in lines:
                if '=' not in line:
                    print(f"Line without '=' found in {path}: {line.strip()}")
                else:
                    a, b = line.split('=')
                    fo.write(f"{format_text(a)}={b}")

# add support for known words?  
def generate_words_from_csv(path):
    data = np.loadtxt(path, delimiter=',', dtype=str, encoding='utf-8') 
    with open("input/words_gen.txt", "w", encoding="utf-8") as f:
        for swiss, english in data:
            if english == "" or swiss == "":
                print(f"Skipping empty entry: Swiss='{swiss}', English='{english}'")
                continue
            swiss_clean = format_text(swiss)
            english_clean = cleanup_text(english).strip()
            f.write(f"{swiss_clean}={english_clean}\n")

generate_words_from_csv('tts/swiss_dict.csv')

# clean_formatted_file("input/test_lesson.txt")
# clean_raw_data("H:/SwissGermanLessons/raw_data")