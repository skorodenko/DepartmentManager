
from http import HTTPStatus


def test_departments(app_client, views):
    response = app_client.get("/departments")
    assert response.status_code == HTTPStatus.OK


def test_department(app_client, views, data_1):
    department_uuid = data_1["departments"][0].uuid
    response = app_client.get("/department/" + department_uuid)
    assert response.status_code == HTTPStatus.OK
