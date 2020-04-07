if (document.getElementById("feedback-banner")) {
    setTimeout(() => closeFeedback(), 2000);
    document.getElementById("close-banner").addEventListener("click", closeFeedback);
}

function closeFeedback() {
    const banner = document.getElementsByClassName("slide-in").item(0);

    banner.classList.add("slide-out");
}
