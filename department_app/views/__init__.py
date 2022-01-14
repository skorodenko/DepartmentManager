

from . import departments
from . import employees


def init_views(app):
    departments.init_departments_view(app) 
    employees.init_employees_view(app)   