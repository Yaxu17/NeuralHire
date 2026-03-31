"""
Pinecone Service
----------------
Manages all interactions with Pinecone vector database:
  - Index initialisation
  - Upserting candidate vectors
  - Querying by cosine similarity
  - Deleting candidates

Architecture:
  Each candidate is stored as a vector (384-dim float32) with metadata:
    {name, email, role, years_experience, skills, resume_preview}
"""

import logging
import time
from typing import Any, Dict, List, Optional

from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings

logger = logging.getLogger(__name__)

_pc: Optional[Pinecone] = None
_index = None


class PineconeService:

    @classmethod
    async def initialize(cls):
        global _pc, _index
        logger.info("Connecting to Pinecone…")
        _pc = Pinecone(api_key=settings.PINECONE_API_KEY)

        try:
            existing_indexes = _pc.list_indexes()
            existing_names = [idx.name for idx in existing_indexes]
        except Exception:
            existing_names = []

        if settings.PINECONE_INDEX_NAME not in existing_names:
            logger.info(f"Creating index '{settings.PINECONE_INDEX_NAME}'")
            _pc.create_index(
                name=settings.PINECONE_INDEX_NAME,
                dimension=settings.PINECONE_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        _index = _pc.Index(settings.PINECONE_INDEX_NAME)
        stats = _index.describe_index_stats()
        logger.info(f"Pinecone ready — {stats.total_vector_count} vectors indexed.")

    @classmethod
    def get_index(cls):
        if _index is None:
            raise RuntimeError("PineconeService not initialized.")
        return _index

    # ── Upsert ──────────────────────────────────────────────────────────────

    @classmethod
    def upsert_candidate(
        cls,
        candidate_id: str,
        vector: List[float],
        metadata: Dict[str, Any],
    ) -> None:
        """Insert or update a single candidate vector."""
        idx = cls.get_index()
        # Pinecone metadata values must be str/int/float/bool/list[str]
        clean_meta = {
            "name": metadata.get("name", ""),
            "email": metadata.get("email", ""),
            "role": metadata.get("role", ""),
            "years_experience": metadata.get("years_experience") or 0,
            "skills": metadata.get("skills", []),
            "resume_preview": str(metadata.get("resume_text", ""))[:500],
        }
        idx.upsert(vectors=[(candidate_id, vector, clean_meta)])
        logger.debug(f"Upserted candidate {candidate_id}")

    @classmethod
    def upsert_batch(cls, records: List[Dict]) -> None:
        """Batch upsert for bulk ingestion (≤100 records per call)."""
        idx = cls.get_index()
        vectors = [
            (r["id"], r["vector"], r["metadata"])
            for r in records
        ]
        for i in range(0, len(vectors), 100):
            idx.upsert(vectors=vectors[i:i + 100])
        logger.info(f"Batch upserted {len(records)} candidates.")

    # ── Query ────────────────────────────────────────────────────────────────

    @classmethod
    def query(
        cls,
        query_vector: List[float],
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Return top-K candidates ranked by cosine similarity to query_vector.

        Returns list of dicts:
          {id, score, metadata}
        """
        idx = cls.get_index()
        t0 = time.time()

        response = idx.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict,
        )

        elapsed_ms = (time.time() - t0) * 1000
        logger.info(f"Pinecone query returned {len(response.matches)} results in {elapsed_ms:.1f}ms")

        results = []
        for match in response.matches:
            results.append({
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata or {},
            })
        return results

    # ── Delete ───────────────────────────────────────────────────────────────

    @classmethod
    def delete_candidate(cls, candidate_id: str) -> None:
        cls.get_index().delete(ids=[candidate_id])
        logger.info(f"Deleted candidate {candidate_id}")

    # ── Stats ────────────────────────────────────────────────────────────────

    @classmethod
    def total_vectors(cls) -> int:
        try:
            stats = cls.get_index().describe_index_stats()
            return stats.total_vector_count
        except Exception:
            return 0

    @classmethod
    def is_ready(cls) -> bool:
        return _index is not None
