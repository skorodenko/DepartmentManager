
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow.fields import String, Method
from marshmallow import EXCLUDE, ValidationError

from department_app.models.department import Department
from .employee import EmployeeSchema

class DepartmentName(String):

    def _deserialize(self, value, attr, data, **kwargs):
        if not data["name"]:
            raise ValidationError("Department name can't be empty")
        return data["name"]



class DepartmentSchema(SQLAlchemyAutoSchema):

    class Meta:

        model = Department

        load_instance = True

        include_relationships = True

        exclude = "id",

        dump_only = "employees",

        unknown = EXCLUDE

    name = DepartmentName(required=True)

    employees = Nested(EmployeeSchema, many=True)

    average_salary = Method("calculate_average_salary")

    @staticmethod
    def calculate_average_salary(department):
        try:
            return round(sum(map(lambda employee: employee.salary,
                            department.employees)) / len(department.employees), 2)
        except ZeroDivisionError:
            return 0
