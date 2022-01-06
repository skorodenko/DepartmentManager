from marshmallow_sqlalchemy.fields import Nested
from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


def init_department_schema(department_model, employee_schema):
    class DepartmentSchema(SQLAlchemyAutoSchema):
    
        class Meta:
    
            model = department_model
    
            load_instance = True
    
            include_relationships = True
    
            required = "name"
    
            exclude = "id",
    
            dump_only = "employees",

            unknown = EXCLUDE
    
        employees = Nested(employee_schema, many=True)

    return DepartmentSchema  