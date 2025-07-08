from sqlalchemy.sql import func
from app.models import db

class Log(db.Model):
    __tablename__ = 'logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255), nullable=False)
    log_time = db.Column(db.DateTime, default=func.current_timestamp())
    details = db.Column(db.Text)

    user = db.relationship('User', backref='logs', lazy=True)