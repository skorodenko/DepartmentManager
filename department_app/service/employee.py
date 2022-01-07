


def init_employee_service(db, employee_model, department_service):
    class EmployeeService:

        @staticmethod
        def get_employees():
            return db.session.query(employee_model).all()

        @staticmethod
        def get_employees_with_department_uuid(department_uuid):
            employees = db.session.query(employee_model).filter_by(
                department_uuid=department_uuid).all()
            if employees is None:
                raise KeyError(f"Invalid department uuid: {department_uuid}")
            return employees

        @staticmethod
        def get_employee_with_uuid(uuid):
            employee = db.session.query(
                employee_model).filter_by(uuid=uuid).first()
            if employee is None:
                raise KeyError(f"Invalid employee uuid: {uuid}")
            return employee

        @staticmethod
        def add_employee(db_schema, employee_json):
            employee = db_schema.load(employee_json, session=db.session)
            department = department_service.get_department_with_uuid(employee.department_uuid)
            department.employees.append(employee)
            db.session.commit()
            return employee

        @classmethod
        def update_employee(cls, db_schema, uuid, employee_json):
            employee = cls.get_employee_with_uuid(uuid)
            employee = db_schema.load(
                employee_json, instance=employee, session=db.session)
            db.session.commit()
            return employee

        @classmethod
        def delete_employee(cls, uuid):
            employee = cls.get_employee_with_uuid(uuid)
            db.session.delete(employee)
            db.session.commit()
            return None

    return EmployeeService
