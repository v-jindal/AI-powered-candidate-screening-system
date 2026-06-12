import os
import sqlite3
from datetime import datetime

DB_PATH = os.getenv('DATABASE_PATH', 'data/interviews.db')


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_name TEXT,
        role TEXT NOT NULL,
        resume_text TEXT,
        skills TEXT,
        created_at TEXT NOT NULL
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        answer TEXT,
        score INTEGER,
        feedback TEXT,
        retrieved_context TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS vector_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        vector TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def create_session(candidate_name, role, resume_text, skills):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO sessions(candidate_name, role, resume_text, skills, created_at) VALUES (?, ?, ?, ?, ?)',
        (candidate_name, role, resume_text, ', '.join(skills), datetime.utcnow().isoformat())
    )
    sid = cur.lastrowid
    conn.commit()
    conn.close()
    return sid


def get_session(session_id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM sessions WHERE id=?', (session_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def save_interaction(session_id, question, answer, score, feedback, retrieved_context):
    conn = get_connection()
    conn.execute(
        'INSERT INTO interactions(session_id, question, answer, score, feedback, retrieved_context, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (session_id, question, answer, score, feedback, retrieved_context, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def get_interactions(session_id):
    conn = get_connection()
    rows = conn.execute('SELECT * FROM interactions WHERE session_id=? ORDER BY id', (session_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def replace_vectors(role, vectors):
    conn = get_connection()
    conn.execute('DELETE FROM vector_chunks WHERE role=?', (role,))
    conn.executemany('INSERT INTO vector_chunks(role, chunk_text, vector) VALUES (?, ?, ?)', vectors)
    conn.commit()
    conn.close()


def load_vectors(role):
    conn = get_connection()
    rows = conn.execute('SELECT * FROM vector_chunks WHERE role=?', (role,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
