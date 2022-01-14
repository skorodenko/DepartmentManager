

from flask import render_template


def init_employees_view(app):

    @app.route("/employees")
    def employees():
        return render_template("employees.html")

    @app.route("/employee/<uuid>")
    def employee(uuid=None):
        return render_template("employee.html", employee_uuid=uuid)
