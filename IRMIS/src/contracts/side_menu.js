const tabs = document.querySelectorAll("#side-menu li");

tabs.forEach(tab => {
    if (location.pathname.includes("/" + tab.dataset.page + "/")) tab.classList.add("active");
    tab.addEventListener("click", changeTab);
});

function changeTab(e) {
    const currTab = e.target;

    tabs.forEach(tab => {
        tab.isSameNode(currTab) ? currTab.classList.add("active") : tab.classList.remove("active");
    });

    location.href = currTab.dataset.list;
}
