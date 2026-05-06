from flask import Blueprint, jsonify, render_template, request

from .commands import project_payload, run_simulated_command
from .db import get_db, rows_to_dicts
from .security import is_rate_limited, request_fingerprint


bp = Blueprint("portfolio", __name__)


@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@bp.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Something went wrong."}), 500


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "/home/eoghain"})


@bp.get("/api/profile")
def profile():
    db = get_db()
    row = db.execute("SELECT * FROM profile WHERE id = 1").fetchone()
    return jsonify(dict(row))


@bp.get("/api/projects")
def projects():
    db = get_db()
    return jsonify(project_payload(db))


@bp.get("/api/skills")
def skills():
    db = get_db()
    rows = db.execute("SELECT * FROM skills ORDER BY sort_order").fetchall()
    return jsonify(rows_to_dicts(rows))


@bp.get("/api/logs")
def logs():
    db = get_db()
    rows = db.execute("SELECT * FROM logs ORDER BY sort_order").fetchall()
    return jsonify(rows_to_dicts(rows))


@bp.post("/api/command")
def command():
    db = get_db()
    ip_hash, user_agent_hash = request_fingerprint()

    if is_rate_limited(ip_hash):
        result = {
            "status": "error",
            "output": "Too many quick command requests. Please wait a moment and try again.",
            "command": "",
        }
        log_command(db, "", "rate_limited", ip_hash, user_agent_hash)
        return jsonify(result), 429

    payload = request.get_json(silent=True) or {}
    result = run_simulated_command(db, payload.get("command", ""))
    log_command(db, result.get("command", ""), result["status"], ip_hash, user_agent_hash)
    return jsonify(result)


@bp.get("/security.txt")
def security_txt():
    return (
        "Contact: mailto:placeholder@example.com\n"
        "Preferred-Languages: en\n"
        "Policy: This student portfolio is read-only. Please report security issues responsibly.\n",
        200,
        {"Content-Type": "text/plain; charset=utf-8"},
    )


def log_command(db, command_text, status, ip_hash, user_agent_hash):
    db.execute(
        """
        INSERT INTO command_logs (command, status, ip_hash, user_agent_hash)
        VALUES (?, ?, ?, ?)
        """,
        (command_text[:80], status, ip_hash, user_agent_hash),
    )
    db.commit()
