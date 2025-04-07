import ollama
from flask import current_app
import json
from datetime import datetime

class OllamaService:
    def __init__(self):
        self.client = ollama.Client()
        self.model = "llama2"  # Default model, can be configured

    def chat(self, message, history=None):
        """Send a message to Ollama and get a response"""
        try:
            # Prepare the chat history
            messages = []
            if history:
                for h in history:
                    messages.append({"role": "user", "content": h["question"]})
                    messages.append({"role": "assistant", "content": h["response"]})
            
            # Add the current message
            messages.append({"role": "user", "content": message})
            
            # Get response from Ollama
            response = self.client.chat(model=self.model, messages=messages)
            
            return {
                "response": response["message"]["content"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            current_app.logger.error(f"Error in Ollama chat: {str(e)}")
            return {
                "response": "I'm sorry, I encountered an error processing your request.",
                "timestamp": datetime.utcnow().isoformat()
            }

    def update_ticket_ai_history(self, ticket, question, response):
        """Update the ticket's AI response history"""
        current_responses = json.loads(ticket.ai_responses or "[]")
        current_responses.append({
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "response": response
        })
        ticket.ai_responses = json.dumps(current_responses) 