import { getContractReports, getReports } from "./assets/reportsAPI";

export function getAssetReport(filters: { [name: string]: any }) {
    return Promise.resolve(getReports(filters))
        .then((surveyReportList) => { return surveyReportList; });
}

export function getContractReport(reportType: string, filters: { [name: string]: [] }) {
    return Promise.resolve(getContractReports(reportType, filters))
        .then((contractReportList) => { return contractReportList; });
}
