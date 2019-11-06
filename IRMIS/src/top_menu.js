const topMenuItems = document.getElementById("top-navigation").children;
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

    for (let item of topMenuItems) {
        item.addEventListener("click", (e) => {
            if (!item.classList.contains("selected")) {
                for (let item of topMenuItems) {
                    item.classList.remove("selected");
                }
                e.target.classList.add("selected");
            }
        });
    }
});

dropdown.addEventListener("click", (e) => {
    e.stopPropagation();
});
