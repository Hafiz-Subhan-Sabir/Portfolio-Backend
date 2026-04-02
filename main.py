import os
import smtplib
from email.message import EmailMessage
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

load_dotenv()

APP_NAME = "Portfolio Backend API"
ALLOWED_ORIGINS = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",") if x.strip()]
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
CONTACT_RECEIVER = os.getenv("CONTACT_RECEIVER", "hafizsubhan909@gmail.com")

app = FastAPI(title=APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactPayload(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    project: Optional[str] = Field(default="General", max_length=200)
    message: str = Field(min_length=5, max_length=3000)


def _send_email(subject: str, body: str, reply_to: str) -> None:
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials are missing")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = CONTACT_RECEIVER
    msg["Reply-To"] = reply_to
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "service": APP_NAME}


@app.post("/api/contact")
def contact(payload: ContactPayload) -> dict:
    subject = f"[Portfolio Contact] {payload.project or 'General'} - {payload.name}"
    body = (
        f"New portfolio message\n\n"
        f"Name: {payload.name}\n"
        f"Email: {payload.email}\n"
        f"Project: {payload.project}\n\n"
        f"Message:\n{payload.message}\n"
    )
    try:
        _send_email(subject, body, str(payload.email))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to send email: {exc}") from exc
    return {"ok": True, "message": "Message sent successfully."}
