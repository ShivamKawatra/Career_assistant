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
        
        # Handle query parameters for path
        if '?' in path:
            path = path.split('?')[0]
        
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
        elif path == '/api/assess':
            result = handle_assess(data)
        elif path == '/api/skills':
            result = handle_skills(data)
        elif path == '/api/resume':
            result = handle_resume(data)
        elif path == '/api/market':
            result = handle_market(data)
        elif path == '/api/learning':
            result = handle_learning(data)
        elif path == '/api/forgot-password':
            result = handle_forgot_password(data)
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
    
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            prompt = f"As a career advisor, answer: {message}"
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
        else:
            response_text = f"Thank you for your message: '{message}'. Please configure your Gemini API key for AI responses."
    except Exception as e:
        response_text = f"Error: {str(e)}"
    
    return {"response": response_text, "history": [[message, response_text]], "updated_history": True}

def handle_contact(data):
    name = data.get('name', '')
    email = data.get('email', '')
    subject = data.get('subject', '')
    message = data.get('message', '')
    
    if not all([name, email, subject, message]):
        return {"error": "Please fill all fields"}
    
    return {"message": "Thank you for contacting us! We'll get back to you soon."}

def handle_assess(data):
    q1 = data.get('q1', '')
    q2 = data.get('q2', '')
    q3 = data.get('q3', '')
    q4 = data.get('q4', '')
    q5 = data.get('q5', '')
    
    if not all([q1, q2, q3, q4, q5]):
        return {"error": "Please answer all questions"}
    
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            prompt = f"""Career assessment:
            1. Work environment: {q1}
            2. Work style: {q2}
            3. Task preference: {q3}
            4. Work-life balance: {q4}
            5. Routine preference: {q5}
            
            Suggest 3 career paths with explanations."""
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
        else:
            response_text = "Please configure your Gemini API key for AI responses."
    except Exception as e:
        response_text = f"Error: {str(e)}"
    
    return {"response": response_text, "history": [[f"Career Assessment: {q1}, {q2}, {q3}, {q4}, {q5}", response_text]], "updated_history": True}

def handle_skills(data):
    current_skills = data.get('current_skills', '')
    target_role = data.get('target_role', '')
    
    if not current_skills or not target_role:
        return {"error": "Please fill both fields"}
    
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            prompt = f"Skills: {current_skills}, Target: {target_role}. Identify gaps and learning path."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
        else:
            response_text = "Please configure your Gemini API key for AI responses."
    except Exception as e:
        response_text = f"Error: {str(e)}"
    
    return {"response": response_text, "history": [[f"Skills Analysis: {current_skills} -> {target_role}", response_text]], "updated_history": True}

def handle_resume(data):
    job_role = data.get('job_role', '')
    experience_level = data.get('experience_level', '')
    
    if not job_role or not experience_level:
        return {"error": "Please fill both fields"}
    
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            prompt = f"Resume tips for {job_role} at {experience_level} level. Give 5 specific tips."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
        else:
            response_text = "Please configure your Gemini API key for AI responses."
    except Exception as e:
        response_text = f"Error: {str(e)}"
    
    return {"response": response_text, "history": [[f"Resume Tips: {job_role} ({experience_level})", response_text]], "updated_history": True}

def handle_market(data):
    field = data.get('field', '')
    location = data.get('location', '')
    
    if not field or not location:
        return {"error": "Please fill both fields"}
    
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            prompt = f"Job market insights for {field} in {location}. Include salary and trends."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
        else:
            response_text = "Please configure your Gemini API key for AI responses."
    except Exception as e:
        response_text = f"Error: {str(e)}"
    
    return {"response": response_text, "history": [[f"Market Insights: {field} in {location}", response_text]], "updated_history": True}

def handle_learning(data):
    skill = data.get('skill', '')
    learning_style = data.get('learning_style', '')
    
    if not skill or not learning_style:
        return {"error": "Please fill both fields"}
    
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            prompt = f"Learning resources for {skill} with {learning_style} learning style."
            response = model.generate_content(prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
        else:
            response_text = "Please configure your Gemini API key for AI responses."
    except Exception as e:
        response_text = f"Error: {str(e)}"
    
    return {"response": response_text, "history": [[f"Learning Resources: {skill} ({learning_style})", response_text]], "updated_history": True}

def handle_forgot_password(data):
    email = data.get('email', '')
    
    if not email:
        return {"error": "Please enter your email"}
    
    return {"message": "Password reset instructions sent to your email!"}