import json
import os

# Assign directory
directory = "d:\\SwissGermanLessons\\raw_data\\"

# Iterate over files in directory

with open('output.txt', 'w', encoding='utf-8') as out:
    for name in os.listdir(directory):
        # Open file
        with open(os.path.join(directory, name), 'r', encoding='utf-8') as f:
            # print(f"Content of '{name}'")

            data = json.load(f)
            for entry in data:
                out.write(f"1/20/25, 08:04 - Me: {entry['phrase-original']}\n")

        
