import pytest


from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope="function")
def app():
    from department_app import create_app

    class TestConfig:
        TESTING = True
        ENV = "development"
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        SQLALCHEMY_TRACK_MODIFICATIONS = True

    return create_app(TestConfig)


@pytest.fixture(scope="function")
def db_setup(app):
    database = SQLAlchemy(app)

    from department_app.models import init_models
    department_model, employee_model = init_models(database)

    from department_app.service import init_services
    department_service, employee_service = init_services(
        database, department_model, employee_model)

    class Setup:
        db = database
        Department = department_model
        Employee = employee_model
        DepartmentService = department_service
        EmployeeService = employee_service

    Setup.db.create_all()
    return Setup


@pytest.fixture(scope="function")
def data_1(db_setup):
    from datetime import datetime

    db = db_setup.db
    Department = db_setup.Department
    Employee = db_setup.Employee

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

    return data


@pytest.fixture(scope="function")
def db_schemas(db_setup):
    from department_app.schemas import init_schemas
    DS, ES = init_schemas(db_setup.Department,
                          db_setup.Employee, db_setup.DepartmentService)

    class Schemas:
        Department = DS
        Employee = ES

    return Schemas


@pytest.fixture(scope="function")
def rest_api(app, db_schemas, db_setup):
    api = Api(app)

    from department_app.rest import init_rest
    init_rest(api, db_setup.DepartmentService, db_setup.EmployeeService,
              db_schemas.Department, db_schemas.Employee)

    return api


@pytest.fixture(scope="function")
def app_client(app):
    return app.test_client()
