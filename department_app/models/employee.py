
import uuid as UUID

from department_app import db


class Employee(db.Model):
    """
    ORM model representing employee

    Parameters:
        - Name => employee name
        - Date of birth => employee's date of birth (yyyy-mm-dd)
        - Salary => employee's salary
        - Department => employee's Department
    """
    # pylint: disable=too-few-public-methods

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.String(36), unique=True)

    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    name = db.Column(db.String(64), nullable=False)

    date_of_birth = db.Column(db.Date, nullable=False)

    salary = db.Column(db.Integer, nullable=False)

    def __init__(self, name=None, date_of_birth=None, salary=0, department=None):

        self.name = name

        self.date_of_birth = date_of_birth

        self.salary = salary

        self.uuid = str(UUID.uuid4())

        self.department = department

    def __repr__(self):
        return f"<Employee: {self.name}, {self.date_of_birth}, {self.salary}>"
