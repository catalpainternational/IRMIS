import { EstradaMedia, makeEstradaMedia, Media, Medias } from "./models/media";

import { ConfigAPI } from "./configAPI";

/** getMediasMetadata
 *
 * Retrieves the Medias metadata from the server for a Related Object
 *
 * @returns a map {id: media_object}
 */
export function getMediasMetadata(objectId: string) {
    const mediaTypeUrlFragment = "protobuf_medias";
    objectId = objectId || "";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${mediaTypeUrlFragment}/${objectId}/`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return Medias.deserializeBinary(uintArray).getMediasList().map(makeEstradaMedia);
        });
}

/** getMediaMetadata
 *
 * Retrieves the metadata for a single media from the server
 *
 * @returns a media_object
 */
export function getMediaMetadata(mediaId: string | number) {
    const mediaTypeUrlFragment = "protobuf_media";

    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${mediaTypeUrlFragment}/${mediaId}`;

    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.arrayBuffer()))
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaMedia(Media.deserializeBinary(uintArray));
        });
}

/** postMediadata
 *
 * Post data for a single Media to the server
 * NOTE: Not currently used, as JS DropZone lbrary handles POSTing media files to the server
 *         and uses a Multipart-Form POST to do so.
 *
 * @returns 200 (success) or 400 (failure)
 */
export function postMediaData(media: EstradaMedia) {
    const assetTypeUrlFragment = "media_create";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("POST");
    postAssetInit.body = media.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Media creation failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaMedia(Media.deserializeBinary(uintArray));
        });
}

/** putMediadata
 *
 * Put data for a single Media to the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function putMediaData(media: EstradaMedia) {
    const assetTypeUrlFragment = "media_update";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = media.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Media update failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaMedia(Media.deserializeBinary(uintArray));
        });
}

/** deleteMediadata
 *
 * Delete data for a single Media from the server
 *
 * @returns 200 (success) or 400 (failure)
 */
export function deleteMediaData(media: EstradaMedia) {
    const assetTypeUrlFragment = "media_delete";
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/${assetTypeUrlFragment}`;

    const postAssetInit = ConfigAPI.requestInit("PUT");
    postAssetInit.body = media.serializeBinary();

    return fetch(metadataUrl, postAssetInit)
        .then((metadataResponse) => {
            if (metadataResponse.ok) { return metadataResponse.arrayBuffer(); }
            throw new Error(`Media deletion failed: ${metadataResponse.statusText}`);
        })
        .then((protobufBytes) => {
            const uintArray = new Uint8Array(protobufBytes);
            return makeEstradaMedia(Media.deserializeBinary(uintArray));
        });
}
