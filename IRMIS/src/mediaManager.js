import { getMediaMetadata, getMediasMetadata, postMediaData, putMediaData } from "./assets/mediaAPI";
import { dispatch } from "./assets/utilities";

export const medias = {};

export function getMedia(id) {
    return Promise.resolve(getMediaMetadata(id))
        .then((media) => {
            return media;
        });
}

export function getMedias(objId) {
    return Promise.resolve(getMediasMetadata(objId))
        .then((medias) => {
            return medias;
        });
}

export function createMedia(media, mediaType) {
    return Promise.resolve(postMediaData(media, mediaType))
        .then((media) => {
            dispatch("estrada.media.created", { detail: { media: media } });
            return media;
        });
}

export function updateMedia(media, mediaType) {
    return Promise.resolve(putMediaData(media, mediaType))
        .then((media) => {
            dispatch("estrada.media.updated", { detail: { media: media } });
            return media;
        });
}
