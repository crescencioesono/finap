from flask import Blueprint, request, jsonify
from app.services import OfficialService
from flask_jwt_extended import jwt_required

official_bp = Blueprint('official', __name__)

@official_bp.route('/', methods=['GET'])
@jwt_required()
def get_officials():
    try:
        officials = OfficialService.get_all_officials()
        return jsonify([official.to_dict() for official in officials]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@official_bp.route('/<int:official_id>', methods=['GET'])
@jwt_required()
def get_official(official_id):
    try:
        official = OfficialService.get_official_by_id(official_id)
        return jsonify(official.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@official_bp.route('/', methods=['POST'])
@jwt_required()
def create_official():
    data = request.get_json()
    try:
        official = OfficialService.create_official(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=data.get('date_of_birth'),
            workplace=data.get('workplace'),
            level=data.get('level'),
            image=data.get('image')
        )
        return jsonify(official.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@official_bp.route('/<int:official_id>', methods=['PUT'])
@jwt_required()
def update_official(official_id):
    data = request.get_json()
    try:
        official = OfficialService.update_official(
            official_id=official_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=data.get('date_of_birth'),
            workplace=data.get('workplace'),
            level=data.get('level'),
            image=data.get('image')
        )
        return jsonify(official.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@official_bp.route('/<int:official_id>', methods=['DELETE'])
@jwt_required()
def delete_official(official_id):
    try:
        OfficialService.delete_official(official_id)
        return jsonify({'message': 'Oficial eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404