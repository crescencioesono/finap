from flask import Blueprint, flash, redirect, request, jsonify, url_for
from flask_jwt_extended import jwt_required
from app.models.batch_tracking import BatchTracking
from app.models.training_history import TrainingHistory
from app.services.auth_service import AuthService
from app.services.training_history_service import TrainingHistoryService
from app.services.log_service import LogService
from app.models import db
from app.utils.auth_decorators import role_required

training_history_bp = Blueprint('training_history', __name__)

@training_history_bp.route('/', methods=['GET'])
@jwt_required()
def get_training_history():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    training_code = request.args.get('training_code')
    all_officials = request.args.get('all_officials', 'false').lower() == 'true'
    current_user = AuthService.get_current_user()
    result = TrainingHistoryService.get_all_training_history(
        current_user=current_user,
        page=page,
        search_query=search_query,
        training_code=training_code,
        all_officials=all_officials
    )
    LogService.create_log(f"Vio el historial de formación por el usuario {current_user.id}", f"Página: {page}, Búsqueda: {search_query}, Training Code: {training_code}, All Officials: {all_officials}")
    return result

@training_history_bp.route('/<int:history_id>', methods=['GET'])
@jwt_required()
def get_training_history_by_id(history_id):
    try:
        history = TrainingHistoryService.get_training_history_by_id(history_id)
        current_user = AuthService.get_current_user()
        LogService.create_log(f"Vio los detalles del historial {history_id} por el usuario {current_user.id}")
        return jsonify(history.to_dict()), 200
    except ValueError as e:
        LogService.create_log(f"Intento fallido de ver el historial {history_id} por el usuario {current_user.id}", f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 404
    
@training_history_bp.route('/<int:history_id>/batch_tracking/<int:tracking_id>', methods=['POST'])
@jwt_required()
def update_batch_tracking(history_id, tracking_id):
    current_user = AuthService.get_current_user()
    tracking = BatchTracking.query.get_or_404(tracking_id)
    if tracking.history_id != history_id:
        LogService.create_log(f"Intento no autorizado de actualizar el seguimiento {tracking_id} por el usuario {current_user.id}", f"History ID mismatch: {history_id}")
        return jsonify({'error': 'Tracking does not belong to this history'}), 403

    data = request.form
    tracking.status = data.get('status', tracking.status)
    tracking.end_date = data.get('end_date') if data.get('end_date') else tracking.end_date
    tracking.grade = data.get('grade') if data.get('grade') else tracking.grade

    db.session.commit()
    LogService.create_log(f"Actualizó el seguimiento {tracking_id} por el usuario {current_user.id}", f"Status: {tracking.status}, End Date: {tracking.end_date}, Grade: {tracking.grade}")

    # Redirect to the official detail page to refresh the view
    history = TrainingHistory.query.get(history_id)
    official_id = history.official_id
    flash('Seguimiento actualizado exitosamente', 'success')
    return redirect(url_for('official.get_official', official_id=official_id))

@training_history_bp.route('/print', methods=['GET'])
@role_required("admin")
def print_training_history():
    search_query = request.args.get('search', None, type=str)
    training_code = request.args.get('training_code')
    all_officials = request.args.get('all_officials', 'false').lower() == 'true'
    current_user = AuthService.get_current_user()
    result = TrainingHistoryService.get_all_training_history(
        current_user=current_user,
        page=1,  # Not paginated for print
        search_query=search_query,
        training_code=training_code,
        all_officials=all_officials
    )
    LogService.create_log(f"Imprimiendo historial de formación por el usuario {current_user.id}", f"Búsqueda: {search_query}, Training Code: {training_code}, All Officials: {all_officials}")
    return result