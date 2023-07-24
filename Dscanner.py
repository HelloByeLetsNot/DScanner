import requests
import json
import re


# Define the function to load common words from a JSON file
def load_common_words(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data["commonWords"]
    except Exception as e:
        print("Error loading custom JSON file. Using default common words.")
        return load_default_common_words()


# Define the function to load common words from the default JSON file
def load_default_common_words():
    url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/words/common.json"
    response = requests.get(url)
    return json.loads(response.text)["commonWords"]


# Define the function to scan the URL for directories
def scan_url(url, words):
    found_directories = []
    for word in words:
        dir_url = url + "/" + word
        print("Scanning:", dir_url)
        response = requests.head(dir_url)
        if response.status_code == 200:
            print("[+] Found directory:", dir_url)
            found_directories.append(dir_url)

    return found_directories


# Get user input for URL
url_to_scan = input("Enter a URL to scan: ")

# Get user input for custom JSON file (optional)
use_custom_json = input("Do you want to use a custom JSON file? (y/n): ").lower()

if use_custom_json == 'y':
    custom_json_path = input("Enter the path to your custom JSON file: ")
    common_words = load_common_words(custom_json_path)
else:
    common_words = load_default_common_words()

# Add scheme (http://) if the URL doesn't have one
if not re.match(r'^https?://', url_to_scan):
    url_to_scan = "http://" + url_to_scan

# Scan for directories
found_directories = scan_url(url_to_scan, common_words)

# Get user input for output format (JSON or plain text)
output_format = input("Select output format (JSON or plain text): ").lower()

if output_format == "json":
    # Output the found directories as a JSON object
    output_data = {"found_directories": found_directories}
    output_json = json.dumps(output_data, indent=2)
    print(output_json)

    # If you want to save the JSON object to a file, uncomment the lines below
    # with open("found_directories.json", "w") as file:
    #     file.write(output_json)
elif output_format == "plain text":
    # Output the found directories as plain text
    print("\nFound Directories:")
    for directory in found_directories:
        print(directory)
else:
    print("Invalid output format. Please choose 'JSON' or 'plain text'.")
