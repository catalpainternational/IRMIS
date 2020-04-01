import { getReports } from "./assets/reportsAPI";

export function getAssetReport(filters: { [name: string]: any }) {
    return Promise.resolve(getReports(filters))
        .then((surveyReportList) => { return surveyReportList; });
}
