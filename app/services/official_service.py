from flask import render_template, flash, redirect, url_for
from app.models import db
from app.models.official import Official
from app.models.training_history import TrainingHistory

class OfficialService:
    @staticmethod
    def create_official(first_name, last_name, date_of_birth, country, address, phone_number, workplace, level, email=None, image=None):
        new_official = Official(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            country=country,
            address=address,
            phone_number=phone_number,
            workplace=workplace,
            level=level,
            email=email,
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
                (Official.country.ilike(search)) |  # New field
                (Official.address.ilike(search)) |  # New field
                (Official.phone_number.ilike(search)) |  # New field
                (Official.email.ilike(search)) |  # New field
                (Official.workplace.ilike(search)) |
                (Official.level.ilike(search))
            )
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('officials.html', officials=pagination.items, current_user=current_user, pagination=pagination)

    @staticmethod
    def get_official_by_id(official_id):
        from app.models import db
        official = Official.query.options(
            db.joinedload(Official.training_history).joinedload(TrainingHistory.batch_tracking)
        ).get_or_404(official_id)
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