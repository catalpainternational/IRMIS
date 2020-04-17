import "bootstrap/js/dist/modal";
import $ from "jquery";

const csrftoken = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");

const deleteLink = document.getElementsByClassName("delete-link");
const deleteAlert = $(".delete-modal");
const discardAlert = $(".discard-modal");
const formModalLink = document.getElementsByClassName("form-modal-link");
const documentFormModal = $(".document-modal");
const inspectionFormModal = $(".inspection-modal");
const paymentFormModal = $(".payment-modal");
const socialDataFormModal = $(".social-data-modal");

let deleteUrl;
let nextUrl;
let requestMethod;
let requestData;

deleteLink.forEach(link => {
    link.addEventListener("click", () => {
        deleteUrl = link.dataset.delete;
        deleteAlert.modal('show');
    });
});

formModalLink.forEach(link => {
    link.addEventListener("click", () => {
        requestMethod = link.dataset.method;
        requestData = link.dataset.object ? JSON.parse(link.dataset.object) : null;

        if (inspectionFormModal.length) inspectionFormModal.modal("show");
        else if (paymentFormModal.length) paymentFormModal.modal("show");
        else if (socialDataFormModal.length) socialDataFormModal.modal("show");
        else if (documentFormModal.length) documentFormModal.modal("show");
    });
});

deleteAlert.on('shown.bs.modal', () => {
    document.getElementsByClassName("delete-item").item(0).addEventListener("click", deleteItem);
});

deleteAlert.on('hidden.bs.modal', () => {
    document.getElementsByClassName("delete-item").item(0).removeEventListener("click", deleteItem);
});

function deleteItem() {
    fetch(deleteUrl, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": csrftoken
        },
    }).then(response => {
        if (response.ok) {
            window.location = "?banner=true";
        } else {
            document.dispatchEvent(new CustomEvent("show-banner", { detail: { banner: document.getElementById("error-banner") } }));
        }
    });
}

document.addEventListener("confirm-changes", (data) => {
    nextUrl = data.detail.nextUrl;
    discardAlert.modal('show');
});

discardAlert.on('shown.bs.modal', () => {
    document.getElementsByClassName("discard-changes").item(0).addEventListener("click", discardChanges);
});

discardAlert.on('hidden.bs.modal', () => {
    document.getElementsByClassName("discard-changes").item(0).removeEventListener("click", discardChanges);
});

function discardChanges() {
    location.href = nextUrl;
}

inspectionFormModal.on('show.bs.modal', () => {
    const dateInput = document.getElementById("inpection-date");
    const entitySelect = document.getElementById("inpection-entity");
    const progressInput = document.getElementById("physical-progress");
    const defectLiabilityPeriod = document.getElementById("defect-liability");
    const today = new Date().toISOString().substring(0, 10);

    dateInput.max = today;

    if (requestData) {
        dateInput.value = requestData.date;
        entitySelect.value = requestData.entity;
        progressInput.value = requestData.progress;
        defectLiabilityPeriod.checked = requestData.defect_liability_period;
    } else {
        dateInput.value = today;
        entitySelect.value = entitySelect.options.item(0).value;
        progressInput.value = 0;
        defectLiabilityPeriod.checked = false;
    }
});

inspectionFormModal.on('shown.bs.modal', () => {
    document.getElementById("save-inspection").addEventListener("click", saveInspection);
});

inspectionFormModal.on('hidden.bs.modal', () => {
    document.getElementById("save-inspection").removeEventListener("click", saveInspection);
});

function saveInspection(e) {
    const fetchURL = requestData ? "/contracts/api/contractinspection/" + requestData.id + "/" : "/contracts/api/contractinspection/";
    const formData = {
        date: document.getElementById("inpection-date").value,
        progress: parseInt(document.getElementById("physical-progress").value, 10),
        entity: parseInt(document.getElementById("inpection-entity").value, 10),
        defect_liability_period: document.getElementById("defect-liability").checked,
        contract: parseInt(e.target.dataset.id, 10),
    };

    fetch(fetchURL, {
        method: requestMethod,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(formData),
    }).then(response => {
        if (response.ok) {
            window.location = "?banner=true";
        } else {
            document.dispatchEvent(new CustomEvent("show-banner", { detail: { banner: document.getElementById("error-banner") } }));
        }
    });
}

paymentFormModal.on('show.bs.modal', () => {
    const dateInput = document.getElementById("payment-date");
    const valueInput = document.getElementById("payment-value");
    const donorSelect = document.getElementById("payment-donor");
    const sourceSelect = document.getElementById("payment-source");
    const destinationSelect = document.getElementById("payment-destination");
    const today = new Date().toISOString().substring(0, 10);

    dateInput.max = today;

    if (requestData) {
        dateInput.value = requestData.date;
        valueInput.value = requestData.value;
        donorSelect.value = requestData.donor;
        sourceSelect.value = requestData.source;
        destinationSelect.value = requestData.destination;
    } else {
        dateInput.value = today;
        valueInput.value = 0;
        donorSelect.value = donorSelect.options.item(0).value;
        sourceSelect.value = sourceSelect.options.item(0).value;
        destinationSelect.value = destinationSelect.options.item(0).value;
    }
});

paymentFormModal.on('shown.bs.modal', () => {
    document.getElementById("save-payment").addEventListener("click", savePayment);
});

paymentFormModal.on('hidden.bs.modal', () => {
    document.getElementById("save-payment").removeEventListener("click", savePayment);
});

function savePayment(e) {
    const fetchURL = requestData ? "/contracts/api/contractpayment/" + requestData.id + "/" : "/contracts/api/contractpayment/";
    const donor = parseInt(document.getElementById("payment-donor").value, 10);
    const formData = {
        date: document.getElementById("payment-date").value,
        value: parseInt(document.getElementById("payment-value").value, 10),
        donor: donor !== 0 ? donor : null,
        source: parseInt(document.getElementById("payment-source").value, 10),
        destination: parseInt(document.getElementById("payment-destination").value, 10),
        contract: parseInt(e.target.dataset.id, 10),
    };

    fetch(fetchURL, {
        method: requestMethod,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(formData),
    }).then(response => {
        if (response.ok) {
            window.location = "?banner=true";
        } else {
            document.dispatchEvent(new CustomEvent("show-banner", { detail: { banner: document.getElementById("error-banner") } }));
        }
    });
}

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
        const month = requestData.month < 10 ? "0" + requestData.month : requestData.month

        reportingMonthInput.value = requestData.year + "-" + month;
        totalEmployees.value = requestData.employees;
        nationalEmployees.value = requestData.national_employees;
        internationalEmployees.value = requestData.international_employees;
        femaleEmployees.value = requestData.female_employees;
        employeesDisabilities.value = requestData.employees_with_disabilities;
        femaleEmployeesDisabilities.value = requestData.female_employees_with_disabilities;
        youngEmployees.value = requestData.young_employees;
        youngFemaleEmployees.value = requestData.young_female_employees;
        totalWorkedDays.value = requestData.total_worked_days;
        femaleEmployeesWorkedDays.value = requestData.female_employees_worked_days;
        employeesDisabilitiesWorkedDays.value = requestData.employees_with_disabilities_worked_days;
        femaleEmployeesDisabilitiesWorkedDays.value = requestData.female_employees_with_disabilities_worked_days;
        youngEmployeesWorkedDays.value = requestData.young_employees_worked_days;
        youngFemaleEmployeesWorkedDays.value = requestData.young_female_employees_worked_days;
        totalWages.value = requestData.total_wage;
        averageGrossWages.value = requestData.average_gross_wage;
        averageNetWages.value = requestData.average_net_wage;
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
    document.getElementById("save-social-data").addEventListener("click", saveSocialData);
});

socialDataFormModal.on('hidden.bs.modal', () => {
    document.getElementById("save-social-data").removeEventListener("click", saveSocialData);
});

function saveSocialData(e) {
    const fetchURL = requestData ? "/contracts/api/socialsafeguarddata/" + requestData.id + "/" : "/contracts/api/socialsafeguarddata/";
    const reportMonthChunks = document.getElementById("reporting-month").value.split("-");
    const year = parseInt(reportMonthChunks[0], 10);
    const month = parseInt(reportMonthChunks[1], 10);
    const formData = {
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

    fetch(fetchURL, {
        method: requestMethod,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(formData),
    }).then(response => {
        if (response.ok) {
            window.location = "?banner=true";
        } else {
            document.dispatchEvent(new CustomEvent("show-banner", { detail: { banner: document.getElementById("error-banner") } }));
        }
    });
}

documentFormModal.on('show.bs.modal', () => {
    const fileName = document.getElementById("document-file-name");
    const title = document.getElementById("document-title");
    const description = document.getElementById("document-description");
    const date = document.getElementById("document-date");
    const type = document.getElementById("document-type");
    const today = new Date().toISOString().substring(0, 10);

    date.max = today;

    if (requestData) {
        fileName.innerHTML = requestData.content;
        title.value = requestData.title;
        description.value = requestData.description;
        date.value = requestData.document_date;
        type.value = requestData.document_type;
    } else {
        fileName.innerHTML = "";
        title.value = "";
        description.value = "";
        date.value = today;
        type.value = type.options.item(0).value;
    }
});

documentFormModal.on('shown.bs.modal', () => {
    document.getElementById("save-document").addEventListener("click", saveDocument);
});

documentFormModal.on('hidden.bs.modal', () => {
    document.getElementById("save-document").removeEventListener("click", saveDocument);
});

function saveDocument(e) {
    const fetchURL = requestData ? "/contracts/api/contractdocument/" + requestData.id + "/" : "/contracts/api/contractdocument/";
    const formElement = $("#doc-upload-form").get(0);

    let formData = new FormData(formElement);

    formData.append(e.target.dataset.profile, [e.target.dataset.id]);

    fetch(fetchURL, {
        method: requestMethod,
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: formData,
    }).then(response => {
        if (response.ok) {
            window.location = "?banner=true";
        } else {
            document.dispatchEvent(new CustomEvent("show-banner", { detail: { banner: document.getElementById("error-banner") } }));
        }
    });
}
