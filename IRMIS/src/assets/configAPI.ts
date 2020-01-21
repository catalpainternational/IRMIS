import { isArray } from "util";

export class ConfigAPI {
    public static requestAssetUrl = `${window.location.origin}/assets`;
    public static requestMediaUrl = `${window.location.origin}/media`;
    public static requestReportUrl = `${window.location.origin}/assets/reports`;

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

    /** Converts an object into a query string
     * e.g. {road_code: "A01", roadchainagestart: 12345}
     * -> ?road_code=A01&roadchainagestart=12345
     */
    public static objectToQueryString(obj: { [name: string]: any }) {
        if (!obj || Object.keys(obj).length === 0) {
            return "";
        }

        const queryParams: string[] = [];
        Object.keys(obj).forEach((key) => {
            if (isArray(obj[key])) {
                obj[key].forEach((element: any) => {
                    queryParams.push(`${key}=${element}`);
                });
            } else {
                if (!obj[key]) {
                    return;
                }
                // Test for the protobuf wrapper types
                if (obj[key].array && obj[key].array.length === 0) {
                    return;
                }
                queryParams.push(`${key}=${obj[key]}`);
            }
        });
        return `?${queryParams.join("&")}`;
    }
}
