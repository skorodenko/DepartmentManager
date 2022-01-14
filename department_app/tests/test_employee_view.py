

from http import HTTPStatus


def test_departments(app_client, views):
    response = app_client.get("/employees")
    assert response.status_code == HTTPStatus.OK


def test_department(app_client, views, data_1):
    employee_uuid = data_1["employees"][0].uuid
    response = app_client.get("/employee/" + employee_uuid)
    assert response.status_code == HTTPStatus.OK
