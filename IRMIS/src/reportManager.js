import { getRoadReport } from "./assets/reportAPI";

export function getRoadSurveyReport(roadId) {
    return Promise.resolve(getRoadReport(roadId))
        .then((surveyReport) => {
            // document.dispatchEvent(new CustomEvent("estrada.auditTable.roadAuditDataAdded", {detail: {auditList}}));
            return surveyReport;
        });
}
