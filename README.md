# /home/eoghain

A personal cybersecurity portfolio built with Flask, SQLite, HTML, CSS, and vanilla JavaScript.

## Overview

`/home/eoghain` is a clean, terminal-inspired portfolio site for presenting my projects and contact details.

The portfolio currently highlights two completed projects:

- Secure Student Online Voting System
- Phishing Awareness Training Platform

## Features

- Flask-backed portfolio data
- SQLite database
- Dynamic project rendering
- Clean responsive frontend
- Security-focused project presentation
- Basic security headers

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## Running Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

The app runs locally at:

```text
http://127.0.0.1:5000
```

## Deployment

For Render or a similar Python hosting platform:

```bash
pip install -r requirements.txt
```

Use this start command:

```bash
gunicorn app:app
```

Set this environment variable before deploying:

```text
SECRET_KEY=<secure-random-value>
```

The SQLite database is created and seeded automatically on first run. Set `DATABASE_PATH` only if the deployment platform needs the database file in a specific writable location.

## Project Structure

```text
home-eoghain/
├── app.py
├── requirements.txt
├── app/
│   ├── routes.py
│   ├── db.py
│   ├── seed.py
│   ├── security.py
│   ├── templates/
│   └── static/
└── instance/
```

## Security Notes

- Security headers are applied to responses.
- Public routes are read-only except for the controlled command API endpoint.
- No production secrets should be committed.
- Set `SECRET_KEY` through an environment variable before deployment.
