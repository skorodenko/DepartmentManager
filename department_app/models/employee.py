

import uuid
from department_app import db


class Employee(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.String(36), unique=True)

    department_id = db.Column(db.Integer, db.ForeignKey("department.id"),
                              nullable=False)

    name = db.Column(db.String(64), nullable=False, unique=True)

    date_of_birth = db.Column(db.DateTime, nullable=False)

    salary = db.Column(db.Integer, nullable=False)

    def __init__(self, name, date_of_birth, salary=0):
        self.name = name

        self.date_of_birth = date_of_birth

        self.salary = salary

        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"{self.name=}, {self.date_of_birth=}, {self.salary=}"
