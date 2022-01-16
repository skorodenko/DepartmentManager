"""
Employee REST API

Classes:
    - BaseEmployeeApi => base class for REST API
    - ListAllEMployeesApi => employee list api class
    - AtomicEmployeeApi => atomic employee api class
    - EmployeeSearchApi => employee search api class
"""
import datetime
from flask import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from department_app.service.employee import EmployeeService
from department_app.schemas.employee import EmployeeSchema


class BaseEmployeeApi:
    """
    Employee REST API base class
    """
    service = EmployeeService
    schema = EmployeeSchema()


class ListAllEmployeesApi(Resource, BaseEmployeeApi):
    """
    Employee REST API to work with list of employees
    """
    def get(self):
        """
        GET request handler

        Fetches all employees in JSON format with satus code 200(OK)
        """
        employees = self.service.get_employees()
        return self.schema.dump(employees, many=True), 200

    def post(self):
        """
        POST request handler

        Deserializes request data and adds employee using employee service

        Returns:
            - added employee with satus code 201(CREATED) 
                if operation succeeded

            - error message with status code 400(BAD REQUEST) 
                in case of validation error
        """
        try:
            employee = self.service.add_employee(self.schema, request.json)
        except ValidationError as exception:
            return exception.messages, 400
        return self.schema.dump(employee), 201


class AtomicEmployeeApi(Resource, BaseEmployeeApi):
    """
    Atomic employee REST API to work with particular employee
    """
    def get(self, uuid):
        """
        GET request handler

        Fetches employee with specified uuid

        Returns:
            - requested employee with status code 200(OK)
                if operation succeeded

            - error message with status code 404(NOT FOUND)
                in case of bad uuid
        """
        try:
            employee = self.service.get_employee_with_uuid(uuid)
        except KeyError as exception:
            return str(exception), 404
        return self.schema.dump(employee), 200

    def put(self, uuid):
        """
        PUT request handler

        Updates employee with specified uuid

        Returns:
            - updated employee with status code 201(CREATED)
                if operation succeeded
            
            - error message with status code 400(BAD REQUEST)
                in case of validation error
            
            - error message with status code 404(NOT FOUND)
                in case of bad uuid
        """
        try:
            employee = self.service.update_employee(
                self.schema, uuid, request.json)
        except ValidationError as exception:
            return exception.messages, 400
        except KeyError as exception:
            return str(exception), 404
        return self.schema.dump(employee), 201

    def delete(self, uuid):
        """
        DELETE request handler

        Deletes employee with specified uuid

        Returns:
            - status code 204(NO CONTENT)
                if operation succeeded
            
            - error message with status code 404(NOT FOUND)
                in case of bad uuid
        """
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
    """
    Employee search REST API to search for employees
        born in specified period or date.
    """
    parser = reqparse.RequestParser()
    parser.add_argument("start_date")
    parser.add_argument("end_date")

    def get(self):
        """
        GET request handler

        Fetches all employees born in specified period
            or date(when start/end date are the same)
        
        Returns:
            - suitable employees with status code 200(OK)
        """
        args = self.parser.parse_args()
        start_date = parse_date(args["start_date"])
        end_date = parse_date(args["end_date"])

        if start_date or end_date:
            employees = self.service.get_employees_born_in_period(
                start_date, end_date)
        else:
            employees = self.service.get_employees()

        return self.schema.dump(employees, many=True), 200
