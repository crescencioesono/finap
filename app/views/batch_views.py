from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services.batch_service import BatchService
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required
from app.services.log_service import LogService
from app.utils.auth_decorators import role_required

batch_bp = Blueprint('batch', __name__)

@batch_bp.route('/', methods=['GET'])
@jwt_required()
def get_batches():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', None, type=str)
    current_user = AuthService.get_current_user()
    batches = BatchService.get_all_batches(current_user=current_user, page=page, search_query=search_query)
    LogService.create_log(f"Vio la lista de códigos por el usuario {current_user.id}", f"Página: {page}, Búsqueda: {search_query}")
    return render_template('batches.html', batches=batches, current_user=current_user, page=page, search_query=search_query)

@batch_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()  # El decorador manejará automáticamente la verificación CSRF
def new_or_update_batch():
    batch_id = request.args.get('id')
    if request.method == 'POST':
        data = request.form
        batch_id = data.get('batch_id')
        if batch_id:
            result = BatchService.update_batch(
                batch_id=batch_id,
                code=data.get('code'),
                description=data.get('description'),
                trainings=data.getlist('trainings')  # Handle multiple training IDs
            )
            current_user = AuthService.get_current_user()
            LogService.create_log(f"Actualizó el código {batch_id} por el usuario {current_user.id}", f"Datos: {data}")
            return result
        else:
            result = BatchService.create_batch(
                code=data.get('code'),
                description=data.get('description'),
                trainings=data.getlist('trainings')  # Handle multiple training IDs
            )
            print(result)
            current_user = AuthService.get_current_user()
            LogService.create_log(f"Creó un código por el usuario {current_user.id}", f"Datos: {data}")
            return result
    else:  # GET
        batch = None
        trainings = BatchService.get_all_trainings()  # Fetch all trainings for the form
        if batch_id:
            try:
                batch = BatchService.get_batch_by_id(batch_id)
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('batch.get_batches'))
        current_user = AuthService.get_current_user()
        LogService.create_log(f"Vio el formulario de nuevo/actualizar código por el usuario {current_user.id}", f"ID de código: {batch_id}")
        return render_template('new_batch.html', batch=batch, current_user=current_user, trainings=trainings, section=1)

@batch_bp.route('/<int:batch_id>', methods=['GET'])
@jwt_required()
def get_batch(batch_id):
    try:
        batch = BatchService.get_batch_by_id(batch_id)
        current_user = AuthService.get_current_user()
        LogService.create_log(f"Vio los detalles del código {batch_id} por el usuario {current_user.id}")
        return render_template('batch_detail.html', batch=batch, trainings=batch.trainings, current_user=current_user)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('batch.get_batches'))

@batch_bp.route('/<int:batch_id>', methods=['POST'])
@jwt_required()
def update_batch(batch_id):
    data = request.form
    result = BatchService.update_batch(
        batch_id=batch_id,
        code=data.get('code'),
        description=data.get('description'),
        trainings=data.getlist('trainings')  # Handle multiple training IDs
    )
    current_user = AuthService.get_current_user()
    LogService.create_log(f"Actualizó el código {batch_id} por el usuario {current_user.id}", f"Datos: {data}")
    return result

@batch_bp.route('/<int:batch_id>', methods=['POST'])
@role_required("admin")
def delete_batch(batch_id):
    result = BatchService.delete_batch(batch_id)
    current_user = AuthService.get_current_user()
    LogService.create_log(f"Eliminó el código {batch_id} por el usuario {current_user.id}")
    return result