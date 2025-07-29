from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.auth_service import AuthService
from app.services.training_history_service import TrainingHistoryService
from app.services.log_service import LogService

training_history_bp = Blueprint('training_history', __name__)

@training_history_bp.route('/', methods=['GET'])
@jwt_required()
def get_training_history():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    current_user = AuthService.get_current_user()
    result = TrainingHistoryService.get_all_training_history(current_user=current_user, page=page, search_query=search_query)
    LogService.create_log(f"Vio el historial de formación por el usuario {current_user.id}", f"Página: {page}, Búsqueda: {search_query}")
    return result

@training_history_bp.route('/<int:history_id>', methods=['GET'])
@jwt_required()
def get_training_history(history_id):
    try:
        history = TrainingHistoryService.get_training_history_by_id(history_id)
        current_user = AuthService.get_current_user()
        LogService.create_log(f"Vio los detalles del historial {history_id} por el usuario {current_user.id}")
        return jsonify(history.to_dict()), 200
    except ValueError as e:
        LogService.create_log(f"Intento fallido de ver el historial {history_id} por el usuario {current_user.id}", f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 404