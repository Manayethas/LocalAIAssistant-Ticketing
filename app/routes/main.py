from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import uuid
from datetime import datetime
from app.models.ticket import Ticket
from app import db
from app.ai.ai_assistant import ask_ai

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/start", methods=["GET", "POST"])
def start_ticket():
    if request.method == "POST":
        ticket_id = str(uuid.uuid4())
        issue = request.form["issue"]
        ticket = Ticket(ticket_id=ticket_id, issue=issue, status="open", last_updated=datetime.now())
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("main.view_ticket", ticket_id=ticket_id))
    return render_template("start.html")

@main.route("/ticket/<ticket_id>")
def view_ticket(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first_or_404()
    return render_template("ticket.html", ticket=ticket)

@main.route("/ticket/ai/<ticket_id>")
def get_ai_response(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first_or_404()
    ai_response = ask_ai(f"The user is having the following issue: {ticket.issue}. How can we help them troubleshoot?")
    return jsonify({"response": ai_response})
