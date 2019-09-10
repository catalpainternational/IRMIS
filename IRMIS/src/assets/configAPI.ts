export class ConfigAPI {
    public static requestAssetUrl = `${window.location.origin}/assets`;

    public static requestAssetInit: RequestInit = {
        headers: { "Content-Type": "application/json" },
        method: "GET",
        mode: "no-cors",
    };

    public static requestMediaUrl = `${window.location.origin}/media`;
}
