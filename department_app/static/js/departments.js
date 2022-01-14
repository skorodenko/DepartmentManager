let SUBMIT_ADD_DEPARTMENT = "modal-add-department"
let ADD_DEPARTMENT_DEPARTMENT_NAME = "modal-add-department-department-name"


$(document).ready(function () {
    fetch("/rest/departments")
        .then((response) => response.json())
        .then((departments) => {
            initDepartmentsTable(departments);
            initForms();
        })
        .catch((err) => {
            console.log(err);
        });
});


function initForms() {
    document.getElementById(SUBMIT_ADD_DEPARTMENT).addEventListener("click", addDepartment)
}


function addDepartment() {
    let data = {
        name: document.getElementById(ADD_DEPARTMENT_DEPARTMENT_NAME).value,
    }

    fetchWithAlert(
        "/rest/departments",
        "POST",
        "Failed to add department",
        data
    )
}


function initDepartmentsTable(departments) {

    let atomic_department_base_url = "/department/"
    $("#departments-table tbody").empty();

    for (let i = 0; i < departments.length; i++) {
        let department = departments[i]

        $("#departments-table tbody").append(
           `<tr>
            <th scope="row">${department.uuid}</th>
            <td>${department.name}</td>
            <td>${department.average_salary}</td>
            <td>
                <a href="${atomic_department_base_url+department.uuid}">
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