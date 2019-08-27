const requestAssetUrl = `${window.location.origin}/assets`;
const requestAssetInit = {
    headers: { "Content-Type": "application/json" },
    method: "GET",
    mode: "no-cors",
};

/** getAssetsMetadata
 *
 * @param assetType  - type of asset to retrieve, defaults to "roads"
 *
 * @returns Promise
 *  - Promise.resolve(json) on success
 *  - Throws error on failure
 */
export function getAssetsMetadata(assetType = "roads") {
    return window.fetch(`${requestAssetUrl}/${assetType}`, requestAssetInit)
        .then((response) => {
            if (response.ok) { return response.json(); }
            throw new Error("Network response was not ok.");
        }).then((json) => json);
}

/** getAssetGeometry
 *
 * @param assetId - database ID of the asset geometry to retrieve
 * @param assetType - type of asset to retrieve, defaults to "roads"
 *
 * @returns Promise
 *  - Promise.resolve(json) on success (hopefully that's GeoJSON)
 *  - Throws error on failure
 */
export function getAssetGeometry(assetId, assetType = "roads") {
    const requestUrl = `${requestAssetUrl}/${assetType}/${assetId}`;

    return window.fetch(requestUrl, requestAssetInit)
        .then((response) => {
            if (response.ok) { return response.json(); }
            throw new Error("Network response was not ok.");
        }).then((json) => json);
}
