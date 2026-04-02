# FastAPI Backend (Contact Email)

This backend powers:

- `POST /api/contact` - sends contact form messages to your email
- `GET /health` - health check

## Local Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Required Environment Variables

- `ALLOWED_ORIGINS` (comma-separated frontend origins)
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD` (Gmail app password recommended)
- `CONTACT_RECEIVER`

## PythonAnywhere Deploy (FastAPI)

1. Create a PythonAnywhere account and open a **Bash console**.
2. Upload/clone this repo.
3. Create venv and install dependencies:
   - `mkvirtualenv --python=/usr/bin/python3.10 portfolio-api`
   - `pip install -r backend/requirements.txt`
4. Set environment variables in your WSGI file (or use `.env` loading in app path).
5. Create a **Web app** (Manual configuration, Python 3.10+).
6. Point WSGI to ASGI app using Uvicorn workers or PythonAnywhere ASGI method.
7. Set static/domain and restart web app.
8. Verify: `https://<your-pythonanywhere-domain>/health`

## Notes

- If SMTP credentials are missing, contact endpoint returns HTTP 500.
