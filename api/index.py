import json
import os
from urllib.parse import parse_qs

def handler(request):
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, session-id, username',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Get request data
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        body = request.get('body', '{}')
        
        if method == 'POST':
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}
        else:
            data = {}
        
        # Route handling
        if path == '/api/' or path == '/api':
            result = {"message": "CareerAI API is running!", "status": "ok"}
        elif path == '/api/signup':
            result = handle_signup(data)
        elif path == '/api/login':
            result = handle_login(data)
        elif path == '/api/chat':
            result = handle_chat(data)
        elif path == '/api/contact':
            result = handle_contact(data)
        else:
            result = {"error": "Endpoint not found"}
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": str(e)})
        }

def handle_signup(data):
    username = data.get('username', '')
    email = data.get('email', '')
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    
    if not username or not email or not password:
        return {"error": "Please fill all fields"}
    if password != confirm_password:
        return {"error": "Passwords don't match"}
    if len(password) < 6:
        return {"error": "Password must be at least 6 characters"}
    
    return {"message": "Account created successfully! Please login."}

def handle_login(data):
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return {"error": "Please enter username and password"}
    
    return {"message": f"Welcome back, {username}!", "session_id": f"{username}_123", "chat_history": []}

def handle_chat(data):
    message = data.get('message', '').strip()
    
    if not message:
        return {"error": "Message cannot be empty"}
    
    # Simple response without AI for now
    response_text = f"Thank you for your message: '{message}'. This is a demo response. Please configure your Gemini API key for AI responses."
    
    return {"response": response_text, "history": [[message, response_text]], "updated_history": True}

def handle_contact(data):
    name = data.get('name', '')
    email = data.get('email', '')
    subject = data.get('subject', '')
    message = data.get('message', '')
    
    if not all([name, email, subject, message]):
        return {"error": "Please fill all fields"}
    
    return {"message": "Thank you for contacting us! We'll get back to you soon."}