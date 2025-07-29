from flask import render_template
from app.models import db
from app.models.official import Official
from app.models.training_history import TrainingHistory

class TrainingHistoryService:
    @staticmethod
    def create_training_history(official_id, training_id, training_date, training_city, modality, duration, state, other_info=None):
        new_training_history = TrainingHistory(
            official_id=official_id,
            training_id=training_id,
            training_date=training_date,
            training_city=training_city,
            modality=modality,
            duration=duration,
            state=state,
            other_info=other_info
        )
        db.session.add(new_training_history)
        db.session.commit()
        return new_training_history
    
    @staticmethod
    def get_all_training_history(current_user=None, page=1, search_query=None):
        per_page = 10
        query = TrainingHistory.query.join(Official).options(
            db.joinedload(TrainingHistory.official),
            db.joinedload(TrainingHistory.batch)
        )
        if search_query:
            search = f"%{search_query}%"
            query = query.filter(
                (Official.first_name.ilike(search)) |
                (Official.last_name.ilike(search)) |
                (TrainingHistory.training_city.ilike(search)) |
                (TrainingHistory.modality.ilike(search)) |
                (TrainingHistory.duration.ilike(search)) |
                (TrainingHistory.status.ilike(search))
            )
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('training_history.html', training_history=pagination.items, pagination=pagination, current_user=current_user)
    
    @staticmethod
    def get_training_history_by_id(history_id):
        return TrainingHistory.query.get(history_id)

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