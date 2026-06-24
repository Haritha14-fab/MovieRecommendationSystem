"""Shared helpers."""

import logging
from functools import wraps

from flask import redirect, session, url_for

from services.poster_service import get_movie_poster

logger = logging.getLogger(__name__)


def movie_detail_url(movie_title: str) -> str:
    """Build the canonical movie detail URL for a title."""
    return url_for("pages.movie_query", title=movie_title)


def login_required(view_function):
    """Redirect anonymous users to the login page."""

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        return view_function(*args, **kwargs)

    return wrapped_view


def build_movie_card(movie_title: str) -> dict:
    """Build a template-friendly movie card payload."""
    return {
        "title": movie_title,
        "poster": get_movie_poster(movie_title),
        "url": movie_detail_url(movie_title),
    }


def track_viewed_movie(movie_title: str) -> None:
    """Keep a short recently-viewed list in the user session."""
    if not movie_title:
        return

    history = session.get("view_history", [])
    history = [title for title in history if title != movie_title]
    history.insert(0, movie_title)
    session["view_history"] = history[:12]
    session.modified = True
