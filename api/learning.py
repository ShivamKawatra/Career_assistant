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

class LearningData(BaseModel):
    skill: str
    learning_style: str

sessions = {}

@app.post("/")
async def learning_resources(data: LearningData, request: Request):
    session_id = request.headers.get("session-id", "guest")
    
    if not data.skill or not data.learning_style:
        raise HTTPException(status_code=400, detail="Please fill both fields")
    
    try:
        prompt = f"Learning resources for {data.skill} with {data.learning_style} learning style."
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        if session_id not in sessions:
            sessions[session_id] = {"chat_history": [], "saved": True}
        
        user_input = f"Learning Resources: {data.skill} ({data.learning_style})"
        sessions[session_id]["chat_history"].append([user_input, response_text])
        sessions[session_id]["saved"] = False
        
        return {"response": response_text, "history": sessions[session_id]["chat_history"], "updated_history": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

handler = app