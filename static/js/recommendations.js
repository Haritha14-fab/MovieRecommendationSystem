document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("recSearch");
    const cardsContainer = document.getElementById("cards");
    const loadingBlock = document.getElementById("loading");
    const pageTitle = document.querySelector("h1 .text-primary")?.textContent?.trim() || searchInput?.value?.trim() || "";

    if (searchInput) {
        MovieAutocomplete.attach("#recSearch", "#recSuggestions", (title) => {
            window.location.href = `/recommendations?title=${encodeURIComponent(title)}`;
        });
    }

    async function renderRecommendations(title) {
        if (!cardsContainer || !loadingBlock) {
            return;
        }

        loadingBlock.classList.remove("d-none");
        cardsContainer.innerHTML = "";

        try {
            const response = await fetch(`/api/recommend?title=${encodeURIComponent(title)}&topn=12`);
            const payload = await response.json();
            loadingBlock.classList.add("d-none");

            if (!payload.results || payload.results.length === 0) {
                cardsContainer.innerHTML = `<div class="col-12 text-center text-muted"><p>No recommendations found.</p></div>`;
                return;
            }

            payload.results.forEach((movie) => {
                const column = document.createElement("div");
                column.className = "col-lg-3 col-md-4 col-sm-6 mb-4";
                column.innerHTML = `
                    <div class="card movie-card h-100 shadow-sm">
                        <div class="poster-wrap">
                            <img src="${window.MoviePosters.placeholder}" data-src="${movie.poster}"
                                 class="card-img-top movie-poster lazy-poster" alt="${movie.title}" loading="lazy">
                            <div class="poster-spinner spinner-border text-light" role="status"></div>
                        </div>
                        <div class="card-body d-flex flex-column text-center">
                            <h6 class="card-title text-truncate">${movie.title}</h6>
                            <a href="/movie.html?title=${encodeURIComponent(movie.title)}"
                               class="btn btn-primary btn-sm mt-auto">View Details</a>
                        </div>
                    </div>
                `;
                cardsContainer.appendChild(column);
            });

            window.MoviePosters.init(cardsContainer);
        } catch (error) {
            loadingBlock.classList.add("d-none");
            cardsContainer.innerHTML = `<div class="col-12 text-center text-danger"><p>Could not load recommendations.</p></div>`;
            console.error(error);
        }
    }

    // Server-rendered cards are already present; only fetch client-side when empty.
    if (cardsContainer && cardsContainer.children.length === 0 && pageTitle) {
        renderRecommendations(pageTitle);
    }
});
