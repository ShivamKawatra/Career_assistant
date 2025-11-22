from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthData(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    confirm_password: Optional[str] = None
    full_name: Optional[str] = None

# Simple in-memory storage (use database in production)
users_db = {}
sessions = {}

@app.post("/")
async def login(data: AuthData):
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="Please enter username and password")
    
    if data.username not in users_db or users_db[data.username]["password"] != data.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    session_id = f"{data.username}_{datetime.now().timestamp()}"
    sessions[session_id] = {
        "username": data.username,
        "chat_history": [],
        "saved": True
    }
    
    if "chat_history" not in users_db[data.username]:
        users_db[data.username]["chat_history"] = []
    
    chat_list = [f"{chat['timestamp']} - {chat['title']}" for chat in users_db[data.username]["chat_history"]]
    return {"message": f"Welcome back, {data.username}!", "session_id": session_id, "chat_history": chat_list}

handler = app