import { getStructureSurveysMetadata, getSurveyMetadata, getSurveysMetadata, postSurveyData, putSurveyData } from "./assets/surveyAPI";

let surveys = {}

export function getSurvey(id) {
    let survey = surveys[id];
    if(survey) return Promise.resolve(survey);
    return getSurveyMetadata(id);
}

export function getAssetSurveys(roadId, surveyAttribute) {
    return Promise.resolve(getSurveysMetadata(roadId, surveyAttribute))
        .then(surveys => {
            return surveys;
        });
}

export function getStructureSurveys(structureId, surveyAttribute) {
    return Promise.resolve(getStructureSurveysMetadata(structureId, surveyAttribute))
        .then(surveys => {
            return surveys;
        });
}

export function createSurvey(survey) {
    return Promise.resolve(postSurveyData(survey))
        .then(survey => {
            surveys[survey.id] = survey;
            return survey;
        });
}

export function updateSurvey(survey) {
    return Promise.resolve(putSurveyData(survey))
        .then(survey => {
            surveys[survey.id] = survey;
            return survey;
        });
}
