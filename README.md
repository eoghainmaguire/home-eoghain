# /home/eoghain

A beginner-friendly, backend-driven personal cybersecurity portfolio for **Eoghain Maguire**.

The project is a clean Flask and SQLite portfolio. It currently highlights two completed projects: Secure Student Online Voting System and Phishing Awareness Training Platform.

## What `/home/eoghain` Means

`/home/eoghain` borrows the idea of a personal home directory from Linux, but the site is not a terminal clone. Visitors get normal navigation, readable cards, clear buttons, and a friendly portfolio experience. Terminal-style details are used as small visual cues.

## Tech Stack

- Python Flask backend
- SQLite database
- HTML templates
- CSS
- Vanilla JavaScript
- No React
- No unnecessary dependencies

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Then open:

```text
http://127.0.0.1:5000
```

## Initialise and Seed the Database

The app creates and seeds `instance/portfolio.db` automatically on startup if the profile table is empty.

To reset seed data during development, stop the server, delete `instance/portfolio.db`, and start the app again.

Seed content lives in:

```text
app/seed.py
```

## API Routes

- `GET /` - portfolio dashboard
- `GET /api/health` - health check
- `GET /api/profile` - profile data
- `GET /api/projects` - completed project data
- `GET /api/skills` - skill matrix API data
- `GET /api/logs` - learning log placeholder API data
- `POST /api/command` - simulated command API handler
- `GET /security.txt` - responsible disclosure placeholder

## Example Command API

There is no command panel on the simplified homepage, but the backend command API remains available for future UI experiments and security testing.

Supported commands:

- `help`
- `whoami`
- `projects`
- `skills`
- `status`
- `clear`

Example request:

```bash
curl -X POST http://127.0.0.1:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "projects"}'
```

Example response:

```json
{
  "status": "ok",
  "output": "Projects: Secure Student Online Voting System, Phishing Awareness Training Platform",
  "command": "projects"
}
```

## Security Design Notes

- The command panel is simulated and does not execute operating system commands.
- The backend never uses `os.system`, `subprocess`, `eval`, `exec`, `shell=True`, or real shell commands for command handling.
- Commands are limited to a strict allowlist.
- Command input is capped at 80 characters.
- Suspicious patterns such as `;`, `&&`, `|`, `<`, `>`, `$`, backticks, path traversal, and backslashes are rejected.
- Command usage is logged with hashed IP address and hashed user agent only.
- Raw IP addresses are not stored.
- Basic in-memory rate limiting protects `POST /api/command`.
- Public routes are read-only except for the controlled simulated command endpoint.
- Security headers are added to every response:
  - `Content-Security-Policy`
  - `X-Content-Type-Options`
  - `Referrer-Policy`
  - `Permissions-Policy`
- Stack traces are not intentionally exposed by application handlers.

## Future Improvements

- Add fuller project case studies when content is ready.
- Add project detail pages when content is ready.
- Add screenshots or diagrams for completed projects.
- Add a small admin-only content editing workflow.
- Move rate limiting to a production-ready store if deployed behind multiple workers.
- Add tests for API routes and command validation.
- Add deployment configuration when the portfolio is ready to publish.

## Content Reminder

Project evidence, screenshots, links, and detailed write-ups should be added later.

For deployment, replace the local development `SECRET_KEY` fallback with an environment-provided secret.
