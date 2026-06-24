document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("movieInput");
    const searchForm = document.getElementById("movieSearchForm");
    const recommendButton = document.getElementById("recommendBtn");

    if (searchInput) {
        MovieAutocomplete.attach("#movieInput", "#suggestions", (title) => {
            searchInput.value = title;
            document.getElementById("suggestions").innerHTML = "";
        });
    }

    if (searchForm) {
        searchForm.addEventListener("submit", (event) => {
            if (!searchInput.value.trim()) {
                event.preventDefault();
                searchInput.focus();
            }
        });
    }

    if (recommendButton && searchInput) {
        recommendButton.addEventListener("click", () => {
            const title = searchInput.value.trim();
            if (!title) {
                searchInput.focus();
                return;
            }
            window.location.href = `/recommendation.html?title=${encodeURIComponent(title)}`;
        });
    }
});
