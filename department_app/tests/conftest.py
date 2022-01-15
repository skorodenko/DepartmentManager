import pytest


@pytest.fixture(scope="session")
def app():
    from department_app import init_app

    class TestConfig:
        TESTING = True
        ENV = "development"
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        SQLALCHEMY_TRACK_MODIFICATIONS = True

    return init_app(TestConfig)


@pytest.fixture(scope="session")
def db_setup(app):
    from department_app import db as database

    from department_app.models import department, employee
    department_model = department.Department
    employee_model = employee.Employee

    from department_app.service import department, employee
    department_service = department.DepartmentService
    employee_service = employee.EmployeeService

    class Setup:
        db = database
        Department = department_model
        Employee = employee_model
        DepartmentService = department_service
        EmployeeService = employee_service

    return Setup


@pytest.fixture(scope="function")
def data_1(db_setup):
    from datetime import datetime

    db = db_setup.db
    Department = db_setup.Department
    Employee = db_setup.Employee

    db.create_all()
    db.session.commit()

    department_1 = Department("Test Department 1")
    department_2 = Department("Test Department 2")
    department_3 = Department("Test Department 3")

    employee_1 = Employee("Test Employee 1", datetime(2002, 5, 12), 10)
    employee_2 = Employee("Test Employee 2", datetime(1394, 9, 12), 41)
    employee_3 = Employee("Test Employee 3", datetime(2005, 12, 30), 1456)
    employee_4 = Employee("Test Employee 4", datetime(1971, 5, 14), 3464)
    employee_5 = Employee("Test Employee 5", datetime(2021, 1, 1), 23)

    department_1.employees = [employee_1, employee_2]
    department_2.employees = [employee_3, employee_4, employee_5]

    data = {
        "departments": [department_1, department_2, department_3],

        "employees": [employee_1, employee_2, employee_3, employee_4, employee_5],
    }

    db.session.add_all(data["departments"])
    db.session.add_all(data["employees"])
    db.session.commit()

    yield data

    db.drop_all()
    db.session.commit()


@pytest.fixture(scope="session")
def db_schemas(db_setup):
    from department_app.schemas import department, employee
    DepartmentSchema = department.DepartmentSchema
    EmployeeSchema = employee.EmployeeSchema

    class Schemas:
        Department = DepartmentSchema
        Employee = EmployeeSchema

    return Schemas


@pytest.fixture(scope="session")
def app_client(app):
    return app.test_client()
