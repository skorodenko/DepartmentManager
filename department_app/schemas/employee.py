# pylint: disable=too-few-public-methods
"""
This module defines schema, used to serialize/deserialize employees

Classes:
    - EmployeeSchema => department serialization/deserialization schema

    - DepartmentNested => nested department for employee schema
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from marshmallow import ValidationError, EXCLUDE

from department_app.models.employee import Employee
from department_app.service.department import DepartmentService


class DepartmentNested(Nested):
    """
    Marshmallow field, used to nest employee's department
    into employee schema
    """
    def __init__(self):
        super().__init__(
            "DepartmentSchema", exclude=("employees", "average_salary"), required=True
        )

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        try:
            department_uuid = data["department"]["uuid"]
            return DepartmentService.get_department_with_uuid(department_uuid)
        except KeyError as exception:
            raise ValidationError(
                "Employees department uuid is invalid"
            ) from exception


class EmployeeSchema(SQLAlchemyAutoSchema):
    """
    Employee serialization/deserialization schema
    """
    class Meta:
        """
        Employee schema metadata
        """

        model = Employee

        load_instance = True

        include_fk = True

        # exclude ids (security)
        exclude = "id", "department_id"

        # excludes unknown fields on deserialization
        unknown = EXCLUDE

    department = DepartmentNested()
