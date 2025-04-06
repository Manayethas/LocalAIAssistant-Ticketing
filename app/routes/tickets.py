from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.ticket import Ticket, AIResponse, Comment
from app.models.user import User
from app import db
from app.ai_assistant import ask_ai
from datetime import datetime

tickets = Blueprint('tickets', __name__)

@tickets.route('/tickets')
@login_required
def list_tickets():
    if current_user.is_technician():
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('tickets/list.html', tickets=tickets)

@tickets.route('/tickets/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        
        ticket = Ticket(
            title=title,
            description=description,
            priority=priority,
            user_id=current_user.id
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        # Get AI response
        ai_prompt = f"Help with ticket: {title}\nDescription: {description}"
        ai_response = ask_ai(ai_prompt)
        
        ai_response_obj = AIResponse(
            ticket_id=ticket.id,
            response=ai_response
        )
        db.session.add(ai_response_obj)
        db.session.commit()
        
        flash('Ticket created successfully!')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    
    return render_template('tickets/create.html')

@tickets.route('/tickets/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not current_user.is_technician() and ticket.user_id != current_user.id:
        flash('You do not have permission to view this ticket')
        return redirect(url_for('tickets.list_tickets'))
    
    return render_template('tickets/view.html', ticket=ticket)

@tickets.route('/tickets/<int:ticket_id>/update', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not current_user.is_technician() and ticket.user_id != current_user.id:
        flash('You do not have permission to update this ticket')
        return redirect(url_for('tickets.list_tickets'))
    
    if request.method == 'POST':
        status = request.form.get('status')
        if status in ['open', 'in_progress', 'resolved', 'closed']:
            ticket.status = status
            ticket.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Ticket status updated successfully')
    
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

@tickets.route('/tickets/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not current_user.is_technician() and ticket.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    content = request.form.get('content')
    if content:
        comment = Comment(
            ticket_id=ticket_id,
            user_id=current_user.id,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'error': 'Comment content required'}), 400

@tickets.route('/tickets/<int:ticket_id>/assign', methods=['POST'])
@login_required
def assign_ticket(ticket_id):
    if not current_user.is_technician():
        return jsonify({'error': 'Unauthorized'}), 403
    
    ticket = Ticket.query.get_or_404(ticket_id)
    technician_id = request.form.get('technician_id')
    
    if technician_id:
        technician = User.query.get(technician_id)
        if technician and technician.is_technician():
            ticket.technician_id = technician_id
            ticket.status = 'in_progress'
            db.session.commit()
            return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid technician'}), 400 