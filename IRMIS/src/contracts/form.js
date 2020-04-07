window.addEventListener("load", () => {
    const startDate = document.getElementById("id_start_date");
    const endDate = document.getElementById("id_end_date");
    const announcementStartDate = document.getElementById("id_announcement_date");
    const submissionStartDate = document.getElementById("id_submission_date");
    const evaluationStartDate = document.getElementById("id_evaluation_date");
    const amendmentStartDate = document.getElementById("id_amendment_start_date");

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
