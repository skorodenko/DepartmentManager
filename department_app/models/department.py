# pylint: disable=too-few-public-methods

import uuid as UUID

from department_app import db


class Department(db.Model):
    """
    ORM model representing department

    Parameters:
        - Name => department name
        - Employees => list of employees of the department
    """

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.String(36), unique=True)

    name = db.Column(db.String(64), nullable=False, unique=True)

    employees = db.relationship("Employee",
                                backref="department",
                                cascade="all,delete-orphan",
                                lazy=True)

    def __init__(self, name=None, employees=None):

        self.name = name

        if not employees:
            self.employees = []
        else:
            self.employees = employees

        self.uuid = str(UUID.uuid4())

    def __repr__(self):
        return f"<Department: {self.name}>"
