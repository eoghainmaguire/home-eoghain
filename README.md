# /home/eoghain

A personal cybersecurity portfolio built with Flask, SQLite, HTML, CSS, and vanilla JavaScript.

## Overview

`/home/eoghain` is a clean, terminal-inspired portfolio site for presenting selected cybersecurity projects and contact details. The design borrows lightly from a personal Linux home directory, but the site uses normal navigation and a simple responsive layout rather than a command-line interface.

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
- Simulated command API functionality

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

## Project Structure

```text
home-eoghain/
├── app.py
├── requirements.txt
├── app/
│   ├── routes.py
│   ├── db.py
│   ├── seed.py
│   ├── commands.py
│   ├── security.py
│   ├── templates/
│   └── static/
└── instance/
```

## Security Notes

- Command-style API behaviour is simulated and does not execute shell commands.
- Command input is handled through a strict allowlist.
- Security headers are applied to responses.
- Public routes are read-only except for the controlled command API endpoint.
- No production secrets should be committed.
- Set `SECRET_KEY` through an environment variable before deployment.

## Current Status

The portfolio currently focuses on two completed projects and can be expanded as more project work is finalised.

## License

No license has been selected yet.
