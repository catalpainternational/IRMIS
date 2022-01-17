const nav = document.querySelectorAll("nav a[data-next]");

nav.forEach(tab => {
    tab.addEventListener("click", (e) => {
        document.dispatchEvent(new CustomEvent("compare-changes", { detail: { nextUrl: e.currentTarget.dataset.next } }));
    });
});
