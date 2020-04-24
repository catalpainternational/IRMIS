import "select2/dist/js/select2.full.min.js";
import $ from "jquery";

const contractSelects = {
    "#id_projects": {
        options: {
            width: "100%",
            containerCssClass: "form-control contracts-select2",
            dropdownCssClass: "contracts-dropdown-select2",
        },
        on: toggleMultipleSelect2,
        off: toggleMultipleSelect2,
    },
    ".asset-code": {
        options: {
            width: "100%",
            tags: true,            
            placeholder: "A01-01",
            allowClear: true,
            containerCssClass: "form-control form-control-lg contracts-select2 asset-code",
            dropdownCssClass: "contracts-dropdown-select2",
        },
    }
};

document.addEventListener("prepare-select2", (data) => {
    const dataTable = data.detail.dataTable;
    const select2Element = `#${data.detail.id}`;
    const placeHolder = data.detail.placeHolder;

    contractSelects[select2Element] = contractSelects[select2Element] ||
    {
        options: {
            width: "unset",
            containerCssClass: "contract-criteria-select2",
            dropdownCssClass: "contract-criteria-dropdown-select2",
            placeholder: placeHolder,
        },
        on: (e) => searchDataTable(dataTable, e),
        off: (e) => searchDataTable(dataTable, e),
    };

    processContractSelects();
});

window.addEventListener("load", () => {
    processContractSelects();
});

function processContractSelects() {
    Object.keys(contractSelects).forEach((selectKey) => {
        if (selectKey.startsWith(".") && !contractSelects[selectKey].processed) {
            const elements = $(selectKey);
            elements.each((_ix, element) => {
                const id = `#${element.id}`;
                contractSelects[id] = JSON.parse(JSON.stringify(contractSelects[selectKey]));
                instantiateSelect2(id);
            });
        } else {
            instantiateSelect2(selectKey);
        }
    });

    function instantiateSelect2(selectKey) {
        $(selectKey).select2(contractSelects[selectKey].options);
        $(selectKey).on('select2:select', contractSelects[selectKey].on);
        $(selectKey).on('select2:unselect', contractSelects[selectKey].off);
    }
}

function toggleMultipleSelect2(e) {
    const selectElement = e.currentTarget;
    const inputElement = selectElement.nextSibling.children.item(0).firstElementChild;

    if (selectElement.value !== "") {
        inputElement.classList.add("active");
    } else {
        inputElement.classList.remove("active");
    }
};

function searchDataTable(dataTable, e) {
    const selectElement = e.currentTarget;
    const inputElement = selectElement.nextSibling.children.item(0).firstElementChild;

    if (selectElement.value !== "") {
        inputElement.classList.add("active");
    } else {
        inputElement.classList.remove("active");
    }

    dataTable.draw();
}
