from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

class ResumeData(BaseModel):
    job_role: str
    experience_level: str

sessions = {}

@app.post("/")
async def resume_tips(data: ResumeData, request: Request):
    session_id = request.headers.get("session-id", "guest")
    
    if not data.job_role or not data.experience_level:
        raise HTTPException(status_code=400, detail="Please fill both fields")
    
    try:
        prompt = f"Resume tips for {data.job_role} at {data.experience_level} level. Give 5 specific tips."
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        if session_id not in sessions:
            sessions[session_id] = {"chat_history": [], "saved": True}
        
        user_input = f"Resume Tips: {data.job_role} ({data.experience_level})"
        sessions[session_id]["chat_history"].append([user_input, response_text])
        sessions[session_id]["saved"] = False
        
        return {"response": response_text, "history": sessions[session_id]["chat_history"], "updated_history": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

handler = app