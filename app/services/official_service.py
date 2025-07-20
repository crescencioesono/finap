from flask import render_template, flash, redirect, url_for
from app.models import db
from app.models.official import Official

class OfficialService:
    @staticmethod
    def create_official(first_name, last_name, date_of_birth, workplace, level, image=None):
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
        flash('Oficial creado exitosamente', 'success')
        return redirect(url_for('official.get_officials'))

    @staticmethod
    def get_all_officials(current_user=None, page=1, search_query=None):
        per_page = 10
        query = Official.query
        if search_query:
            search = f"%{search_query}%"
            query = query.filter(
                (Official.first_name.ilike(search)) |
                (Official.last_name.ilike(search)) |
                (Official.workplace.ilike(search)) |
                (Official.level.ilike(search))
            )
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('officials.html', officials=pagination.items, current_user=current_user, pagination=pagination)

    @staticmethod
    def get_official_by_id(official_id):
        official = Official.query.get(official_id)
        if not official:
            raise ValueError("Oficial no encontrado")
        return official

    @staticmethod
    def update_official(official_id, **kwargs):
        official = Official.query.get(official_id)
        if not official:
            raise ValueError("Oficial no encontrado")
        for key, value in kwargs.items():
            if hasattr(official, key):
                setattr(official, key, value)
        db.session.commit()
        flash('Oficial actualizado exitosamente', 'success')
        return redirect(url_for('official.get_officials'))

    @staticmethod
    def delete_official(official_id):
        official = Official.query.get(official_id)
        if not official:
            raise ValueError("Oficial no encontrado")
        db.session.delete(official)
        db.session.commit()
        flash('Oficial eliminado exitosamente', 'success')
        return redirect(url_for('official.get_officials'))