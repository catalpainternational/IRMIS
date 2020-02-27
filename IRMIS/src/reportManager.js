import { getRoadReports } from "./assets/reportsAPI";

export function getAssetReport(filters) {
    return Promise.resolve(getRoadReports(filters))
        .then((surveyReportList) => { return surveyReportList; });
}
