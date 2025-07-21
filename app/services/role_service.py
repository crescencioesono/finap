from app.models import db
from app.models.role import Role

class RoleService:
    @staticmethod
    def create_role(name):
        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()
        return new_role
    
    @staticmethod
    def get_all_roles():
        return Role.query.all()
    
    @staticmethod
    def get_role_by_id(role_id):
        return Role.query.get(role_id)

    @staticmethod
    def get_role_by_name(name):
        return Role.query.filter_by(name=name).first()

    @staticmethod
    def update_role(role_id, name):
        role = Role.query.get(role_id)
        if not role:
            raise ValueError("Rol no encontrado")
        role.name = name
        db.session.commit()
        return role

    @staticmethod
    def delete_role(role_id):
        role = Role.query.get(role_id)
        if not role:
            raise ValueError("Rol no encontrado")
        db.session.delete(role)
        db.session.commit()
        return True