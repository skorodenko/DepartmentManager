let SUBMIT_ADD_EMPLOYEE = "modal-add-employee"

let ADD_EMPLOYEE_NAME = "add-employee-name"
let ADD_EMPLOYEE_DEPARTMENT_SELECT = "add-employee-department-select"
let ADD_EMPLOYEE_DATE_OF_BIRTH = "add-employee-date-of-birth"
let ADD_EMPLOYEE_SALARY = "add-employee-salary"

let DATEPICKER_START = "datepicker-start"
let DATEPICKER_END = "datepicker-end"


$(document).ready(function () {
    fetch("/rest/employees")
        .then((response) => response.json())
        .then((employees) => {
            initEmployeesTable(employees);
            initForms();
        })
        .catch((err) => {
            console.log(err);
        });
});


function initForms() {
    document.getElementById(SUBMIT_ADD_EMPLOYEE).addEventListener("click", addEmployee)
    fetch("/rest/departments")
        .then( response => response.json() )
        .then( departments => initAddEmployeeModal(departments) )
    $("#datepicker").datepicker({
        keyboardNavigation: false,
        format: "yyyy-mm-dd",
        clearBtn: true,
        autoclose: true
    });
    $("#add-employee-date-of-birth").datepicker({
        keyboardNavigation: false,
        format: "yyyy-mm-dd",
        clearBtn: true,
        autoclose: true
    });
}


function addEmployee() {
    let data = {
        name: document.getElementById(ADD_EMPLOYEE_NAME).value,
        date_of_birth: document.getElementById(ADD_EMPLOYEE_DATE_OF_BIRTH).value,
        salary: document.getElementById(ADD_EMPLOYEE_SALARY).value,
        department: {
            uuid: document.getElementById(ADD_EMPLOYEE_DEPARTMENT_SELECT).value,
        },
    }

    fetchWithAlert(
        "/rest/employees",
        "POST",
        "Failed to add employee",
        data
    )
}


function initAddEmployeeModal(departments) {
    
    for (let i = 0; i < departments.length; i++) {
        let department = departments[i]

        $("#add-employee-department-select").append(
            `<option value="${department.uuid}">${department.name}</option>`
        )
    }

}


function initEmployeesTable(employees) {

    let atomic_employee_base_url = "/employee/"
    $("#employees-table tbody").empty();

    for (let i = 0; i < employees.length; i++) {
        let employee = employees[i]
        
        $("#employees-table tbody").append(
            `<tr>
            <th scope="row">${employee.uuid}</th>
            <td>${employee.department.name}</td>
            <td>${employee.name}</td>
            <td>${employee.date_of_birth}</td>
            <td>${employee.salary}</td>
            <td>
                <a href="${atomic_employee_base_url+employee.uuid}">
                    <i class="bi bi-info-circle"></i>
                </a>
            </td>
            </tr>`);

    }
}


function searchByDate() {
    fetch(`/rest/employees/search?start_date=${document.getElementById(DATEPICKER_START).value}&end_date=${document.getElementById(DATEPICKER_END).value}`)
        .then(response => response.json())
        .then(employees => initEmployeesTable(employees));
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