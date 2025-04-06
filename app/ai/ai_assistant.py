import requests

OLLAMA_URL = "http://192.168.1.177:11434/api/generate"  # Update IP as needed

def ask_ai(prompt):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "mistral",
            "prompt": prompt,
            "stream": True
        }, stream=True)

        output = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if data.startswith("data: "):
                    chunk = data.replace("data: ", "")
                    output += chunk
        return output.strip()
    except Exception as e:
        return f"AI Error: {str(e)}"
