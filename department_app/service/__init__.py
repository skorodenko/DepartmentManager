from . import department
from . import employee


def init_services(db, department_model, employee_model):
    department_service = department.init_department_service(
        db, department_model)
    employee_service = employee.init_employee_service(
        db, employee_model, department_service)
    return department_service, employee_service
