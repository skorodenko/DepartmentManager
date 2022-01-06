
from . import department
from . import employee


def init_schemas(department_model, employee_model):

#    class EmployeeSchema(SQLAlchemyAutoSchema):
#        
#        class Meta:
#    
#            model = employee_model
#    
#            load_instance = True
#
#            #include_relationships = True
#
#            #include_fk = True
#    
#            required = "name", "date_of_birth", "salary", "department_uuid"
#    
#            exclude = "id",
#
#        #department_uuid = Nested(lambda: DepartmentSchema(only=("uuid",)))
#
#
#    class DepartmentSchema(SQLAlchemyAutoSchema):
#    
#        class Meta:
#    
#            model = department_model
#    
#            load_instance = True
#    
#            include_relationships = True
#    
#            required = "name"
#    
#            exclude = "id",
#
#            dump_only = "employees",
#
#            unknown = EXCLUDE
#    
#        employees = Nested(EmployeeSchema, many=True)   

    employee_schema = employee.init_employee_schema(employee_model)

    department_schema = department.init_department_schema(department_model, employee_schema)

    return department_schema, employee_schema