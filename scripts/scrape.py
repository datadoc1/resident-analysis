import csv
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import json
import time
import random
import os
import sys

def main():
    # Set the folder name
    folder_name = sys.argv[1]

    # Read the CSV file
    filename = folder_name + '/residency_explorer_links.csv'
    url = "https://www.residencyexplorer.org/"
    pages = []

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            pages.append(row)


    # Create a new Chrome browser instance
    driver = uc.Chrome(headless=False,use_subprocess=False)

    # Go to residencyexplorer.org
    driver.get(url)
    time.sleep(8)
    # Find the element by CSS selector
    driver.find_element(By.CSS_SELECTOR, "#containerSiteHeaderLogin > div > a").click()
    time.sleep(10)
    # Find the username input field by ID and send keys
    username_input = driver.find_element(By.ID, "IDToken1")
    username_input.send_keys("keola1001")
    # Find the password input field by ID and send keys
    password_input = driver.find_element(By.ID, "IDToken2")
    password_input.send_keys("jWEk$Nhmc6Mq")

    # Find the login button by CSS selector and click it
    login_button = driver.find_element(By.CSS_SELECTOR, "#login-btn > span.mdc-button__label")
    login_button.click()
    time.sleep(6)
    # Pull the first link from data

    # Go to the first link
    def scrape_data(link):
        driver.get(link)
        time.sleep(random.uniform(1, 5))

        data = {}
        # Extracting Text with Element Type and Index
        text_elements = driver.find_elements(By.XPATH, "//p | //h1 | //h2 | //h3 | //label | //span | //th | //td")
        for element in text_elements:
            key = f"{element.tag_name}_{text_elements.index(element)}"
            value = element.text.strip()  # Remove leading/trailing whitespace

            # Skip empty elements
            if value:
                data[key] = value

        # Get the h1_38 tag and save as [h1_38].json
        program = data.get("h1_38").replace("/", " ")
        filename = folder_name + "/json/" + program + ".json"

        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

    # Check how many files are in the json directory
    json_folder = folder_name + "/json"
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    
    json_files = os.listdir(json_folder)
    num_files = len(json_files)

    for page in pages[num_files:]:
        print(page[0])
        retries = 0
        while retries < 5:
            try:
                scrape_data(page[0])
                break
            except Exception as e:
                print(f"Exception occurred: {e}")
                retries += 1

if __name__ == '__main__':
    main()