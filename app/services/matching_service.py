"""
Matching Service
----------------
Core ranking engine that:
  1. Embeds the job description using Sentence-Transformers
  2. Queries Pinecone for the top-K nearest candidate vectors
  3. Enriches results with compatibility scores, labels, and match summaries
  4. Applies optional experience-level filters
"""

import logging
import time
from typing import List, Optional

from app.models.schemas import CandidateMatch, JobMatchResponse
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService
from app.core.config import settings

logger = logging.getLogger(__name__)


# Experience band mapping
EXPERIENCE_FILTERS = {
    "junior": {"years_experience": {"$lte": 3}},
    "mid":    {"years_experience": {"$gte": 3, "$lte": 6}},
    "senior": {"years_experience": {"$gte": 6}},
}

# Score → label thresholds
def _label(score: float) -> str:
    if score >= 0.88:
        return "hot"
    if score >= 0.72:
        return "strong"
    if score >= 0.55:
        return "fair"
    return "weak"


def _generate_summary(score: float, metadata: dict) -> str:
    """Generate a one-line human-readable match summary from metadata + score."""
    name = metadata.get("name", "Candidate")
    role = metadata.get("role", "professional")
    skills = metadata.get("skills", [])
    skill_str = ", ".join(skills[:3]) if skills else "general skills"
    yoe = metadata.get("years_experience", 0)

    if score >= 0.88:
        return f"Excellent fit — {yoe}yr {role} with strong alignment in {skill_str}."
    if score >= 0.72:
        return f"Good match — relevant experience in {skill_str}; minor gaps possible."
    if score >= 0.55:
        return f"Partial match — {role} background, some skill overlap with {skill_str}."
    return f"Low alignment — {role} profile, limited skill intersection with JD."


class MatchingService:

    @classmethod
    def match_job_description(
        cls,
        job_description: str,
        top_k: int = 10,
        score_threshold: float = 0.0,
        experience_filter: Optional[str] = None,
    ) -> JobMatchResponse:
        """
        Full pipeline:
          JD text → embedding vector → Pinecone query → ranked CandidateMatch list
        """
        t0 = time.time()

        # 1. Embed the job description
        logger.info("Embedding job description…")
        jd_vector = EmbeddingService.embed(job_description).tolist()

        # 2. Build optional metadata filter
        pinecone_filter = None
        if experience_filter and experience_filter in EXPERIENCE_FILTERS:
            pinecone_filter = EXPERIENCE_FILTERS[experience_filter]

        # 3. Query Pinecone
        raw_results = PineconeService.query(
            query_vector=jd_vector,
            top_k=top_k,
            filter_dict=pinecone_filter,
        )

        # 4. Enrich results
        matches: List[CandidateMatch] = []
        for r in raw_results:
            score = r["score"]
            if score < score_threshold:
                continue
            meta = r["metadata"]
            matches.append(
                CandidateMatch(
                    id=r["id"],
                    name=meta.get("name", "Unknown"),
                    email=meta.get("email", ""),
                    role=meta.get("role"),
                    years_experience=meta.get("years_experience"),
                    skills=meta.get("skills", []),
                    score=round(score, 4),
                    score_pct=int(round(score * 100)),
                    match_label=_label(score),
                    match_summary=_generate_summary(score, meta),
                )
            )

        elapsed_ms = round((time.time() - t0) * 1000, 2)
        logger.info(f"Matching complete — {len(matches)} results in {elapsed_ms}ms")

        return JobMatchResponse(
            query_time_ms=elapsed_ms,
            total_indexed=PineconeService.total_vectors(),
            results=matches,
            model_used=settings.EMBEDDING_MODEL,
        )
