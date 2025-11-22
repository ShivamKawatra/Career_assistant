from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}
sessions = {}

@app.post("/")
async def save_chat(request: Request):
    session_id = request.headers.get("session-id")
    username = request.headers.get("username")
    
    if not session_id or not username or username not in users_db:
        raise HTTPException(status_code=400, detail="Please login to save chats")
    
    if session_id not in sessions or not sessions[session_id]["chat_history"]:
        raise HTTPException(status_code=400, detail="No chat to save")
    
    if sessions[session_id]["saved"]:
        return {"message": "Chat already saved"}
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history = sessions[session_id]["chat_history"]
    title = "New Chat"
    if history:
        title = history[0][0][:30] + "..." if len(history[0][0]) > 30 else history[0][0]
    
    chat_data = {
        "title": title,
        "timestamp": timestamp,
        "messages": history.copy()
    }
    
    users_db[username]["chat_history"].append(chat_data)
    sessions[session_id]["saved"] = True
    
    return {"message": "Chat saved successfully!"}

handler = app