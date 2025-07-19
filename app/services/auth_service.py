from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, make_response, flash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies
)
from datetime import timedelta
from app.models.user import User
from app.models import db

class AuthService:
    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Nombre de usuario o contraseña incorrectos', 'error')
            return render_template('login.html'), 401

        try:
            access_token = create_access_token(identity=user.username, expires_delta=timedelta(hours=1))
            refresh_token = create_refresh_token(identity=user.username)
        except Exception as e:
            flash('Error al generar el token de autenticación', 'error')
            return render_template('login.html'), 500

        # Create response with dashboard template
        response = make_response(render_template('dashboard.html', current_user=user))
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        flash('Login exitoso!', 'success')
        return response

    @staticmethod
    @jwt_required(refresh=True)
    def refresh_token():
        current_username = get_jwt_identity()
        new_access_token = create_access_token(identity=current_username, expires_delta=timedelta(hours=1))
        
        # Create response with dashboard template
        user = User.query.filter_by(username=current_username).first()
        if not user:
            flash('Usuario no encontrado', 'error')
            return render_template('login.html'), 401
        
        response = make_response(render_template('dashboard.html', current_user=user))
        set_access_cookies(response, new_access_token)
        flash('Token actualizado exitosamente', 'success')
        return response

    @staticmethod
    @jwt_required()
    def get_current_user():
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError("Usuario no encontrado")
        return user