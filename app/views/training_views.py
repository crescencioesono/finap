from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services.official_service import OfficialService
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required

official_bp = Blueprint('official', __name__)

@official_bp.route('/', methods=['GET'])
@jwt_required()
def get_officials():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    current_user = AuthService.get_current_user()
    return OfficialService.get_all_officials(current_user=current_user, page=page, search_query=search_query)

@official_bp.route('/', methods=['POST'])
@jwt_required()
def create_official():
    data = request.form
    return OfficialService.create_official(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=data.get('date_of_birth'),
        workplace=data.get('workplace'),
        level=data.get('level'),
        image=data.get('image')
    )

@official_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()  # El decorador manejará automáticamente la verificación CSRF
def new_or_update_official():
    official_id = request.args.get('id')
    if request.method == 'POST':
        data = request.form
        official_id = data.get('official_id')
        if official_id:
            return OfficialService.update_official(
                official_id=official_id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                date_of_birth=data.get('date_of_birth'),
                workplace=data.get('workplace'),
                level=data.get('level'),
                image=data.get('image')
            )
        else:
            return OfficialService.create_official(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                date_of_birth=data.get('date_of_birth'),
                workplace=data.get('workplace'),
                level=data.get('level'),
                image=data.get('image')
            )
    else:  # GET
        official = None
        if official_id:
            try:
                official = OfficialService.get_official_by_id(official_id)
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('official.get_officials'))
        current_user = AuthService.get_current_user()
        return render_template('new_official.html', official=official, current_user=current_user, section=1)

@official_bp.route('/<int:official_id>', methods=['GET'])
@jwt_required()
def get_official(official_id):
    try:
        official = OfficialService.get_official_by_id(official_id)
        current_user = AuthService.get_current_user()
        return render_template('official_detail.html', official=official, current_user=current_user)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('official.get_officials'))

@official_bp.route('/<int:official_id>', methods=['PUT'])
@jwt_required()
def update_official(official_id):
    data = request.form
    return OfficialService.update_official(
        official_id=official_id,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=data.get('date_of_birth'),
        workplace=data.get('workplace'),
        level=data.get('level'),
        image=data.get('image')
    )

@official_bp.route('/<int:official_id>', methods=['DELETE'])
@jwt_required()
def delete_official(official_id):
    return OfficialService.delete_official(official_id)

@official_bp.route('/<int:official_id>/assign-course', methods=['GET'])
@jwt_required()
def assign_course(official_id):
    try:
        official = OfficialService.get_official_by_id(official_id)
        current_user = AuthService.get_current_user()
        return render_template('assign_course.html', official=official, current_user=current_user)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('official.get_officials'))