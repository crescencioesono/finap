from app.models import db
from app.models.official import Official

class OfficialService:
    @staticmethod
    def create_official(first_name, last_name, date_of_birth, workplace, level, image):
        new_official = Official(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            workplace=workplace,
            level=level,
            image=image
        )
        db.session.add(new_official)
        db.session.commit()
        return new_official

    @staticmethod
    def get_official_by_id(official_id):
        return Official.query.get(official_id)

    @staticmethod
    def update_official(official_id, **kwargs):
        official = Official.query.get(official_id)
        if not official:
            raise ValueError("Oficial no encontrado")
        for key, value in kwargs.items():
            setattr(official, key, value)
        db.session.commit()
        return official

    @staticmethod
    def delete_official(official_id):
        official = Official.query.get(official_id)
        if not official:
            raise ValueError("Oficial no encontrado")
        db.session.delete(official)
        db.session.commit()
        return True