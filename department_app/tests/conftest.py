from enum import unique
import pytest


from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import uuid as UUID


@pytest.fixture(scope="session")
def app():
    from department_app import create_app

    class TestConfig:
        TESTING = True
        ENV = "development"
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        SQLALCHEMY_TRACK_MODIFICATIONS = True

    return create_app(TestConfig)


@pytest.fixture(scope="session")
def setup_db(app):
    from department_app.models import department, employee
    db = SQLAlchemy(app)

    class Department(db.Model):
    
        # pylint: disable=too-few-public-methods
    
        id = db.Column(db.Integer, primary_key=True)
    
        uuid = db.Column(db.String(36), unique=True)
    
        name = db.Column(db.String(64), nullable=False, unique=True)
    
        employees = db.relationship("Employee", backref="department", cascade="all,delete-orphan")
    
        def __init__(self, name, employees=None, id=None, uuid=None):
            if id is not None:
                self.id = id
    
            if uuid is not None:
                self.uuid = uuid
            else:
                self.uuid = str(UUID.uuid4())    
            
            self.name = name
    
            if employees is None:
                self.employees = []
            else:
                self.employees = employees


    def __repr__(self):
        return f"<Department: {self.name}>"


    class Employee(db.Model):
    
        # pylint: disable=too-few-public-methods
    
        id = db.Column(db.Integer, primary_key=True)
    
        uuid = db.Column(db.String(36), unique=True)
    
        department_uuid = db.Column(db.String(36), db.ForeignKey("department.uuid"),
                                    nullable=False)
    
        name = db.Column(db.String(64), nullable=False)
    
        date_of_birth = db.Column(db.DateTime, nullable=False)
    
        salary = db.Column(db.Integer, nullable=False)
    
        def __init__(self, name, date_of_birth, salary=0, id=None, uuid=None):
            if id is not None:
                self.id = id
    
            if uuid is not None:
                self.uuid = uuid
            else:
                self.uuid = str(UUID.uuid4())
    
            self.name = name
    
            self.date_of_birth = date_of_birth
    
            self.salary = salary
    
        def __repr__(self):
            return f"<Employee: {self.name}, {self.date_of_birth}, {self.salary}>"

    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture(scope="session")
def data_1(setup_db):
    from datetime import date

    from department_app.models.department import Department
    from department_app.models.employee import Employee

    db = setup_db

    department_1 = Department("Test Department 1")
    department_2 = Department("Test Department 2")
    department_3 = Department("Test Department 3")

    employee_1 = Employee("Test Employee 1", date(2002, 5, 12), 10)
    employee_2 = Employee("Test Employee 2", date(1394, 9, 12), 41)
    employee_3 = Employee("Test Employee 3", date(2005, 12, 30), 1456)
    employee_4 = Employee("Test Employee 4", date(1971, 5, 14), 3464)

    department_1.employees = [employee_1, employee_2, employee_3]
    department_2.employees = [employee_4]

    db.session.add_all((department_1, department_2, department_3))
    db.session.add_all((employee_1, employee_2, employee_3, employee_4))
    db.session.commit()

    data = {
        "db": db,

        "departments": [department_1, department_2, department_3],

        "employees": [employee_1, employee_2, employee_3, employee_4],
    }

    yield data


@pytest.fixture(scope="session")
def rest_api(app):
    api = Api(app)

    from department_app.rest import init_rest
    init_rest(api)

    return api


@pytest.fixture(scope="module")
def department_schema():
    from department_app.schemas.department import DepartmentSchema
    return DepartmentSchema()


@pytest.fixture(scope="module")
def employee_schema():
    from department_app.schemas.employee import EmployeeSchema
    return EmployeeSchema()


@pytest.fixture(scope="module")
def app_client(app):
    return app.test_client()
