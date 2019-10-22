import { getSurveyMetadata, getSurveysMetadata, postSurveyData, putSurveyData } from "./assets/surveyAPI";

let surveys = {}

export function getSurvey(id) {
    let survey = surveys[id];
    if(survey) return Promise.resolve(survey);
    return getSurveyMetadata(id);
}

export function getRoadSurveys(roadId) {
    return Promise.resolve(getSurveysMetadata(roadId))
        .then(surveys => {
            // document.dispatchEvent(new CustomEvent("estrada.table.surveyMetaDataUpdated", {detail: {survey}}));
            return surveys;
        });
}

export function createSurvey(survey) {
    return Promise.resolve(postSurveyData(survey))
        .then(survey => {
            surveys[survey.getId()] = survey;
            // document.dispatchEvent(new CustomEvent("estrada.table.surveyMetaDataUpdated", {detail: {survey}}));
            return survey;
        });
}

export function updateSurvey(survey) {
    return Promise.resolve(putSurveyData(survey))
        .then(survey => {
            surveys[survey.getId()] = survey;
            // document.dispatchEvent(new CustomEvent("estrada.table.surveyMetaDataUpdated", {detail: {survey}}));
            return survey;
        });
}
