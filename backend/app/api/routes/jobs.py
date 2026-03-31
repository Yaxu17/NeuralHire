"""
Jobs Router
-----------
Endpoints:
  POST /api/jobs/match    — Semantic search: JD → ranked candidates
"""

import logging
from fastapi import APIRouter, HTTPException

from app.models.schemas import JobMatchRequest, JobMatchResponse
from app.services.matching_service import MatchingService
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/match", response_model=JobMatchResponse)
async def match_job_to_candidates(request: JobMatchRequest):
    """
    Core semantic matching endpoint.

    Accepts a job description and returns candidates ranked by
    cosine similarity of their resume embeddings.

    - Uses `all-MiniLM-L6-v2` for encoding
    - Queries Pinecone ANN index
    - Returns score (0–1), percentage, label (hot/strong/fair/weak),
      and a natural-language match summary per candidate
    """
    if not EmbeddingService.is_ready():
        raise HTTPException(status_code=503, detail="Embedding model not loaded yet.")
    if not PineconeService.is_ready():
        raise HTTPException(status_code=503, detail="Pinecone not connected yet.")

    try:
        result = MatchingService.match_job_description(
            job_description=request.job_description,
            top_k=request.top_k,
            score_threshold=request.score_threshold,
            experience_filter=request.experience_filter,
        )
        return result
    except Exception as e:
        logger.exception("Matching failed")
        raise HTTPException(status_code=500, detail=f"Matching error: {str(e)}")
