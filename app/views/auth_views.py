from flask import Blueprint, flash, request, render_template, redirect, url_for, make_response
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.form
    return AuthService.login_user(
        username=data.get('username'),
        password=data.get('password')
    )

@auth_bp.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = AuthService.get_current_user()
    return render_template('dashboard.html', current_user=current_user)

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    flash('Has cerrado sesión exitosamente', 'success')
    return response

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    return AuthService.refresh_token()