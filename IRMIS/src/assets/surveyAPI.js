import { Survey } from "../../protobuf/surveys_pb";
import { EstradaSurvey } from "../survey";
import { ConfigAPI } from "./configAPI";

/** getSurveysMetadataChunks
 *
 * Retrieves the details for the survey metadata chunks from the server
 *
 * @returns a map {id: survey_object}
 */
export function getSurveysMetadataChunks() {
    const surveyTypeUrlFragment = "survey_chunks";
    const metadataUrl = `${ConfigAPI.requestSurveyUrl}/${surveyTypeUrlFragment}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((jsonResponse) => (jsonResponse.json()));
}

/** getSurveysMetadata
 *
 * Retrieves the survey metadata from the server
 *
 * @returns a map {id: survey_object}
 */
export function getSurveysMetadata(chunkName) {
    const surveyTypeUrlFragment = "protobuf_surveys";
    chunkName = chunkName || "";
    const metadataUrl = `${ConfigAPI.requestSurveyUrl}/${surveyTypeUrlFragment}/${chunkName}`;

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

    const metadataUrl = `${ConfigAPI.requestSurveyUrl}/${surveyTypeUrlFragment}/${surveyId}`;

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
