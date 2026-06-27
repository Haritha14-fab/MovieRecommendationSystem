"""Page routes for authenticated browsing."""

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from config import Config
from services.movie_metadata import fetch_movie_details
from services.poster_service import get_movie_poster
from utils.helpers import build_movie_card, login_required, track_viewed_movie

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
@login_required
def home():
    """Home page with search and trending movie cards."""
    catalog = current_app.extensions["movie_catalog"]
    homepage_titles = catalog.get_homepage_titles()
    trending_titles = catalog.get_trending_titles()

    movies = [build_movie_card(title) for title in homepage_titles]
    trending_movies = [build_movie_card(title) for title in trending_titles]

    return render_template(
        "index.html",
        user=session["user"],
        movies=movies,
        trending_movies=trending_movies,
    )


@pages_bp.route("/search")
@pages_bp.route("/search.html")
@login_required
def search_page():
    """Show the searched movie and hybrid recommendations."""
    catalog = current_app.extensions["movie_catalog"]
    engine = current_app.extensions["recommendation_engine"]

    raw_title = request.args.get(
        "title",
        request.args.get("movie", request.args.get("q", "")),
    )
    resolved_title = catalog.resolve_title(raw_title)

    if not resolved_title:
        return redirect(url_for("pages.home"))

    recommendations = engine.hybrid_recommend(
        resolved_title,
        Config.DEFAULT_RECOMMENDATION_COUNT,
    )

    return render_template(
        "search.html",
        movie=build_movie_card(resolved_title),
        recommendations=recommendations,
    )


@pages_bp.route("/recommendations")
@pages_bp.route("/recommendation.html")
@login_required
def recommendations_page():
    """Dedicated recommendations view for a selected title."""
    catalog = current_app.extensions["movie_catalog"]
    engine = current_app.extensions["recommendation_engine"]

    raw_title = request.args.get("title", "")
    resolved_title = catalog.resolve_title(raw_title)
    recommendation_list = engine.hybrid_recommend(
        resolved_title,
        Config.DEFAULT_RECOMMENDATION_COUNT,
    )

    return render_template(
        "recommendations.html",
        title=resolved_title,
        recommendations=recommendation_list,
    )


@pages_bp.route("/profile")
@login_required
def profile():
    """User profile with personalized picks and browsing history."""
    catalog = current_app.extensions["movie_catalog"]
    engine = current_app.extensions["recommendation_engine"]

    seed_title = catalog.movie_titles[0] if catalog.movie_titles else ""
    personalized = engine.recommend_by_embedding(seed_title, 8)

    history_titles = session.get("view_history", [])
    history_movies = [build_movie_card(title) for title in history_titles]

    return render_template(
        "profile.html",
        user=session["user"],
        movie_count=len(catalog.movie_titles),
        recommendations=personalized,
        history_movies=history_movies,
    )


@pages_bp.route("/movie/<title>")
@login_required
def movie_detail(title):
    """Movie detail page with metadata and similar titles."""
    engine = current_app.extensions["recommendation_engine"]
    resolved_title = current_app.extensions["movie_catalog"].resolve_title(title)

    track_viewed_movie(resolved_title)
    similar_movies = engine.hybrid_recommend(resolved_title, 10)

    return render_template(
        "movie.html",
        title=resolved_title,
        poster=get_movie_poster(resolved_title),
        placeholder_poster="/static/images/no-poster.svg",
        details=fetch_movie_details(resolved_title),
        trailer=f"https://www.youtube.com/results?search_query={resolved_title}+trailer",
        watch=f"https://www.youtube.com/results?search_query={resolved_title}+full+movie",
        recommendations=similar_movies,
    )




@pages_bp.route("/movie")
@pages_bp.route("/movie.html")
@login_required
def movie_query():
    """Movie detail page reached via query string."""
    raw_title = request.args.get("title", "")
    resolved_title = current_app.extensions["movie_catalog"].resolve_title(raw_title)

    if not resolved_title:
        return redirect(url_for("pages.home"))

    return movie_detail(resolved_title)
