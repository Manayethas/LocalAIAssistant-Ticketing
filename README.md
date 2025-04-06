# 🧠 Local AI Assistant Ticketing System

A fully self-hosted helpdesk ticketing system with AI integration, designed to assist non-technical users and reduce helpdesk load by handling common IT issues automatically.

---

## 🚀 Features

- AI-guided troubleshooting (powered by Ollama + Mistral or TinyLLaMA)
- Real-time streaming responses from AI
- Local ticket database (SQLite)
- Resume & resolve tickets
- Session tracking with Flask
- Knowledge base auto-generation (planned)

---

## ⚙️ Requirements

- Python 3.10 or newer
- Flask
- SQLAlchemy
- requests
- Ollama (running separately with models like `mistral`)

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Manayethas/LocalAIAssistant-Ticketing.git
cd LocalAIAssistant-Ticketing
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Delete old test database

```bash
rm instance/tickets.db
```

### 5. Create the database

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

---

## 🧠 Setting up Ollama

Install and run Ollama separately on the same or a different system:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
```

Then start the server with:

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

Make sure port 11434 is open and accessible from your Flask app.

---

## 🔧 Configure Ollama URL & Secret Key

### Edit `app/ai/ai_assistant.py`:
```python
OLLAMA_URL = "http://<your-ai-server-ip>:11434/api/generate"
```

### Edit `app/__init__.py`:
```python
app.config['SECRET_KEY'] = 'replace-this-with-a-secure-secret'
```

You can generate a secret key with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## ✅ Start the Flask App

```bash
python run.py
```

Visit in browser:
```
http://<your-server-ip>:5000
```

---

## 📡 Live Streaming Setup

The AI response stream uses:
- Flask `stream_with_context`
- Proper `text/event-stream` headers
- JavaScript `fetch()` + `ReadableStream`

Make sure you’re not behind a proxy that buffers (e.g., disable NGINX buffering).

---

## 🔐 Notes

- All data stays local.
- No API keys required.
- Easy to deploy on Docker, Proxmox, or bare metal.

---

## 🛠️ Roadmap

- Persistent chat for tickets
- Auto-escalation logic
- Tech-side dashboard
- KB article generation from resolved tickets
