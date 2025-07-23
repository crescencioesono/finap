from app.models import db
from sqlalchemy import func

batch_training = db.Table(
    'batch_trainings',
    db.Column('batch_id', db.Integer, db.ForeignKey('batches.id'), primary_key=True),
    db.Column('training_id', db.Integer, db.ForeignKey('trainings.id'), primary_key=True)
)

class Batch(db.Model):
    __tablename__ = 'batches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    trainings = db.relationship('Training', secondary='batch_trainings', back_populates='batches')  # Changed to plural