

from flask import render_template

from department_app import app


def init_employees_view():

    @app.route("/employees")
    def employees():
        return render_template("employees.html")

    @app.route("/employee/<uuid>")
    def employee(uuid=None):
        return render_template("employee.html", employee_uuid=uuid)
