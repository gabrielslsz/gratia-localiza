from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Ticket, Comment
from app.extensions import db
from app.utils.decorators import role_required

attendant_bp = Blueprint('attendant', __name__, url_prefix='/attendant')

@attendant_bp.route('/dashboard')
@login_required
@role_required('attendant')
def dashboard():
    my_tickets = Ticket.query.filter_by(attendant_id=current_user.id).order_by(Ticket.updated_at.desc()).all()
    unassigned_tickets = Ticket.query.filter_by(attendant_id=None, status='open').order_by(Ticket.created_at.desc()).all()
    return render_template('attendant/dashboard.html', my_tickets=my_tickets, unassigned_tickets=unassigned_tickets)

@attendant_bp.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
@role_required('attendant', 'admin')
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('O comentário não pode estar vazio.', 'danger')
        else:
            comment = Comment(ticket_id=ticket.id, user_id=current_user.id, content=content)
            db.session.add(comment)
            db.session.commit()
            flash('Comentário enviado!', 'success')
            return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))
            
    return render_template('attendant/view_ticket.html', ticket=ticket)

@attendant_bp.route('/ticket/<int:ticket_id>/assign', methods=['POST'])
@login_required
@role_required('attendant', 'admin')
def assign_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.attendant_id is not None:
        flash('Este chamado já possui um atendente atribuído.', 'warning')
    else:
        ticket.attendant_id = current_user.id
        ticket.status = 'in_progress'
        db.session.commit()
        flash('Chamado atribuído a você com sucesso!', 'success')
    return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))

@attendant_bp.route('/ticket/<int:ticket_id>/status', methods=['POST'])
@login_required
@role_required('attendant', 'admin')
def update_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if ticket.attendant_id != current_user.id and current_user.role != 'admin':
        flash('Você não tem permissão para alterar o status deste chamado.', 'danger')
        return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))
        
    status = request.form.get('status')
    if status in ['in_progress', 'resolved', 'closed']:
        ticket.status = status
        db.session.commit()
        flash(f'Status do chamado alterado para: {status}', 'success')
    else:
        flash('Status inválido.', 'danger')
        
    return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))
