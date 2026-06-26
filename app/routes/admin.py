from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import User, Ticket
from app.extensions import db
from app.utils.decorators import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    total_tickets = len(tickets)
    open_tickets = sum(1 for t in tickets if t.status == 'open')
    in_progress = sum(1 for t in tickets if t.status == 'in_progress')
    resolved = sum(1 for t in tickets if t.status == 'resolved')
    closed = sum(1 for t in tickets if t.status == 'closed')
    
    return render_template('admin/dashboard.html', 
                           tickets=tickets,
                           total_tickets=total_tickets,
                           open_tickets=open_tickets,
                           in_progress=in_progress,
                           resolved=resolved,
                           closed=closed)

@admin_bp.route('/users', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def users():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not name or not email or not password:
            flash('Todos os campos são obrigatórios.', 'danger')
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Este e-mail já está em uso.', 'danger')
            else:
                attendant = User(name=name, email=email, role='attendant')
                attendant.set_password(password)
                db.session.add(attendant)
                db.session.commit()
                flash(f'Atendente {name} cadastrado com sucesso!', 'success')
                return redirect(url_for('admin.users'))
                
    attendants = User.query.filter_by(role='attendant').all()
    return render_template('admin/users.html', attendants=attendants)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'attendant':
        flash('Somente atendentes podem ser removidos.', 'danger')
    else:
        tickets = Ticket.query.filter_by(attendant_id=user.id).all()
        for t in tickets:
            t.attendant_id = None
            if t.status == 'in_progress':
                t.status = 'open'
        
        db.session.delete(user)
        db.session.commit()
        flash('Atendente removido com sucesso!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/reports')
@login_required
@role_required('admin')
def reports():
    tickets = Ticket.query.all()
    total_tickets = len(tickets)
    
    status_counts = {
        'Abertos': sum(1 for t in tickets if t.status == 'open'),
        'Em Atendimento': sum(1 for t in tickets if t.status == 'in_progress'),
        'Resolvidos': sum(1 for t in tickets if t.status == 'resolved'),
        'Fechados': sum(1 for t in tickets if t.status == 'closed')
    }
    
    attendants = User.query.filter_by(role='attendant').all()
    attendant_stats = []
    for a in attendants:
        assigned = Ticket.query.filter_by(attendant_id=a.id).count()
        resolved = Ticket.query.filter_by(attendant_id=a.id, status='resolved').count()
        closed = Ticket.query.filter_by(attendant_id=a.id, status='closed').count()
        attendant_stats.append({
            'name': a.name,
            'email': a.email,
            'assigned': assigned,
            'resolved_closed': resolved + closed
        })
        
    return render_template('admin/reports.html', 
                           total_tickets=total_tickets,
                           status_counts=status_counts,
                           attendant_stats=attendant_stats)
