# pylint: disable=invalid-name,redefined-builtin
"""
Department service used to make database queries

Classes:
    - "DepartmentService" => department service
"""

from department_app import db
from department_app.models.department import Department


class DepartmentService:
    """
    Department service to make database queries
    """

    @staticmethod
    def get_departments():
        """
        Fetches all departments
        """
        return db.session.query(Department).all()

    @staticmethod
    def get_department_with_uuid(uuid):
        """
        Fetches department with specified uuid

        Raises:
            - KeyError if department uuid is invalid
        """
        department = db.session.query(
            Department).filter_by(uuid=uuid).first()
        if department is None:
            raise KeyError(f"Invalid department uuid: {uuid}")
        return department

    @staticmethod
    def add_department(db_schema, department_json):
        """
        Deserializes department and adds it to the database
        """
        department = db_schema.load(department_json, session=db.session)

        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def update_department(cls, db_schema, uuid, department_json):
        """
        Updates department

        Raises:
            - KeyError if department uuid is invalid
        """
        department = cls.get_department_with_uuid(uuid)

        department = db_schema.load(
            department_json, instance=department, session=db.session)
        db.session.commit()
        return department

    @classmethod
    def delete_department(cls, uuid):
        """
        Deletes department

        Raises:
            - KeyError if department uuid is invalid
        """
        department = cls.get_department_with_uuid(uuid)

        db.session.delete(department)
        db.session.commit()
