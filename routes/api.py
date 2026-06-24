"""JSON API routes."""

from flask import Blueprint, current_app, jsonify, request

from services.poster_service import get_movie_poster
from services.r_pipeline import get_r_output_status, run_r_script

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/search")
def search_movies():
    """Substring movie search used by older clients."""
    catalog = current_app.extensions["movie_catalog"]
    query = request.args.get("q", "").lower().strip()

    if not query:
        return jsonify({"results": []})

    return jsonify({"results": catalog.search_substring(query)})


@api_bp.route("/title_suggest")
def title_suggest():
    """Autocomplete suggestions with poster URLs for richer UI."""
    catalog = current_app.extensions["movie_catalog"]
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"results": []})

    titles = catalog.suggest_titles(query)
    suggestions = [
        {
            "title": title,
            "poster": get_movie_poster(title),
        }
        for title in titles
    ]
    return jsonify({"results": suggestions})


@api_bp.route("/recommend")
def recommend():
    """Hybrid recommendations for a movie title."""
    catalog = current_app.extensions["movie_catalog"]
    engine = current_app.extensions["recommendation_engine"]

    raw_title = request.args.get("title", "")
    top_n = int(request.args.get("topn", 12))
    resolved_title = catalog.resolve_title(raw_title)

    results = engine.hybrid_recommend(resolved_title, top_n)
    return jsonify({"title": resolved_title, "results": results})


@api_bp.route("/recommend_ai")
def recommend_ai():
    """Python-only recommendations without the R pipeline."""
    engine = current_app.extensions["recommendation_engine"]
    raw_title = request.args.get("title", "")
    top_n = int(request.args.get("topn", 10))

    results = engine.recommend_ai_only(raw_title, top_n)
    return jsonify({"results": results})


@api_bp.route("/poster")
def poster():
    """Return a poster URL for a single movie title."""
    movie_title = request.args.get("title", "")
    return jsonify({"url": get_movie_poster(movie_title)})


@api_bp.route("/run_r", methods=["POST"])
def run_r():
    """Manually trigger an approved R script."""
    payload = request.get_json(silent=True) or {}
    script_name = payload.get("script")

    try:
        result = run_r_script(script_name)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"stdout": result.stdout, "stderr": result.stderr})


@api_bp.route("/r/status")
def r_status():
    """Expose R output file availability."""
    return jsonify(get_r_output_status())
