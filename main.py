from pathlib import Path
import json
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
MESSAGES = DATA / "messages.json"

app = FastAPI(title="Ejigboye Newsong Jesuloluwa Portfolio API")

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/contact")
def contact(payload: ContactMessage):
    messages = []
    if MESSAGES.exists():
        try:
            messages = json.loads(MESSAGES.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            messages = []

    messages.append({
        "name": payload.name,
        "email": str(payload.email),
        "message": payload.message,
        "received_at": datetime.now(timezone.utc).isoformat()
    })
    MESSAGES.write_text(json.dumps(messages, indent=2), encoding="utf-8")
    return {"message": "Message received"}

app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")
