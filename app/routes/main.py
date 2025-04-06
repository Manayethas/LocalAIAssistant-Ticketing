from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import login_required, current_user
from app import db
from app.models.ticket import Ticket
from app.models.user import User
from app.ai_assistant import ask_ai
import uuid
from datetime import datetime
import json

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/create_ticket", methods=["GET", "POST"])
@login_required
def create_ticket():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority", "medium")

        if not title or not description:
            flash("Title and description are required", "error")
            return redirect(url_for("main.create_ticket"))

        ticket = Ticket(
            title=title,
            description=description,
            priority=priority,
            status="open",
            user_id=current_user.id
        )

        db.session.add(ticket)
        db.session.commit()

        session["processing_ticket_id"] = ticket.id
        return redirect(url_for("main.waiting"))

    return render_template("create_ticket.html")

@main.route("/ticket/<int:ticket_id>")
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("view_ticket.html", ticket=ticket)

@main.route("/tickets")
@login_required
def list_tickets():
    if current_user.is_technician:
        tickets = Ticket.query.filter_by(requires_technician=True).all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template("list_tickets.html", tickets=tickets)

@main.route("/ask_ai/<int:ticket_id>", methods=["POST"])
@login_required
def ask_ai_for_help(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    question = request.form.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Build history context
    chat_history = [
        f"User: {ticket.description}"
    ]
    existing_responses = json.loads(ticket.ai_responses or "[]")
    for entry in existing_responses:
        chat_history.append(f"AI: {entry['response']}")

    chat_history.append(f"User: {question}")
    prompt = "\n".join(chat_history)

    # Ask the AI
    ai_response = ask_ai(prompt)

    # Save the new response
    existing_responses.append({
        "timestamp": datetime.utcnow().isoformat(),
        "response": ai_response
    })
    ticket.ai_responses = json.dumps(existing_responses)

    if "I couldn't help" in ai_response or "I don't know" in ai_response:
        ticket.requires_technician = True

    db.session.commit()
    return jsonify({"response": ai_response})

@main.route("/assign_technician/<int:ticket_id>", methods=["POST"])
@login_required
def assign_technician(ticket_id):
    if not current_user.is_technician:
        return jsonify({"error": "Unauthorized"}), 403

    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.technician_id = current_user.id
    ticket.status = "in_progress"
    db.session.commit()

    return jsonify({"message": "Technician assigned successfully"})

@main.route("/ticket/<int:ticket_id>/resolve", methods=["POST"])
@login_required
def mark_resolved(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = "resolved"
    db.session.commit()
    return redirect(url_for("main.view_ticket", ticket_id=ticket_id))

@main.route('/waiting')
@login_required
def waiting():
    if 'processing_ticket_id' not in session:
        return redirect(url_for('main.index'))
    return render_template('waiting.html')

@main.route('/check_ai_status')
@login_required
def check_ai_status():
    if 'processing_ticket_id' in session:
        return jsonify({
            'complete': True,
            'redirect_url': url_for('main.view_ticket', ticket_id=session.get('processing_ticket_id'))
        })
    return jsonify({'complete': False})
