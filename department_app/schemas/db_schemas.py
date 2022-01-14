from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow.fields import Field, String, Method
from marshmallow import EXCLUDE, ValidationError


def init_schemas(department_model, employee_model, department_service):

    class DepartmentUUID(Field):

        def _serialize(self, value, attr, obj, **kwargs):
            if value is not None:
                return value
            else:
                return department_service.get_department_with_id(obj.department_id).uuid

        def _deserialize(self, value, attr, data, partial=None, **kwargs):
            try:
                department_uuid = data["department_uuid"]
                return department_service.get_department_with_uuid(department_uuid).uuid
            except KeyError as error:
                raise ValidationError(
                    "Employees department is invalid"
                ) from error

    class DepartmentName(String):

        def _deserialize(self, value, attr, data, **kwargs):
            if not data["name"]:
                raise ValidationError("Department name can't be empty")
            return data["name"]

    class EmployeeSchema(SQLAlchemyAutoSchema):

        class Meta:

            model = employee_model

            load_instance = True

            include_fk = True

            exclude = "id", "department_id"

        department_uuid = DepartmentUUID()

    class DepartmentSchema(SQLAlchemyAutoSchema):

        class Meta:

            model = department_model

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
                return sum(map(lambda employee: employee.salary,
                               department.employees)) / len(department.employees)
            except ZeroDivisionError:
                return 0

    return DepartmentSchema, EmployeeSchema
