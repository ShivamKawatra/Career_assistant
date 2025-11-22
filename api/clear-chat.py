from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.get("/")
async def clear_chat(request: Request):
    session_id = request.headers.get("session-id", "guest")
    if session_id in sessions:
        sessions[session_id]["chat_history"] = []
        sessions[session_id]["saved"] = True
    return {"message": "Chat cleared!", "history": []}

handler = app