from .db import rows_to_dicts


ALLOWED_COMMANDS = {"help", "whoami", "projects", "skills", "status", "clear"}
SUSPICIOUS_PATTERNS = [";", "&&", "|", ">", "<", "$", "`", "../", "./", "~/", "\\"]
MAX_COMMAND_LENGTH = 80


def validate_command(raw_command):
    if not isinstance(raw_command, str):
        return "blocked", ""

    command = raw_command.strip().lower()
    if len(command) > MAX_COMMAND_LENGTH:
        return "blocked", command[:MAX_COMMAND_LENGTH]

    if any(pattern in command for pattern in SUSPICIOUS_PATTERNS):
        return "blocked", command

    if command not in ALLOWED_COMMANDS:
        return "error", command

    return "ok", command


def run_simulated_command(db, raw_command):
    """Return controlled portfolio content. This never executes operating system commands."""
    validation_status, command = validate_command(raw_command)

    if validation_status == "blocked":
        return {
            "status": "blocked",
            "output": "Input rejected by command validation.",
            "command": command,
        }

    if validation_status == "error":
        return {
            "status": "error",
            "output": "Command not recognised. Try: help, whoami, projects, skills, status, or clear.",
            "command": command,
        }

    if command == "help":
        output = "Try: whoami, projects, skills, status, or clear. You can also use the normal page navigation."
    elif command == "whoami":
        profile = db.execute("SELECT name, role_line, location FROM profile WHERE id = 1").fetchone()
        output = f"{profile['name']} - {profile['role_line']} - {profile['location']}"
    elif command == "projects":
        rows = db.execute("SELECT title FROM projects ORDER BY sort_order").fetchall()
        output = "Projects: " + ", ".join(row["title"] for row in rows)
    elif command == "skills":
        rows = db.execute("SELECT name, level FROM skills ORDER BY sort_order").fetchall()
        output = "Skill matrix: " + ", ".join(f"{row['name']} ({row['level']})" for row in rows)
    elif command == "status":
        output = "Current status: Building practical cybersecurity projects. Portfolio mode: Read-only."
    else:
        output = ""

    return {"status": "ok", "output": output, "command": command}


def project_payload(db):
    projects = rows_to_dicts(db.execute("SELECT * FROM projects ORDER BY sort_order").fetchall())
    for project in projects:
        project["tags"] = [tag.strip() for tag in project["tags"].split(",")]
        project["tech_stack"] = [item.strip() for item in project["tech_stack"].split(",") if item.strip()]
        project["key_features"] = [item.strip() for item in project["key_features"].split(",") if item.strip()]
        project["security_focus"] = [item.strip() for item in project["security_focus"].split(",") if item.strip()]
    return projects
