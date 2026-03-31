"""
Unit tests for NeuralHire backend services.
Run with: pytest tests/ -v
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from app.services.matching_service import _label, _generate_summary


# ──────────────── Label Tests ────────────────────────────────────────────────

def test_label_hot():
    assert _label(0.92) == "hot"

def test_label_strong():
    assert _label(0.80) == "strong"

def test_label_fair():
    assert _label(0.60) == "fair"

def test_label_weak():
    assert _label(0.40) == "weak"

def test_label_boundary_hot():
    assert _label(0.88) == "hot"

def test_label_boundary_strong():
    assert _label(0.72) == "strong"


# ──────────────── Summary Tests ──────────────────────────────────────────────

def test_generate_summary_hot():
    meta = {"name": "Alice", "role": "Engineer", "skills": ["Python", "FastAPI"], "years_experience": 7}
    summary = _generate_summary(0.92, meta)
    assert "Excellent" in summary
    assert "Python" in summary

def test_generate_summary_strong():
    meta = {"name": "Bob", "role": "Developer", "skills": ["JS"], "years_experience": 4}
    summary = _generate_summary(0.75, meta)
    assert "Good match" in summary

def test_generate_summary_fair():
    meta = {"name": "Bob", "role": "Dev", "skills": ["JS"], "years_experience": 2}
    summary = _generate_summary(0.60, meta)
    assert "Partial" in summary

def test_generate_summary_weak():
    meta = {"name": "Charlie", "role": "Manager", "skills": [], "years_experience": 1}
    summary = _generate_summary(0.30, meta)
    assert "Low alignment" in summary


# ──────────────── Embedding Tests ────────────────────────────────────────────

@patch("app.services.embedding_service._model")
def test_embed_returns_normalized_vector(mock_model):
    """Embedding should return a 1D array of shape (384,)."""
    fake_vector = np.random.rand(384).astype("float32")
    fake_vector /= np.linalg.norm(fake_vector)
    mock_model.encode.return_value = np.array([fake_vector])

    from app.services.embedding_service import EmbeddingService
    result = EmbeddingService.embed("Senior Python Developer with 5 years experience in FastAPI")
    assert result.shape == (384,)
    assert abs(np.linalg.norm(result) - 1.0) < 1e-4


@patch("app.services.embedding_service._model")
def test_embed_batch(mock_model):
    """Batch embedding should return shape (N, 384)."""
    fake_vecs = np.random.rand(3, 384).astype("float32")
    mock_model.encode.return_value = fake_vecs

    from app.services.embedding_service import EmbeddingService
    result = EmbeddingService.embed(["text1", "text2", "text3"])
    assert result.shape == (3, 384)


# ──────────────── Resume Parser Tests ────────────────────────────────────────

def test_extract_text_unsupported_extension():
    from app.utils.resume_parser import extract_resume_text
    with pytest.raises(ValueError, match="Unsupported"):
        extract_resume_text("resume.xyz", b"some bytes")

def test_extract_text_too_short():
    from app.utils.resume_parser import extract_resume_text
    with pytest.raises(ValueError, match="enough text"):
        extract_resume_text("resume.txt", b"hi")

def test_extract_text_txt():
    from app.utils.resume_parser import extract_resume_text
    content = b"John Doe Software Engineer Python FastAPI PostgreSQL AWS 5 years experience building scalable APIs"
    result = extract_resume_text("resume.txt", content)
    assert "John Doe" in result
    assert len(result) > 20
