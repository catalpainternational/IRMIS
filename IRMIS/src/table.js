import "datatables.net-bs4";

import $ from "jquery";

const tableData = [
    {
        code: "A1", condition: "Poor", length: 10, name: "Aileu",
    },
    {
        code: "A2", condition: "Good", length: 15, name: "Ainaro",
    },
    {
        code: "B1", condition: "Poor", length: 30, name: "Baucau",
    },
    {
        code: "B2", condition: "Good", length: 70, name: "Bobonaro",
    },
    {
        code: "C1", condition: "Poor", length: 30, name: "Covalima",
    },
    {
        code: "D1", condition: "Excellent", length: 50, name: "Dili",
    },
    {
        code: "E1", condition: "Poor", length: 45, name: "Ermera",
    },
    {
        code: "L1", condition: "Good", length: 60, name: "Lautem",
    },
    {
        code: "L2", condition: "Poor", length: 90, name: "Liquica",
    },
    {
        code: "M1", condition: "Good", length: 100, name: "Manatuto",
    },
    {
        code: "M2", condition: "Poor", length: 5, name: "Manufahi",
    },
    {
        code: "O1", condition: "Good", length: 35, name: "Oecusse",
    },
    {
        code: "V1", condition: "Poor", length: 80, name: "Viqueque",
    },
];

const table = $("#data-table").DataTable({
    columns: [
        {
            data: "name", title: "Name",
        },
        {
            data: "code", title: "Code",
        },
        {
            data: "condition", title: "Condition",
        },
        {
            data: "length", title: "Length",
        },
    ],
    data: tableData,
    bLengthChange : false, // hide table length
    searching: false, // hide search box
});

// params: (settings, data, dataIndex, row, counter)
/*
function length_search(settings, data) {
    const minLength = parseInt(document.getElementById("min-length-filter").value, 10);
    const maxLength = parseInt(document.getElementById("max-length-filter").value, 10);
    const currLength = parseInt(data[3], 10);

    if (Number.isNaN(minLength) && Number.isNaN(maxLength)) { return true; }
    if (Number.isNaN(minLength) && currLength <= maxLength) { return true; }
    if (Number.isNaN(maxLength) && currLength >= minLength) { return true; }
    if (currLength <= maxLength && currLength >= minLength) { return true; }
    return false;
}

function condition_search(settings, data) {
    const condition = document.getElementById("condition-filter").value;
    const currCondition = data[2];

    if (condition === "" || condition === currCondition) { return true; }
    return false;
}

function code_search(settings, data) {
    const code = document.getElementById("code-filter").value;
    const currCode = data[1];

    if (code === "" || code === currCode) { return true; }
    return false;
}

$.fn.dataTable.ext.search.push(condition_search);
$.fn.dataTable.ext.search.push(length_search);
$.fn.dataTable.ext.search.push(code_search);
*/

export function filter(element, elementId) {
    // table.draw();
    const filterBlock = document.getElementById(elementId);
    const clear = filterBlock.getElementsByClassName("clear-filter").item(0);
    const header = filterBlock.getElementsByClassName("header").item(0);
    const checkbox = element.getElementsByTagName("span").item(0);

    checkbox.classList.toggle("selected");
    if (filterBlock.getElementsByClassName("selected").length) {
        header.classList.add("active");
        clear.hidden = false;
    } else {
        header.classList.remove("active");
        clear.hidden = true;
    }
}

export function toggle_column(element) {
    const checkbox = element.getElementsByClassName("checkbox").item(0);
    const column = table.column(element.dataset.column);
    checkbox.classList.toggle("selected");
    column.visible(!column.visible());
}
