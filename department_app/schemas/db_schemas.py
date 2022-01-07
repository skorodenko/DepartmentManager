from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow.fields import Field
from marshmallow import EXCLUDE, ValidationError


def init_schemas(department_model, employee_model, department_service):

    class DepartmentUUID(Field):

        def _serialize(self, value, attr, obj, **kwargs):
            if value is not None:
                return value
            else:
                return department_service.get_deaprtment_with_id(obj.department_id).uuid

        def _deserialize(self, value, attr, data, partial=None, **kwargs):
            try:
                department_uuid = data["department_uuid"]
                return department_service.get_department_with_uuid(department_uuid).uuid
            except KeyError as error:
                raise ValidationError(
                    "Employees department is invalid"
                ) from error

    class EmployeeSchema(SQLAlchemyAutoSchema):
        
        class Meta:
    
            model = employee_model
    
            load_instance = True

            #include_relationships = True

            include_fk = True
    
            required = "name", "date_of_birth", "salary"
    
            exclude = "id", "department_id"

        department_uuid = DepartmentUUID()


    class DepartmentSchema(SQLAlchemyAutoSchema):
    
        class Meta:
    
            model = department_model
    
            load_instance = True
    
            include_relationships = True
    
            required = "name"
    
            exclude = "id",

            dump_only = "employees",

            unknown = EXCLUDE
    
        employees = Nested(EmployeeSchema, many=True)   


    return DepartmentSchema, EmployeeSchema