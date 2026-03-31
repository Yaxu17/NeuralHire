from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        pinecone_connected=PineconeService.is_ready(),
        model_loaded=EmbeddingService.is_ready(),
        indexed_candidates=PineconeService.total_vectors(),
        version="1.0.0",
    )
