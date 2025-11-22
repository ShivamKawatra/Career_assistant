from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai
from datetime import datetime

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Simple storage
users_db = {}
sessions = {}

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, session-id, username')
        self.end_headers()

    def do_POST(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, session-id, username')
            self.end_headers()

            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            path = self.path
            session_id = self.headers.get('session-id', 'guest')
            
            if path == '/api/signup':
                result = self.handle_signup(data)
            elif path == '/api/login':
                result = self.handle_login(data)
            elif path == '/api/chat':
                result = self.handle_chat(data, session_id)
            elif path == '/api/assess':
                result = self.handle_assess(data, session_id)
            elif path == '/api/skills':
                result = self.handle_skills(data, session_id)
            elif path == '/api/resume':
                result = self.handle_resume(data, session_id)
            elif path == '/api/market':
                result = self.handle_market(data, session_id)
            elif path == '/api/learning':
                result = self.handle_learning(data, session_id)
            elif path == '/api/contact':
                result = self.handle_contact(data)
            else:
                result = {"error": "Endpoint not found"}
            
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_signup(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not username or not email or not password:
            return {"error": "Please fill all fields"}
        if password != confirm_password:
            return {"error": "Passwords don't match"}
        if len(password) < 6:
            return {"error": "Password must be at least 6 characters"}
        if username in users_db:
            return {"error": "Username already exists"}
        
        users_db[username] = {
            "email": email,
            "password": password,
            "full_name": data.get('full_name', username),
            "chat_history": []
        }
        return {"message": "Account created successfully! Please login."}

    def handle_login(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return {"error": "Please enter username and password"}
        
        if username not in users_db or users_db[username]["password"] != password:
            return {"error": "Invalid username or password"}
        
        session_id = f"{username}_{datetime.now().timestamp()}"
        sessions[session_id] = {
            "username": username,
            "chat_history": [],
            "saved": True
        }
        
        return {"message": f"Welcome back, {username}!", "session_id": session_id, "chat_history": []}

    def handle_chat(self, data, session_id):
        message = data.get('message', '').strip()
        
        if not message:
            return {"error": "Message cannot be empty"}
        
        try:
            if not api_key:
                return {"error": "API key not configured"}
                
            prompt = f"As a career advisor, answer: {message}"
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            if session_id not in sessions:
                sessions[session_id] = {"chat_history": [], "saved": True}
            
            sessions[session_id]["chat_history"].append([message, response_text])
            sessions[session_id]["saved"] = False
            
            return {"response": response_text, "history": sessions[session_id]["chat_history"], "updated_history": True}
        except Exception as e:
            return {"error": f"AI Error: {str(e)}"}

    def handle_assess(self, data, session_id):
        q1 = data.get('q1')
        q2 = data.get('q2')
        q3 = data.get('q3')
        q4 = data.get('q4')
        q5 = data.get('q5')
        
        if not all([q1, q2, q3, q4, q5]):
            return {"error": "Please answer all questions"}
        
        try:
            prompt = f"""Career assessment:
            1. Work environment: {q1}
            2. Work style: {q2}
            3. Task preference: {q3}
            4. Work-life balance: {q4}
            5. Routine preference: {q5}
            
            Suggest 3 career paths with explanations."""
            
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            return {"response": response_text}
        except Exception as e:
            return {"error": f"AI Error: {str(e)}"}

    def handle_skills(self, data, session_id):
        current_skills = data.get('current_skills')
        target_role = data.get('target_role')
        
        if not current_skills or not target_role:
            return {"error": "Please fill both fields"}
        
        try:
            prompt = f"Skills: {current_skills}, Target: {target_role}. Identify gaps and learning path."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            return {"response": response_text}
        except Exception as e:
            return {"error": f"AI Error: {str(e)}"}

    def handle_resume(self, data, session_id):
        job_role = data.get('job_role')
        experience_level = data.get('experience_level')
        
        if not job_role or not experience_level:
            return {"error": "Please fill both fields"}
        
        try:
            prompt = f"Resume tips for {job_role} at {experience_level} level. Give 5 specific tips."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            return {"response": response_text}
        except Exception as e:
            return {"error": f"AI Error: {str(e)}"}

    def handle_market(self, data, session_id):
        field = data.get('field')
        location = data.get('location')
        
        if not field or not location:
            return {"error": "Please fill both fields"}
        
        try:
            prompt = f"Job market insights for {field} in {location}. Include salary and trends."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            return {"response": response_text}
        except Exception as e:
            return {"error": f"AI Error: {str(e)}"}

    def handle_learning(self, data, session_id):
        skill = data.get('skill')
        learning_style = data.get('learning_style')
        
        if not skill or not learning_style:
            return {"error": "Please fill both fields"}
        
        try:
            prompt = f"Learning resources for {skill} with {learning_style} learning style."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            return {"response": response_text}
        except Exception as e:
            return {"error": f"AI Error: {str(e)}"}

    def handle_contact(self, data):
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        if not all([name, email, subject, message]):
            return {"error": "Please fill all fields"}
        
        return {"message": "Thank you for contacting us! We'll get back to you soon."}