from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = UserService.get_all_users()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    try:
        user = UserService.update_user(
            user_id=user_id,
            username=data.get('username'),
            password=data.get('password'),
            role_id=data.get('role_id')
        )
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        UserService.delete_user(user_id)
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404