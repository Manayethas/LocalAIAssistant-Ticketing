from app import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(100), unique=True, nullable=False)
    issue = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="open")
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
