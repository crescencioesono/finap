from flask import Blueprint, request, jsonify
from app.services.log_service import LogService
from flask_jwt_extended import jwt_required

log_bp = Blueprint('log', __name__)

@log_bp.route('/', methods=['GET'])
@jwt_required()
def get_logs():
    try:
        logs = LogService.get_all_logs()
        return jsonify([log.to_dict() for log in logs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@log_bp.route('/<int:log_id>', methods=['GET'])
@jwt_required()
def get_log(log_id):
    try:
        log = LogService.get_log_by_id(log_id)
        return jsonify(log.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@log_bp.route('/', methods=['POST'])
@jwt_required()
def create_log():
    data = request.get_json()
    try:
        log = LogService.create_log(
            user_id=data.get('user_id'),
            action=data.get('action'),
            details=data.get('details')
        )
        return jsonify(log.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@log_bp.route('/<int:log_id>', methods=['PUT'])
@jwt_required()
def update_log(log_id):
    data = request.get_json()
    try:
        log = LogService.update_log(
            log_id=log_id,
            action=data.get('action'),
            details=data.get('details')
        )
        return jsonify(log.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@log_bp.route('/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(log_id):
    try:
        LogService.delete_log(log_id)
        return jsonify({'message': 'Registro de log eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404