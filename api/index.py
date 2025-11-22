from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
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

# Load API key
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Data models
class ChatMessage(BaseModel):
    message: str

class AuthData(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    confirm_password: Optional[str] = None
    full_name: Optional[str] = None

class ContactData(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class AssessmentData(BaseModel):
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str

class SkillsData(BaseModel):
    current_skills: str
    target_role: str

class ResumeData(BaseModel):
    job_role: str
    experience_level: str

class MarketData(BaseModel):
    field: str
    location: str

class LearningData(BaseModel):
    skill: str
    learning_style: str

# Storage
users_db = {}
sessions = {}

@app.get("/")
async def read_root():
    return {"message": "CareerAI API is running!", "status": "ok"}

@app.post("/signup")
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

@app.post("/login")
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
    
    return {"message": f"Welcome back, {data.username}!", "session_id": session_id, "chat_history": []}

@app.post("/chat")
async def chat(data: ChatMessage, request: Request):
    session_id = request.headers.get("session-id", "guest")
    
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
            
        prompt = f"As a career advisor, answer: {data.message}"
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        if session_id not in sessions:
            sessions[session_id] = {"chat_history": [], "saved": True}
        
        sessions[session_id]["chat_history"].append([data.message, response_text])
        
        return {"response": response_text, "history": sessions[session_id]["chat_history"], "updated_history": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/assess")
async def assess_career(data: AssessmentData):
    if not all([data.q1, data.q2, data.q3, data.q4, data.q5]):
        raise HTTPException(status_code=400, detail="Please answer all questions")
    
    try:
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
            
        prompt = f"""Career assessment:
        1. Work environment: {data.q1}
        2. Work style: {data.q2}
        3. Task preference: {data.q3}
        4. Work-life balance: {data.q4}
        5. Routine preference: {data.q5}
        
        Suggest 3 career paths with explanations."""
        
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/skills")
async def analyze_skills(data: SkillsData):
    if not data.current_skills or not data.target_role:
        raise HTTPException(status_code=400, detail="Please fill both fields")
    
    try:
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
            
        prompt = f"Skills: {data.current_skills}, Target: {data.target_role}. Identify gaps and learning path."
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/resume")
async def resume_tips(data: ResumeData):
    if not data.job_role or not data.experience_level:
        raise HTTPException(status_code=400, detail="Please fill both fields")
    
    try:
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
            
        prompt = f"Resume tips for {data.job_role} at {data.experience_level} level. Give 5 specific tips."
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/market")
async def market_insights(data: MarketData):
    if not data.field or not data.location:
        raise HTTPException(status_code=400, detail="Please fill both fields")
    
    try:
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
            
        prompt = f"Job market insights for {data.field} in {data.location}. Include salary and trends."
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/learning")
async def learning_resources(data: LearningData):
    if not data.skill or not data.learning_style:
        raise HTTPException(status_code=400, detail="Please fill both fields")
    
    try:
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
            
        prompt = f"Learning resources for {data.skill} with {data.learning_style} learning style."
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/contact")
async def contact_us(data: ContactData):
    if not all([data.name, data.email, data.subject, data.message]):
        raise HTTPException(status_code=400, detail="Please fill all fields")
    return {"message": "Thank you for contacting us! We'll get back to you soon."}

handler = app