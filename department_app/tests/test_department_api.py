
from http import HTTPStatus


def test_get_departments(app_client, db_setup, db_schemas, data_1):
    expected_response = db_schemas.Department(
        many=True).dump(data_1["departments"])

    response = app_client.get("/rest/departments")

    assert response.status_code == HTTPStatus.OK
    assert expected_response == response.json


def test_get_department_success(app_client, db_setup, db_schemas, data_1):
    expected_response = data_1["departments"][0]

    response = app_client.get("/rest/department/"+expected_response.uuid)

    assert response.status_code == HTTPStatus.OK
    assert db_schemas.Department().dump(expected_response) == response.json


def test_get_department_failure(app_client, data_1):

    response = app_client.get("/rest/department/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_post_department_success(app_client, db_setup, db_schemas, data_1):
    expected_result = {"name": "POST department"}

    response = app_client.post("/rest/departments", json=expected_result)

    assert response.status_code == HTTPStatus.CREATED


def test_post_department_failure(app_client, db_setup, db_schemas, data_1):
    expected_result = {"name": None}

    response = app_client.post(
        "/rest/departments", json=expected_result)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_put_department_success(app_client, db_setup, db_schemas, data_1):
    expected_result = "Changed name"
    dep = data_1["departments"][1]
    dep.name = expected_result

    response = app_client.put("/rest/department/"+dep.uuid,
                              data=db_schemas.Department().dumps(dep), content_type="application/json")

    assert response.status_code == HTTPStatus.CREATED

    response = app_client.get("/rest/department/"+dep.uuid)

    assert db_schemas.Department().dump(dep) == response.json


def test_put_department_failure(app_client, db_setup, db_schemas, data_1):
    expected_result = "Changed name"
    dep = data_1["departments"][1]
    dep.name = expected_result

    response = app_client.put(
        "/rest/department/"+dep.uuid, data=db_schemas.Department().dump(dep))

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_department_success(app_client, data_1):
    expected_deletion = data_1["departments"][2]

    response = app_client.delete("/rest/department/" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NO_CONTENT

    response = app_client.get("/rest/department/" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_department_failure(app_client, data_1):

    response = app_client.delete("/rest/department/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND
