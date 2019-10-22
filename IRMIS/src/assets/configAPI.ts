export class ConfigAPI {
    public static requestAssetUrl = `${window.location.origin}/assets`;
    public static requestMediaUrl = `${window.location.origin}/media`;

    /** Build the fetch RequestInit structure for all requests
     *
     * @param method - HTTP method required, defaults to "GET"
     */
    public static requestInit(method: any = "GET"): RequestInit {
        const noCSRF = ["GET", "HEAD", "OPTIONS", "TRACE"].indexOf(method) > -1;

        if (noCSRF) {
            return {
                headers: {
                    "Content-Type": "application/json",
                },
                method,
                mode: "no-cors",
            } as RequestInit;
        }

        return {
            // body: -- set this in your code
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/octet-stream",
                "X-CSRFToken": document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
            },
            method,
            mode: "cors",
            responseType: "arraybuffer",
        } as RequestInit;
    }
}
