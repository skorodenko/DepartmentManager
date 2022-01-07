from setuptools import setup, find_packages

setup(
    name="Department Manager",
    version="1.0",
    author="Skorodenko Dmytro",
    author_email="mskorodenko@gmail.com",
    description="Web application to manage departments and employees",
    url="https://github.com/skorodenko/DepartmentManager",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    requires=[
        "Flask==2.0.2",
        "Flask_SQLAlchemy==2.5.1",
        "Flask-RESTful==0.3.9",
        "Flask_Migrate==3.1.0",
        "mysql-connector-python==8.0.27",
    ]
)