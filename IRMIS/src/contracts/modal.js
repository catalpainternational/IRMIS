import "bootstrap/js/dist/modal";
import $ from "jquery";

const csrftoken = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");

const deleteLink = document.getElementsByClassName("delete-link");
const deleteAlert = $(".delete-modal");
const discardLink = document.getElementsByClassName("discard-link");
const discardAlert = $(".discard-modal");
const formModalLink = document.getElementsByClassName("form-modal-link");
const inspectionFormModal = $(".inspection-modal");
const paymentFormModal = $(".payment-modal");
const socialDataFormModal = $(".social-data-modal");

let deleteUrl;
let backUrl;
let requestMethod;
let requestData;
let requestId;

deleteLink.forEach(link => {
    link.addEventListener("click", () => {
        deleteUrl = link.dataset.delete;
        deleteAlert.modal('show');
    });
});

discardLink.forEach(link => {
    link.addEventListener("click", () => {
        backUrl = link.dataset.back;
        discardAlert.modal('show');
    });
});

formModalLink.forEach(link => {
    link.addEventListener("click", () => {
        requestMethod = link.dataset.method;
        requestData = link.dataset.object;
        requestId = link.dataset.id;

        if (inspectionFormModal.length) inspectionFormModal.modal('show');
        else if (paymentFormModal.length) paymentFormModal.modal('show');
        else if (socialDataFormModal.length) socialDataFormModal.modal('show');
    });
});

deleteAlert.on('shown.bs.modal', () => {
    document.getElementsByClassName("delete-item").item(0).addEventListener("click", () => {
        fetch(deleteUrl, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrftoken
            },
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    });
});

discardAlert.on('shown.bs.modal', () => {
    document.getElementsByClassName("discard-changes").item(0).addEventListener("click", () => {
        location.href = backUrl;
    });
});

inspectionFormModal.on('show.bs.modal', () => {
    const dateInput = document.getElementById("inpection-date");
    const entitySelect = document.getElementById("inpection-entity");
    const progressInput = document.getElementById("physical-progress");
    const defectLiabilityPeriod = document.getElementById("defect-liability");
    const today = new Date().toISOString().substring(0, 10);

    dateInput.max = today;

    if (requestData) {
        const parsedData = JSON.parse(requestData);

        dateInput.value = parsedData.date;
        entitySelect.value = parsedData.entity;
        progressInput.value = parsedData.progress;
        defectLiabilityPeriod.checked = parsedData.defect_liability_period;
    } else {
        dateInput.value = today;
        entitySelect.value = 1;
        progressInput.value = 0;
        defectLiabilityPeriod.checked = false;
    }
});

inspectionFormModal.on('shown.bs.modal', () => {
    document.getElementById("save-inspection").addEventListener("click", (e) => {
        const data = {
            date: document.getElementById("inpection-date").value,
            progress: parseInt(document.getElementById("physical-progress").value, 10),
            entity: parseInt(document.getElementById("inpection-entity").value, 10),
            defect_liability_period: document.getElementById("defect-liability").checked,
            contract: parseInt(e.target.dataset.id, 10),
        };

        fetch(requestId ? e.target.dataset.url + requestId + "/" : e.target.dataset.url, {
            method: requestMethod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data),
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    });
});

paymentFormModal.on('show.bs.modal', () => {
    const dateInput = document.getElementById("payment-date");
    const valueInput = document.getElementById("payment-value");
    const donorSelect = document.getElementById("payment-donor");
    const sourceSelect = document.getElementById("payment-source");
    const destinationSelect = document.getElementById("payment-destination");
    const today = new Date().toISOString().substring(0, 10);

    dateInput.max = today;

    if (requestData) {
        const parsedData = JSON.parse(requestData);

        dateInput.value = parsedData.date;
        valueInput.value = parsedData.value;
        donorSelect.value = parsedData.donor;
        sourceSelect.value = parsedData.source;
        destinationSelect.value = parsedData.destination;
    } else {
        dateInput.value = today;
        valueInput.value = 0;
        donorSelect.value = 0;
        sourceSelect.value = 1;
        destinationSelect.value = 1;
    }
});

paymentFormModal.on('shown.bs.modal', () => {
    document.getElementById("save-payment").addEventListener("click", (e) => {
        const data = {
            date: document.getElementById("payment-date").value,
            value: parseInt(document.getElementById("payment-value").value, 10),
            donor: parseInt(document.getElementById("payment-donor").value, 10),
            source: parseInt(document.getElementById("payment-source").value, 10),
            destination: parseInt(document.getElementById("payment-destination").value, 10),
            contract: parseInt(e.target.dataset.id, 10),
        };

        fetch(requestId ? e.target.dataset.url + requestId + "/" : e.target.dataset.url, {
            method: requestMethod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data),
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    });
});

socialDataFormModal.on('show.bs.modal', () => {
    const reportingMonthInput = document.getElementById("reporting-month");
    const totalEmployees = document.getElementById("total-employees");
    const nationalEmployees = document.getElementById("national-employees");
    const internationalEmployees = document.getElementById("international-employees");
    const femaleEmployees = document.getElementById("female-employees");
    const employeesDisabilities = document.getElementById("employees-disabilities");
    const femaleEmployeesDisabilities = document.getElementById("female-employees-disabilities");
    const youngEmployees = document.getElementById("young-employees");
    const youngFemaleEmployees = document.getElementById("young-female-employees");
    const totalWorkedDays = document.getElementById("total-worked-days");
    const femaleEmployeesWorkedDays = document.getElementById("female-employees-worked-days");
    const employeesDisabilitiesWorkedDays = document.getElementById("employees-disabilities-worked-days");
    const femaleEmployeesDisabilitiesWorkedDays = document.getElementById("female-employees-disabilities-worked-days");
    const youngEmployeesWorkedDays = document.getElementById("young-employees-worked-days");
    const youngFemaleEmployeesWorkedDays = document.getElementById("young-female-employees-worked-days");
    const totalWages = document.getElementById("total-wages");
    const averageGrossWages = document.getElementById("average-gross-wages");
    const averageNetWages = document.getElementById("average-net-wages");
    const today = new Date().toISOString().substring(0, 7);

    reportingMonthInput.max = today;

    if (requestData) {
        const parsedData = JSON.parse(requestData);
        const month = parsedData.month < 10 ? "0" + parsedData.month : parsedData.month

        reportingMonthInput.value = parsedData.year + "-" + month;
        totalEmployees.value = parsedData.employees;
        nationalEmployees.value = parsedData.national_employees;
        internationalEmployees.value = parsedData.international_employees;
        femaleEmployees.value = parsedData.female_employees;
        employeesDisabilities.value = parsedData.employees_with_disabilities;
        femaleEmployeesDisabilities.value = parsedData.female_employees_with_disabilities;
        youngEmployees.value = parsedData.young_employees;
        youngFemaleEmployees.value = parsedData.young_female_employees;
        totalWorkedDays.value = parsedData.total_worked_days;
        femaleEmployeesWorkedDays.value = parsedData.female_employees_worked_days;
        employeesDisabilitiesWorkedDays.value = parsedData.employees_with_disabilities_worked_days;
        femaleEmployeesDisabilitiesWorkedDays.value = parsedData.female_employees_with_disabilities_worked_days;
        youngEmployeesWorkedDays.value = parsedData.young_employees_worked_days;
        youngFemaleEmployeesWorkedDays.value = parsedData.young_female_employees_worked_days;
        totalWages.value = parsedData.total_wage;
        averageGrossWages.value = parsedData.average_gross_wage;
        averageNetWages.value = parsedData.average_net_wage;
    } else {
        reportingMonthInput.value = today;
        totalEmployees.value = 0;
        nationalEmployees.value = "";
        internationalEmployees.value = "";
        femaleEmployees.value = "";
        employeesDisabilities.value = "";
        femaleEmployeesDisabilities.value = "";
        youngEmployees.value = "";
        youngFemaleEmployees.value = "";
        totalWorkedDays.value = "";
        femaleEmployeesWorkedDays.value = "";
        employeesDisabilitiesWorkedDays.value = "";
        femaleEmployeesDisabilitiesWorkedDays.value = "";
        youngEmployeesWorkedDays.value = "";
        youngFemaleEmployeesWorkedDays.value = "";
        totalWages.value = "";
        averageGrossWages.value = "";
        averageNetWages.value = "";
    }
});

socialDataFormModal.on('shown.bs.modal', () => {
    document.getElementById("save-social-data").addEventListener("click", (e) => {
        const reportMonthChunks = document.getElementById("reporting-month").value.split("-");
        const year = parseInt(reportMonthChunks[0], 10);
        const month = parseInt(reportMonthChunks[1], 10);
        const data = {
            year: year,
            month: month,
            employees: parseInt(document.getElementById("total-employees").value, 10),
            national_employees: parseInt(document.getElementById("national-employees").value, 10),
            international_employees: parseInt(document.getElementById("international-employees").value, 10),
            female_employees: parseInt(document.getElementById("female-employees").value, 10),
            employees_with_disabilities: parseInt(document.getElementById("employees-disabilities").value, 10),
            female_employees_with_disabilities: parseInt(document.getElementById("female-employees-disabilities").value, 10),
            young_employees: parseInt(document.getElementById("young-employees").value, 10),
            young_female_employees: parseInt(document.getElementById("young-female-employees").value, 10),
            total_worked_days: parseInt(document.getElementById("total-worked-days").value, 10),
            female_employees_worked_days: parseInt(document.getElementById("female-employees-worked-days").value, 10),
            employees_with_disabilities_worked_days: parseInt(document.getElementById("employees-disabilities-worked-days").value, 10),
            female_employees_with_disabilities_worked_days: parseInt(document.getElementById("female-employees-disabilities-worked-days").value, 10),
            young_employees_worked_days: parseInt(document.getElementById("young-employees-worked-days").value, 10),
            young_female_employees_worked_days: parseInt(document.getElementById("young-female-employees-worked-days").value, 10),
            total_wage: parseInt(document.getElementById("total-wages").value, 10),
            average_gross_wage: parseInt(document.getElementById("average-gross-wages").value, 10),
            average_net_wage: parseInt(document.getElementById("average-net-wages").value, 10),
            contract: parseInt(e.target.dataset.id, 10),
        };

        fetch(requestId ? e.target.dataset.url + requestId + "/" : e.target.dataset.url, {
            method: requestMethod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data),
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    });
});
