import { Report } from "../../protobuf/survey_pb";
import { EstradaSurveyReport } from "../surveyReport";
import { ConfigAPI } from "./configAPI";
import { makeEstradaObject } from "./protoBufUtilities";

/** getRoadReport
 *
 * Retrieves a report for all surveys of a given road PK from the server
 *
 * @returns a Report object
 */
export function getRoadReport(roadId) {
    const assetTypeUrlFragment = "road_report";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}/${roadId}`;

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

function makeEstradaSurveyReport(pbsurveyreport) {
    return makeEstradaObject(EstradaSurveyReport, pbsurveyreport);
}
