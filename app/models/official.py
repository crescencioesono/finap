from sqlalchemy.sql import func
from app.models import db

class Official(db.Model):
    __tablename__ = 'officials'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    country = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150))
    workplace = db.Column(db.String(150), nullable=False)
    level = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())