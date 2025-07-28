from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func
from app.models import db

class BatchTracking(db.Model):
    __tablename__ = 'batch_tracking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    history_id = db.Column(db.Integer, db.ForeignKey('training_history.id'), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='En progreso')
    end_date = db.Column(db.Date, nullable=True)
    grade = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint("status IN ('En progreso', 'Incompleto', 'Completo')", name='check_training_status'),
    )

    history = db.relationship('TrainingHistory', back_populates='batch_tracking', lazy=True)
    training = db.relationship('Training', backref='batch_tracking', lazy=True)