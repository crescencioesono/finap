from app.models import db
from app.models.log import Log

class LogService:
    @staticmethod
    def create_log(user_id, action, details=None):
        new_log = Log(
            user_id=user_id,
            action=action,
            details=details
        )
        db.session.add(new_log)
        db.session.commit()
        return new_log

    @staticmethod
    def get_log_by_id(log_id):
        return Log.query.get(log_id)

    @staticmethod
    def get_logs_by_user(user_id):
        return Log.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_log(log_id, action=None, details=None):
        log = Log.query.get(log_id)
        if not log:
            raise ValueError("Registro de log no encontrado")
        if action:
            log.action = action
        if details:
            log.details = details
        db.session.commit()
        return log

    @staticmethod
    def delete_log(log_id):
        log = Log.query.get(log_id)
        if not log:
            raise ValueError("Registro de log no encontrado")
        db.session.delete(log)
        db.session.commit()
        return True