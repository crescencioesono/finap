from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from app.views import auth_views, user_views, role_views, official_views, training_views, training_history_views, log_views
from app.models import db
from app.models.user import User
from app.models.role import Role
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object('app.config.Config')

    # JWT configuration for cookies - CONFIGURACIÓN CORREGIDA
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token_cookie'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Enable CSRF protection
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
    app.config['JWT_CSRF_IN_COOKIES'] = True  # IMPORTANTE: Poner CSRF en cookies separadas
    app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = 'csrf_access_token'
    app.config['JWT_REFRESH_CSRF_COOKIE_NAME'] = 'csrf_refresh_token'

    jwt = JWTManager(app)

    jwt = JWTManager(app)
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        return jsonify({'msg': 'Missing or invalid CSRF token', 'error': str(error)}), 401

    @app.route('/get-csrf-token')
    @jwt_required()
    def get_csrf_token_route():
        try:
            # En lugar de obtener desde JWT, leerlo desde las cookies
            csrf_token = request.cookies.get('csrf_access_token')
            if csrf_token:
                return jsonify({'csrf_token': csrf_token})
            else:
                return jsonify({'error': 'CSRF token not found in cookies'}), 422
        except Exception as e:
            return jsonify({'error': str(e)}), 422

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
        app.register_blueprint(auth_views.auth_bp, url_prefix='/')
        app.register_blueprint(user_views.user_bp, url_prefix='/user')
        app.register_blueprint(role_views.role_bp, url_prefix='/role')
        app.register_blueprint(official_views.training_bp, url_prefix='/official')
        app.register_blueprint(training_views.training_bp, url_prefix='/training')
        app.register_blueprint(training_history_views.training_history_bp, url_prefix='/training-history')
        app.register_blueprint(log_views.log_bp, url_prefix='/log')

    return app