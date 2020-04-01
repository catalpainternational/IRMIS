import * as riot from "riot";

import Top_Menu from "./riot/top_menu.riot.html";

riot.register("top_menu", Top_Menu);
riot.mount("top_menu");

window.addEventListener("load", function() {
    const menuToggle = document.getElementById("topmenu_toggle");
    const dropdown = document.getElementById("settings");

    menuToggle.addEventListener("click", () => {
        function clickOutside(e) {
            if (!menuToggle.contains(e.target)) {
                dropdown.hidden = true;
            }
        }

        if (dropdown.hidden) {
            document.addEventListener("click", clickOutside);
        } else {
            document.removeEventListener("click", clickOutside);
        }

        dropdown.hidden = !dropdown.hidden;
    });

    dropdown.addEventListener("click", (e) => {
        e.stopPropagation();
    });

    hashCheck();
});

window.addEventListener("hashchange", () => {
    hashCheck();
});

function hashCheck() {
    const asset_manager = document.getElementById("asset_manager_button");
    const reports = document.getElementById("reports_button");
    const planning = document.getElementById("planning_button");
    const contracts = document.getElementById("contracts_button");

    asset_manager.classList.remove("selected");
    reports.classList.remove("selected");
    planning.classList.remove("selected");
    contracts.classList.remove("selected");

    if (/#reports\/(.*)\/?/.exec(location.hash)) {
        reports.classList.add("selected");
    } else if (/#planning/.exec(location.hash)) {
        planning.classList.add("selected");
    } else if (/contracts/.exec(location.pathname)) {
        contracts.classList.add("selected");
    } else {
        asset_manager.classList.add("selected");
    }
}
