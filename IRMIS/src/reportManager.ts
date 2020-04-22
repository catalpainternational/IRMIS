import { getContractReports, getReports } from "./assets/reportsAPI";

export function getAssetReport(filters: { [name: string]: any }) {
    return Promise.resolve(getReports(filters))
        .then((surveyReportList) => { return surveyReportList; });
}

export function getContractReport(report_type: string, filters: { [name: string]: [] }) {
    return Promise.resolve(getContractReports(report_type, filters))
        .then((contractReportList) => { return contractReportList; });
}
