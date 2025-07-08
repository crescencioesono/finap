from flask import Flask
from flask_jwt_extended import JWTManager
from app.views import auth_views, user_views, role_views, official_views, training_views, training_history_views, log_views

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    jwt = JWTManager(app)

    # Registra los blueprints
    app.register_blueprint(auth_views.auth_bp)
    app.register_blueprint(user_views.user_bp)
    app.register_blueprint(role_views.role_bp)
    app.register_blueprint(official_views.official_bp)
    app.register_blueprint(training_views.training_bp)
    app.register_blueprint(training_history_views.training_history_bp)
    app.register_blueprint(log_views.log_bp)

    return app