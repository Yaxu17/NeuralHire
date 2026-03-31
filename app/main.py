"""
NeuralHire — Smart Resume-to-Job Matching Engine
FastAPI Backend Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

from app.api.routes import candidates, jobs, health
from app.core.logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.services.embedding_service import EmbeddingService
    from app.services.pinecone_service import PineconeService
    await EmbeddingService.initialize()
    await PineconeService.initialize()
    print("✅ NeuralHire API ready.")
    yield
    print("NeuralHire shutting down.")


app = FastAPI(
    title="NeuralHire API",
    description="AI-powered semantic resume-to-job matching using Sentence-Transformers + Pinecone",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS — allow all so file:// frontend works when opened directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Routers
app.include_router(health.router,     prefix="/api",            tags=["Health"])
app.include_router(candidates.router, prefix="/api/candidates", tags=["Candidates"])
app.include_router(jobs.router,       prefix="/api/jobs",       tags=["Jobs"])


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
