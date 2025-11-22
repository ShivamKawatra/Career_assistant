from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.post("/")
async def signup(data: AuthData):
    if not data.username or not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Please fill all fields")
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    users_db[data.username] = {
        "email": data.email,
        "password": data.password,
        "full_name": data.full_name or data.username,
        "chat_history": []
    }
    return {"message": "Account created successfully! Please login."}

handler = app