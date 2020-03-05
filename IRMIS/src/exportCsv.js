import { LocalSave } from "./localFileAccess";

export function exportCsv(headers, rows) {
    const date = new Date();
    const month = date.getMonth() + 1;
    const title = "Estrada_" + date.getFullYear() + "-" + month + "-" + date.getDate();
    const fileName = title + ".csv";

    const csvDump = [];
    csvDump.push(headers.map((h) => '"' + h + '"').join(","));

    rows.forEach((row) => {
        const rowCells = [];
        row.forEach((cell) => {
            if (cell == null) {
                cell = "";
            }
            if (!cell) {
                rowCells.push(cell);
            } else {
                const cellNumber = Number(cell);
                if (isNaN(cellNumber)) {
                    rowCells.push('"' + cell + '"');
                } else {
                    rowCells.push(cellNumber);
                }
            }
        });

        csvDump.push(rowCells.join(","));
    });

    // Using default Windoze line terminators, because ... well ...
    LocalSave(fileName, csvDump.join("\r\n"));
}
