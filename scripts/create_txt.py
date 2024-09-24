import json
import os
import sys

folder_name = sys.argv[1]

# Path to the folder containing JSON files
json_folder = folder_name + '/json'

# Path to the output text folder
txt_folder = folder_name + '/text'

# Create the text folder if it doesn't exist
if not os.path.exists(txt_folder):
    os.makedirs(txt_folder)

# Iterate over the files in the JSON folder
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        # Construct the paths for the JSON file and output text file
        json_file = os.path.join(json_folder, filename)
        txt_file = os.path.join(txt_folder, filename.replace('.json', '.txt'))

        # Read the JSON file
        with open(json_file) as f:
            data = json.load(f)

        # Extract all the values
        values = data.values()

        # Write the values to the text file
        with open(txt_file, 'w') as f:
            for value in values:
                f.write(str(value) + '\n')