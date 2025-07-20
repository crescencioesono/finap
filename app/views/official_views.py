from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services.training_service import TrainingService
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required

training_bp = Blueprint('training', __name__)

@training_bp.route('/', methods=['POST'])
@jwt_required()
def create_training():
    data = request.form
    return TrainingService.create_training(
        name=data.get('name'),
    )

@training_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()  # El decorador manejará automáticamente la verificación CSRF
def new_or_update_training():
    training_id = request.args.get('id')
    if request.method == 'POST':
        data = request.form
        training_id = data.get('training_id')
        if training_id:
            return TrainingService.update_training(
                training_id=training_id,
                name=data.get('name'),
            )
        else:
            return TrainingService.create_training(
                name=data.get('name'),
            )
    else:  # GET
        training = None
        if training_id:
            try:
                training = TrainingService.get_training_by_id(training_id)
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('training.get_trainings'))
        current_user = AuthService.get_current_user()
        return render_template('new_training.html', training=training, current_user=current_user, section=1)

@training_bp.route('/<int:training_id>', methods=['GET'])
@jwt_required()
def get_training(training_id):
    try:
        training = TrainingService.get_training_by_id(training_id)
        current_user = AuthService.get_current_user()
        return render_template('training_detail.html', training=training, current_user=current_user)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('training.get_trainings'))

@training_bp.route('/<int:training_id>', methods=['PUT'])
@jwt_required()
def update_training(training_id):
    data = request.form
    return TrainingService.update_training(
        training_id=training_id,
        name=data.get('name'),
    )

@training_bp.route('/<int:training_id>', methods=['DELETE'])
@jwt_required()
def delete_training(training_id):
    return TrainingService.delete_training(training_id)