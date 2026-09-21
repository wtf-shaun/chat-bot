import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, name TEXT NOT NULL, target_person TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, conversation_id INTEGER NOT NULL, timestamp TEXT, sender TEXT NOT NULL, message TEXT NOT NULL, is_target INTEGER DEFAULT 0, FOREIGN KEY(conversation_id) REFERENCES conversations(id));
CREATE TABLE IF NOT EXISTS style_profiles (conversation_id INTEGER PRIMARY KEY, target_person TEXT NOT NULL, profile_json TEXT NOT NULL, FOREIGN KEY(conversation_id) REFERENCES conversations(id));
CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, conversation_id INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(conversation_id) REFERENCES conversations(id));
CREATE TABLE IF NOT EXISTS session_messages (id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(session_id) REFERENCES sessions(id));
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_target ON messages(conversation_id, is_target);
"""


def init_db(path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)

@contextmanager
def connection(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def json_dumps(value):
    return json.dumps(value, ensure_ascii=False)
