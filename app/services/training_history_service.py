from flask import flash, render_template
from app.models import db
from app.models.batch import Batch
from app.models.official import Official
from app.models.training_history import TrainingHistory

class TrainingHistoryService:
    @staticmethod
    def get_all_training_history(current_user, page=1, search_query=None, training_code=None, all_officials=False):
        per_page = 10  # Adjust as needed
        query = TrainingHistory.query.join(Official).join(Batch)
        
        # Apply filters
        if training_code:
            query = query.filter(Batch.code == training_code)

        # Apply search
        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                (Official.first_name.ilike(search_pattern)) |
                (Official.last_name.ilike(search_pattern)) |
                (Batch.code.ilike(search_pattern))
            )

        # Paginate results
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        histories = pagination.items

        if not histories:
            flash('No se encontraron registros de historial de formación.', 'info')

        # Prepare data for template
        history_data = [
            {
                'official_name': f"{history.official.first_name} {history.official.last_name}",
                'training_code': history.batch.code if history.batch else 'No asignado',
                'end_date': history.end_date.strftime('%Y-%m-%d') if history.end_date else '',
                'training_city': history.training_city if history.training_city else '',
                'modality': history.modality if history.modality else '',
                'duration': history.duration if history.duration else '',
                'status': history.status if history.status else ''
            } for history in histories
        ]

        return render_template('training_history.html', training_history=history_data, pagination=pagination, current_user=current_user)
    
    @staticmethod
    def get_training_history_by_id(history_id):
        history = TrainingHistory.query.get_or_404(history_id)
        if not history:
            raise ValueError("Historial de formación no encontrado")
        return history

    @staticmethod
    def get_training_history_by_official(official_id):
        return TrainingHistory.query.filter_by(official_id=official_id).all()

    @staticmethod
    def update_training_history(history_id, **kwargs):
        training_history = TrainingHistory.query.get(history_id)
        if not training_history:
            raise ValueError("Historial de entrenamiento no encontrado")
        for key, value in kwargs.items():
            setattr(training_history, key, value)
        db.session.commit()
        return training_history

    @staticmethod
    def delete_training_history(history_id):
        training_history = TrainingHistory.query.get(history_id)
        if not training_history:
            raise ValueError("Historial de entrenamiento no encontrado")
        db.session.delete(training_history)
        db.session.commit()
        return True