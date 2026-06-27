"""Flask application factory."""

import logging
import os
import secrets

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import Config
from database.user_store import init_user_database
from routes.api import api_bp
from routes.auth import auth_bp
from routes.pages import pages_bp
from services.movie_catalog import MovieCatalog
from services.recommendation_engine import RecommendationEngine

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app(config_class: type[Config] = Config) -> Flask:
    """Build and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder=os.path.join(PROJECT_ROOT, "templates"),
        static_folder=os.path.join(PROJECT_ROOT, "static"),
    )
    app.config.from_object(config_class)

    if not app.config.get("SECRET_KEY") or app.config["SECRET_KEY"] == "dev-secret-change-in-production":
        app.secret_key = secrets.token_hex(32)
    else:
        app.secret_key = config_class.SECRET_KEY

    app.permanent_session_lifetime = config_class.PERMANENT_SESSION_LIFETIME

    # Initialize CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    init_user_database()

    movie_catalog = MovieCatalog()
    recommendation_engine = RecommendationEngine(movie_catalog)

    app.extensions["movie_catalog"] = movie_catalog
    app.extensions["recommendation_engine"] = recommendation_engine

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def inject_helpers():
        """Expose small helpers to Jinja templates."""
        return {"placeholder_poster": Config.PLACEHOLDER_POSTER}

    return app
