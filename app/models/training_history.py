from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func
from app.models import db

class TrainingHistory(db.Model):
    __tablename__ = 'training_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    official_id = db.Column(db.Integer, db.ForeignKey('officials.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    training_date = db.Column(db.Date, nullable=False)
    training_city = db.Column(db.String(100), nullable=False)
    modality = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='En progreso')
    other_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    __table_args__ = (
        CheckConstraint("status IN ('En progreso', 'Incompleto', 'Completo')", name='check_batch_status'),
    )
    # Relación con Official y Batch
    official = db.relationship('Official', back_populates='training_history', lazy=True)
    batch = db.relationship('Batch', backref='training_history', lazy=True)