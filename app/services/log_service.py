from flask import render_template

from app.models import db
from app.models.log import Log
from app.services.auth_service import AuthService

class LogService:
    @staticmethod
    def create_log(action, details=""):
        current_user = AuthService.get_current_user()
        if current_user and current_user.id:
            new_log = Log(
                user_id=current_user.id,
                action=action,
                details=details
            )
            db.session.add(new_log)
            db.session.commit()
        else:
            print(f"Warning: No user logged in to create log for action: {action}")

    @staticmethod
    def get_all_logs(current_user=None, page=1, search_query=None):
        per_page = 10
        query = Log.query.join(Log.user).options(db.joinedload(Log.user))
        if search_query:
            search = f"%{search_query}%"
            query = query.filter(
                (Log.action.ilike(search)) |
                (Log.details.ilike(search)) |
                (Log.user.username.ilike(search))  # Assume User has a username
            )
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('logs.html', logs=pagination.items, pagination=pagination, current_user=current_user)