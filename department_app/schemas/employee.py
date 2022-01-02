from marshmallow.decorators import validates_schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from department_app.models.employee import Employee


class EmployeeSchema(SQLAlchemyAutoSchema):

    class Meta:

        model = Employee

        load_instance = True

        include_fk = True

        required = "name", "date_of_birth", "salary", "department_uuid"

        exclude = "id",

    @validates_schema
    def validate_employee(self):
        ...
