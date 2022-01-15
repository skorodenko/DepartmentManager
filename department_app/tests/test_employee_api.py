
from http import HTTPStatus


def test_get_employees(app_client, db_setup, db_schemas, data_1):
    expected_response = db_schemas.Employee(
        many=True).dump(data_1["employees"])

    response = app_client.get("/rest/employees")

    assert response.status_code == HTTPStatus.OK
    assert expected_response == response.json


def test_get_employee_success(app_client, db_setup, db_schemas, data_1):
    expected_response = data_1["employees"][0]

    response = app_client.get("/rest/employee/"+expected_response.uuid)

    assert response.status_code == HTTPStatus.OK
    assert db_schemas.Employee().dump(expected_response) == response.json


def test_get_employee_failure(app_client, data_1):

    response = app_client.get("/rest/employee/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_post_employee_success(app_client, db_setup, db_schemas, data_1):
    expected_department = data_1["departments"][0]
    expexted_result = {"name": "POST employee", "date_of_birth": "1971-3-4",
                       "salary": "1000", "department": {"uuid": expected_department.uuid,
                                                        "name": expected_department.name}}
    response = app_client.post("/rest/employees", json=expexted_result)

    assert response.status_code == HTTPStatus.CREATED


def test_post_employee_failure(app_client, db_setup, db_schemas, data_1):
    expexted_result = {"name": "POST employee", "date_of_birth": "1971-3-4",
                       "salary": "1000", "department": {"uuid": "random_uuid",
                                                        "name": "random_name"}}

    response = app_client.post(
        "/rest/employees", json=expexted_result)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_put_employee_success(app_client, db_setup, db_schemas, data_1):
	expected_result = "Changed name"
	empl = data_1["employees"][0]
	empl.name = expected_result

	response = app_client.put("/rest/employee/"+empl.uuid,
							  data=db_schemas.Employee().dumps(empl), content_type="application/json")

	assert response.status_code == HTTPStatus.CREATED

	response = app_client.get("/rest/employee/"+empl.uuid)

	assert db_schemas.Employee().dump(empl) == response.json


def test_put_employee_failure(app_client, db_setup, db_schemas, data_1):
    expected_result = "Changed name"
    empl = data_1["employees"][0]
    empl.name = expected_result

    response = app_client.put("/rest/employee/"+empl.uuid,
                              data=db_schemas.Employee().dump(empl), content_type="application/json")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_employee_success(app_client, data_1):
    expected_deletion = data_1["employees"][2]

    response = app_client.delete("/rest/employee/" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NO_CONTENT

    response = app_client.get("/rest/employee/" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_department_failure(app_client, data_1):

    response = app_client.delete("/rest/department/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND
