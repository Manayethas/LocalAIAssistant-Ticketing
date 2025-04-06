import requests

OLLAMA_URL = "http://192.168.1.182:11434/api/generate"  # Replace with your AI container's IP

def ask_ai(prompt):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        result = response.json()
        return result.get("response", "Sorry, I couldn't generate a response.")
    except Exception as e:
        return f"AI Error: {str(e)}"
