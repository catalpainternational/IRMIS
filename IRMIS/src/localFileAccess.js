// see: https://github.com/eligrey/FileSaver.js
import { saveAs } from "file-saver";

/** while save can work with a fileBody of any serialised type,
 * you really should define something
 * Which seems to get ignored ...
 */
export function LocalSave(filename, fileBody, bodyType = "text/plain;charset=utf-8") {
    try {
        const isFileSaverSupported = !!new Blob();
    } catch (e) {
        throw new Error("Your browser does not support saving files locally");
    }

    const blob = new Blob([fileBody], {type: bodyType});

    // autoBom is only honored (supposedly) if charset=utf-8
    saveAs(blob, filename, { autoBom: true });
}
