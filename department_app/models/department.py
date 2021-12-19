
import uuid
from department_app import db


class Department(db.Model):

    # pylint: disable=too-few-public-methods

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.String(36), unique=True)

    name = db.Column(db.String(64), nullable=False, unique=True)

    employees = db.relationship("Employee", backref="department", lazy=True)

    def __init__(self, name, employees=None):
        self.name = name

        if employees is None:
            self.employees = []
        else:
            self.employees = employees

        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"{self.name=}"
