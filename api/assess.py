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

class AssessmentData(BaseModel):
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str

sessions = {}

@app.post("/")
async def assess_career(data: AssessmentData, request: Request):
    session_id = request.headers.get("session-id", "guest")
    
    if not all([data.q1, data.q2, data.q3, data.q4, data.q5]):
        raise HTTPException(status_code=400, detail="Please answer all questions")
    
    try:
        prompt = f"""Career assessment:
        1. Work environment: {data.q1}
        2. Work style: {data.q2}
        3. Task preference: {data.q3}
        4. Work-life balance: {data.q4}
        5. Routine preference: {data.q5}
        
        Suggest 3 career paths with explanations."""
        
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        if session_id not in sessions:
            sessions[session_id] = {"chat_history": [], "saved": True}
        
        user_input = f"Career Assessment: {data.q1}, {data.q2}, {data.q3}, {data.q4}, {data.q5}"
        sessions[session_id]["chat_history"].append([user_input, response_text])
        sessions[session_id]["saved"] = False
        
        return {"response": response_text, "history": sessions[session_id]["chat_history"], "updated_history": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

handler = app