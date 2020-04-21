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
    ".form-control.asset-code": {
        options: {
            width: "100%",
            tags: true,
            containerCssClass: "form-control form-control-lg contracts-select2 asset-code",
            dropdownCssClass: "contracts-dropdown-select2",
        },
   
    }
};

window.addEventListener("load", () => {
    // Convert class selectors to actual Ids
    Object.keys(contractSelects).forEach((selectKey) => {
        if (selectKey.startsWith(".")) {
            const elements = $(selectKey);
            elements.each((ix, element) => {
                const id = `#${element.id}`;
                const definition = JSON.parse(JSON.stringify(contractSelects[selectKey]));
                contractSelects[id] = definition;
            });
        }
    })

    Object.keys(contractSelects).forEach((selectKey) => {
        if (selectKey.startsWith("#")) {
            $(selectKey).select2(contractSelects[selectKey].options);
            $(selectKey).on('select2:select', contractSelects[selectKey].on);
            $(selectKey).on('select2:unselect', contractSelects[selectKey].off);
        }
    });
});

function toggleMultipleSelect2(e) {
    const selectElement = e.currentTarget;
    const inputElement = selectElement.nextSibling.children.item(0).firstElementChild;

    if (selectElement.value !== "") {
        inputElement.classList.add("active");
    } else {
        inputElement.classList.remove("active");
    }
};
