from app.models import db
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