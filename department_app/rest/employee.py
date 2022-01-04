from flask import request
from flask_restful import Resource
from marshmallow import ValidationError


from department_app import EmployeeSchema
from department_app.service.employee import EmployeeService


class BaseEmployeeApi:
    schema = EmployeeSchema()
    service = EmployeeService()


class ListAllEmployeesApi(Resource, BaseEmployeeApi):

    def get(self):
        employees = self.service.get_employees()
        return self.schema.dump(employees, many=True), 200

    def post(self):
        try:
            employee = self.service.add_employee(self.schema, request.json)
        except ValidationError as e:
            return e.messages, 400
        return self.schema.dump(employee), 201


class AtomicEmployeeApi(Resource, BaseEmployeeApi):

    def get(self, uuid):
        try:
            employee = self.service.get_employee_with_uuid(uuid)
        except KeyError as e:
            return str(e), 404
        return self.schema.dump(employee), 200

    def put(self, uuid):
        try:
            employee = self.service.update_employee(
                self.schema, uuid, request.json)
        except ValidationError as e:
            return e.messages, 400
        except KeyError as e:
            return str(e), 404
        return self.schema.dump(employee), 201

    def delete(self, uuid):
        try:
            return self.service.delete_employee(uuid), 204
        except KeyError as e:
            return str(e), 404
