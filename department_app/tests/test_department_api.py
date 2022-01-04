
from http import HTTPStatus


def test_get_departments(app_client, department_schema, rest_api, data_1):
    expected_response = [department_schema.dump(
        dep) for dep in data_1["departments"]]

    response = app_client.get("/rest/departments")

    assert response.status_code == HTTPStatus.OK
    assert expected_response == response.json


def test_get_department_success(app_client, department_schema, rest_api, data_1):
    expected_response = data_1["departments"][0]

    response = app_client.get("/rest/department/"+expected_response.uuid)

    assert response.status_code == HTTPStatus.OK
    assert department_schema.dump(expected_response) == response.json


def test_get_department_failure(app_client, rest_api):

    response = app_client.get("/rest/department/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_post_department_success(app_client, department_schema, rest_api, data_1):
    from department_app.models.department import Department

    expected_result = Department("New Department")

    response_1 = app_client.post("/rest/departments", data=department_schema.dumps(
        expected_result), content_type="application/json")

    response_2 = app_client.get("/rest/department/" + expected_result.uuid)

    assert response_1.status_code == HTTPStatus.CREATED
    assert department_schema.dump(expected_result) == response_2.json


def test_post_department_failure(app_client, department_schema, rest_api, data_1):
    from department_app.models.department import Department

    expected_result = Department("Department of IT development")

    response = app_client.post(
        "/rest/departments", data=department_schema.dump(expected_result))

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_put_department_success(app_client, department_schema, rest_api, data_1):

    expected_result = "Changed name"
    dep = data_1["departments"][2]
    dep.name = expected_result

    response = app_client.put("/rest/department/"+dep.uuid,
                              data=department_schema.dumps(dep), content_type="application/json")

    assert response.status_code == HTTPStatus.CREATED

    response = app_client.get("/rest/department/"+dep.uuid)

    assert department_schema.dump(dep) == response.json


def test_put_department_failure(app_client, department_schema, rest_api, data_1):

    expected_result = "Changed name"
    dep = data_1["departments"][2]
    dep.name = expected_result

    response = app_client.put(
        "/rest/department/"+dep.uuid, data=department_schema.dump(dep))

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_department_success(app_client, rest_api, data_1):

    expected_deletion = data_1["departments"][1]

    response = app_client.delete("/rest/department/" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NO_CONTENT

    response = app_client.get("/rest/department" + expected_deletion.uuid)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_department_failure(app_client, rest_api, data_1):

    response = app_client.delete("/rest/department/random_stuff")

    assert response.status_code == HTTPStatus.NOT_FOUND
