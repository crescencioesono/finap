from flask import redirect, url_for
from app.models import db
from app.models.batch import Batch
from app.models.training import Training

class BatchService:
    @staticmethod
    def create_batch(code, description, trainings=None):
        batch = Batch(code=code, description=description)
        db.session.add(batch)
        if trainings:
            batch.trainings = [Training.query.get(int(id)) for id in trainings if id]
        db.session.commit()
        return redirect(url_for('batch.get_batches'))

    @staticmethod
    def update_batch(batch_id, code, description, trainings=None):
        batch = Batch.query.get_or_404(batch_id)
        batch.code = code
        batch.description = description
        if trainings is not None:  # Only update if trainings are provided
            batch.trainings = [Training.query.get(int(id)) for id in trainings if id]
        db.session.commit()
        return redirect(url_for('batch.get_batches'))

    @staticmethod
    def get_batch_by_id(batch_id):
        batch = Batch.query.options(db.joinedload(Batch.trainings)).get_or_404(batch_id)
        return batch

    @staticmethod
    def get_all_trainings():
        return Training.query.all()

    @staticmethod
    def get_all_batches(current_user=None, page=1, search_query=None):
        per_page = 10
        query = Batch.query
        if search_query:
            query = query.filter(Batch.code.ilike(f'%{search_query}%'))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def delete_batch(batch_id):
        batch = Batch.query.get_or_404(batch_id)
        db.session.delete(batch)
        db.session.commit()
        return redirect(url_for('batch.get_batches'))