from bs4 import BeautifulSoup
import os
import csv
import sys

folder_path = sys.argv[1]

# Get the path to the HTML file
html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]
html_file_path = os.path.join(folder_path, html_files[0])

# Open the HTML file with latin1 encoding
with open(html_file_path, encoding='latin1') as file:
    # Read the file content
    html_content = file.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <a> tags with href attribute matching the specified format
links = soup.find_all('a', href=lambda href: href and '/Program/GetById/' in href)

# Extract the link URLs
link_urls = [link['href'] for link in links]

# Print the extracted links
for link_url in link_urls:
    print(link_url)

print(f"Number of links extracted: {len(link_urls)}")
# Define the path to the CSV file
csv_file_path = os.path.join(folder_path, 'residency_explorer_links.csv')

# Write the links to the CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows([[link_url] for link_url in link_urls])

print(f"Links saved to: {csv_file_path}")