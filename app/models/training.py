from app.models import db

class Training(db.Model):
    __tablename__ = 'trainings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    batches = db.relationship('Batch', secondary='batch_trainings', back_populates='trainings')  # Reciprocal relationship