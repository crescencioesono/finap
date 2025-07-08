from flask import Blueprint, request, jsonify
from app.services import RoleService
from flask_jwt_extended import jwt_required

role_bp = Blueprint('role', __name__)

@role_bp.route('/', methods=['GET'])
@jwt_required()
def get_roles():
    try:
        roles = RoleService.get_all_roles()
        return jsonify([role.to_dict() for role in roles]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/<int:role_id>', methods=['GET'])
@jwt_required()
def get_role(role_id):
    try:
        role = RoleService.get_role_by_id(role_id)
        return jsonify(role.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@role_bp.route('/', methods=['POST'])
@jwt_required()
def create_role():
    data = request.get_json()
    try:
        role = RoleService.create_role(name=data.get('name'))
        return jsonify(role.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@role_bp.route('/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    data = request.get_json()
    try:
        role = RoleService.update_role(role_id=role_id, name=data.get('name'))
        return jsonify(role.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@role_bp.route('/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    try:
        RoleService.delete_role(role_id)
        return jsonify({'message': 'Rol eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404