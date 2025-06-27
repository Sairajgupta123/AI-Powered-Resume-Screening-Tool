from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Ranker:
    """Rank resumes against a job description using TF‑IDF + cosine similarity."""

    def __init__(self, model_path: Path | None = None):
        self.model_path = model_path
        if model_path and model_path.exists():
            self.vectorizer: TfidfVectorizer = joblib.load(model_path)
        else:
            # bi‑grams often capture phrases like "machine learning"
            self.vectorizer = TfidfVectorizer(max_features=8000, ngram_range=(1, 2))

    def fit(self, corpus: List[str]) -> None:
        self.vectorizer.fit(corpus)
        if self.model_path:
            joblib.dump(self.vectorizer, self.model_path)

    def _transform(self, corpus: List[str]):
        return self.vectorizer.transform(corpus)

    def rank(self, resumes: List[Dict], job_desc: str) -> List[Dict]:
        """Add a similarity *score* to each resume and return them sorted."""
        texts = [r["raw_text"] for r in resumes] + [job_desc]
        matrix = self._transform(texts)
        jd_vec = matrix[-1]
        res_vecs = matrix[:-1]
        scores = cosine_similarity(jd_vec, res_vecs).flatten()
        for r, s in zip(resumes, scores):
            r["score"] = float(s)
        return sorted(resumes, key=lambda x: x["score"], reverse=True)
