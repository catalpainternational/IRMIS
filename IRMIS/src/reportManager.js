import { getRoadReports } from "./assets/reportsAPI";

export function getRoadReport(filters) {
    return Promise.resolve(getRoadReports(filters))
        .then((surveyReportList) => { return surveyReportList; });
}
