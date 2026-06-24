"""Content-based and hybrid recommendation engine."""

import logging
import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import Config
from services.movie_catalog import MovieCatalog
from services.poster_service import get_movie_poster
from services.r_pipeline import load_r_recommendations

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Python + R hybrid movie recommender."""

    def __init__(self, catalog: MovieCatalog):
        self.catalog = catalog
        self.embedding_model = None
        self.movie_embeddings = None
        self.tfidf_vectorizer: TfidfVectorizer | None = None
        self.tfidf_matrix = None
        self._model_loaded = False

    def _load_similarity_model(self) -> None:
        """Load SentenceTransformer embeddings or fall back to TF-IDF."""
        if self._model_loaded:
            return

        movie_titles = self.catalog.movie_titles

        if Config.USE_TRANSFORMERS:
            try:
                from sentence_transformers import SentenceTransformer

                self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL_NAME)
                self.movie_embeddings = self.embedding_model.encode(
                    movie_titles,
                    show_progress_bar=False,
                )
                self._model_loaded = True
                logger.info("Loaded SentenceTransformer embedding model")
                return
            except Exception as exc:
                logger.warning(
                    "SentenceTransformer unavailable; using TF-IDF fallback: %s", exc
                )

        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(movie_titles)
        self._model_loaded = True
        logger.info("Loaded TF-IDF similarity model")

    def _similarity_scores_for_index(self, movie_index: int) -> np.ndarray:
        """Compute cosine similarity between one movie and the full catalog."""
        if self.movie_embeddings is not None:
            query_vector = self.movie_embeddings[movie_index].reshape(1, -1)
            return cosine_similarity(query_vector, self.movie_embeddings)[0]

        query_vector = self.tfidf_matrix[movie_index]
        return cosine_similarity(query_vector, self.tfidf_matrix)[0]

    def _similarity_scores_for_query(self, query_title: str) -> np.ndarray:
        """Compute similarity scores for a free-text movie title."""
        if self.embedding_model is not None and self.movie_embeddings is not None:
            query_vector = self.embedding_model.encode([query_title])
            return cosine_similarity(query_vector, self.movie_embeddings)[0]

        query_vector = self.tfidf_vectorizer.transform([query_title])
        return cosine_similarity(query_vector, self.tfidf_matrix)[0]

    def _build_result(self, movie_index: int, score: float) -> dict:
        """Format a single recommendation result with poster URL."""
        row = self.catalog.movies_df.iloc[movie_index]
        movie_title = row["title"]
        return {
            "movie_id": int(row["movie_id"]),
            "title": movie_title,
            "score": float(score),
            "poster": get_movie_poster(movie_title),
        }

    def recommend_by_cosine(self, query_title: str, top_n: int = 10) -> list[dict]:
        """Recommend movies similar to a catalog title using cosine similarity."""
        self._load_similarity_model()

        matched_rows = self.catalog.movies_df[
            self.catalog.movies_df["title"].str.contains(
                query_title, case=False, na=False
            )
        ]
        if matched_rows.empty:
            return []

        movie_index = matched_rows.index[0]
        similarity_scores = self._similarity_scores_for_index(movie_index)
        top_indices = np.argsort(similarity_scores)[::-1][1 : top_n + 1]

        return [
            self._build_result(index, similarity_scores[index])
            for index in top_indices
        ]

    def recommend_by_embedding(self, query_title: str, top_n: int = 10) -> list[dict]:
        """Recommend movies using embedding or TF-IDF query similarity."""
        self._load_similarity_model()

        similarity_scores = self._similarity_scores_for_query(query_title)
        top_indices = np.argsort(similarity_scores)[::-1][1 : top_n + 20]

        results = []
        for index in top_indices:
            results.append(self._build_result(index, similarity_scores[index]))
            if len(results) >= top_n:
                break
        return results

    def hybrid_recommend(self, query_title: str, top_n: int = 10) -> list[dict]:
        """Merge R hybrid output with Python content-based recommendations."""
        resolved_title = self.catalog.resolve_title(query_title)

        r_results = load_r_recommendations(top_n)
        cosine_results = self.recommend_by_cosine(resolved_title, top_n)
        embedding_results = self.recommend_by_embedding(resolved_title, top_n)

        seen_titles: set[str] = set()
        merged_results: list[dict] = []

        if resolved_title:
            seen_titles.add(resolved_title.lower())

        for candidate in r_results + cosine_results + embedding_results:
            title_key = candidate["title"].lower()
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)
            merged_results.append(candidate)

        return merged_results[:top_n]

    def recommend_ai_only(self, query_title: str, top_n: int = 10) -> list[dict]:
        """Python-only recommendations without the R pipeline."""
        cosine_results = self.recommend_by_cosine(query_title, top_n)
        embedding_results = self.recommend_by_embedding(query_title, top_n)

        seen_titles: set[str] = set()
        merged_results: list[dict] = []

        for candidate in cosine_results + embedding_results:
            if candidate["title"] in seen_titles:
                continue
            seen_titles.add(candidate["title"])
            merged_results.append(candidate)

        return merged_results[:top_n]
