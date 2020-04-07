window.addEventListener("load", () => {
    const navigationLink = document.getElementsByClassName("discard-link");

    const status = document.getElementById("id_status");
    const program = document.getElementById("id_program");
    const name = document.getElementById("id_name");
    const code = document.getElementById("id_code");
    const description = document.getElementById("id_description");
    const assetCode = document.getElementsByClassName("asset-code");
    const assetStartChainage = document.getElementsByClassName("asset-start-chainage");
    const assetEndChainage = document.getElementsByClassName("asset-end-chainage");
    const typeOfWork = document.getElementById("id_type_of_work");
    const startDate = document.getElementById("id_start_date");
    const endDate = document.getElementById("id_end_date");
    const announcementStartDate = document.getElementById("id_announcement_date");
    const submissionStartDate = document.getElementById("id_submission_date");
    const evaluationStartDate = document.getElementById("id_evaluation_date");
    const amendmentStartDate = document.getElementById("id_amendment_start_date");

    let originalForm = {};
    let currentForm = {};

    navigationLink.forEach(link => {
        link.addEventListener("click", () => {
            const backUrl = link.dataset.back;

            saveValue(currentForm, status);
            saveValue(currentForm, program);
            saveValue(currentForm, name);
            saveValue(currentForm, code);
            saveValue(currentForm, description);
            saveFormsetValue(currentForm, assetCode);
            saveFormsetValue(currentForm, assetStartChainage);
            saveFormsetValue(currentForm, assetEndChainage);
            saveValue(currentForm, typeOfWork);

            if (JSON.stringify(originalForm) !== JSON.stringify(currentForm)) {
                document.dispatchEvent(new CustomEvent("confirm-changes", { detail: { backUrl: backUrl } }));
            } else {
                location.href = backUrl;
            }
        });
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

    if (startDate) {
        startDate.type = "date";
    }

    if (endDate) {
        endDate.type = "date";
    }

    if (announcementStartDate) {
        announcementStartDate.type = "date";
    }

    if (submissionStartDate) {
        submissionStartDate.type = "date";
    }

    if (evaluationStartDate) {
        evaluationStartDate.type = "date";
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
