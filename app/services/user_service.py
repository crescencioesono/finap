from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash

from app.models import db
from app.models.user import User

class UserService:
    @staticmethod
    def create_user(username, password, role_id):
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username, 
            password=hashed_password, 
            role_id=role_id
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('user.get_users'))

    @staticmethod
    def get_all_users(current_user=None, page=1, search_query=None):
        per_page = 10
        query = User.query
        if search_query:
            search = f"%{search_query}%"
            query = query.filter(
                (User.username.ilike(search)) |
                (User.role.name.ilike(search))
            )
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('users.html', users=pagination.items, current_user=current_user, pagination=pagination)

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        return user

    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('user.get_users'))

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Curso no encontrado")
        db.session.delete(user)
        db.session.commit()
        flash('Curso eliminado exitosamente', 'success')
        return redirect(url_for('user.get_users'))