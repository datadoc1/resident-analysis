import subprocess

folder_name = 'diagnostic_radiology'

# Run extract_links.py
subprocess.run(['python', 'extract_links.py', folder_name])

# Run import_csv.py
subprocess.run(['python', 'scrape.py', folder_name])

# Run create_txt.py with text_extract argument
subprocess.run(['python', 'create_txt.py', folder_name])

# Run text_extract.py
subprocess.run(['python', 'text_extract.py', folder_name, 'Radiology - Diagnostic'])