import os
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import init_db, create_session, get_session, save_interaction, get_interactions
from app.resume_parser import extract_text_from_pdf, extract_candidate_name, extract_skills
from app.rag import ingest_knowledge_base, retrieve_context, ROLES
from app.question_generator import generate_question, evaluate_answer

app = FastAPI(title='Role Based Candidate Screening System')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

UPLOAD_DIR = 'data/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

class GenerateQuestionRequest(BaseModel):
    session_id: int

class SubmitAnswerRequest(BaseModel):
    session_id: int
    question: str
    answer: str
    retrieved_context: Optional[str] = ''

@app.on_event('startup')
def startup():
    init_db()
    ingest_knowledge_base()

@app.get('/')
def home():
    return {'message': 'Role Based Candidate Screening System API is running'}

@app.get('/roles')
def roles():
    return {'roles': list(ROLES.keys())}

@app.post('/upload-resume')
def upload_resume(role: str = Form(...), file: UploadFile = File(...)):
    if role not in ROLES:
        raise HTTPException(status_code=400, detail='Invalid role selected')
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Please upload a PDF resume')
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = extract_text_from_pdf(path)
    if not text:
        raise HTTPException(status_code=400, detail='Could not extract text from resume')
    name = extract_candidate_name(text)
    skills = extract_skills(text)
    session_id = create_session(name, role, text, skills)
    return {
        'session_id': session_id,
        'candidate_name': name,
        'role': role,
        'skills': skills,
        'message': 'Resume uploaded and parsed successfully'
    }

@app.post('/generate-question')
def generate_next_question(payload: GenerateQuestionRequest):
    session = get_session(payload.session_id)

    if not session:
        raise HTTPException(status_code=404, detail='Session not found')

    skills_text = session.get('skills', '')
    skills = [s.strip() for s in skills_text.split(',') if s.strip()]

    previous_records = get_interactions(payload.session_id)

    asked_questions = [
        item.get('question', '')
        for item in previous_records
        if item.get('question')
    ]

    previous_answers = [
        item.get('answer', '')
        for item in previous_records
        if item.get('answer')
    ]

    context = retrieve_context(session['role'], skills, previous_answers)

    question = generate_question(
        role=session['role'],
        skills=skills,
        context=context,
        asked_questions=asked_questions,
        question_number=len(asked_questions) + 1
    )

    return {
        'session_id': payload.session_id,
        'question': question,
        'question_number': len(asked_questions) + 1,
        'retrieved_context': context
    }
@app.post('/submit-answer')
def submit_answer(payload: SubmitAnswerRequest):
    session = get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail='Session not found')
    score, feedback = evaluate_answer(payload.question, payload.answer)
    save_interaction(payload.session_id, payload.question, payload.answer, score, feedback, payload.retrieved_context or '')
    return {'score': score, 'feedback': feedback, 'message': 'Answer stored successfully'}

@app.get('/summary/{session_id}')
def summary(session_id: int):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail='Session not found')
    interactions = get_interactions(session_id)
    scores = [x['score'] for x in interactions if x['score'] is not None]
    avg = round(sum(scores) / len(scores), 2) if scores else 0
    return {
        'session': session,
        'interactions': interactions,
        'total_questions': len(interactions),
        'average_score': avg,
        'insight': 'Candidate shows stronger performance when answers include concepts, metrics, examples, and real project reasoning.'
    }
