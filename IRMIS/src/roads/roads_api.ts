const requestRoadUrl = `${window.location.origin}/assets/roads`;
const requestRoadInit: RequestInit = {
    headers: { "Content-Type": "application/json" },
    method: "GET",
    mode: "no-cors",
};

export function getRoadMetadata() {
    return window.fetch(requestRoadUrl, requestRoadInit)
        .then((response) => {
            if (response.ok) { return response.json(); }
            throw new Error("Network response was not ok.");
        }).then((json) => json);
}

/** getRoadGeometry
 *
 * @param roadId - database ID of the road geometry to retrieve
 *
 * @returns Promise
 *  - Promise.resolve(json) on success
 *  - Promise.resolve(undefined) on network error or no road geometry
 *  - Promise.reject(roadId) on error
 */
export async function getRoadGeometry(roadId: number): Promise<any> {
    const requestUrl = `${requestRoadUrl}/${roadId}`;

    try {
        const response = await fetch(requestUrl, requestRoadInit);
        if (!response.ok) {
            return Promise.resolve(undefined);
        }
        const responsejson = response.json();
        if (!responsejson) {
            // no json
            return Promise.resolve(undefined);
        }
        return Promise.resolve(responsejson);
    } catch (error) {
        // TODO: log this error, network error
        return Promise.reject(roadId);
    }
}
