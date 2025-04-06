import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ai(user_question, history=None):
    if history is None:
        history = []

    prompt = (
        "You are an IT helpdesk assistant responding to a non-technical user. "
        "Use simple language and provide clear, step-by-step instructions.\n"
    )

    for turn in history:
        prompt += f"User: {turn['question']}\nAssistant: {turn['response']}\n"
    prompt += f"User: {user_question}\nAssistant:"

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Sorry, I couldn’t process that.")
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
