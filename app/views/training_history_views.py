from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.auth_service import AuthService
from app.services.training_history_service import TrainingHistoryService

training_history_bp = Blueprint('training_history', __name__)

@training_history_bp.route('/', methods=['GET'])
@jwt_required()
def get_training_history():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    current_user = AuthService.get_current_user()
    return TrainingHistoryService.get_all_training_history(current_user=current_user, page=page, search_query=search_query)

@training_history_bp.route('/<int:history_id>', methods=['GET'])
@jwt_required()
def get_training_history(history_id):
    try:
        history = TrainingHistoryService.get_training_history_by_id(history_id)
        return jsonify(history.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404