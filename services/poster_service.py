"""Movie poster lookup with TMDb, OMDb fallback, and local caching."""

import json
import logging
import os
import re
import threading
from typing import Optional

import requests

from config import Config

logger = logging.getLogger(__name__)

_cache_lock = threading.Lock()
_poster_cache: dict[str, str] = {}


def _normalize_title(movie_title: str) -> str:
    """Normalize a movie title for consistent cache keys."""
    cleaned = re.sub(r"\s+", " ", (movie_title or "").strip())
    return cleaned.lower()


def _title_for_api_lookup(movie_title: str) -> str:
    """Strip MovieLens-style release years before external API lookup."""
    cleaned = re.sub(r"\s+", " ", (movie_title or "").strip())
    without_year = re.sub(r"\s*\(\d{4}\)\s*$", "", cleaned)
    return without_year or cleaned


def _load_cache_from_disk() -> None:
    """Load poster URL cache from the JSON file."""
    global _poster_cache

    cache_path = Config.POSTER_CACHE_PATH
    if not os.path.exists(cache_path):
        return

    try:
        with open(cache_path, "r", encoding="utf-8") as cache_file:
            _poster_cache = json.load(cache_file)
        logger.info("Loaded %d cached poster URLs", len(_poster_cache))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read poster cache: %s", exc)
        _poster_cache = {}


def _save_cache_to_disk() -> None:
    """Persist the in-memory poster cache."""
    cache_path = Config.POSTER_CACHE_PATH
    cache_dir = os.path.dirname(cache_path)

    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)

    try:
        with open(cache_path, "w", encoding="utf-8") as cache_file:
            json.dump(_poster_cache, cache_file, indent=2, sort_keys=True)
    except OSError as exc:
        logger.warning("Could not write poster cache: %s", exc)


def _search_tmdb_poster(movie_title: str) -> Optional[str]:
    """Search TMDb for a movie and return its poster URL."""
    if not Config.TMDB_API_KEY:
        return None

    try:
        response = requests.get(
            Config.TMDB_SEARCH_URL,
            params={
                "api_key": Config.TMDB_API_KEY,
                "query": movie_title,
                "include_adult": "false",
            },
            timeout=8,
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        for match in results:
            poster_path = match.get("poster_path")
            if poster_path:
                return f"{Config.TMDB_POSTER_BASE}{poster_path}"

    except requests.RequestException as exc:
        logger.debug("TMDb lookup failed for '%s': %s", movie_title, exc)

    return None


def _search_omdb_poster(movie_title: str) -> Optional[str]:
    """Fetch a poster URL from the OMDb API."""
    if not Config.OMDB_API_KEY:
        return None

    try:
        response = requests.get(
            Config.OMDB_API_URL,
            params={"apikey": Config.OMDB_API_KEY, "t": movie_title},
            timeout=8,
        )
        response.raise_for_status()
        poster_url = response.json().get("Poster", "")

        if poster_url and poster_url != "N/A":
            return poster_url

    except requests.RequestException as exc:
        logger.debug("OMDb lookup failed for '%s': %s", movie_title, exc)

    return None


def get_movie_poster(movie_title: str) -> str:
    """Return a poster URL for a movie title.

    Lookup order:
    1. Local cache
    2. TMDb API
    3. OMDb API
    4. Static placeholder image
    """
    if not movie_title or not movie_title.strip():
        return Config.PLACEHOLDER_POSTER

    cache_key = _normalize_title(movie_title)

    with _cache_lock:
        if not _poster_cache and os.path.exists(Config.POSTER_CACHE_PATH):
            _load_cache_from_disk()

        cached_url = _poster_cache.get(cache_key)
        if cached_url:
            return cached_url

    poster_url = _search_tmdb_poster(_title_for_api_lookup(movie_title))

    if not poster_url:
        poster_url = _search_omdb_poster(_title_for_api_lookup(movie_title))

    if not poster_url:
        poster_url = Config.PLACEHOLDER_POSTER

    with _cache_lock:
        _poster_cache[cache_key] = poster_url
        _save_cache_to_disk()

    return poster_url


def warm_poster_cache(movie_titles: list[str]) -> None:
    """Pre-fetch posters for a list of titles (used on startup for home page)."""
    for title in movie_titles:
        try:
            get_movie_poster(title)
        except Exception as exc:
            logger.warning("Poster warm-up failed for '%s': %s", title, exc)


# Backward-compatible alias used by older code paths.
get_poster = get_movie_poster
