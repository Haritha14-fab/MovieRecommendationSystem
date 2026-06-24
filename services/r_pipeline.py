"""R recommenderlab pipeline integration."""

import logging
import os
import subprocess

import pandas as pd

from config import Config
from services.poster_service import get_movie_poster

logger = logging.getLogger(__name__)

ALLOWED_R_SCRIPTS = frozenset(
    {"Run_All", "Recommendation", "Hybrid_model", "Evaluation"}
)

R_OUTPUT_FILES = {
    "recommendations": Config.R_RECOMMENDATIONS_PATH,
    "evaluation": os.path.join("Output", "evaluation_results.csv"),
    "optimization": os.path.join("Output", "optimization_results.csv"),
    "hybrid_matrix": os.path.join("Output", "hybrid_matrix.csv"),
}


def run_r_pipeline_if_needed() -> bool:
    """Run the full R pipeline when recommendation output is missing."""
    if os.path.exists(Config.R_RECOMMENDATIONS_PATH):
        return True

    if not Config.ALLOW_R_PIPELINE:
        logger.info("R pipeline auto-run disabled by configuration")
        return False

    script_path = os.path.join("Scripts", "Run_All.R")
    try:
        subprocess.run(
            [Config.RSCRIPT_CMD, script_path],
            capture_output=True,
            text=True,
            timeout=120,
            check=True,
        )
        return os.path.exists(Config.R_RECOMMENDATIONS_PATH)
    except (subprocess.SubprocessError, OSError) as exc:
        logger.warning("R pipeline could not run automatically: %s", exc)
        return False


def load_r_recommendations(top_n: int = 10) -> list[dict]:
    """Load hybrid recommendations produced by the R workflow."""
    if not run_r_pipeline_if_needed():
        return []

    try:
        recommendations_df = pd.read_csv(Config.R_RECOMMENDATIONS_PATH)
    except (pd.errors.ParserError, OSError) as exc:
        logger.warning("Could not read R recommendations: %s", exc)
        return []

    title_column = None
    for column in ("Movie", "title", "Title"):
        if column in recommendations_df.columns:
            title_column = column
            break

    if title_column is None:
        return []

    recommendations = []
    for _, row in recommendations_df.head(top_n).iterrows():
        movie_title = str(row[title_column]).strip()
        if not movie_title:
            continue

        recommendations.append(
            {
                "title": movie_title,
                "score": float(row.get("Predicted_Rating", 0) or 0),
                "match_percentage": float(row.get("Match_Percentage", 0) or 0),
                "strength": str(row.get("Recommendation_Strength", "R Hybrid")),
                "source": "R Hybrid",
                "poster": get_movie_poster(movie_title),
            }
        )

    return recommendations


def run_r_script(script_name: str) -> subprocess.CompletedProcess:
    """Execute an approved R script and return subprocess output."""
    if script_name not in ALLOWED_R_SCRIPTS:
        raise ValueError(f"Script '{script_name}' is not allowed")

    return subprocess.run(
        [Config.RSCRIPT_CMD, f"Scripts/{script_name}.R"],
        capture_output=True,
        text=True,
        check=False,
    )


def get_r_output_status() -> dict[str, bool]:
    """Report which R output files currently exist on disk."""
    return {name: os.path.exists(path) for name, path in R_OUTPUT_FILES.items()}
