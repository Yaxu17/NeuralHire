"""
Application Configuration — loads from environment variables / .env file
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "NeuralHire"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"

    # Pinecone
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1-aws"
    PINECONE_INDEX_NAME: str = "neuralhire-candidates"
    PINECONE_DIMENSION: int = 384          # matches all-MiniLM-L6-v2

    # Embedding Model (HuggingFace Sentence-Transformers)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_BATCH_SIZE: int = 32

    # Search
    TOP_K_RESULTS: int = 20
    SCORE_THRESHOLD: float = 0.0           # minimum cosine similarity (0.0 = return all)

    # CORS — includes file:// for opening index.html directly
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "null",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
