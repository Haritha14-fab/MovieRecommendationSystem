/**
 * Shared poster loading: lazy fetch, spinner, and broken-image fallback.
 */
(function () {
    const PLACEHOLDER = "/static/images/no-poster.svg";

    function hideSpinner(imageElement) {
        const wrapper = imageElement.closest(".poster-wrap");
        if (wrapper) {
            const spinner = wrapper.querySelector(".poster-spinner");
            if (spinner) {
                spinner.classList.add("d-none");
            }
        }
    }

    function applyFallback(imageElement) {
        imageElement.onerror = null;
        imageElement.src = PLACEHOLDER;
        hideSpinner(imageElement);
    }

    function loadPoster(imageElement) {
        const posterUrl = imageElement.dataset.src;
        if (!posterUrl || posterUrl === PLACEHOLDER) {
            imageElement.src = PLACEHOLDER;
            hideSpinner(imageElement);
            return;
        }

        imageElement.onload = () => hideSpinner(imageElement);
        imageElement.onerror = () => applyFallback(imageElement);
        imageElement.src = posterUrl;
        imageElement.classList.add("is-loaded");
    }

    function initLazyPosters(root) {
        const scope = root || document;
        scope.querySelectorAll("img.lazy-poster").forEach((imageElement) => {
            if (imageElement.dataset.loaded === "true") {
                return;
            }
            imageElement.dataset.loaded = "true";
            loadPoster(imageElement);
        });
    }

    window.MoviePosters = {
        init: initLazyPosters,
        placeholder: PLACEHOLDER,
    };

    document.addEventListener("DOMContentLoaded", () => initLazyPosters());
})();
