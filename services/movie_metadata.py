"""External movie metadata lookup via OMDb."""

import logging
import re

import requests

from config import Config

logger = logging.getLogger(__name__)


def fetch_movie_details(movie_title: str) -> dict:
    """Return plot, cast, and rating metadata for a movie title."""
    if not movie_title or not Config.OMDB_API_KEY:
        return {}

    lookup_title = re.sub(r"\s*\(\d{4}\)\s*$", "", movie_title.strip())

    try:
        response = requests.get(
            Config.OMDB_API_URL,
            params={"apikey": Config.OMDB_API_KEY, "t": lookup_title},
            timeout=8,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.warning("OMDb metadata lookup failed for '%s': %s", movie_title, exc)
        return {}
