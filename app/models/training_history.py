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
    state = db.Column(db.String(100), nullable=False)
    other_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    official = db.relationship('Official', backref='training_history', lazy=True)
    batch = db.relationship('Batch', backref='training_history', lazy=True)