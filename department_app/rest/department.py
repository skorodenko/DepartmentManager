"""
Department REST API

Classes:
    - BaseDepartmentApi => base class for REST API
    - ListDepartmentApi => department list api class
    - AtomicDeparmtnetApi => atomic department api class
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from department_app.service.department import DepartmentService
from department_app.service.employee import EmployeeService
from department_app.schemas.department import DepartmentSchema


class BaseDepartmentApi:
    """
    Department REST API base class
    """
    service = DepartmentService
    employee_service = EmployeeService
    schema = DepartmentSchema()


class ListDepartmentApi(Resource, BaseDepartmentApi):
    """
    Department REST API to work with list of departments
    """

    def get(self):
        """
        GET request handler

        Fetches all departments in JSON format with satus code 200(OK)
        """
        departments = self.service.get_departments()
        return self.schema.dump(departments, many=True), 200

    def post(self):
        """
        POST request handler

        Deserializes request data and adds department using department service

        Returns:
            - added department with satus code 201(CREATED) 
                if operation succeeded

            - error message with status code 400(BAD REQUEST) 
                in case of validation error
                in case of duplicate department name
        """
        try:
            department = self.service.add_department(
                self.schema, request.json)
        except ValidationError as exception:
            return exception.messages, 400
        except IntegrityError:
            return "Duplicate department name", 400
        return self.schema.dump(department), 201


class AtomicDepartmentApi(Resource, BaseDepartmentApi):
    """
    Atomic department REST API to work with particular department
    """
    def get(self, uuid):
        """
        GET request handler

        Fetches department with specified uuid

        Returns:
            - requested department with status code 200(OK)
                if operation succeeded

            - error message with status code 404(NOT FOUND)
                in case of bad uuid
        """
        try:
            department = self.service.get_department_with_uuid(uuid)
        except KeyError as exception:
            return str(exception), 404
        return self.schema.dump(department), 200

    def put(self, uuid):
        """
        PUT request handler

        Updates department with specified uuid

        Returns:
            - updated department with status code 201(CREATED)
                if operation succeeded
            
            - error message with status code 400(BAD REQUEST)
                in case of validation error
                in case of duplicate department name
            
            - error message with status code 404(NOT FOUND)
                in case of bad uuid
        """
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
        """
        DELETE request handler

        Deletes department(and all its employees) with specified uuid

        Returns:
            - status code 204(NO CONTENT)
                if operation succeeded
            
            - error message with status code 404(NOT FOUND)
                in case of bad uuid
        """
        try:
            return self.service.delete_department(uuid), 204
        except KeyError as exception:
            return str(exception), 404
