# AI-Powered Role-Based Candidate Screening System

## Overview

AI-Powered Role-Based Candidate Screening System is an intelligent interview automation platform designed to simulate structured technical interviews using Retrieval-Augmented Generation (RAG). The system dynamically generates interview questions based on the candidate's resume, selected job role, and a role-specific knowledge base, creating a personalized and context-aware screening experience.

Unlike traditional questionnaire-based systems, this platform adapts interview topics according to the candidate's technical background, enabling more relevant and meaningful assessments.

---

## Key Features

### Resume Intelligence

* PDF resume upload and processing
* Candidate name extraction
* Automated skill identification
* Technology stack recognition
* Resume-driven interview personalization

### Role-Based Screening

* Dynamic role selection
* Role-specific knowledge repositories
* Context-aware evaluation strategy
* Customized interview flow

### Retrieval-Augmented Generation (RAG)

* Knowledge base ingestion
* Intelligent text chunking
* Embedding generation
* Vector storage and retrieval
* Context-aware question generation
* Retrieval traceability

### Interactive Interview Engine

* Dynamic question generation
* Multi-stage interview workflow
* Candidate response collection
* Session continuity management
* Context preservation across interview rounds

### Evaluation & Analytics

* Automated answer scoring
* Feedback generation
* Interview session tracking
* Candidate performance summary
* Historical interaction storage

---

## System Architecture

```text
                           Candidate Resume
                                   │
                                   ▼
                          Resume Processing
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
              Skill Extraction           Role Selection
                     │                           │
                     └─────────────┬─────────────┘
                                   ▼
                        Context Construction
                                   │
                                   ▼
                        Retrieval-Augmented
                          Generation (RAG)
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
 Knowledge Base           Embedding Engine          Vector Storage
                                   │
                                   ▼
                        Similarity-Based Retrieval
                                   │
                                   ▼
                        Interview Question Generator
                                   │
                                   ▼
                         Candidate Response
                                   │
                                   ▼
                         Evaluation & Scoring
                                   │
                                   ▼
                            Session Summary
```

---

## Technology Stack

### Frontend

* React.js
* Vite
* Axios
* CSS

### Backend

* FastAPI
* Python
* Pydantic
* SQLite

### AI/ML Components

* Retrieval-Augmented Generation (RAG)
* Text Chunking
* Embedding Generation
* Similarity Search
* Resume Parsing
* Skill Extraction

### Database

* SQLite
* Vector Storage Layer
* Session Persistence

---

## Retrieval-Augmented Generation Pipeline

### Knowledge Ingestion

Role-specific knowledge sources are processed and transformed into searchable chunks.

### Chunking Strategy

Documents are segmented into overlapping chunks to preserve contextual continuity while improving retrieval efficiency.

### Embedding Generation

Each chunk is converted into a vector representation using a lightweight embedding mechanism.

### Vector Storage

Generated embeddings and associated text chunks are stored in a dedicated vector storage layer within SQLite.

### Retrieval Process

Interview context is constructed dynamically using:

* Selected job role
* Extracted resume skills
* Previous candidate responses

Relevant knowledge chunks are retrieved using cosine similarity search.

### Context-Aware Question Generation

Retrieved content is used to generate role-specific interview questions tailored to the candidate's profile.

---

## Workflow

### Step 1: Candidate Registration

* Candidate uploads resume
* Candidate selects target role

### Step 2: Resume Analysis

* Resume text extraction
* Skill identification
* Technology mapping

### Step 3: Context Construction

* Resume insights combined with selected role
* Dynamic query generation

### Step 4: Knowledge Retrieval

* Similarity search over role-specific knowledge base
* Retrieval of relevant content chunks

### Step 5: Interview Generation

* Context-aware technical questions generated
* Questions aligned with candidate expertise

### Step 6: Response Evaluation

* Candidate answers recorded
* Scores and feedback generated

### Step 7: Summary Generation

* Complete interview report
* Performance insights
* Session analytics

---

## API Endpoints

| Method | Endpoint                | Description                            |
| ------ | ----------------------- | -------------------------------------- |
| GET    | `/roles`                | Retrieve available roles               |
| POST   | `/upload-resume`        | Upload and parse candidate resume      |
| POST   | `/generate-question`    | Generate contextual interview question |
| POST   | `/submit-answer`        | Submit and evaluate answer             |
| GET    | `/summary/{session_id}` | Retrieve interview summary             |

---

## Database Design

### Sessions Table

Stores:

* Candidate information
* Selected role
* Resume content
* Extracted skills
* Session metadata

### Interactions Table

Stores:

* Generated questions
* Candidate answers
* Scores
* Feedback
* Retrieved context

### Vector Chunks Table

Stores:

* Knowledge chunks
* Vector embeddings
* Role mappings

---

## Design Decisions

### FastAPI

Selected for high performance, clean API design, asynchronous support, and automatic OpenAPI documentation.

### React + Vite

Chosen to provide a responsive user experience with rapid development and lightweight build tooling.

### SQLite

Used as a lightweight persistence layer requiring minimal setup while supporting structured data and vector storage.

### Local Vector Database

A custom vector retrieval layer was implemented within SQLite to eliminate external infrastructure dependencies while maintaining retrieval capabilities.

### Explainable RAG

Retrieved context is stored and exposed within the workflow to ensure transparency and traceability of generated interview questions.

---

## Project Structure

```text
project/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── rag.py
│   │   ├── database.py
│   │   ├── resume_parser.py
│   │   └── question_generator.py
│   │
│   ├── data/
│   └── requirements.txt
│
└── README.md
```

---

## Setup Instructions

### Backend

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

API Documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## Future Enhancements

* LLM-powered answer evaluation
* Advanced semantic embeddings
* FAISS/ChromaDB integration
* Multi-role interview pathways
* Difficulty adaptation based on performance
* Candidate ranking system
* PDF interview report generation
* Authentication and authorization
* Administrative analytics dashboard
* Cloud deployment support

---

## Conclusion

This project demonstrates the integration of Artificial Intelligence, Retrieval-Augmented Generation, Backend Engineering, Frontend Development, and Database Design into a unified candidate screening platform. The system provides a scalable foundation for automated technical interviews while maintaining transparency, contextual relevance, and structured evaluation.
