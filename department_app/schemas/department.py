# pylint: disable=trailing-comma-tuple,too-few-public-methods,cyclic-import
"""
This module defines schema, used to serialize/deserialize departments

Classes:
    - DepartmentSchema => department serialization/deserialization schema
    
    - DepartmentName => marshmallow class to validate department name
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow.fields import String, Method
from marshmallow import EXCLUDE, ValidationError

from department_app.models.department import Department
from .employee import EmployeeSchema


class DepartmentName(String):
    """
    Marshmallow field, used to verify department name
    is not empty("")
    """

    def _deserialize(self, value, attr, data, **kwargs):
        if not data["name"]:
            raise ValidationError("Department name can't be empty")
        return data["name"]


class DepartmentSchema(SQLAlchemyAutoSchema):
    """
    Department serialization/deserialization schema
    """
    class Meta:
        """
        Department schema metadata
        """

        model = Department

        load_instance = True

        include_relationships = True

        # exclude id (security)
        exclude = "id",

        # include employees only when serializing department
        dump_only = "employees",
        
        # excludes unknown fields on deserialization
        unknown = EXCLUDE

    name = DepartmentName(required=True)

    employees = Nested(EmployeeSchema, many=True)

    average_salary = Method("calculate_average_salary")

    @staticmethod
    def calculate_average_salary(department):
        """
        Calculates average salary for department
        """
        try:
            return round(sum(map(lambda employee: employee.salary,
                                 department.employees)) / len(department.employees), 2)
        except ZeroDivisionError:
            return 0
