

from department_app.rest import department


def init_department_service(db, department_model):
    class DepartmentService:

        @staticmethod
        def get_departments():
            return db.session.query(department_model).all()

        @staticmethod
        def get_deaprtment_with_id(id):
            department = db.session.query(
                department_model).filter_by(id=id).first()
            if department is None:
                raise KeyError(f"Invalid department id: {id}")
            return department

        @staticmethod
        def get_department_with_uuid(uuid):
            department = db.session.query(
                department_model).filter_by(uuid=uuid).first()
            if department is None:
                raise KeyError(f"Invalid department uuid: {uuid}")
            return department

        @staticmethod
        def get_department_with_name(name):
            department = db.session.query(
                department_model).filter_by(name=name).first()
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
            db.session.commit()
            return department

        @classmethod
        def delete_department(cls, uuid):
            department = cls.get_department_with_uuid(uuid)

            db.session.delete(department)
            db.session.commit()
            return None

    return DepartmentService
