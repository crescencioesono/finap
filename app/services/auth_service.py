from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta

class AuthService:
    @staticmethod
    def register_user(username, password, role_id):
        if User.query.filter_by(username=username).first():
            raise ValueError("El nombre de usuario ya está en uso")
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_id': user.id,
                'username': user.username,
                'role_id': user.role_id
            }
        else:
            raise ValueError("Nombre de usuario o contraseña incorrectos")

    @staticmethod
    def refresh_token():
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id, expires_delta=timedelta(hours=1))
        return {'access_token': new_access_token}

    @staticmethod
    def get_current_user():
        user_id = get_jwt_identity()
        return User.query.get(user_id)