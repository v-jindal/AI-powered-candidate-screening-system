# Role-Based Candidate Screening System

A complete AI/ML & Backend Intern assignment project.

## What it does

The system simulates a structured technical interview where questions are dynamically generated using:

- Uploaded candidate resume
- User-selected target role
- Role-specific knowledge base
- RAG-style retrieval from stored vectors
- Candidate answer history

The role is **not hardcoded**. The user selects the target role from the UI.

## Tech Stack

### Frontend
- React
- Vite
- Axios

### Backend
- Python
- FastAPI
- SQLite
- PyMuPDF
- NumPy
- Scikit-learn

### RAG / Vector Storage
- Role-specific text corpus
- Chunking strategy
- Local embedding generation using hashed bag-of-words vectors
- SQLite-based vector storage table
- Cosine similarity retrieval
- Retrieved context shown in UI for traceability

This avoids ChromaDB, TensorFlow, and Microsoft C++ Build Tools errors on Windows.

## Features

- Resume PDF upload
- Role selection
- Resume parsing
- Candidate name extraction
- Skills extraction
- Knowledge base ingestion
- Text chunking
- Embedding generation
- Vector storage in SQLite
- Dynamic context retrieval
- Question generation influenced by role, resume skills, and previous answers
- Answer submission
- Basic score and feedback
- Final summary page
- FastAPI Swagger docs

## Architecture

```text
Frontend React UI
    ↓
FastAPI Backend
    ↓
Resume Parser → Skills + Candidate Name
    ↓
Role Selection
    ↓
RAG Pipeline
    ↓
Knowledge Base → Chunking → Embeddings → SQLite Vector Store
    ↓
Retrieve Relevant Context
    ↓
Generate Question
    ↓
Candidate Answer
    ↓
SQLite Storage
    ↓
Summary Page
```

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## API Flow

1. `GET /roles`
2. `POST /upload-resume`
3. `POST /generate-question`
4. `POST /submit-answer`
5. `GET /summary/{session_id}`

## Database Tables

### sessions
Stores candidate name, selected role, resume text, extracted skills, and timestamp.

### interactions
Stores questions, answers, scores, feedback, retrieved context, and timestamp.

### vector_chunks
Stores role-specific knowledge chunks and generated vectors.

## Demo Video Script

1. Open frontend.
2. Select role from dropdown.
3. Upload resume PDF.
4. Show extracted candidate name and skills.
5. Click Generate Interview Question.
6. Open retrieved context dropdown to show RAG traceability.
7. Submit answer.
8. Show score and feedback.
9. Generate another question.
10. Open final summary.
11. Open FastAPI docs.
12. Show project folder and SQLite database file.

## Design Decisions

- SQLite was used for persistence because it is lightweight and easy to run locally.
- FastAPI was selected for clean API design and automatic Swagger documentation.
- React/Vite was selected for a smooth frontend development experience.
- Local vector storage was implemented in SQLite to avoid Windows installation errors caused by ChromaDB and TensorFlow dependencies.
- Retrieved context is displayed in the UI to show traceability from knowledge base to question.

## Future Improvements

- Add Gemini/OpenAI-based question generation.
- Add FAISS or ChromaDB in production environment.
- Add login/authentication.
- Add admin dashboard.
- Add PDF report export.
- Add stronger answer evaluation using an LLM.
- Add more role-specific knowledge bases.
