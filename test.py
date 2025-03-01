import requests
import json
import re
import os

def fetch_repo_file_contents(url, json_filename="github_repo_files.json"):
    # Extract owner and repo name from the URL
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not match:
        print("Invalid GitHub repository URL.")
        return
    
    owner, repo = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    # Make API request to get file list
    response = requests.get(api_url)

    if response.status_code == 200:
        files_data = response.json()

        # Load existing JSON file if exists
        if os.path.exists(json_filename):
            with open(json_filename, "r") as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}

        # Fetch code for each file
        repo_data = {}
        for file in files_data:
            if file["type"] == "file" and file.get("download_url"):
                file_name = file["name"]
                file_url = file["download_url"]

                # Fetch the file content
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    repo_data[file_name] = file_response.text
                else:
                    repo_data[file_name] = "Error fetching file"

        # Update JSON with repository code
        existing_data[repo] = repo_data

        # Save updated data
        with open(json_filename, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
        
        print(f"File contents updated in {json_filename}")

    elif response.status_code == 404:
        print("Repository or contents not found. Check the URL.")
    else:
        print(f"Failed to fetch repository contents. Status Code: {response.status_code}")

# Example usage
repo_url = input("Enter a GitHub repository URL: ")
fetch_repo_file_contents(repo_url)
