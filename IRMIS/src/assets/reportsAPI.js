import { Report } from "../../protobuf/report_pb";
import { EstradaRoadSurveyReport } from "../surveyReport";

import { ConfigAPI } from "./configAPI";
import { makeEstradaObject } from "./protoBufUtilities";

/** getRoadSurveyReports
 *
 * Retrieves the road survey data from the server
 *
 * @returns a map {id: road_object}
 */
export function getRoadSurveyReports(roadCode) {
    const assetTypeUrlFragment = "road_report";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${roadCode}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => {
            if (metadataResponse.ok) {
                return metadataResponse.arrayBuffer();
            }
            throw new Error(`Survey report retrieval failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSurveyReport(Report.deserializeBinary(uintArray));
        });
}

/** getRoadReports
 *
 * Retrieves the road report data from the server
 *
 * @returns a map {id: road_object}
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
