import requests
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama3-70b-8192",  # updated to available model
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is data?"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.text)
