
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Field, Nested
from marshmallow import ValidationError

from department_app.models.employee import Employee
from department_app.service.department import DepartmentService


class DepartmentNested(Nested):
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

    class Meta:

        model = Employee

        load_instance = True

        include_fk = True

        exclude = "id", "department_id"

    department = DepartmentNested()
