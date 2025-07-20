from flask import render_template, flash, redirect, url_for
from app.models import db
from app.models.training import Training

class TrainingService:
    @staticmethod
    def create_training(name):
        new_training = Training(
            name=name,
        )
        db.session.add(new_training)
        db.session.commit()
        flash('Curso creado exitosamente', 'success')
        return redirect(url_for('training.get_trainings'))

    @staticmethod
    def get_all_trainings(current_user=None, page=1, search_query=None):
        per_page = 10
        query = Training.query
        if search_query:
            search = f"%{search_query}%"
            query = query.filter(
                (Training.name.ilike(search))
            )
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('trainings.html', trainings=pagination.items, current_user=current_user, pagination=pagination)

    @staticmethod
    def get_training_by_id(training_id):
        training = Training.query.get(training_id)
        if not training:
            raise ValueError("Curso no encontrado")
        return training

    @staticmethod
    def update_training(training_id, **kwargs):
        training = Training.query.get(training_id)
        if not training:
            raise ValueError("Curso no encontrado")
        for key, value in kwargs.items():
            if hasattr(training, key):
                setattr(training, key, value)
        db.session.commit()
        flash('Curso actualizado exitosamente', 'success')
        return redirect(url_for('training.get_trainings'))

    @staticmethod
    def delete_training(training_id):
        training = Training.query.get(training_id)
        if not training:
            raise ValueError("Curso no encontrado")
        db.session.delete(training)
        db.session.commit()
        flash('Curso eliminado exitosamente', 'success')
        return redirect(url_for('training.get_trainings'))