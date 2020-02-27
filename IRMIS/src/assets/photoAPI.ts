import { Photo, Photos } from "../../protobuf/photo_pb";
import { EstradaPhoto, makeEstradaPhoto } from "./models/photo";

import { ConfigAPI } from "./configAPI";

/** getPhotosMetadata
 *
 * Retrieves the Photos metadata from the server for a Related Object
 *
 * @returns a map {id: photo_object}
 */
export function getPhotosMetadata(objectId: string) {
    const photoTypeUrlFragment = "protobuf_photos";
    objectId = objectId || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${photoTypeUrlFragment}/${objectId}/`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Photos.deserializeBinary(uintArray).getPhotosList().map(makeEstradaPhoto);
        });
}

/** getPhotoMetadata
 *
 * Retrieves the metadata for a single photo from the server
 *
 * @returns a photo_object
 */
export function getPhotoMetadata(photoId: string | number) {
    const photoTypeUrlFragment = "protobuf_photo";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${photoTypeUrlFragment}/${photoId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPhoto(Photo.deserializeBinary(uintArray));
        });
}

/** postPhotodata
 *
 * Post data for a single Photo to the server
 * NOTE: Not currently used, as JS DropZone lbrary handles POSTing photo files to the server
 *         and uses a Multipart-Form POST to do so.
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postPhotoData(photo: EstradaPhoto) {
    const assetTypeUrlFragment = "photo_create";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("POST");
    postAssetInit.body = photo.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Photo creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPhoto(Photo.deserializeBinary(uintArray));
        });
}

/** putPhotodata
 *
 * Put data for a single Photo to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putPhotoData(photo: EstradaPhoto) {
    const assetTypeUrlFragment = "photo_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = photo.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Photo creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPhoto(Photo.deserializeBinary(uintArray));
        });
}

/** deletePhotodata
 *
 * Delete data for a single Photo from the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function deletePhotoData(photo: EstradaPhoto) {
    const assetTypeUrlFragment = "photo_delete";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = photo.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Photo deletion failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaPhoto(Photo.deserializeBinary(uintArray));
        });
}
