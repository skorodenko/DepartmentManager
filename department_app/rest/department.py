
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from department_app.service.department import DepartmentService
from department_app.service.employee import EmployeeService
from department_app.schemas.department import DepartmentSchema


class BaseDepartmentApi:
    service = DepartmentService
    employee_service = EmployeeService
    schema = DepartmentSchema()


class ListDepartmentApi(Resource, BaseDepartmentApi):

    def get(self):
        departments = self.service.get_departments()
        return self.schema.dump(departments, many=True), 200

    def post(self):
        try:
            department = self.service.add_department(
                self.schema, request.json)
        except ValidationError as exception:
            return exception.messages, 400
        except IntegrityError:
            return "Duplicate department name", 400
        return self.schema.dump(department), 201


class AtomicDepartmentApi(Resource, BaseDepartmentApi):

    def get(self, uuid):
        try:
            department = self.service.get_department_with_uuid(uuid)
        except KeyError as exception:
            return str(exception), 404
        return self.schema.dump(department), 200

    def put(self, uuid):
        try:
            department = self.service.update_department(
                self.schema, uuid, request.json)
        except ValidationError as exception:
            return exception.messages, 400
        except IntegrityError:
            return "Duplicate department name", 400
        except KeyError as exception:
            return str(exception), 404
        return self.schema.dump(department), 201

    def delete(self, uuid):
        try:
            return self.service.delete_department(uuid), 204
        except KeyError as exception:
            return str(exception), 404
