from flask import Blueprint, request, jsonify
from app.services.training_service import TrainingService
from flask_jwt_extended import jwt_required

training_bp = Blueprint('training', __name__)

@training_bp.route('/', methods=['GET'])
@jwt_required()
def get_trainings():
    try:
        trainings = TrainingService.get_all_trainings()
        return jsonify([training.to_dict() for training in trainings]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_bp.route('/<int:training_id>', methods=['GET'])
@jwt_required()
def get_training(training_id):
    try:
        training = TrainingService.get_training_by_id(training_id)
        return jsonify(training.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@training_bp.route('/', methods=['POST'])
@jwt_required()
def create_training():
    data = request.get_json()
    try:
        training = TrainingService.create_training(name=data.get('name'))
        return jsonify(training.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@training_bp.route('/<int:training_id>', methods=['PUT'])
@jwt_required()
def update_training(training_id):
    data = request.get_json()
    try:
        training = TrainingService.update_training(training_id=training_id, name=data.get('name'))
        return jsonify(training.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@training_bp.route('/<int:training_id>', methods=['DELETE'])
@jwt_required()
def delete_training(training_id):
    try:
        TrainingService.delete_training(training_id)
        return jsonify({'message': 'Entrenamiento eliminado exitosamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404