# pylint: disable=wrong-import-order
"""
This package contains modules with department and employee REST APIs

Modules:
    - "department.py" => defines department api

    - "employee.py" => defines employee api

Functions:
    - "init_api" => register REST API endpoints
"""

from . import department
from . import employee

from department_app import api


def init_rest():
    api.add_resource(department.ListDepartmentApi, "/rest/departments")
    api.add_resource(department.AtomicDepartmentApi, "/rest/department/<uuid>")

    api.add_resource(employee.ListAllEmployeesApi, "/rest/employees")
    api.add_resource(employee.AtomicEmployeeApi, "/rest/employee/<uuid>")
    api.add_resource(employee.EmployeeSearchApi, "/rest/employees/search")
