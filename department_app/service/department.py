

from department_app import db
from department_app.models.department import Department


class DepartmentService:

    @staticmethod
    def get_departments():
        return db.session.query(Department).all()

    @staticmethod
    def get_department_with_uuid(uuid):
        department = db.session.query(Department).filter_by(uuid=uuid).first()
        if department is None:
            raise KeyError(f"Invalid department uuid: {uuid}")
        return department

    @staticmethod
    def get_department_with_name(name):
        department = db.session.query(Department).filter_by(name=name).first()
        if department is None:
            raise KeyError(f"Invalid department name: {name}")
        return department

    @staticmethod
    def add_department(db_schema, department_json):
        department = db_schema.load(department_json, session=db.session)

        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def update_department(cls, db_schema, uuid, department_json):
        department = cls.get_department_with_uuid(uuid)

        department = db_schema.load(
            department_json, instance=department, session=db.session)
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def delete_department(cls, uuid):
        department = cls.get_department_with_uuid(uuid)

        db.session.delete(department)
        db.session.commit()
        return None
