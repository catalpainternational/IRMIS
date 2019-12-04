const asset_manager = document.getElementById("asset_manager_button");
const reports = document.getElementById("reports_button");
const planning = document.getElementById("planning_button");
const menuToggle = document.getElementById("topmenu_toggle");
const dropdown = document.getElementById("settings");

window.addEventListener("load", function() {
    menuToggle.addEventListener("click", () => {
        function clickOutside(e) {
            if (!menuToggle.contains(e.target)) {
                dropdown.hidden = true;
            }
        }

        if (dropdown.hidden) document.addEventListener("click", clickOutside);
        else document.removeEventListener("click", clickOutside);

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
    if (/#reports\/(\d?)/.exec(location.hash)) {
        asset_manager.classList.remove("selected");
        reports.classList.add("selected");
        planning.classList.remove("selected");
    } else if (/#planning/.exec(location.hash)) {
        asset_manager.classList.remove("selected");
        reports.classList.remove("selected");
        planning.classList.add("selected");
    } else {
        asset_manager.classList.add("selected");
        reports.classList.remove("selected");
        planning.classList.remove("selected");
    }
}
