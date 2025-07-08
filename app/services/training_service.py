from app.models import db
from app.models.training import Training

class TrainingService:
    @staticmethod
    def create_training(name):
        new_training = Training(name=name)
        db.session.add(new_training)
        db.session.commit()
        return new_training

    @staticmethod
    def get_training_by_id(training_id):
        return Training.query.get(training_id)

    @staticmethod
    def get_training_by_name(name):
        return Training.query.filter_by(name=name).first()

    @staticmethod
    def update_training(training_id, name=None):
        training = Training.query.get(training_id)
        if not training:
            raise ValueError("Entrenamiento no encontrado")
        if name:
            training.name = name
        db.session.commit()
        return training

    @staticmethod
    def delete_training(training_id):
        training = Training.query.get(training_id)
        if not training:
            raise ValueError("Entrenamiento no encontrado")
        db.session.delete(training)
        db.session.commit()
        return True