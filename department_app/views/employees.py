"""
Employee views used to manage employees
"""

from flask import render_template

from department_app import app


def init_employees_view():
    """
    Init employee views
    """
    @app.route("/employees")
    def employees():
        """
        Render employees page
        """
        return render_template("employees.html")

    @app.route("/employee/<uuid>")
    def employee(uuid=None):
        """
        Render employee page
        """
        return render_template("employee.html", employee_uuid=uuid)
