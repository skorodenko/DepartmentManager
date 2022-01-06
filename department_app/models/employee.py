
import uuid as UUID


def init_employee_model(db):

    class Employee(db.Model):
    
        # pylint: disable=too-few-public-methods
    
        id = db.Column(db.Integer, primary_key=True)
    
        uuid = db.Column(db.String(36), unique=True, nullable=False)
    
        department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

        department_uuid = db.Column(db.String(36), unique=True)
    
        name = db.Column(db.String(64), nullable=False)
    
        date_of_birth = db.Column(db.DateTime, nullable=False)
    
        salary = db.Column(db.Integer, nullable=False)
    
        def __init__(self, name=None, date_of_birth=None, salary=0, uuid=None, department_uuid=None):
    
            self.name = name
    
            self.date_of_birth = date_of_birth
    
            self.salary = salary

            if uuid is None:
                self.uuid = str(UUID.uuid4())
            else:
                self.uuid = uuid
            
            self.department_uuid = department_uuid

        def __repr__(self):
            return f"<Employee: {self.name}, {self.date_of_birth}, {self.salary}>"
    
    return Employee