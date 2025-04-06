import requests

OLLAMA_URL = "http://192.168.1.177:11434/api/generate"

def ask_ai(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False  # Important: non-streamed mode
    })

    try:
        return response.json()["response"]
    except Exception as e:
        return f"[⚠️ AI error: {str(e)}]"
