import { Report } from "../../protobuf/report_pb";

import { ConfigAPI } from "./configAPI";
import { makeEstradaNetworkSurveyReport } from "./models/surveyReport";

/** getReports
 *
 * Retrieves asset/structure report data from the server
 */
export function getReports(filters: { [name: string]: any }) {
    const filterParams = ConfigAPI.objectToQueryString(filters);
    const reportUrl = `${ConfigAPI.requestReportUrl}/${filterParams}`;

    const request = ConfigAPI.requestInit();

    return fetch(reportUrl, request)
        .then((metadataResponse) => {
            if (metadataResponse.ok) {
                return metadataResponse.arrayBuffer();
            } else {
                // Handle all fetch level errors
                return undefined;
            }
        })
        .then((protobufBytes) => {
            if (typeof protobufBytes === "undefined") {
                // return an empty EstradaNetworkSurveyReport
                return makeEstradaNetworkSurveyReport();
            }

            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaNetworkSurveyReport(Report.deserializeBinary(uintArray));
        });
}
