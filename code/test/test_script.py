import os
import json
import requests
from pathlib import Path

def send_post_requests(directory: str, url: str, headers: dict = None):
    """
    Reads all .json files in the specified directory and sends POST requests to the given URL.
    
    :param directory: Path to the directory containing .json files.
    :param url: Endpoint to send POST requests to.
    :param headers: Optional headers for the request.
    """
    headers = headers or {"Content-Type": "application/json"}
    
    json_files = Path(directory).glob("*.json")
    
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as file:
                payload = json.load(file)
                
                response = requests.post(url, json=payload, headers=headers)
                
                print(f"File: {json_file.name} -> Status: {response.status_code}")
                print(f"Response: {response.text}\n")
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")

if __name__ == "__main__":
    DIRECTORY = "./payloads"  # Change this to your directory path
    URL = "http://localhost:5000/contextualTesting"  # Change this to your target API URL
    
    send_post_requests(DIRECTORY, URL)
