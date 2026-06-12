import json
import os
import re
from collections import Counter
import numpy as np
from app.database import replace_vectors, load_vectors

KB_DIR = 'data/knowledge_base'
ROLES = {
    'AI/ML Engineer': 'ai_ml_engineer.txt',
    'Backend Engineer': 'backend_engineer.txt'
}


def tokenize(text):
    return re.findall(r'[a-zA-Z][a-zA-Z0-9+#.]*', text.lower())


def chunk_text(text, chunk_size=650, overlap=120):
    chunks = []
    start = 0
    while start < len(text):
        part = text[start:start + chunk_size].strip()
        if part:
            chunks.append(part)
        start += chunk_size - overlap
    return chunks


def make_embedding(text):
    # Lightweight local embedding: hashed bag-of-words vector. Stored in SQLite as vector DB.
    vec = np.zeros(384, dtype=float)
    words = tokenize(text)
    counts = Counter(words)
    for word, count in counts.items():
        idx = hash(word) % len(vec)
        vec[idx] += float(count)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


def ingest_knowledge_base():
    os.makedirs(KB_DIR, exist_ok=True)
    for role, file_name in ROLES.items():
        path = os.path.join(KB_DIR, file_name)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        rows = []
        for chunk in chunk_text(text):
            vector = make_embedding(chunk).tolist()
            rows.append((role, chunk, json.dumps(vector)))
        replace_vectors(role, rows)


def cosine(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def retrieve_context(role, skills=None, previous_answers=None, top_k=3):
    rows = load_vectors(role)
    if not rows:
        ingest_knowledge_base()
        rows = load_vectors(role)
    query = f"Role: {role}. Skills: {', '.join(skills or [])}. Previous answers: {' '.join(previous_answers or [])}"
    qvec = make_embedding(query)
    scored = []
    for row in rows:
        score = cosine(qvec, json.loads(row['vector']))
        scored.append((score, row['chunk_text']))
    scored.sort(reverse=True, key=lambda x: x[0])
    return '\n\n'.join(chunk for _, chunk in scored[:top_k])
