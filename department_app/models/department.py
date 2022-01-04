
import uuid as  UUID


def init_department_model(db):
    
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
    
            if not employees:
                self.employees = []
            else:
                self.employees = employees
    
    
        def __repr__(self):
            return f"<Department: {self.name}>"
    
    return Department