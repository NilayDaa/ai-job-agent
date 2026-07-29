# AI Job Agent

## 🚀 One-line Elevator Pitch

A prototype AI Job Agent that scrapes job listings, indexes them with embeddings for semantic search, and matches candidate CVs to relevant job postings. Built to demonstrate web scraping, NLP/embeddings, background processing, and modern API design.

---

# Why This Project?

This project demonstrates an end-to-end AI-powered recruitment pipeline:

- Automated job scraping from online job boards
- Persistent storage of job listings
- Semantic search using vector embeddings
- AI-powered CV matching and ranking
- Background processing with task queues
- REST API for frontend integration

It showcases practical backend engineering, AI, and DevOps skills that are valuable for software engineering and AI-focused roles.

---

# Features

### Job Scraping

- Scrapes job postings using Playwright
- Handles dynamic websites
- Stores structured job data into PostgreSQL

### Semantic Search

- Generates embeddings using Sentence Transformers
- Builds a local vector index
- Searches jobs by meaning instead of exact keywords

### CV Matching

- Parses candidate CVs
- Extracts skills
- Matches jobs based on semantic similarity
- Returns ranked job recommendations

### Skill Extraction

- Uses a curated technical skill dictionary
- Identifies relevant technologies and competencies from resumes

### Background Processing

- APScheduler automatically schedules scraping jobs
- Redis + RQ workers handle long-running tasks
- Prevents blocking API requests

### REST API

FastAPI backend provides endpoints for:

- Job listings
- Semantic search
- CV matching
- Authentication
- Health checks

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Backend | Python, FastAPI |
| Scraper | Playwright |
| AI/NLP | Sentence Transformers |
| LLM Integration | Google Gemini / OpenAI (Environment Configurable) |
| Database | PostgreSQL |
| Queue | Redis |
| Background Worker | RQ |
| Scheduler | APScheduler |
| Containerization | Docker, Docker Compose |
| Database Migration | Alembic |

---

# Project Structure

```text
ai-job-agent/
│
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── run_scraper.py         # Manual scraper execution
│   ├── scheduler.py           # Scheduled scraping
│   ├── worker.py              # Redis RQ worker
│   │
│   ├── agents/                # AI agent logic
│   ├── core/                  # Database models & repositories
│   ├── services/              # Business logic
│   │   ├── scraper.py
│   │   ├── semantic_search.py
│   │   ├── vector_store.py
│   │   ├── embedding_service.py
│   │   ├── skill_extractor.py
│   │   ├── jwt_service.py
│   │   └── llm_service.py
│
├── frontend/
│
├── data/                      # Vector index files
│
├── alembic/
├── docker-compose.yml
├── alembic.ini
└── README.md
```

---

# System Architecture

```text
                Scheduler
                    │
                    ▼
            Playwright Scraper
                    │
                    ▼
             PostgreSQL Database
                    │
                    ▼
      Sentence Transformer Embeddings
                    │
                    ▼
          Local Vector Store (data/)
                    │
                    ▼
        Semantic Search & CV Matching
                    │
                    ▼
             FastAPI REST API
                    │
                    ▼
               Frontend Client

        Background Tasks
              │
              ▼
         Redis + RQ Worker
```

---

# How Everything Works

1. A scheduler (or manual trigger) starts the scraper.
2. Playwright collects job listings from supported job boards.
3. Jobs are stored in PostgreSQL.
4. Sentence Transformer generates embeddings for every job.
5. Embeddings are saved into a local vector index.
6. Users submit a search query or upload a CV.
7. Semantic search compares embeddings to find similar jobs.
8. Skill extraction improves ranking accuracy.
9. FastAPI returns ranked job recommendations.
10. Heavy tasks like scraping and indexing are executed asynchronously by Redis workers.

---

# Running the Project

## Prerequisites

- Docker
- Docker Compose

---

## 1. Clone Repository

```bash
git clone https://github.com/NilayDaa/ai-job-agent

cd ai-job-agent
```

---

## 2. Create `.env`

```env
POSTGRES_DB=ai_jobs

POSTGRES_USER=postgres

POSTGRES_PASSWORD=strongpassword

REDIS_HOST=redis

REDIS_PORT=6379

JWT_SECRET=your-secret-key

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

LLM_API_KEY=your-api-key
```

---

## 3. Start Services

```bash
docker compose up --build
```

---

## 4. Run Scraper

```bash
docker compose exec ai-job-agent python app/run_scraper.py
```

---

## 5. Start Worker

```bash
docker compose exec ai-job-agent python app/worker.py
```

---

## 6. Access API

FastAPI

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# Important Configuration

## JWT Secret

Replace the default secret key with a secure environment variable before production.

---

## Embedding Model

Ensure the configured embedding model matches the expected vector dimension (384 for MiniLM models).

---

## Data Directory

The vector index is stored inside:

```
data/
```

Persist this directory in production.

---

## Redis Lock

The scheduler uses:

```
scraper_running
```

For multi-instance deployments, prefix the lock key to avoid collisions.

---

## Docker Credentials

Current PostgreSQL and Redis passwords are intended for local development only.

---

# Important Files

| File | Purpose |
|------|----------|
| `app/config.py` | Search keywords and configuration |
| `app/services/scraper.py` | Job scraping logic |
| `app/services/vector_store.py` | Embedding index |
| `app/services/semantic_search.py` | Semantic search |
| `app/services/skill_extractor.py` | Skill extraction |
| `app/services/jwt_service.py` | Authentication |
| `app/main.py` | FastAPI application |
| `docker-compose.yml` | Local deployment |

---

# Engineering Decisions

### Why Sentence Transformers?

- Lightweight
- Fast inference
- Good semantic similarity
- Open-source
- Works well without expensive APIs

---

### Why Redis + RQ?

- Simple task queue
- Reliable background processing
- Easy integration with FastAPI
- Prevents blocking HTTP requests

---

### Why PostgreSQL?

- Strong relational model
- Reliable indexing
- Easy migrations using Alembic

---

### Why FastAPI?

- Automatic API documentation
- Excellent performance
- Type safety
- Async support

---

# Future Improvements

- Support multiple job boards through modular scraper adapters
- Replace static skill lists with NER or LLM-based extraction
- Store embeddings in a scalable vector database (Milvus, Pinecone, or Weaviate)
- Improve scraper resilience against website changes
- Add authentication with candidate profiles and dashboards
- Build a recommendation engine using user feedback
- Deploy using Kubernetes
- Add automated testing and CI/CD pipelines

---

# Interview Talking Points

If discussing this project in an interview, focus on:

- Designing scalable web scrapers
- Semantic search with vector embeddings
- Trade-offs between embedding models
- Background task processing with Redis and RQ
- Efficient indexing and updating of vector stores
- Production deployment considerations
- Extending the system for multiple job sources
- Using AI to improve recruitment workflows

---

# Repository

GitHub:

**https://github.com/NilayDaa/ai-job-agent**

---

# Live Demo

Visit: **https://nilaydas.com**

---

# Author

**Nilay Das**

Bachelor of Information and Communication Technology

JAMK University of Applied Sciences

Software Engineering | AI | Cyber Security

GitHub: https://github.com/NilayDaa
