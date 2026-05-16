(function () {
    const header = document.querySelector(".site-header");
    if (header) {
        const onScroll = () => {
            header.classList.toggle("is-scrolled", window.scrollY > 24);
        };
        onScroll();
        window.addEventListener("scroll", onScroll, { passive: true });
    }

    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 700,
            easing: "ease-out-cubic",
            once: true,
            offset: 40,
        });
    }
})();
