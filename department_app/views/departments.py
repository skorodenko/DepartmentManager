"""
Department views used to manage departments
"""
from flask import render_template, redirect

from department_app import app


def init_departments_view():
    """
    Initialize department views
    """
    @app.route("/")
    def root():
        """
        Redirect from / to /departments.
        """
        return redirect("/departments")

    @app.route("/departments")
    def departments():
        """
        Render departments page
        """
        return render_template("departments.html")

    @app.route("/department/<uuid>")
    def department(uuid=None):
        """
        Render department page
        """
        return render_template("department.html", department_uuid=uuid)
