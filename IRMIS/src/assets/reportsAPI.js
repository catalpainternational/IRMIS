import { Report } from "../../protobuf/report_pb";
import { EstradaRoadSurveyReport } from "./models/surveyReport";

import { ConfigAPI } from "./configAPI";
import { makeEstradaObject } from "./protoBufUtilities";

/** getRoadReports
 *
 * Retrieves the road report data from the server
 */
export function getRoadReports(filters) {
    const filterParams = ConfigAPI.objectToQueryString(filters);
    const reportUrl = `${ConfigAPI.requestReportUrl}${filterParams}`;

    const request = ConfigAPI.requestInit();

    return fetch(reportUrl, request)
        .then((metadataResponse) => {
            if (metadataResponse.ok) {
                return metadataResponse.arrayBuffer();
            }
            throw new Error(`Road report retrieval failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSurveyReport(Report.deserializeBinary(uintArray));
        });
}

function makeEstradaSurveyReport(pbsurveyreport) {
    return makeEstradaObject(EstradaRoadSurveyReport, pbsurveyreport);
}
