from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

def init_employee_schema(employee_model):
    class EmployeeSchema(SQLAlchemyAutoSchema):
    
        class Meta:
    
            model = employee_model
    
            load_instance = True
    
            include_fk = True

            include_relatiships = True

            required = "name", "date_of_birth", "salary", "department_uuid"
    
            exclude = "id",
    
    return EmployeeSchema
