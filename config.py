"""Application configuration loaded from environment variables."""

import os
from datetime import timedelta

from dotenv import load_dotenv

# Load .env but don't let malformed lines spam warnings / break startup.
# If your .env is invalid, warnings are annoying; parsing errors should be non-fatal.
load_dotenv(override=False, verbose=False, dotenv_path=None)



class Config:
    """Central config for the Flask movie recommendation app."""

    SECRET_KEY = os.environ.get("FLASK_SECRET", "dev-secret-change-in-production")
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    DATABASE_PATH = os.environ.get("DATABASE_PATH", "users.db")
    MOVIELENS_ITEM_PATH = os.environ.get(
        "MOVIELENS_ITEM_PATH", "Dataset/ml-100k/u.item"
    )

    TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY") or "4c8b368d"

    TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
    TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w500"
    OMDB_API_URL = "https://www.omdbapi.com/"

    POSTER_CACHE_PATH = os.environ.get(
        "POSTER_CACHE_PATH", "cache/poster_cache.json"
    )
    PLACEHOLDER_POSTER = "/static/images/no-poster.svg"

    R_RECOMMENDATIONS_PATH = os.environ.get(
        "R_RECOMMENDATIONS_PATH", "Output/recommendations.csv"
    )
    RSCRIPT_CMD = os.environ.get("RSCRIPT_CMD", "Rscript")
    ALLOW_R_PIPELINE = os.environ.get("ALLOW_R_PIPELINE", "true").lower() == "true"

    USE_TRANSFORMERS = os.environ.get("USE_TRANSFORMERS", "0") == "1"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

    HOME_MOVIE_COUNT = 20
    TRENDING_MOVIE_COUNT = 12
    DEFAULT_RECOMMENDATION_COUNT = 12
