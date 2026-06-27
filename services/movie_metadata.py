"""Movie metadata lookup.

Primary: OMDb (title + optional year)
Fallback: TMDb (search + details)

Return value is shaped to match OMDb keys used by templates:
- imdbRating
- Genre
- Director
- Actors
- Plot
"""

import logging
import re
from typing import Optional

import requests

from config import Config

logger = logging.getLogger(__name__)


def _split_title_and_year(raw_title: str) -> tuple[str, Optional[str]]:
    """Extract trailing (YYYY) if present."""
    raw = (raw_title or "").strip()
    year_match = re.search(r"\s*\((\d{4})\)\s*$", raw)
    year = year_match.group(1) if year_match else None
    title_without_year = re.sub(r"\s*\(\d{4}\)\s*$", "", raw).strip() or raw
    return title_without_year, year


def _omdb_lookup(movie_title: str, year: Optional[str] = None) -> dict | None:
    if not Config.OMDB_API_KEY:
        return None

    params = {"apikey": Config.OMDB_API_KEY, "t": movie_title}
    if year:
        params["y"] = year

    try:
        response = requests.get(Config.OMDB_API_URL, params=params, timeout=8)
        response.raise_for_status()
        payload = response.json() or {}

        # OMDb returns Response="False" on miss.
        if payload.get("Response") == "False":
            return None

        return payload
    except requests.RequestException as exc:
        logger.warning(
            "OMDb metadata lookup failed for '%s' with params %s: %s",
            movie_title,
            params,
            exc,
        )
        return None


def _search_tmdb_movie(movie_title: str) -> Optional[int]:
    """Return TMDb movie_id for the best match."""
    if not Config.TMDB_API_KEY:
        return None

    try:
        resp = requests.get(
            Config.TMDB_SEARCH_URL,
            params={
                "api_key": Config.TMDB_API_KEY,
                "query": movie_title,
                "include_adult": "false",
            },
            timeout=8,
        )
        resp.raise_for_status()
        results = resp.json().get("results", []) or []
        if not results:
            return None

        # Prefer highest vote_average then popularity.
        # (best-effort; we don't have year match here)
        results_sorted = sorted(
            results,
            key=lambda r: (r.get("vote_average", 0), r.get("popularity", 0)),
            reverse=True,
        )
        return results_sorted[0].get("id")
    except requests.RequestException as exc:
        logger.warning("TMDb search failed for '%s': %s", movie_title, exc)
        return None


def _tmdb_details_to_omdb_shape(movie_id: int) -> dict | None:
    """Fetch TMDb details and map to OMDb-like keys."""
    if not Config.TMDB_API_KEY:
        return None

    tmdb_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    tmdb_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    try:
        # Details
        details_resp = requests.get(
            tmdb_details_url,
            params={"api_key": Config.TMDB_API_KEY, "language": "en-US"},
            timeout=8,
        )
        details_resp.raise_for_status()
        details = details_resp.json() or {}

        # Credits (for director + actors)
        credits_resp = requests.get(
            tmdb_credits_url,
            params={"api_key": Config.TMDB_API_KEY, "language": "en-US"},
            timeout=8,
        )
        credits_resp.raise_for_status()
        credits = credits_resp.json() or {}

        # Director
        director_names = []
        for crew in credits.get("crew", []) or []:
            if crew.get("job") == "Director":
                name = crew.get("name")
                if name:
                    director_names.append(name)
        director = ", ".join(director_names) if director_names else "N/A"

        # Actors (top billed)
        cast = credits.get("cast", []) or []
        actor_names = [c.get("name") for c in cast[:6] if c.get("name")]
        actors = ", ".join(actor_names) if actor_names else "N/A"

        # Genres
        genre_list = details.get("genres", []) or []
        genres = ", ".join([g.get("name") for g in genre_list if g.get("name")])
        genres = genres if genres else "N/A"

        # Plot
        plot = details.get("overview") or ""

        # imdbRating: TMDb doesn't provide IMDb rating reliably without extra endpoints.
        # Keep key for template compatibility; show N/A when missing.
        return {
            "imdbRating": "N/A",
            "Genre": genres,
            "Director": director,
            "Actors": actors,
            "Plot": plot or "No description available.",
        }

    except requests.RequestException as exc:
        logger.warning("TMDb details fetch failed for movie_id=%s: %s", movie_id, exc)
        return None


def fetch_movie_details(movie_title: str) -> dict:
    """Return plot, cast, and rating metadata for a movie title."""

    if not movie_title:
        return {}

    raw_title = movie_title.strip()
    title_without_year, year = _split_title_and_year(raw_title)

    # OMDb-first: try year-aware, then no-year, then full string.
    if year:
        payload = _omdb_lookup(title_without_year, year=year)
        if payload:
            return payload

    payload = _omdb_lookup(title_without_year, year=None)
    if payload:
        return payload

    payload = _omdb_lookup(raw_title, year=None)
    if payload:
        return payload

    # TMDb fallback when OMDb fails.
    tmdb_id = _search_tmdb_movie(title_without_year)
    if tmdb_id:
        tmdb_payload = _tmdb_details_to_omdb_shape(tmdb_id)
        if tmdb_payload:
            return tmdb_payload

    return {}


