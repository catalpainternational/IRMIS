import { getRoadReports } from "./assets/reportsAPI";

export function getRoadReport(filters) {
    return Promise.resolve(getRoadReports(filters))
        .then((surveyReportList) => {
            // document.dispatchEvent(new CustomEvent("estrada.auditTable.roadAuditDataAdded", {detail: {auditList}}));
            return surveyReportList;
        });
}
