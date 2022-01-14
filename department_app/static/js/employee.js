let SUBMIT_EDIT_EMPLOYEE = "modal-edit-employee"

let EDIT_EMPLOYEE_NAME = "edit-employee-name"
let EDIT_EMPLOYEE_DEPARTMENT_SELECT = "edit-employee-department-select"
let EDIT_EMPLOYEE_DATE_OF_BIRTH = "edit-employee-date-of-birth"
let EDIT_EMPLOYEE_SALARY = "edit-employee-salary"

let SUBMIT_DELETE_EMPLOYEE = "modal-delete-employee"


$(document).ready(function () {
    fetch("/rest/employee/"+employee_uuid)
        .then((response) => response.json())
        .then((employee) => {
            initAtomicEmployee(employee);
        })
        .catch((err) => {
            console.log(err);
        });
});


function initAtomicEmployee(employee) {
    $("#name").append(employee.name)
    fetch("/rest/department/"+employee.department_uuid)
        .then(response => response.json())
        .then(department => {
            $("#department-name").append(department.name)
            $("#edit-employee-department-select").append(
                `<option selected disabled hidden value="${department.uuid}">${department.name}</option>`
                )})
    $("#date-of-birth").append(employee.date_of_birth)
    $("#salary").append(employee.salary)

    document.getElementById(EDIT_EMPLOYEE_NAME).placeholder = employee.name
    document.getElementById(EDIT_EMPLOYEE_DATE_OF_BIRTH).placeholder = employee.date_of_birth
    document.getElementById(EDIT_EMPLOYEE_SALARY).placeholder = employee.salary
    document.getElementById(SUBMIT_EDIT_EMPLOYEE).addEventListener("click", editEmployee)
    document.getElementById(SUBMIT_DELETE_EMPLOYEE).addEventListener("click", deleteEmployee)
    fetch("/rest/departments")
        .then( response => response.json() )
        .then( departments => initEditEmployeeModal(departments) )

    $("#edit-employee-date-of-birth").datepicker({
        keyboardNavigation: false,
        format: "yyyy-mm-dd",
        clearBtn: true,
        autoclose: true
    });
}


function initEditEmployeeModal(departments) {

    for (let i = 0; i < departments.length; i++) {
        let department = departments[i]

        $("#edit-employee-department-select").append(
            `<option value="${department.uuid}">${department.name}</option>`
        )
    }

}


function editEmployee() {

    let new_name = document.getElementById(EDIT_EMPLOYEE_NAME).value
    let old_name = document.getElementById(EDIT_EMPLOYEE_NAME).placeholder

    let new_department_uuid = document.getElementById(EDIT_EMPLOYEE_DEPARTMENT_SELECT).value
    let old_department_uuid = document.getElementById(EDIT_EMPLOYEE_DEPARTMENT_SELECT).placeholder

    let new_date_of_birth = document.getElementById(EDIT_EMPLOYEE_DATE_OF_BIRTH).value
    let old_date_of_birth = document.getElementById(EDIT_EMPLOYEE_DATE_OF_BIRTH).placeholder

    let new_salary = document.getElementById(EDIT_EMPLOYEE_SALARY).value
    let old_salary = document.getElementById(EDIT_EMPLOYEE_SALARY).placeholder

    let data = {
        name: new_name ? new_name : old_name,
        department_uuid: new_department_uuid ? new_department_uuid : old_department_uuid,
        date_of_birth: new_date_of_birth ? new_date_of_birth : old_date_of_birth,
        salary: new_salary ? new_salary : old_salary,
    }

    fetchWithAlert(
        "/rest/employee/"+employee_uuid,
        "PUT",
        "Failed to edit employee",
        data
    )
}


function deleteEmployee() {
    fetchWithAlert(
        "/rest/employee/"+employee_uuid,
        "DELETE",
        "Failed to delete employee",
    )
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
        .then((employee) => {
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