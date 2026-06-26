from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_dashboard()
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect_dashboard()
        else:
            flash('E-mail ou senha inválidos.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect_dashboard()
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/register.html')
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este e-mail já está cadastrado.', 'danger')
            return render_template('auth/register.html')
            
        user = User(email=email, name=name, role='customer')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('customer.dashboard'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

def redirect_dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'attendant':
        return redirect(url_for('attendant.dashboard'))
    else:
        return redirect(url_for('customer.dashboard'))
