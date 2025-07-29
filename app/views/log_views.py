from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.log_service import LogService
from app.services.auth_service import AuthService
from app.utils.auth_decorators import role_required

log_bp = Blueprint('log', __name__)

@log_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('admin')  # Restrict log viewing to admins
def get_logs():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    current_user = AuthService.get_current_user()
    return LogService.get_all_logs(current_user=current_user, page=page, search_query=search_query)