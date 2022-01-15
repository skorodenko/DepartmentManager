# pylint: disable=too-few-public-methods

import datetime
from flask import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from department_app.service.employee import EmployeeService
from department_app.schemas.employee import EmployeeSchema


class BaseEmployeeApi:
    service = EmployeeService
    schema = EmployeeSchema()


class ListAllEmployeesApi(Resource, BaseEmployeeApi):

    def get(self):
        employees = self.service.get_employees()
        return self.schema.dump(employees, many=True), 200

    def post(self):
        try:
            employee = self.service.add_employee(self.schema, request.json)
        except ValidationError as exception:
            return exception.messages, 400
        return self.schema.dump(employee), 201


class AtomicEmployeeApi(Resource, BaseEmployeeApi):

    def get(self, uuid):
        try:
            employee = self.service.get_employee_with_uuid(uuid)
        except KeyError as exception:
            return str(exception), 404
        return self.schema.dump(employee), 200

    def put(self, uuid):
        try:
            employee = self.service.update_employee(
                self.schema, uuid, request.json)
        except ValidationError as exception:
            return exception.messages, 400
        except KeyError as exception:
            return str(exception), 404
        return self.schema.dump(employee), 201

    def delete(self, uuid):
        try:
            return self.service.delete_employee(uuid), 204
        except KeyError as exception:
            return str(exception), 404


def parse_date(date_str):
    try:
        return datetime.date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


class EmployeeSearchApi(Resource, BaseEmployeeApi):
    parser = reqparse.RequestParser()
    parser.add_argument("start_date")
    parser.add_argument("end_date")

    def get(self):
        args = self.parser.parse_args()
        start_date = parse_date(args["start_date"])
        end_date = parse_date(args["end_date"])

        if start_date or end_date:
            employees = self.service.get_employees_born_in_period(
                start_date, end_date)
        else:
            employees = self.service.get_employees()

        return self.schema.dump(employees, many=True), 200
