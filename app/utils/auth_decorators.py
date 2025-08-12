from functools import wraps
from flask import redirect, url_for, flash
from flask_jwt_extended import jwt_required
from app.services.auth_service import AuthService

def role_required(role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user = AuthService.get_current_user()
            if not current_user or current_user.role.name != role:
                flash(f'Solo los usuarios con rol {role} pueden realizar esta acción.', 'error')
                return redirect(url_for('official.get_officials'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator