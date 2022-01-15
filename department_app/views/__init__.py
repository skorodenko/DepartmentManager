

from . import departments
from . import employees


def init_views():
    departments.init_departments_view()
    employees.init_employees_view()
