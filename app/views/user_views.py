from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.services.auth_service import AuthService

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    current_user = AuthService.get_current_user()
    return UserService.get_all_users(current_user=current_user, page=page, search_query=search_query)

@user_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()
def new_or_update_user():
    user_id = request.args.get('id')
    if request.method == 'POST':
        data = request.form
        user_id = data.get('user_id')
        if user_id:
            return UserService.update_user(
                user_id=user_id,
                username=data.get('username'),
                password=generate_password_hash(data.get('password')),
                role_id=data.get('role_id')
            )
        else:
            return UserService.create_user(
                username=data.get('username'),
                password=data.get('password'),
                role_id=data.get('role_id')
            )
    else:  # GET
        user = None
        roles = RoleService.get_all_roles()
        if user_id:
            try:
                user = UserService.get_user_by_id(user_id)  
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('user.get_users'))
        current_user = AuthService.get_current_user()
        return render_template('new_user.html', user=user, roles=roles, current_user=current_user, section=1)

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        current_user = AuthService.get_current_user()
        return render_template('user_detail.html', user=user, current_user=current_user)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('user.get_users'))

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.form
    return UserService.update_user(
        user_id=user_id,
        name=data.get('name'),
    )

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return UserService.delete_user(user_id)