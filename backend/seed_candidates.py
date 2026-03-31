"""
seed_candidates.py
------------------
Populate Pinecone with sample candidate profiles for demo/testing.

Usage:
    python seed_candidates.py

Requires:
    - .env file with PINECONE_API_KEY configured
    - pip install -r requirements.txt
"""

import asyncio
import uuid
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.services.pinecone_service import PineconeService

SAMPLE_CANDIDATES = [
    {
        "name": "Aisha Mehta",
        "email": "aisha.mehta@example.com",
        "role": "Senior Backend Engineer",
        "years_experience": 7,
        "skills": ["Python", "FastAPI", "PostgreSQL", "AWS", "Kubernetes", "Docker"],
        "resume_text": (
            "Senior Backend Engineer with 7 years building scalable distributed systems. "
            "Expert in Python and FastAPI for high-throughput REST API design. "
            "Deep experience with PostgreSQL query optimization, AWS ECS/Lambda, "
            "Kubernetes cluster management, and Docker containerization. "
            "Led migration of monolithic system to microservices at Series-B fintech startup. "
            "Strong understanding of event-driven architecture with Kafka and RabbitMQ."
        ),
    },
    {
        "name": "Ravi Krishnamurthy",
        "email": "ravi.k@example.com",
        "role": "Platform Engineer",
        "years_experience": 6,
        "skills": ["Python", "Django", "PostgreSQL", "Docker", "GCP", "Terraform"],
        "resume_text": (
            "Platform Engineer with 6 years of experience in backend development using Python and Django. "
            "Proficient in building RESTful APIs and managing PostgreSQL databases. "
            "Experienced in GCP infrastructure, Cloud Run, and Terraform for IaC. "
            "Docker enthusiast with CI/CD pipeline expertise on GitHub Actions and Cloud Build. "
            "Contributed to open-source Django packages. Less AWS experience but very GCP-focused."
        ),
    },
    {
        "name": "Priya Nair",
        "email": "priya.nair@example.com",
        "role": "Full-Stack Engineer",
        "years_experience": 5,
        "skills": ["Python", "Flask", "MySQL", "Docker", "React", "REST APIs"],
        "resume_text": (
            "Full-Stack Engineer with 5 years of Python and JavaScript development. "
            "Backend built with Flask and MySQL, REST API design for mobile and web clients. "
            "Frontend work in React. Familiar with Docker for local development environments. "
            "Limited microservices and cloud infrastructure experience. "
            "Strong in building CRUD applications and data-driven dashboards."
        ),
    },
    {
        "name": "James Okafor",
        "email": "james.o@example.com",
        "role": "Backend Engineer",
        "years_experience": 4,
        "skills": ["Node.js", "PostgreSQL", "AWS", "Docker", "GraphQL", "TypeScript"],
        "resume_text": (
            "Backend Engineer specializing in Node.js and TypeScript microservices. "
            "Built GraphQL APIs and PostgreSQL schemas for e-commerce platforms. "
            "AWS certified (Associate) with Lambda, S3, and RDS experience. "
            "Docker for containerization. No Python experience — primarily JavaScript ecosystem. "
            "Comfortable with REST and GraphQL API paradigms."
        ),
    },
    {
        "name": "Chen Wei",
        "email": "chen.wei@example.com",
        "role": "Data Engineer",
        "years_experience": 5,
        "skills": ["Python", "Apache Spark", "Airflow", "S3", "Redshift", "dbt"],
        "resume_text": (
            "Data Engineer with 5 years of building batch and streaming data pipelines. "
            "Python scripting, Apache Spark for large-scale processing, and Airflow for orchestration. "
            "AWS S3, Redshift, and Glue for data lake architecture. dbt for data transformations. "
            "Not focused on API development or web backends — primarily ETL and analytics engineering."
        ),
    },
    {
        "name": "Sara O'Brien",
        "email": "sara.obrien@example.com",
        "role": "Senior Software Engineer",
        "years_experience": 8,
        "skills": ["Python", "FastAPI", "SQLAlchemy", "Redis", "AWS", "gRPC"],
        "resume_text": (
            "Senior Software Engineer with 8 years at FAANG-adjacent companies. "
            "Python expert — FastAPI, SQLAlchemy ORM, Redis caching layers. "
            "gRPC service design for internal microservices. AWS (EKS, RDS, CloudFront). "
            "Led team of 5 engineers, defined API contracts, and implemented observability stacks. "
            "Strong in system design, scalability, and production incident response."
        ),
    },
]


async def main():
    print("Initializing services…")
    await PineconeService.initialize()

    model = SentenceTransformer(settings.EMBEDDING_MODEL)
    print(f"Loaded model: {settings.EMBEDDING_MODEL}")

    records = []
    for c in SAMPLE_CANDIDATES:
        vector = model.encode(c["resume_text"], normalize_embeddings=True).tolist()
        records.append({
            "id": str(uuid.uuid4()),
            "vector": vector,
            "metadata": {
                "name": c["name"],
                "email": c["email"],
                "role": c["role"],
                "years_experience": c["years_experience"],
                "skills": c["skills"],
                "resume_text": c["resume_text"],
            },
        })

    PineconeService.upsert_batch(records)
    print(f"✅ Seeded {len(records)} candidates into Pinecone index '{settings.PINECONE_INDEX_NAME}'")


if __name__ == "__main__":
    asyncio.run(main())
