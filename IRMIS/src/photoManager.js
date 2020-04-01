import { getPhotoMetadata, getPhotosMetadata, postPhotoData, putPhotoData } from "./assets/photoAPI";
import { dispatch } from "./assets/utilities";

export const photos = {};

export function getPhoto(id) {
    return Promise.resolve(getPhotoMetadata(id))
        .then((photo) => {
            return photo;
        });
}

export function getPhotos(objId) {
    return Promise.resolve(getPhotosMetadata(objId))
        .then((photos) => {
            return photos;
        });
}

export function createPhoto(photo, photoType) {
    return Promise.resolve(postPhotoData(photo, photoType))
        .then((photo) => {
            dispatch("estrada.photo.created", { detail: { photo: photo } });
            return photo;
        });
}

export function updatePhoto(photo, photoType) {
    return Promise.resolve(putPhotoData(photo, photoType))
        .then((photo) => {
            dispatch("estrada.photo.updated", { detail: { photo: photo } });
            return photo;
        });
}
