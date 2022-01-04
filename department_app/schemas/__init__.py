
from . import department
from . import employee


def init_schemas(department_model, employee_model):

    employee_schema = employee.init_employee_schema(employee_model)

    department_schema = department.init_department_schema(department_model, employee_schema)

    return department_schema, employee_schema