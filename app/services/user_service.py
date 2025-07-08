from app.models import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def create_user(username, password, role_id):
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, role_id=role_id)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error al crear el usuario: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def update_user(user_id, username=None, password=None, role_id=None):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password)
        if role_id:
            user.role_id = role_id
        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error al actualizar el usuario: {str(e)}")

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        db.session.delete(user)
        db.session.commit()
        return True