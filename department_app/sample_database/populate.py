from datetime import date

from department_app import db
from department_app.models.department import Department
from department_app.models.employee import Employee


def populate_database():

    db.create_all()

    department_1 = Department("Department of IT development")
    department_2 = Department("Quality assurence")
    department_3 = Department("Research and development")

    employee_1 = Employee("Spike Spigel", date(1998, 11, 9), 2000)
    employee_2 = Employee("Jane Dou", date(1971, 12, 28), 2100)
    employee_3 = Employee("Edward Elrick", date(1899, 11, 24), 1800)

    department_1.employees = [employee_1]
    department_2.employees = [employee_2]
    department_3.employees = [employee_3]

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)

    db.session.commit()
    db.session.close()
