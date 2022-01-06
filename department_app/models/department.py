
import uuid as UUID


def init_department_model(db):

    class Department(db.Model):

        # pylint: disable=too-few-public-methods

        id = db.Column(db.Integer, primary_key=True)

        uuid = db.Column(db.String(36), unique=True, nullable=False)

        name = db.Column(db.String(64), nullable=False, unique=True)

        employees = db.relationship("Employee", 
                                    backref="department", 
                                    cascade="all,delete-orphan", 
                                    lazy=True)

        def __init__(self, name=None, employees=None, uuid=None):

            self.name = name

            if not employees:
                self.employees = []
            else:
                self.employees = employees

            if uuid is None:
                self.uuid = str(UUID.uuid4())
            else:
                self.uuid = uuid

        def __repr__(self):
            return f"<Department: {self.name}>"

    return Department
