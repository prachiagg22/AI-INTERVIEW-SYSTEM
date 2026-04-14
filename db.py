import sqlite3, json
from datetime import datetime

DB_PATH = "interviews.db"
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS interviews (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate   TEXT NOT NULL,
        domain      TEXT NOT NULL,
        difficulty  TEXT NOT NULL,
        total_score REAL,
        skill_scores TEXT,
        feedback    TEXT,
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS sessions (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        interview_id INTEGER,
        question     TEXT,
        answer       TEXT,
        evaluation   TEXT,
        FOREIGN KEY(interview_id) REFERENCES interviews(id)
    );
    """)
    conn.commit()
    conn.close()

def save_interview(candidate, domain, difficulty, total_score, skill_scores, feedback):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO interviews (candidate,domain,difficulty,total_score,skill_scores,feedback) VALUES (?,?,?,?,?,?)",
        (candidate, domain, difficulty, total_score, json.dumps(skill_scores), feedback)
    )
    interview_id = cur.lastrowid
    conn.commit()
    conn.close()
    return interview_id

def save_session(interview_id, question, answer, evaluation):
    conn = get_conn()
    conn.execute(
        "INSERT INTO sessions (interview_id,question,answer,evaluation) VALUES (?,?,?,?)",
        (interview_id, question, answer, json.dumps(evaluation))
    )
    conn.commit()
    conn.close()

def get_all_interviews():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM interviews ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]