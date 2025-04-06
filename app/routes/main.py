from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import uuid
from datetime import datetime
from app.models.ticket import Ticket
from app import db
from app.ai.ai_assistant import ask_ai

main = Blueprint("main", __name__)

@main.route("/")
def index():
    last_ticket = session.get('last_ticket_id')
    return render_template("index.html", last_ticket=last_ticket)

@main.route("/start", methods=["GET", "POST"])
def start_ticket():
    if request.method == "POST":
        ticket_id = str(uuid.uuid4())
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get("User-Agent")
        ticket = Ticket(
            ticket_id=ticket_id,
            issue=request.form["issue"],
            status="open",
            last_updated=datetime.now(),
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            email=request.form["email"],
            username=request.form["username"],
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(ticket)
        db.session.commit()
        session['last_ticket_id'] = ticket_id
        return redirect(url_for("main.view_ticket", ticket_id=ticket_id))
    return render_template("start.html")

@main.route("/ticket/<ticket_id>")
def view_ticket(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first_or_404()
    return render_template("ticket.html", ticket=ticket)

@main.route("/ticket/ai/<ticket_id>", methods=["GET", "POST"])
def get_ai_response(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first_or_404()
    if request.method == "POST":
        user_message = request.json.get("message")
        prompt = f"The user is continuing with this message: {user_message}
Previous issue: {ticket.issue}"
        ai_response = ask_ai(prompt)
        return jsonify({"response": ai_response})
    else:
        ai_response = ask_ai(f"The user is having the following issue: {ticket.issue}. How can we help them troubleshoot?")
        return jsonify({"response": ai_response})

@main.route("/ticket/<ticket_id>/resolve", methods=["POST"])
def mark_resolved(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first_or_404()
    ticket.status = "resolved"
    db.session.commit()
    return redirect(url_for("main.view_ticket", ticket_id=ticket_id))
