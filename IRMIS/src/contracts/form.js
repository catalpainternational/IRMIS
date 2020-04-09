window.addEventListener("load", () => {
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

    let originalForm = {};
    let currentForm = {};

    document.addEventListener("compare-changes", (data) => {
        const nextUrl = data.detail.nextUrl;

        saveValue(currentForm, status);
        saveValue(currentForm, program);
        saveValue(currentForm, name);
        saveValue(currentForm, code);
        saveValue(currentForm, description);
        saveFormsetValue(currentForm, assetCode);
        saveFormsetValue(currentForm, assetStartChainage);
        saveFormsetValue(currentForm, assetEndChainage);
        saveValue(currentForm, typeOfWork);
        saveValue(currentForm, fundingSource);
        saveValue(currentForm, donor);
        saveFormsetValue(currentForm, budgetValue);
        saveFormsetValue(currentForm, budgetYear);
        saveValue(currentForm, startDate);
        saveValue(currentForm, duration);
        saveFormsetValue(currentForm, milestoneDaysOfWork);
        saveFormsetValue(currentForm, milestoneProgress);
        saveValue(currentForm, projects);
        saveValue(currentForm, announcementDate);
        saveValue(currentForm, submissionDate);
        saveValue(currentForm, tenderingCompanies);
        saveValue(currentForm, evaluationDate);
        saveValue(currentForm, address);
        saveValue(currentForm, phone);
        saveValue(currentForm, email);
        saveValue(currentForm, tin);
        saveValue(currentForm, iban);
        saveValue(currentForm, representativeName);
        saveValue(currentForm, representativePhone);
        saveValue(currentForm, representativeEmail);
        saveValue(currentForm, womanLed);
        saveValue(currentForm, tender);
        saveValue(currentForm, contractCode);
        saveValue(currentForm, contractor);
        saveValue(currentForm, subcontractor);
        saveFormsetValue(currentForm, supervisorName);
        saveFormsetValue(currentForm, supervisorPhone);
        saveValue(currentForm, endDate);
        saveValue(currentForm, dlp);
        saveFormsetValue(currentForm, amendmentValue);
        saveFormsetValue(currentForm, amendmentYear);
        saveValue(currentForm, amendmentStartDate);
        saveValue(currentForm, amendmentDuration);
        saveValue(currentForm, amendmentDescription);

        if (JSON.stringify(originalForm) !== JSON.stringify(currentForm)) {
            document.dispatchEvent(new CustomEvent("confirm-changes", { detail: { nextUrl: nextUrl } }));
        } else {
            location.href = nextUrl;
        }
    });

    saveValue(originalForm, status);
    saveValue(originalForm, status);
    saveValue(originalForm, program);
    saveValue(originalForm, name);
    saveValue(originalForm, code);
    saveValue(originalForm, description);
    saveFormsetValue(originalForm, assetCode);
    saveFormsetValue(originalForm, assetStartChainage);
    saveFormsetValue(originalForm, assetEndChainage);
    saveValue(originalForm, typeOfWork);
    saveValue(originalForm, fundingSource);
    saveValue(originalForm, donor);
    saveFormsetValue(originalForm, budgetValue);
    saveFormsetValue(originalForm, budgetYear);
    saveValue(originalForm, startDate);
    saveValue(originalForm, duration);
    saveFormsetValue(originalForm, milestoneDaysOfWork);
    saveFormsetValue(originalForm, milestoneProgress);
    saveValue(originalForm, projects);
    saveValue(originalForm, announcementDate);
    saveValue(originalForm, submissionDate);
    saveValue(originalForm, tenderingCompanies);
    saveValue(originalForm, evaluationDate);
    saveValue(originalForm, address);
    saveValue(originalForm, phone);
    saveValue(originalForm, email);
    saveValue(originalForm, tin);
    saveValue(originalForm, iban);
    saveValue(originalForm, representativeName);
    saveValue(originalForm, representativePhone);
    saveValue(originalForm, representativeEmail);
    saveValue(originalForm, womanLed);
    saveValue(originalForm, tender);
    saveValue(originalForm, contractCode);
    saveValue(originalForm, contractor);
    saveValue(originalForm, subcontractor);
    saveFormsetValue(originalForm, supervisorName);
    saveFormsetValue(originalForm, supervisorPhone);
    saveValue(originalForm, endDate);
    saveValue(originalForm, dlp);
    saveFormsetValue(originalForm, amendmentValue);
    saveFormsetValue(originalForm, amendmentYear);
    saveValue(originalForm, amendmentStartDate);
    saveValue(originalForm, amendmentDuration);
    saveValue(originalForm, amendmentDescription);

    if (startDate) {
        startDate.type = "date";
    }

    if (endDate) {
        endDate.type = "date";
    }

    if (announcementDate) {
        announcementDate.type = "date";
    }

    if (submissionDate) {
        submissionDate.type = "date";
    }

    if (evaluationDate) {
        evaluationDate.type = "date";
    }

    if (amendmentStartDate) {
        amendmentStartDate.type = "date";
    }
});

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
