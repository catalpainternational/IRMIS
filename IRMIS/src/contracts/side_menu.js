const tabs = document.querySelectorAll("#side-menu li");

tabs.forEach(tab => {
    if (location.pathname.includes("/" + tab.dataset.page + "/")) tab.classList.add("active");
    tab.addEventListener("click", (e) => {
        document.dispatchEvent(new CustomEvent("compare-changes", { detail: { nextUrl: e.target.dataset.list } }));
    });
});
