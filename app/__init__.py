import os
from flask import Flask, redirect, url_for
from flask_login import current_user
from app.extensions import db, login_manager, migrate
from app.models import User

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-default')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///atendimento.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.customer import customer_bp
    from app.routes.attendant import attendant_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(attendant_bp)
    app.register_blueprint(admin_bp)
    
    # Root route redirects
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'attendant':
                return redirect(url_for('attendant.dashboard'))
            else:
                return redirect(url_for('customer.dashboard'))
        return redirect(url_for('auth.login'))
        
    # Create tables and initial admin user
    with app.app_context():
        db.create_all()
        create_initial_admin()
        
    return app

def create_initial_admin():
    admin_email = os.environ.get('ADMIN_INITIAL_EMAIL', 'admin@sistema.com')
    admin_password = os.environ.get('ADMIN_INITIAL_PASSWORD', 'admin123')
    
    # Check if admin already exists
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        # Check if there is any admin at all
        any_admin = User.query.filter_by(role='admin').first()
        if not any_admin:
            admin = User(
                email=admin_email,
                name='Administrador',
                role='admin'
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin inicial criado com sucesso: {admin_email}")
