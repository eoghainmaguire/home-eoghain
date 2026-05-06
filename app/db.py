import sqlite3
from pathlib import Path

from flask import current_app, g

from .seed import seed_database


SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    role_line TEXT NOT NULL,
    location TEXT NOT NULL,
    intro TEXT NOT NULL,
    email TEXT NOT NULL,
    github_url TEXT NOT NULL,
    linkedin_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    tags TEXT NOT NULL,
    status TEXT NOT NULL,
    tech_stack TEXT NOT NULL DEFAULT '',
    key_features TEXT NOT NULL DEFAULT '',
    security_focus TEXT NOT NULL DEFAULT '',
    note_label TEXT NOT NULL DEFAULT '',
    note TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    level TEXT NOT NULL,
    evidence_note TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    status TEXT NOT NULL,
    sort_order INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS command_logs (
    id INTEGER PRIMARY KEY,
    command TEXT NOT NULL,
    status TEXT NOT NULL,
    ip_hash TEXT NOT NULL,
    user_agent_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db():
    if "db" not in g:
        db_path = Path(current_app.config["DATABASE"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    ensure_project_columns(db)
    seed_database(db)
    db.commit()


def rows_to_dicts(rows):
    return [dict(row) for row in rows]


def ensure_project_columns(db):
    columns = {row["name"] for row in db.execute("PRAGMA table_info(projects)").fetchall()}
    additions = {
        "tech_stack": "TEXT NOT NULL DEFAULT ''",
        "key_features": "TEXT NOT NULL DEFAULT ''",
        "security_focus": "TEXT NOT NULL DEFAULT ''",
        "note_label": "TEXT NOT NULL DEFAULT ''",
        "note": "TEXT NOT NULL DEFAULT ''",
    }

    for column, definition in additions.items():
        if column not in columns:
            db.execute(f"ALTER TABLE projects ADD COLUMN {column} {definition}")
