"""
Resume Parser Utility
---------------------
Extracts plain text from uploaded resume files:
  - PDF  → via pdfplumber
  - DOCX → via python-docx
  - TXT  → direct read

Returns a single cleaned string ready for embedding.
"""

import io
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return ""


def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        logger.error(f"DOCX extraction failed: {e}")
        return ""


def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    """
    Dispatch to the correct parser based on file extension.
    Raises ValueError for unsupported types.
    """
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_bytes)
    elif ext in (".docx", ".doc"):
        text = extract_text_from_docx(file_bytes)
    elif ext == ".txt":
        text = file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {ext}. Please upload PDF, DOCX, or TXT.")

    cleaned = _clean_text(text)

    if len(cleaned) < 20:
        raise ValueError("Could not extract enough text from the file. Please upload a valid resume.")

    return cleaned


def _clean_text(text: str) -> str:
    """Normalise whitespace and strip non-printable characters."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)
    return text.strip()
