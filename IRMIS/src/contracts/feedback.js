document.addEventListener("show-banner", (e) => {
    visibleBanner = e.detail.banner;
    visibleBanner.classList.remove("d-none");
    setTimeout(() => closeFeedback(), 2000);
    visibleBanner.querySelector("#close-banner").addEventListener("click", closeFeedback);
});

let visibleBanner = document.getElementById("message-banner");
let params = new URL(document.location).searchParams;

if (visibleBanner) {
    setTimeout(() => closeFeedback(), 2000);
    visibleBanner.querySelector("#close-banner").addEventListener("click", closeFeedback);
}

if (params.get("banner")) {
    document.dispatchEvent(new CustomEvent("show-banner", { detail: { banner: document.getElementById("success-banner") } }));
}

function closeFeedback() {
    const element = visibleBanner.getElementsByClassName("slide-in").item(0);

    element.classList.add("slide-out");
    setTimeout(() => {
        element.classList.remove("slide-out");
        visibleBanner.classList.add("d-none");
    }, 300);
}
