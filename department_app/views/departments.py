
from flask import render_template, redirect


def init_departments_view(app):

    @app.route("/")
    def root():
        return redirect("/departments")

    @app.route("/departments")
    def departments():
        return render_template("departments.html")

    @app.route("/department/<uuid>")
    def department(uuid=None):
        return render_template("department.html", department_uuid=uuid)
