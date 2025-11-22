from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ForgotPasswordData(BaseModel):
    email: str

users_db = {}

@app.post("/")
async def forgot_password(data: ForgotPasswordData):
    if not data.email:
        raise HTTPException(status_code=400, detail="Please enter your email")
    
    user_found = False
    for username, user_data in users_db.items():
        if user_data["email"] == data.email:
            user_found = True
            break
    
    if not user_found:
        raise HTTPException(status_code=400, detail="Email not found")
    
    return {"message": "Password reset instructions sent to your email!"}

handler = app