import { ConfigAPI } from "./configAPI";

export function requestApiToken() {
    const metadataUrl = `${ConfigAPI.requestAssetUrl}/api_token_request/`;
    return fetch(metadataUrl, ConfigAPI.requestInit())
        .then((metadataResponse) => (metadataResponse.json()))
        .then((tokenResponse) => {
            return tokenResponse;
        });
}
