# FastAPI AI Interview Coach

A backend project for practicing interview questions using AI analysis. Built with FastAPI, this service allows users to go through sessions, submit answers, and receive automated feedback. Includes JWT authentication, automated tests, and CI/CD integration.

## Features

- RESTful API with FastAPI
- AI response analysis module
- JWT authentication (RS256)
- PostgreSQL database via SQLAlchemy
- Automated testing with pytest
- GitHub Actions CI/CD pipeline

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL + SQLAlchemy
- Pydantic
- Pytest + httpx + pytest-asyncio
- GitHub Actions (CI/CD)


## Testing

pytest
Covers:
```bash
Business logic (sessions, answers, analysis)

API endpoints (async testing with httpx)

JWT auth (RS256)

Database interactions

CI/CD
```
GitHub Actions runs:
```bash
Automated tests

Type checking (mypy)

Code linting (ruff)
```
Quick Start
```bash
git clone https://github.com/bbtqqrl/FastApi-AI-Interview-Coach
cd FastApi-AI-Interview-Coach
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
