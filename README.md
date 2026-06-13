# AI-Powered Candidate Screening System

A role-based candidate screening platform that combines resume parsing, Retrieval-Augmented Generation (RAG), and dynamic interview generation to create personalized technical interviews.

The system analyzes a candidate's resume, extracts technical skills, retrieves relevant knowledge from a role-specific knowledge base, and generates interview questions tailored to the candidate's profile.

## Features

* Resume upload and PDF parsing
* Candidate name and skill extraction
* Role selection
* Role-specific knowledge retrieval
* RAG-based question generation
* Context-aware interview flow
* Automated answer evaluation
* Performance scoring and feedback
* Interview summary generation
* FastAPI API documentation

## Architecture

```text
Candidate Resume
        │
        ▼
 Resume Parsing
        │
        ▼
 Skill Extraction
        │
        ▼
 Role Selection
        │
        ▼
 Knowledge Base
        │
        ▼
 Text Chunking
        │
        ▼
 Embedding Generation
        │
        ▼
 Vector Storage
        │
        ▼
 Similarity Retrieval
        │
        ▼
 Question Generation
        │
        ▼
 Candidate Response
        │
        ▼
 Evaluation & Summary
```

## Tech Stack

### Frontend

* React
* Vite
* Axios

### Backend

* Python
* FastAPI
* Pydantic

### Database

* SQLite

### AI Components

* Resume Parsing
* Skill Extraction
* Retrieval-Augmented Generation (RAG)
* Embedding Generation
* Cosine Similarity Search

## Project Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── database.py
│   ├── resume_parser.py
│   └── question_generator.py
│
├── data/
│   ├── interviews.db
│   └── knowledge_base/
│
└── requirements.txt

frontend/
├── src/
├── public/
└── package.json
```

## How It Works

1. Upload a resume in PDF format.
2. Select the target role.
3. The system extracts candidate information and skills.
4. Relevant context is retrieved from the role-specific knowledge base.
5. Interview questions are generated dynamically.
6. Candidate responses are evaluated and scored.
7. A final interview summary is generated.

## API Endpoints

| Method | Endpoint                | Description                 |
| ------ | ----------------------- | --------------------------- |
| GET    | `/roles`                | Get available roles         |
| POST   | `/upload-resume`        | Upload and parse resume     |
| POST   | `/generate-question`    | Generate interview question |
| POST   | `/submit-answer`        | Evaluate answer             |
| GET    | `/summary/{session_id}` | Retrieve interview summary  |

## Setup

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Design Decisions

A lightweight SQLite-based vector storage layer was implemented to demonstrate the complete RAG workflow without requiring external vector database services. This keeps the project easy to run, evaluate, and deploy while preserving retrieval functionality.

Questions are generated using retrieved context, extracted skills, selected role, and previous interview responses, ensuring a more personalized screening experience.

## Future Improvements

* LLM-based answer evaluation
* Gemini/OpenAI integration
* FAISS or ChromaDB support
* Candidate ranking dashboard
* Authentication and authorization
* PDF interview reports
* Cloud deployment
