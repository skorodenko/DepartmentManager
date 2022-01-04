from marshmallow.decorators import validates_schema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


from department_app.models.department import Department
from .employee import EmployeeSchema


class DepartmentSchema(SQLAlchemyAutoSchema):

    class Meta:

        model = Department

        load_instance = True

        include_relationships = True

        required = "name"

        exclude = "id",

        #load_only = "employees",

    employees = Nested(EmployeeSchema, many=True, exclude=("department_uuid",))
    