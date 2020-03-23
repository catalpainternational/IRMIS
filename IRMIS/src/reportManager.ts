import { getRoadReports } from "./assets/reportsAPI";

export function getAssetReport(filters: { [name: string]: any }) {
    return Promise.resolve(getRoadReports(filters))
        .then((surveyReportList) => { return surveyReportList; });
}
