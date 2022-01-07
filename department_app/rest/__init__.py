from . import department
from . import employee


def init_rest(api, department_service, employee_service, department_schema, employee_schema):

    department.init_department_rest(
        api, department_service, employee_service, department_schema)

    employee.init_employee_rest(api, employee_service, employee_schema)
