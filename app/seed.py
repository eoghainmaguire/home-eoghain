PROFILE = {
    "id": 1,
    "name": "Eoghain Maguire",
    "title": "/home/eoghain",
    "role_line": "Computing student specialising in Cybersecurity & Digital Forensics",
    "location": "Ireland",
    "intro": "A personal cybersecurity portfolio focused on secure development, practical labs, and learning through building.",
    "email": "placeholder@example.com",
    "github_url": "https://github.com/placeholder",
    "linkedin_url": "https://linkedin.com/in/placeholder",
}

PROJECTS = [
    {
        "slug": "secure-student-online-voting-system",
        "title": "Secure Student Online Voting System",
        "summary": "A Flask-based student voting platform designed to support secure elections, anonymous voting, role-based access, and audit logging.",
        "tags": "Flask, MySQL, RBAC, Audit Logging, Ranked-choice voting",
        "status": "Completed academic team project",
        "tech_stack": "Python, Flask, SQLAlchemy, MySQL, HTML, CSS, JavaScript",
        "key_features": "Student login, Admin election management, Candidate management, One vote per student per election, Anonymous vote handling, Results page, Ranked-choice / instant-runoff voting, Auditor role, Audit logging",
        "security_focus": "Password hashing, Login lockout after failed attempts, Role-based access control, Server-side validation, Audit logging, One-vote-per-election constraint, Separation between voter identity and vote visibility",
        "note_label": "Contribution",
        "note": "Built as a team academic project. My contribution focused on backend functionality, database structure, security features, ranked-choice tallying, dashboard styling, and general bug fixing/refinement.",
        "sort_order": 1,
    },
    {
        "slug": "phishing-awareness-training-platform",
        "title": "Phishing Awareness Training Platform",
        "summary": "A small Flask and SQLite security project exploring phishing awareness, behavioural risk signals, secure input handling, and audit-style interaction logging.",
        "tags": "Flask, SQLite, CSRF, Security Review, Behavioural Analytics",
        "status": "Completed personal security project",
        "tech_stack": "Python, Flask, SQLite, HTML, CSS, JavaScript",
        "key_features": "Simulated phishing awareness campaigns, User interaction tracking, Click-rate tracking, Time-to-click measurement, Repeat interaction detection, Simple behavioural risk scoring, Audit-style event logging, Admin-style overview of campaign/user behaviour",
        "security_focus": "CSRF protection added to sensitive actions, Server-side validation, Reduced trust in client-side input, Safer handling of user-controlled data, Audit-style logging of interactions, Behavioural detection logic for risky patterns",
        "note_label": "Learning note",
        "note": "This project was used to explore how AI-assisted development can generate functional code that still needs security review. The main learning outcome was reviewing, questioning, and improving generated code from a security perspective.",
        "sort_order": 2,
    },
]

SKILLS = [
    ("Web Security", "Application Security", "Learning", "Evidence link to be added later.", 1),
    ("Flask", "Backend Development", "Building", "Evidence link to be added later.", 2),
    ("SQL", "Data", "Practising", "Evidence link to be added later.", 3),
    ("Linux", "Systems", "Practising", "Evidence link to be added later.", 4),
    ("Networking", "Infrastructure", "Learning", "Evidence link to be added later.", 5),
    ("Secure Coding", "Development Practice", "Building", "Evidence link to be added later.", 6),
    ("Git/GitHub", "Workflow", "Practising", "Evidence link to be added later.", 7),
    ("Wireshark", "Network Analysis", "Learning", "Evidence link to be added later.", 8),
]

LOGS = [
    ("Building secure Flask apps", "Placeholder learning log. Full write-up to be added later.", "Draft placeholder", 1),
    ("Learning OT security basics", "Placeholder learning log. Full write-up to be added later.", "Draft placeholder", 2),
    ("Reviewing AI-generated code securely", "Placeholder learning log. Full write-up to be added later.", "Draft placeholder", 3),
]


def seed_database(db):
    db.execute(
        """
        INSERT INTO profile (id, name, title, role_line, location, intro, email, github_url, linkedin_url)
        VALUES (:id, :name, :title, :role_line, :location, :intro, :email, :github_url, :linkedin_url)
        ON CONFLICT(id) DO NOTHING
        """,
        PROFILE,
    )

    sync_projects(db)

    existing_skills = db.execute("SELECT id FROM skills LIMIT 1").fetchone()
    if not existing_skills:
        db.executemany(
            """
            INSERT INTO skills (name, category, level, evidence_note, sort_order)
            VALUES (?, ?, ?, ?, ?)
            """,
            SKILLS,
        )

    existing_logs = db.execute("SELECT id FROM logs LIMIT 1").fetchone()
    if not existing_logs:
        db.executemany(
            """
            INSERT INTO logs (title, summary, status, sort_order)
            VALUES (?, ?, ?, ?)
            """,
            LOGS,
        )


def sync_projects(db):
    db.execute("DELETE FROM projects")
    db.executemany(
        """
        INSERT INTO projects (
            slug,
            title,
            summary,
            tags,
            status,
            tech_stack,
            key_features,
            security_focus,
            note_label,
            note,
            sort_order
        )
        VALUES (
            :slug,
            :title,
            :summary,
            :tags,
            :status,
            :tech_stack,
            :key_features,
            :security_focus,
            :note_label,
            :note,
            :sort_order
        )
        """,
        PROJECTS,
    )
