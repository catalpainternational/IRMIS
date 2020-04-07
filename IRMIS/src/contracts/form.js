window.addEventListener("load", () => {
    const navigationLink = document.getElementsByClassName("discard-link");

    const status = document.getElementById("id_status");
    const program = document.getElementById("id_program");
    const name = document.getElementById("id_name");
    const code = document.getElementById("id_code");
    const description = document.getElementById("id_description");
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

            currentForm["status"] = status.value;
            currentForm["program"] = program.value;
            currentForm["name"] = name.value;
            currentForm["code"] = code.value;
            currentForm["description"] = description.value;
            currentForm["typeOfWork"] = typeOfWork.value;

            if (JSON.stringify(originalForm) !== JSON.stringify(currentForm)) {
                document.dispatchEvent(new CustomEvent("confirm-changes", { detail: { backUrl: backUrl } }));
            } else {
                location.href = backUrl;
            }
        });
    });

    if (status) {
        originalForm["status"] = status.value;
    }

    if (program) {
        originalForm["program"] = program.value;
    }

    if (name) {
        originalForm["name"] = name.value;
    }

    if (code) {
        originalForm["code"] = code.value;
    }

    if (description) {
        originalForm["description"] = description.value;
    }

    if (typeOfWork) {
        originalForm["typeOfWork"] = typeOfWork.value;
    }

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
