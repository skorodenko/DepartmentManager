
from flask import render_template, redirect

from department_app import app


def init_departments_view():

    @app.route("/")
    def root():
        return redirect("/departments")

    @app.route("/departments")
    def departments():
        return render_template("departments.html")

    @app.route("/department/<uuid>")
    def department(uuid=None):
        return render_template("department.html", department_uuid=uuid)
