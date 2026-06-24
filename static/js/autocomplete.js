/**
 * Debounced movie title autocomplete with optional poster thumbnails.
 */
(function () {
    function debounce(callback, waitMs) {
        let timerId;
        return (...args) => {
            clearTimeout(timerId);
            timerId = setTimeout(() => callback(...args), waitMs);
        };
    }

    function renderSuggestionItem(suggestion, onSelect) {
        const item = document.createElement("button");
        item.type = "button";
        item.className = "list-group-item list-group-item-action suggestion-item";

        if (typeof suggestion === "string") {
            item.textContent = suggestion;
            item.addEventListener("click", () => onSelect(suggestion));
            return item;
        }

        const posterSrc = suggestion.poster || window.MoviePosters.placeholder;
        item.innerHTML = `
            <img src="${posterSrc}" class="suggestion-poster" alt="" loading="lazy">
            <span class="suggestion-title">${suggestion.title}</span>
        `;
        item.addEventListener("click", () => onSelect(suggestion.title));
        return item;
    }

    function attach(inputSelector, listSelector, onSelect, minLength = 2) {
        const inputElement = document.querySelector(inputSelector);
        const listElement = document.querySelector(listSelector);

        if (!inputElement || !listElement) {
            return;
        }

        const fetchSuggestions = debounce(async () => {
            const query = inputElement.value.trim();
            listElement.innerHTML = "";

            if (query.length < minLength) {
                return;
            }

            try {
                const response = await fetch(`/api/title_suggest?q=${encodeURIComponent(query)}`);
                const payload = await response.json();
                (payload.results || []).forEach((suggestion) => {
                    listElement.appendChild(renderSuggestionItem(suggestion, onSelect));
                });
            } catch (error) {
                console.error("Autocomplete request failed:", error);
            }
        }, 250);

        inputElement.addEventListener("input", fetchSuggestions);

        document.addEventListener("click", (event) => {
            if (!listElement.contains(event.target) && event.target !== inputElement) {
                listElement.innerHTML = "";
            }
        });
    }

    window.MovieAutocomplete = { attach };
})();
