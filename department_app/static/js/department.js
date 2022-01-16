let SUBMIT_EDIT_DEPARTMENT = "modal-edit-department"
let EDIT_DEPARTMENT_DEPARTMENT_NAME = "modal-edit-department-department-name"

let SUBMIT_DELETE_DEPARTMENT = "modal-delete-department"


$(document).ready(function () {
    fetch("/rest/department/"+department_uuid)
        .then((response) => response.json())
        .then((department) => {
            initAtomicDepartment(department);
            initEmployeesTable(department.employees);
        })
        .catch((err) => {
            console.log(err);
        });
});


function initAtomicDepartment(department) {
    $("#department-name").append(
        `<h3>${department.name}</h3>`
    )
    document.getElementById(EDIT_DEPARTMENT_DEPARTMENT_NAME).placeholder = department.name
    document.getElementById(SUBMIT_EDIT_DEPARTMENT).addEventListener("click", editDepartment)
    document.getElementById(SUBMIT_DELETE_DEPARTMENT).addEventListener("click", deleteDepartment)
}


function editDepartment() {

    let old_name = document.getElementById(EDIT_DEPARTMENT_DEPARTMENT_NAME).placeholder
    let new_name = document.getElementById(EDIT_DEPARTMENT_DEPARTMENT_NAME).value

    let data = {
        name: new_name ? new_name : old_name,
    }

    fetchWithAlert(
        "/rest/department/"+department_uuid,
        "PUT",
        "Failed to edit department",
        data
    )
}


function deleteDepartment() {
    fetchWithAlert(
        "/rest/department/"+department_uuid,
        "DELETE",
        "Failed to delete department",
    )
}


function initEmployeesTable(employees) {

    let atomic_employee_base_url = "/employee/"

    for (let i = 0; i < employees.length; i++) {
        let employee = employees[i]

        $("#department-employees-table tbody").append(
           `<tr>
            <th scope="row">${employee.uuid}</th>
            <td>${employee.name}</td>
            <td>${employee.date_of_birth}</td>
            <td>${employee.salary}</td>
            <td>
                <a href="${atomic_employee_base_url+employee.uuid}">
                    <i class="bi bi-info-circle"></i>
                </a>
            </td>
            </tr>`
        );
    }
}


function fetchWithAlert(url, method, failureMessage, data = {}) {
    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(checkStatus)
      .then((response) => {
            if (response.status === 204) {
                history.back();
                return response;
            }
            return response.json()
        })
        .then((department) => {
            document.location.reload();
        })
        .catch((err) => {
            console.log(err);
            alert_failure(failureMessage, false);
        });
}

function checkStatus(response) {
    if (response.ok) {
        return Promise.resolve(response);
    } else {
        return Promise.reject(new Error(response.statusText));
    }
}

function alert_failure(message) {
    $("#alert-message").empty()
    $("#alert-message").append(message)
    $("#alert-failure").modal("show")
}