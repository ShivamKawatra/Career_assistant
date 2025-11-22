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

class ContactData(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@app.post("/")
async def contact_us(data: ContactData):
    if not all([data.name, data.email, data.subject, data.message]):
        raise HTTPException(status_code=400, detail="Please fill all fields")
    return {"message": "Thank you for contacting us! We'll get back to you soon."}

handler = app