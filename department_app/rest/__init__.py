
def init_rest(api):
    from department_app.rest import department
    from department_app.rest import employee

    api.add_resource(department.ListDepartmentApi, "/rest/departments")

    api.add_resource(department.AtomicDepartmentApi, "/rest/department/<uuid>")

    api.add_resource(employee.ListAllEmployeesApi, "/rest/employees")

    api.add_resource(employee.AtomicEmployeeApi, "/rest/employee/<uuid>")
