from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Ticket, Comment
from app.extensions import db
from app.utils.decorators import role_required

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/dashboard')
@login_required
@role_required('customer')
def dashboard():
    tickets = Ticket.query.filter_by(customer_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    return render_template('customer/dashboard.html', tickets=tickets)

@customer_bp.route('/ticket/create', methods=['GET', 'POST'])
@login_required
@role_required('customer')
def create_ticket():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title or not description:
            flash('Título e descrição são obrigatórios.', 'danger')
            return render_template('customer/create_ticket.html')
            
        ticket = Ticket(title=title, description=description, customer_id=current_user.id, status='open')
        db.session.add(ticket)
        db.session.commit()
        
        flash('Chamado aberto com sucesso!', 'success')
        return redirect(url_for('customer.dashboard'))
        
    return render_template('customer/create_ticket.html')

@customer_bp.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
@role_required('customer')
def view_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id, customer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('O comentário não pode estar vazio.', 'danger')
        else:
            comment = Comment(ticket_id=ticket.id, user_id=current_user.id, content=content)
            # If the user posts a comment on their ticket and the ticket was resolved, maybe they want to keep it?
            # We don't automatically change state, but we save comment.
            db.session.add(comment)
            db.session.commit()
            flash('Comentário enviado!', 'success')
            return redirect(url_for('customer.view_ticket', ticket_id=ticket.id))
            
    return render_template('customer/view_ticket.html', ticket=ticket)
