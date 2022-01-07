

from . import department, employee


def init_models(db):
    return department.init_department_model(db), employee.init_employee_model(db)
