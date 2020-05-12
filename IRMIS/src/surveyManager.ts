import { getStructureSurveysMetadata, getSurveyMetadata, getSurveysMetadata, postSurveyData, putSurveyData } from "./assets/surveyAPI";
import { EstradaSurvey } from "./assets/models/survey";

export let surveys: { [name: string]: EstradaSurvey } = {}

export function getSurvey(id: string) {
    const survey = surveys[id];
    if (survey) {
        return Promise.resolve(survey);
    }
    return getSurveyMetadata(id);
}

export function getAssetSurveys(roadId: string, surveyAttribute: string) {
    return Promise.resolve(getSurveysMetadata(roadId, surveyAttribute))
        .then((estradaSurveys: EstradaSurvey[]) => {
            return estradaSurveys;
        });
}

export function getStructureSurveys(structureId: string, surveyAttribute: string) {
    return Promise.resolve(getStructureSurveysMetadata(structureId, surveyAttribute))
        .then((estradaSurveys: EstradaSurvey[]) => {
            return estradaSurveys;
        });
}

export function createSurvey(survey: EstradaSurvey) {
    return Promise.resolve(postSurveyData(survey))
        .then(estradaSurvey => {
            surveys[estradaSurvey.id] = estradaSurvey;
            return survey;
        });
}

export function updateSurvey(survey: EstradaSurvey) {
    return Promise.resolve(putSurveyData(survey))
        .then(estradaSurvey => {
            surveys[estradaSurvey.id] = estradaSurvey;
            return survey;
        });
}
