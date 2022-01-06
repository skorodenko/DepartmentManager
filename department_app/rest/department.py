from flask import request
from flask_restful import Resource
from marshmallow import ValidationError


def init_department_rest(api, department_service, employeeService, department_schema):
    class BaseDepartmentApi:
        service = department_service
        employee_service = employeeService
        schema = department_schema()
    
    
    class ListDepartmentApi(Resource, BaseDepartmentApi):
    
        def get(self):
            departments = self.service.get_departments()
            return self.schema.dump(departments, many=True), 200
    
        def post(self):
            try:
                department = self.service.add_department(self.schema, request.json)
            except ValidationError as e:
                return e.messages, 400
            return self.schema.dump(department), 201
    
    
    class AtomicDepartmentApi(Resource, BaseDepartmentApi):
    
        def get(self, uuid):
            try:
                department = self.service.get_department_with_uuid(uuid)
            except KeyError as e:
                return str(e), 404
            return self.schema.dump(department), 200
    
        def put(self, uuid):
            try:
                department = self.service.update_department(
                    self.schema, uuid, request.json)
            except ValidationError as e:
                return e.messages, 400
            except KeyError as e:
                return str(e), 404
            return self.schema.dump(department), 201
    
        def delete(self, uuid):
            try:
                return self.service.delete_department(uuid), 204
            except KeyError as e:
                return str(e), 404
    
    
    api.add_resource(ListDepartmentApi, "/rest/departments")
    api.add_resource(AtomicDepartmentApi, "/rest/department/<uuid>")
