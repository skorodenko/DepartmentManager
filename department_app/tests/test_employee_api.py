
from datetime import datetime
from http import HTTPStatus


def test_get_employees(app_client, db_setup, db_schemas, rest_api, data_1):
    expected_response = db_schemas.Employee(many=True).dump(data_1["employees"])

    response = app_client.get("/rest/employees")

    assert response.status_code == HTTPStatus.OK
    assert expected_response == response.json


def test_get_employee_success(app_client, db_setup, db_schemas, rest_api, data_1):
    expected_response = data_1["employees"][0]

    response = app_client.get("/rest/employee/"+expected_response.uuid)

    assert response.status_code == HTTPStatus.OK
    assert db_schemas.Employee().dump(expected_response) == response.json


def test_get_employee_failure(app_client, rest_api):

    response = app_client.get("/rest/employee/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_post_employee_success(app_client, db_setup, db_schemas, rest_api, data_1):
    from datetime import datetime
    expected_department = data_1["departments"][0]
    expected_result = db_setup.Employee("New Employee", datetime(1971, 3, 4), 1000)
    expected_result.department_uuid = expected_department.uuid

    response_1 = app_client.post("/rest/employees", data=db_schemas.Employee().dumps(expected_result),
                                 content_type="application/json")

    response_2 = app_client.get("/rest/employee/" + expected_result.uuid)
    
    assert response_1.status_code == HTTPStatus.CREATED
    assert db_schemas.Employee().dump(expected_result) == response_2.json


def test_post_employee_failure(app_client, db_setup, db_schemas, rest_api, data_1):
    from datetime import datetime
    expected_result = db_setup.Employee("New Employee", datetime(2000,3,4), 0)

    response = app_client.post(
        "/rest/employees", data=db_schemas.Employee().dump(expected_result))

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_put_department_success(app_client, db_setup, db_schemas, rest_api, data_1):
    expected_result = "Changed name"
    empl = data_1["employees"][0]
    empl.name = expected_result

    response = app_client.put("/rest/employee/"+empl.uuid,
                              data=db_schemas.Employee().dumps(empl), content_type="application/json")

    print(response.json)
    assert response.status_code == HTTPStatus.CREATED

    response = app_client.get("/rest/employee/"+empl.uuid)

    assert db_schemas.Employee().dump(empl) == response.json

"""
def test_put_department_failure(app_client, db_setup, db_schemas, rest_api, data_1):
    expected_result = "Changed name"
    dep = data_1["departments"][1]
    dep.name = expected_result

    response = app_client.put(
        "/rest/department/"+dep.uuid, data=db_schemas.Department().dump(dep))

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_department_success(app_client, rest_api, data_1):
    expected_deletion = data_1["departments"][2]

    response = app_client.delete("/rest/department/" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NO_CONTENT

    response = app_client.get("/rest/department" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_department_failure(app_client, rest_api, data_1):

    response = app_client.delete("/rest/department/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND
"""
