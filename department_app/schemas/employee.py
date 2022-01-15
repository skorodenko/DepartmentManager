
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Field
from marshmallow import EXCLUDE, ValidationError

from department_app.models.employee import Employee
from department_app.service.department import DepartmentService


class DepartmentUUID(Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is not None:
            return value
        else:
            return DepartmentService.get_department_with_id(obj.department_id).uuid

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        try:
            department_uuid = data["department_uuid"]
            return DepartmentService.get_department_with_uuid(department_uuid).uuid
        except KeyError as error:
            raise ValidationError(
                "Employees department is invalid"
            ) from error


class EmployeeSchema(SQLAlchemyAutoSchema):

    class Meta:

        model = Employee

        load_instance = True

        include_fk = True

        exclude = "id", "department_id"

    department_uuid = DepartmentUUID()