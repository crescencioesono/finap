from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response
from flask_jwt_extended import jwt_required, unset_jwt_cookies

from app.services.auth_service import AuthService
from app.services.log_service import LogService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        LogService.create_log("Accedió a la página de inicio de sesión")
        return render_template('login.html')
    
    data = request.form
    response, status_code = AuthService.login_user(
        username=data.get('username'),
        password=data.get('password')
    )
    if status_code == 200:
        LogService.create_log(f"Inicio de sesión exitoso para el usuario {data.get('username')}", f"IP: {request.remote_addr}")
    elif status_code == 401:
        LogService.create_log(f"Intento fallido de inicio de sesión para el usuario {data.get('username')}", f"IP: {request.remote_addr}")
    elif status_code == 500:
        LogService.create_log(f"Error de inicio de sesión para el usuario {data.get('username')}", f"IP: {request.remote_addr}, Error: Fallo en la generación del token")
    return response

@auth_bp.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = AuthService.get_current_user()
    LogService.create_log(f"Vio el tablero por el usuario {current_user.id}", f"Nombre de usuario: {current_user.username}")
    return render_template('dashboard.html', current_user=current_user)

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    current_user = AuthService.get_current_user()
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    LogService.create_log(f"Cierre de sesión por el usuario {current_user.id}", f"Nombre de usuario: {current_user.username}")
    flash('Has cerrado sesión exitosamente', 'success')
    return response

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = AuthService.get_current_user()
    result, status_code = AuthService.refresh_token()
    if status_code == 200:
        LogService.create_log(f"Token renovado para el usuario {current_user.id}", f"Nombre de usuario: {current_user.username}")
    return result