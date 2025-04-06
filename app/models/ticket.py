from app import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    priority = db.Column(db.String(10), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # AI assistance history
    ai_responses = db.Column(db.Text, nullable=True)  # Store AI responses as JSON string
    requires_technician = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Ticket {self.id}: {self.title}>'
