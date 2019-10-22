import { Survey, Surveys } from "../../protobuf/survey_pb";
import { EstradaSurvey } from "../survey";
import { ConfigAPI } from "./configAPI";

/** getSurveysMetadataChunks
 *
 * Retrieves the details for the survey metadata chunks from the server
 *
 * @returns a map {id: survey_object}
 */
export function getSurveysMetadataChunks() {
    const surveyTypeUrlFragment = "protobuf_surveys";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${surveyTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((jsonResponse) => (jsonResponse.json()));
}

/** getSurveysMetadata
 *
 * Retrieves the survey metadata from the server
 *
 * @returns a map {id: survey_object}
 */
export function getSurveysMetadata(roadCode) {
    const surveyTypeUrlFragment = "protobuf_road_surveys";
    roadCode = roadCode || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${surveyTypeUrlFragment}/${roadCode}`;

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
export function getSurveyMetadata(surveyId) {
    const surveyTypeUrlFragment = "protobuf_survey";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${surveyTypeUrlFragment}/${surveyId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSurvey(Survey.deserializeBinary(uintArray));
        });
}

function makeEstradaSurvey(pbsurvey) {
    var estradaSurvey = Object.create(EstradaSurvey.prototype);
    Object.assign(estradaSurvey, pbsurvey);
    return estradaSurvey;
}

/** postSurveydata
 *
 * Post data for a single Survey to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postSurveyData(survey) {
    const assetTypeUrlFragment = "survey_create";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("POST");
    postAssetInit.body = survey.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then(metadataResponse => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Survey creation failed: ${metadataResponse.statusText}`);
        })
        .then(protobufBytes => {
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
export function putSurveyData(survey) {
    const assetTypeUrlFragment = "survey_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = survey.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then(metadataResponse => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Survey creation failed: ${metadataResponse.statusText}`);
        })
        .then(protobufBytes => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaSurvey(Survey.deserializeBinary(uintArray));
        });
}
