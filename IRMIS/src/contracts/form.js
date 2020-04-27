const status = document.getElementById("id_status");
const program = document.getElementById("id_program");
const name = document.getElementById("id_name");
const code = document.getElementById("id_code");
const description = document.getElementById("id_description");
const assetCode = document.getElementsByClassName("asset-code");
const assetStartChainage = document.getElementsByClassName("asset-start-chainage");
const assetEndChainage = document.getElementsByClassName("asset-end-chainage");
const typeOfWork = document.getElementById("id_type_of_work");
const fundingSource = document.getElementById("id_funding_source");
const donor = document.getElementById("id_donor");
const budgetValue = document.getElementsByClassName("budget-value");
const budgetYear = document.getElementsByClassName("budget-year");
const startDate = document.getElementById("id_start_date");
const duration = document.getElementById("id_duration");
const milestoneDaysOfWork = document.getElementsByClassName("milestone-days-work");
const milestoneProgress = document.getElementsByClassName("milestone-progress");
const projects = document.getElementById("id_projects");
const announcementDate = document.getElementById("id_announcement_date");
const submissionDate = document.getElementById("id_submission_date");
const tenderingCompanies = document.getElementById("id_tendering_companies");
const evaluationDate = document.getElementById("id_evaluation_date");
const address = document.getElementById("id_address");
const phone = document.getElementById("id_phone");
const email = document.getElementById("id_email");
const tin = document.getElementById("id_TIN");
const iban = document.getElementById("id_iban");
const representativeName = document.getElementById("id_rep_name");
const representativePhone = document.getElementById("id_rep_phone");
const representativeEmail = document.getElementById("id_rep_email");
const womanLed = document.getElementById("id_woman_led");
const category = document.getElementById("id_category");
const tender = document.getElementById("id_tender");
const contractCode = document.getElementById("id_contract_code");
const contractor = document.getElementById("id_contractor");
const subcontractor = document.getElementById("id_subcontractor");
const supervisorName = document.getElementsByClassName("supervisor-name");
const supervisorPhone = document.getElementsByClassName("supervisor-phone");
const endDate = document.getElementById("id_end_date");
const dlp = document.getElementById("id_defect_liability_days");
const amendmentValue = document.getElementsByClassName("amendment-value");
const amendmentYear = document.getElementsByClassName("amendment-year");
const amendmentStartDate = document.getElementById("id_amendment_start_date");
const amendmentDuration = document.getElementById("id_amendment_duration");
const amendmentDescription = document.getElementById("id_amendment_description");

window.addEventListener("load", () => {
    let originalForm = {};
    let currentForm = {};

    document.addEventListener("compare-changes", (data) => {
        const nextUrl = data.detail.nextUrl;

        saveFormValues(currentForm);

        if (JSON.stringify(originalForm) !== JSON.stringify(currentForm)) {
            document.dispatchEvent(new CustomEvent("confirm-changes", { detail: { nextUrl: nextUrl } }));
        } else {
            location.href = nextUrl;
        }
    });

    saveFormValues(originalForm);

    if (program) {
        isElementValid(program);
    }

    if (name) {
        isElementValid(name);
    }

    if (code) {
        isElementValid(code);
    }

    if (description) {
        isElementValid(description);
    }

    if (assetStartChainage) {
        isFormsetElementValid(assetStartChainage);
    }

    if (assetEndChainage) {
        isFormsetElementValid(assetEndChainage);
    }

    if (typeOfWork) {
        isElementValid(typeOfWork);
    }

    if (fundingSource) {
        isElementValid(fundingSource);
    }

    if (donor) {
        isElementValid(donor);
    }

    if (budgetYear) {
        isFormsetElementValid(budgetYear);
    }

    if (budgetValue) {
        isFormsetElementValid(budgetValue);
    }

    if (startDate) {
        startDate.type = "date";
        isElementValid(startDate);
    }

    if (duration) {
        isElementValid(duration);
    }

    if (milestoneDaysOfWork) {
        isFormsetElementValid(milestoneDaysOfWork);
    }

    if (milestoneProgress) {
        isFormsetElementValid(milestoneProgress);
    }

    if (announcementDate) {
        announcementDate.type = "date";
        isElementValid(announcementDate);
    }

    if (submissionDate) {
        submissionDate.type = "date";
        isElementValid(submissionDate);
    }

    if (tenderingCompanies) {
        isElementValid(tenderingCompanies);
    }

    if (evaluationDate) {
        evaluationDate.type = "date";
        isElementValid(evaluationDate);
    }

    if (amendmentStartDate) {
        amendmentStartDate.type = "date";
    }

    if (address) {
        isElementValid(address);
    }

    if (phone) {
        isElementValid(phone);
    }

    if (email) {
        isElementValid(email);
    }

    if (tin) {
        isElementValid(tin);
    }

    if (iban) {
        isElementValid(iban);
    }

    if (representativeName) {
        isElementValid(representativeName);
    }

    if (representativePhone) {
        isElementValid(representativePhone);
    }

    if (representativeEmail) {
        isElementValid(representativeEmail);
    }

    if (womanLed) {
        isElementValid(womanLed);
    }

    if (category) {
        isElementValid(category);
    }

    if (tender) {
        isElementValid(tender);
    }

    if (contractCode) {
        isElementValid(contractCode);
    }

    if (contractor) {
        isElementValid(contractor);
    }

    if (subcontractor) {
        isElementValid(subcontractor);
    }

    if (supervisorName) {
        isFormsetElementValid(supervisorName);
    }

    if (supervisorPhone) {
        isFormsetElementValid(supervisorPhone);
    }

    if (endDate) {
        endDate.type = "date";
        isElementValid(endDate);
    }

    if (dlp) {
        isElementValid(dlp);
    }

});

function isElementValid(element) {
    isValid(element);
    element.addEventListener("change", () => {
        isValid(element);
    });

    function isValid(element) {
        if (element.value) element.classList.remove("inactive");
        else element.classList.add("inactive");
    }
}

function isFormsetElementValid(elements) {
    elements.forEach((element) => {
        isElementValid(element);
    });
}

function saveFormValues(state) {
    saveValue(state, status);
    saveValue(state, program);
    saveValue(state, name);
    saveValue(state, code);
    saveValue(state, description);
    saveFormsetValue(state, assetCode);
    saveFormsetValue(state, assetStartChainage);
    saveFormsetValue(state, assetEndChainage);
    saveValue(state, typeOfWork);
    saveValue(state, fundingSource);
    saveValue(state, donor);
    saveFormsetValue(state, budgetValue);
    saveFormsetValue(state, budgetYear);
    saveValue(state, startDate);
    saveValue(state, duration);
    saveFormsetValue(state, milestoneDaysOfWork);
    saveFormsetValue(state, milestoneProgress);
    saveValue(state, projects);
    saveValue(state, announcementDate);
    saveValue(state, submissionDate);
    saveValue(state, tenderingCompanies);
    saveValue(state, evaluationDate);
    saveValue(state, address);
    saveValue(state, phone);
    saveValue(state, email);
    saveValue(state, tin);
    saveValue(state, iban);
    saveValue(state, representativeName);
    saveValue(state, representativePhone);
    saveValue(state, representativeEmail);
    saveValue(state, womanLed);
    saveValue(state, tender);
    saveValue(state, contractCode);
    saveValue(state, contractor);
    saveValue(state, subcontractor);
    saveFormsetValue(state, supervisorName);
    saveFormsetValue(state, supervisorPhone);
    saveValue(state, endDate);
    saveValue(state, dlp);
    saveFormsetValue(state, amendmentValue);
    saveFormsetValue(state, amendmentYear);
    saveValue(state, amendmentStartDate);
    saveValue(state, amendmentDuration);
    saveValue(state, amendmentDescription);
}

function saveValue(state, field) {
    if (field) {
        state[field.name] = field.value;
    }
}

function saveFormsetValue(state, field) {
    if (field.length) {
        for (let index = 0; index < field.length; index++) {
            const element = field.item(index);

            state[element.name] = element.value;
        }
    }
}
