import { getRoadReports, getRoadSurveyReports } from "./assets/reportsAPI";

export function getRoadSurveyReport(roadCode) {
    return Promise.resolve(getRoadSurveyReports(roadCode))
        .then((surveyReportList) => {
            // document.dispatchEvent(new CustomEvent("estrada.auditTable.roadAuditDataAdded", {detail: {auditList}}));
            return surveyReportList;
        });
}

export function getRoadReport(filters) {
    return Promise.resolve(getRoadReports(filters))
        .then((surveyReportList) => {
            // document.dispatchEvent(new CustomEvent("estrada.auditTable.roadAuditDataAdded", {detail: {auditList}}));
            return surveyReportList;
        });
}
