"""MovieLens catalog loading and title search helpers."""

import logging

import pandas as pd

from config import Config

logger = logging.getLogger(__name__)


class MovieCatalog:
    """In-memory catalog built from the MovieLens u.item file."""

    def __init__(self, dataset_path: str | None = None):
        self.dataset_path = dataset_path or Config.MOVIELENS_ITEM_PATH
        self.movies_df = pd.DataFrame(columns=["movie_id", "title"])
        self.movie_titles: list[str] = []
        self._load_dataset()

    def _load_dataset(self) -> None:
        """Load movie IDs and titles from the MovieLens item file."""
        try:
            raw_df = pd.read_csv(
                self.dataset_path,
                sep="|",
                encoding="latin-1",
                header=None,
            )
            self.movies_df = raw_df.iloc[:, :2].copy()
            self.movies_df.columns = ["movie_id", "title"]
            self.movie_titles = (
                self.movies_df["title"].fillna("").astype(str).tolist()
            )
            logger.info("Loaded %d movies from MovieLens catalog", len(self.movie_titles))
        except Exception as exc:
            logger.error("Failed to load MovieLens dataset: %s", exc)
            self.movies_df = pd.DataFrame(columns=["movie_id", "title"])
            self.movie_titles = []

    def resolve_title(self, query: str) -> str:
        """Match a user query to the closest catalog title."""
        cleaned_query = (query or "").strip()
        if not cleaned_query:
            return ""

        query_lower = cleaned_query.lower()

        for title in self.movie_titles:
            if title.lower() == query_lower:
                return title

        for title in self.movie_titles:
            if query_lower in title.lower():
                return title

        return cleaned_query

    def search_substring(self, query: str, limit: int = 10) -> list[str]:
        """Return titles containing the query string."""
        normalized = (query or "").lower().strip()
        if not normalized:
            return []

        matches = []
        for title in self.movie_titles:
            if normalized in title.lower():
                matches.append(title)
            if len(matches) >= limit:
                break
        return matches

    def suggest_titles(self, query: str, limit: int = 10) -> list[str]:
        """Return prefix matches first, then substring matches."""
        normalized = (query or "").lower().strip()
        if not normalized:
            return []

        prefix_matches = []
        substring_matches = []

        for title in self.movie_titles:
            title_lower = title.lower()
            if title_lower.startswith(normalized):
                prefix_matches.append(title)
            elif normalized in title_lower:
                substring_matches.append(title)

            if len(prefix_matches) + len(substring_matches) >= limit:
                break

        return (prefix_matches + substring_matches)[:limit]

    def get_trending_titles(self, count: int | None = None) -> list[str]:
        """Return a slice of catalog titles for the trending section."""
        limit = count or Config.TRENDING_MOVIE_COUNT
        # MovieLens file order is stable; first N titles work as a browse set.
        return self.movie_titles[:limit]

    def get_homepage_titles(self, count: int | None = None) -> list[str]:
        """Titles shown on the authenticated home page."""
        limit = count or Config.HOME_MOVIE_COUNT
        return self.movie_titles[:limit]
