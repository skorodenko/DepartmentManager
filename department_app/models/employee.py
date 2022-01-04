

import uuid as UUID
from department_app import db


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
