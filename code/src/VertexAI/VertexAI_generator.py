import requests
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLEAI_STUDIO_API_KEY = os.getenv("GOOGLEAI_STUDIO_API_KEY")
MODEL = "gemini-1.5-pro"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GOOGLEAI_STUDIO_API_KEY}"

def generate(query: str) -> str:

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": query
                    }
                ]
            }
        ],
        "generation_config":{
            "responseMimeType":"application/json"
        }
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(URL, json=data, headers=headers)

    response = response.json()
    print(response)
    return response["candidates"][0]['content']['parts'][0]['text']
