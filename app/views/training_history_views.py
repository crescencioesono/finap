from flask import Blueprint, request, jsonify
from app.services import TrainingHistoryService
from flask_jwt_extended import jwt_required

training_history_bp = Blueprint('training_history', __name__)

@training_history_bp.route('/', methods=['GET'])
@jwt_required()
def get_training_histories():
    try:
        training_histories = TrainingHistoryService.get_all_training_histories()
        return jsonify([history.to_dict() for history in training_histories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_history_bp.route('/<int:history_id>', methods=['GET'])
@jwt_required()
def get_training_history(history_id):
    try:
        history = TrainingHistoryService.get_training_history_by_id(history_id)
        return jsonify(history.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@training_history_bp.route('/', methods=['POST'])
@jwt_required()
def create_training_history():
    data = request.get_json()
    try:
        history = TrainingHistoryService.create_training_history(
            official_id=data.get('official_id'),
            training_id=data.get('training_id'),
            training_date=data.get('training_date'),
            training_city=data.get('training_city'),
            modality=data.get('modality'),
            duration=data.get('duration'),
            state=data.get('state'),
            other_info=data.get('other_info')
        )
        return jsonify(history.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@training_history_bp.route('/<int:history_id>', methods=['PUT'])
@jwt_required()
def update_training_history(history_id):
    data = request.get_json()
    try:
        history = TrainingHistoryService.update_training_history(
            history_id=history_id,
            official_id=data.get('official_id'),
            training_id=data.get('training_id'),
            training_date=data.get('training_date'),
            training_city=data.get('training_city'),
            modality=data.get('modality'),
            duration=data.get('duration'),
            state=data.get('state'),
            other_info=data.get('other_info')
        )
        return jsonify(history.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@training_history_bp.route('/<int:history_id>', methods=['DELETE'])
@jwt_required()
def delete_training_history(history_id):
    try:
        TrainingHistoryService.delete_training_history(history_id)
        return jsonify({'message': 'Historial de entrenamiento eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404