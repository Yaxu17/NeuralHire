"""
Candidates Router
-----------------
Endpoints:
  POST /api/candidates/          — Add a candidate (JSON body with resume_text)
  POST /api/candidates/upload    — Add a candidate via resume file upload (PDF/DOCX/TXT)
  GET  /api/candidates/{id}      — Retrieve candidate metadata
  DELETE /api/candidates/{id}    — Remove candidate from index
"""

import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from app.models.schemas import CandidateCreate, CandidateResponse
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService
from app.utils.resume_parser import extract_resume_text

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_UPLOAD_BYTES = 5 * 1024 * 1024   # 5 MB


@router.post("/", response_model=CandidateResponse, status_code=201)
async def create_candidate(candidate: CandidateCreate):
    """
    Register a new candidate by providing resume text directly.
    The service embeds the resume and upserts the vector into Pinecone.
    """
    candidate_id = str(uuid.uuid4())

    # Embed resume text
    vector = EmbeddingService.embed(candidate.resume_text).tolist()

    # Store in Pinecone
    PineconeService.upsert_candidate(
        candidate_id=candidate_id,
        vector=vector,
        metadata={
            **candidate.model_dump(),
        },
    )

    logger.info(f"Registered candidate {candidate_id} — {candidate.name}")
    return CandidateResponse(
        **candidate.model_dump(),
        id=candidate_id,
        created_at=datetime.utcnow(),
    )


@router.post("/upload", response_model=CandidateResponse, status_code=201)
async def upload_candidate_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    role: str = Form(default=""),
    years_experience: int = Form(default=0),
    skills: str = Form(default=""),          # comma-separated
):
    """
    Upload a resume file (PDF / DOCX / TXT).
    Extracts text, embeds it, and stores in Pinecone.
    """
    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 5 MB).")

    try:
        resume_text = extract_resume_text(file.filename, raw)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    candidate_id = str(uuid.uuid4())
    vector = EmbeddingService.embed(resume_text).tolist()

    PineconeService.upsert_candidate(
        candidate_id=candidate_id,
        vector=vector,
        metadata={
            "name": name,
            "email": email,
            "role": role,
            "years_experience": years_experience,
            "skills": skills_list,
            "resume_text": resume_text,
        },
    )

    return CandidateResponse(
        id=candidate_id,
        name=name,
        email=email,
        role=role,
        years_experience=years_experience,
        skills=skills_list,
        resume_text=resume_text,
        created_at=datetime.utcnow(),
    )


@router.delete("/{candidate_id}", status_code=204)
async def delete_candidate(candidate_id: str):
    """Remove a candidate's vector from Pinecone."""
    PineconeService.delete_candidate(candidate_id)
    logger.info(f"Deleted candidate {candidate_id}")
