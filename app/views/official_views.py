from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required

from app.services.official_service import OfficialService
from app.services.auth_service import AuthService
from app.models import db
from app.models.batch import Batch
from app.models.training_history import TrainingHistory

official_bp = Blueprint('official', __name__)

@official_bp.route('/', methods=['GET'])
@jwt_required()
def get_officials():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    current_user = AuthService.get_current_user()
    return OfficialService.get_all_officials(current_user=current_user, page=page, search_query=search_query)

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
                country=data.get('country'),
                address=data.get('address'),
                phone_number=data.get('phone_number'),
                email=data.get('email'),
                workplace=data.get('workplace'),
                level=data.get('level'),
                image=data.get('image')
            )
        else:
            return OfficialService.create_official(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                date_of_birth=data.get('date_of_birth'),
                country=data.get('country'),
                address=data.get('address'),
                phone_number=data.get('phone_number'),
                email=data.get('email'),
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

@official_bp.route('/<int:official_id>', methods=['DELETE'])
@jwt_required()
def delete_official(official_id):
    return OfficialService.delete_official(official_id)

@official_bp.route('/<int:official_id>/assign-course', methods=['GET', 'POST'])
@jwt_required()
def assign_course(official_id):
    try:
        official = OfficialService.get_official_by_id(official_id)
        if request.method == 'POST':
            data = request.form
            # Check for existing TrainingHistory with the same official_id and batch_id
            existing_training = TrainingHistory.query.filter_by(
                official_id=official_id,
                batch_id=data.get('batch_id')
            ).first()
            if existing_training:
                # Update existing record
                existing_training.end_date = data.get('end_date')
                existing_training.training_city = data.get('training_city')
                existing_training.modality = data.get('modality')
                existing_training.duration = data.get('duration')
                existing_training.status = data.get('status', 'En progreso')
                existing_training.other_info = data.get('other_info')
                db.session.commit()
                flash('Curso actualizado exitosamente', 'success')
            else:
                # Create new record
                new_training = TrainingHistory(
                    official_id=official_id,
                    batch_id=data.get('batch_id'),
                    end_date=data.get('end_date'),
                    training_city=data.get('training_city'),
                    modality=data.get('modality'),
                    duration=data.get('duration'),
                    status=data.get('status', 'En progreso'),
                    other_info=data.get('other_info')
                )
                db.session.add(new_training)
                db.session.commit()
                flash('Curso asignado exitosamente', 'success')
            return redirect(url_for('official.get_officials'))
        else:  # GET
            batches = Batch.query.all()  # Fetch all batches for the dropdown
            return render_template('assign_course.html', official=official, batches=batches, current_user=AuthService.get_current_user())
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('official.get_officials'))