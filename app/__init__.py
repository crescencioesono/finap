from flask import Flask
from flask_jwt_extended import JWTManager
from app.views import auth_views, user_views, role_views, official_views, training_views, training_history_views, log_views
from app.models import db
from app.models.user import User
from app.models.role import Role
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object('app.config.Config')

    # JWT configuration for cookies
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token_cookie'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # Enable CSRF protection
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'

    jwt = JWTManager(app)
    
    with app.app_context():
        db.init_app(app)
        db.create_all()  # Create database tables
        
        # Create default roles if they don't exist
        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin')
            db.session.add(admin_role)
        if not Role.query.filter_by(name='user').first():
            user_role = Role(name='user')
            db.session.add(user_role)
        db.session.commit()  # Commit roles to get their IDs

        # Create default admin user if it doesn't exist
        default_username = app.config.get('DEFAULT_USERNAME')
        default_password = app.config.get('DEFAULT_PASSWORD')

        if not default_username or not default_password:
            raise ValueError("DEFAULT_USERNAME and DEFAULT_PASSWORD must be set in configuration")

        if not User.query.filter_by(username=default_username).first():
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                raise ValueError("Admin role not found in database")
            default_user = User(
                username=default_username,
                password=generate_password_hash(default_password),
                role_id=admin_role.id
            )
            db.session.add(default_user)
            db.session.commit()

        # Register blueprints
        app.register_blueprint(auth_views.auth_bp)
        app.register_blueprint(user_views.user_bp)
        app.register_blueprint(role_views.role_bp)
        app.register_blueprint(official_views.official_bp)
        app.register_blueprint(training_views.training_bp)
        app.register_blueprint(training_history_views.training_history_bp)
        app.register_blueprint(log_views.log_bp)

    return app