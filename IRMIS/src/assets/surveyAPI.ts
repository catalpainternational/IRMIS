import { Survey, Surveys } from "../../protobuf/survey_pb";
import { EstradaSurvey, makeEstradaSurvey } from "./models/survey";

import { ConfigAPI } from "./configAPI";

/** getSurveysMetadata
 *
 * Retrieves the Road survey metadata from the server
 *
 * @returns a map {id: survey_object}
 */
export function getSurveysMetadata(roadId: string, surveyAttribute: string) {
    const surveyTypeUrlFragment = "protobuf_road_surveys";
    roadId = roadId || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${surveyTypeUrlFragment}/${roadId}/${surveyAttribute}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Surveys.deserializeBinary(uintArray).getSurveysList().map(makeEstradaSurvey);
        });
}

/** getSurveysMetadata
 *
 * Retrieves the Road survey metadata from the server
 *
 * @returns a map {id: survey_object}
 */
export function getStructureSurveysMetadata(structureId, surveyAttribute) {
    const surveyTypeUrlFragment = "protobuf_structure_surveys";
    structureId = structureId || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${surveyTypeUrlFragment}/${structureId}/${surveyAttribute}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Surveys.deserializeBinary(uintArray).getSurveysList().map(makeEstradaSurvey);
        });
}

/** getSurveyMetadata
 *
 * Retrieves the metadata for a single survey from the server
 *
 * @returns a survey_object
 */
export function getSurveyMetadata(surveyId: string | number) {
    const surveyTypeUrlFragment = "protobuf_survey";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${surveyTypeUrlFragment}/${surveyId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSurvey(Survey.deserializeBinary(uintArray));
        });
}

/** postSurveydata
 *
 * Post data for a single Survey to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postSurveyData(survey: EstradaSurvey) {
    const assetTypeUrlFragment = "survey_create";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("POST");
    postAssetInit.body = survey.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Survey creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSurvey(Survey.deserializeBinary(uintArray));
        });
}

/** putSurveydata
 *
 * Put data for a single Survey to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putSurveyData(survey: EstradaSurvey) {
    const assetTypeUrlFragment = "survey_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = survey.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Survey creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSurvey(Survey.deserializeBinary(uintArray));
        });
}
