from werkzeug.security import check_password_hash
from flask import render_template, make_response, flash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
)
from datetime import timedelta
from app.models.user import User

class AuthService:
    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Nombre de usuario o contraseña incorrectos', 'error')
            return render_template('login.html'), 401

        try:
            access_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=10))
            refresh_token = create_refresh_token(identity=user.username)
        except Exception as e:
            flash('Error al generar el token de autenticación', 'error')
            return render_template('login.html'), 500

        # Create response with dashboard template
        response = make_response(render_template('dashboard.html', current_user=user))
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        flash('Login exitoso!', 'success')
        return response, 200

    @staticmethod
    @jwt_required(refresh=True)
    def refresh_token():
        try:
            new_access_token = create_access_token(identity=get_jwt_identity(), expires_delta=timedelta(hours=1))
            response = make_response({"message": "Token refreshed"})
            set_access_cookies(response, new_access_token)
            return response, 200
        except Exception as e:
            flash('Error al refrescar el token', 'error')
            return make_response({"error": str(e)}), 500

    @staticmethod
    @jwt_required()
    def get_current_user():
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError("Usuario no encontrado")
        return user
