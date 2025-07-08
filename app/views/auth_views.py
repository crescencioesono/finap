from flask import Blueprint, request, jsonify
from app.services import AuthService
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = AuthService.register_user(
            username=data.get('username'),
            password=data.get('password'),
            role_id=data.get('role_id')
        )
        return jsonify({'message': 'Usuario registrado exitosamente', 'user': user.to_dict()}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        response = AuthService.login_user(
            username=data.get('username'),
            password=data.get('password')
        )
        return jsonify(response), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        response = AuthService.refresh_token()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500