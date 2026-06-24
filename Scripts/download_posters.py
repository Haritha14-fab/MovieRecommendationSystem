"""Offline batch poster downloader using the shared poster service."""

import os
import sys

import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from services.poster_service import get_movie_poster, warm_poster_cache  # noqa: E402

DATASET_PATH = os.path.join(PROJECT_ROOT, "Dataset", "ml-100k", "u.item")


def main() -> None:
    """Warm the poster cache for every title in the MovieLens catalog."""
    column_names = ["movie_id", "title"] + [f"extra_{index}" for index in range(22)]
    movies = pd.read_csv(
        DATASET_PATH,
        sep="|",
        encoding="latin-1",
        header=None,
        names=column_names,
        usecols=["title"],
    )

    titles = movies["title"].dropna().astype(str).tolist()
    print(f"Warming poster cache for {len(titles)} movies...")
    warm_poster_cache(titles)
    print("Done. Cache stored at cache/poster_cache.json")


if __name__ == "__main__":
    main()
