# ⚡ NeuralHire — Smart Resume-to-Job Matching Engine

> AI-powered semantic recruitment portal using **Sentence-Transformers + Pinecone + FastAPI**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-5A67D8)](https://pinecone.io)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?logo=huggingface)](https://huggingface.co)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://python.org)

---

## 🧠 What It Does

NeuralHire replaces keyword-matching ATS systems with **semantic understanding**. It embeds both resumes and job descriptions into the same high-dimensional vector space and ranks candidates by **cosine similarity** — capturing meaning, not just matching words.

### The Problem It Solves

| Problem | Traditional ATS | NeuralHire |
|---------|----------------|------------|
| Keyword stuffing | ❌ Fooled easily | ✅ Semantic gap detection |
| Java developer vs Java enthusiast | ❌ Same score | ✅ Context-aware ranking |
| 70% recruiter time waste | ❌ Still happens | ✅ Instant ranked shortlist |
| False negatives (great candidate, wrong words) | ❌ 45% miss rate | ✅ Concept-level matching |

---

## 🏗️ Architecture

```
Resume / JD Text
       │
       ▼
┌─────────────────────────────┐
│  Sentence-Transformers      │  ← all-MiniLM-L6-v2 (384-dim)
│  HuggingFace                │
└────────────┬────────────────┘
             │  float32 vector
             ▼
┌─────────────────────────────┐
│  Pinecone Vector Database   │  ← HNSW ANN index, cosine metric
│  Serverless · us-east-1     │
└────────────┬────────────────┘
             │  top-K matches
             ▼
┌─────────────────────────────┐
│  FastAPI Backend            │  ← /api/jobs/match
│  Ranking + Score Labels     │
└────────────┬────────────────┘
             │  JSON response
             ▼
┌─────────────────────────────┐
│  React Frontend             │  ← Vite + CSS Modules
│  Recruiter Dashboard        │
└─────────────────────────────┘
```

---

## 📁 Project Structure

```
neuralhire/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── core/
│   │   │   ├── config.py            # Pydantic settings
│   │   │   └── logging.py           # Logging setup
│   │   ├── models/
│   │   │   └── schemas.py           # Request/response schemas
│   │   ├── services/
│   │   │   ├── embedding_service.py # HuggingFace wrapper
│   │   │   ├── pinecone_service.py  # Pinecone CRUD + query
│   │   │   └── matching_service.py  # Core ranking engine
│   │   ├── api/routes/
│   │   │   ├── candidates.py        # POST/DELETE /candidates
│   │   │   ├── jobs.py              # POST /jobs/match
│   │   │   └── health.py            # GET /health
│   │   └── utils/
│   │       └── resume_parser.py     # PDF/DOCX/TXT extraction
│   ├── tests/
│   │   └── test_services.py
│   ├── seed_candidates.py           # Populate Pinecone with demo data
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   └── index.html               # Standalone HTML demo (no build needed)
│   ├── src/
│   │   ├── main.jsx                 # React entry
│   │   ├── App.jsx                  # Router
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── CandidateCard.jsx
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx
│   │   │   ├── Dashboard.jsx        # Main recruiter portal
│   │   │   └── UploadPage.jsx       # Resume ingestion
│   │   ├── hooks/
│   │   │   ├── useMatching.js       # API call + state for matching
│   │   │   └── useUpload.js         # Resume upload state
│   │   ├── utils/
│   │   │   └── api.js               # Axios API client
│   │   └── styles/
│   │       └── global.css
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- [Pinecone account](https://pinecone.io) (free tier works)

### 1. Clone & Configure Backend

```bash
cd backend
cp .env.example .env
# Edit .env — add your PINECONE_API_KEY
```

### 2. Install & Run Backend

```bash
pip install -r requirements.txt

# Seed with sample candidates (optional)
python seed_candidates.py

# Start API server
uvicorn app.main:app --reload --port 8000
```

API docs available at: **http://localhost:8000/api/docs**

### 3. Install & Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: **http://localhost:5173**

> **No build needed for demo**: Open `frontend/public/index.html` directly in a browser for the standalone HTML demo.

### 4. Docker (Full Stack)

```bash
# From root
cp backend/.env.example backend/.env
# Edit backend/.env with your Pinecone key

docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/docs

---

## 🔌 API Reference

### `POST /api/jobs/match`
Semantic match a job description against all indexed candidates.

```json
// Request
{
  "job_description": "Senior Python Engineer with FastAPI, PostgreSQL, AWS...",
  "top_k": 10,
  "score_threshold": 0.0,
  "experience_filter": "senior"   // optional: junior | mid | senior
}

// Response
{
  "query_time_ms": 12.4,
  "total_indexed": 12847,
  "model_used": "all-MiniLM-L6-v2",
  "results": [
    {
      "id": "uuid",
      "name": "Aisha Mehta",
      "role": "Senior Backend Engineer",
      "skills": ["Python", "FastAPI", "PostgreSQL"],
      "score": 0.961,
      "score_pct": 96,
      "match_label": "hot",
      "match_summary": "Excellent fit — 7yr Senior Backend Engineer with strong alignment..."
    }
  ]
}
```

### `POST /api/candidates/`
Add a candidate via JSON (resume text).

### `POST /api/candidates/upload`
Add a candidate via resume file upload (PDF/DOCX/TXT, multipart form).

### `DELETE /api/candidates/{id}`
Remove a candidate from the index.

### `GET /api/health`
Check API, model, and Pinecone connection status.

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## 📚 Learning Objectives Covered

| Competency | Where |
|------------|-------|
| **NLP / Sentence Embeddings** | `embedding_service.py` — HuggingFace all-MiniLM-L6-v2 |
| **Vector Databases** | `pinecone_service.py` — upsert, query, delete |
| **Semantic vs Lexical Search** | `matching_service.py` — cosine similarity vs keywords |
| **API Development** | `app/api/routes/` — FastAPI async endpoints |
| **Vector Mathematics** | `_label()`, `cosine_similarity()` — score thresholds |
| **Full-Stack AI Architecture** | End-to-end: file upload → embed → index → query → UI |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Embedding Model | `sentence-transformers` — all-MiniLM-L6-v2 (384-dim) |
| Vector Database | Pinecone (serverless, cosine metric) |
| Backend Framework | FastAPI + uvicorn |
| Schema Validation | Pydantic v2 |
| PDF Parsing | pdfplumber |
| DOCX Parsing | python-docx |
| Frontend Framework | React 18 + Vite |
| Routing | React Router v6 |
| HTTP Client | Axios |
| File Upload UI | react-dropzone |
| Containerisation | Docker + Docker Compose |

---

## 📄 License

MIT — free to use, modify, and distribute.
