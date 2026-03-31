"""
Embedding Service
-----------------
Wraps HuggingFace Sentence-Transformers to produce dense vector embeddings
from raw text (resumes or job descriptions).

Model used: all-MiniLM-L6-v2
  - Output dimension: 384
  - Speed: very fast (~14k sentences/sec on GPU)
  - Quality: strong semantic similarity performance on STS benchmarks
"""

import logging
import time
from typing import List, Union, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings

logger = logging.getLogger(__name__)

_model: Optional[SentenceTransformer] = None


class EmbeddingService:

    @classmethod
    async def initialize(cls):
        global _model
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        t0 = time.time()
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info(f"Model loaded in {time.time() - t0:.2f}s")

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if _model is None:
            raise RuntimeError("EmbeddingService not initialized. Call initialize() first.")
        return _model

    @classmethod
    def embed(cls, text: Union[str, List[str]]) -> np.ndarray:
        """
        Encode a single string or a list of strings into L2-normalised vectors.

        Returns:
            np.ndarray of shape (N, 384) for a list input, or (384,) for a single string.
        """
        model = cls.get_model()
        single = isinstance(text, str)
        texts = [text] if single else text

        # Preprocess: truncate very long texts to avoid OOM
        texts = [t[:8192] for t in texts]

        vectors = model.encode(
            texts,
            batch_size=settings.EMBEDDING_BATCH_SIZE,
            normalize_embeddings=True,      # L2-normalise → cosine similarity == dot product
            show_progress_bar=False,
        )
        return vectors[0] if single else vectors

    @classmethod
    def cosine_similarity(cls, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two normalised vectors."""
        return float(np.dot(a, b))

    @classmethod
    def is_ready(cls) -> bool:
        return _model is not None
