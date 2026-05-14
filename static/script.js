let sessionId = 'guest';
let currentUser = null;

// Modal Management
function openModal(type) {
    if (type === 'login') {
        document.getElementById('login-modal').style.display = 'block';
    } else if (type === 'signup') {
        document.getElementById('signup-modal').style.display = 'block';
    } else if (type === 'forgot') {
        document.getElementById('forgot-modal').style.display = 'block';
    }
}

async function forgotPassword() {
    const email = document.getElementById('forgot-email').value;
    
    if (!validateEmail(email)) {
        showMessage('forgot-message', 'Please enter a valid email address', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/forgot-password', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('forgot-message', data.message, 'success');
            setTimeout(() => {
                closeModal('forgot-modal');
            }, 2000);
        } else {
            showMessage('forgot-message', data.detail, 'error');
        }
    } catch (error) {
        showMessage('forgot-message', 'Network error occurred', 'error');
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function openService(serviceType) {
    const modal = document.getElementById('service-modal');
    const title = document.getElementById('service-title');
    
    // Hide all service contents
    document.querySelectorAll('.service-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Show selected service
    document.getElementById(serviceType + '-service').classList.add('active');
    
    // Set title
    const titles = {
        'chat': 'AI Chat Assistant',
        'assessment': 'Career Assessment',
        'skills': 'Skills Analysis',
        'resume': 'Resume Enhancement',
        'market': 'Market Insights',
        'learning': 'Learning Resources'
    };
    
    title.textContent = titles[serviceType];
    modal.style.display = 'block';
}

// Smooth scrolling
function scrollToServices() {
    document.getElementById('services').scrollIntoView({ behavior: 'smooth' });
}

// Form Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    const minLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    const score = [minLength, hasUpper, hasLower, hasNumber, hasSpecial].filter(Boolean).length;
    return { score, minLength, hasUpper, hasLower, hasNumber, hasSpecial };
}

function updatePasswordStrength() {
    const password = document.getElementById('signup-password').value;
    const strengthEl = document.getElementById('password-strength');
    
    if (!password) {
        strengthEl.className = 'password-strength';
        return;
    }
    
    const validation = validatePassword(password);
    
    if (validation.score < 3) {
        strengthEl.className = 'password-strength weak';
    } else if (validation.score < 5) {
        strengthEl.className = 'password-strength medium';
    } else {
        strengthEl.className = 'password-strength strong';
    }
}

function validateName(name) {
    return name.length >= 2 && /^[a-zA-Z\s]+$/.test(name);
}

// Authentication
async function signup() {
    const fullName = document.getElementById('signup-fullname').value;
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm').value;
    
    // Validation
    if (!validateName(fullName)) {
        showMessage('signup-message', 'Please enter a valid full name (letters only, min 2 chars)', 'error');
        return;
    }
    
    if (username.length < 3) {
        showMessage('signup-message', 'Username must be at least 3 characters long', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showMessage('signup-message', 'Please enter a valid email address', 'error');
        return;
    }
    
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.minLength) {
        showMessage('signup-message', 'Password must be at least 8 characters long', 'error');
        return;
    }
    
    if (passwordValidation.score < 3) {
        showMessage('signup-message', 'Password is too weak. Include uppercase, lowercase, numbers, and special characters', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showMessage('signup-message', 'Passwords do not match', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/signup', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username, email, password, confirm_password: confirmPassword, full_name: fullName
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('signup-message', data.message, 'success');
            setTimeout(() => {
                closeModal('signup-modal');
                openModal('login');
            }, 1500);
        } else {
            showMessage('signup-message', data.detail, 'error');
        }
    } catch (error) {
        showMessage('signup-message', 'Network error occurred', 'error');
    }
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        const data = await response.json();
        
        if (response.ok) {
            sessionId = data.session_id;
            currentUser = username;
            showMessage('login-message', data.message, 'success');
            
            // Update UI
            document.querySelector('.auth-buttons .btn-login').style.display = 'none';
            document.querySelector('.auth-buttons .btn-signup').style.display = 'none';
            document.getElementById('user-info').style.display = 'flex';
            document.getElementById('username-display').textContent = username;
            
            setTimeout(() => closeModal('login-modal'), 1500);
        } else {
            showMessage('login-message', data.detail, 'error');
        }
    } catch (error) {
        showMessage('login-message', 'Network error occurred', 'error');
    }
}

function logout() {
    sessionId = 'guest';
    currentUser = null;
    
    // Update UI
    document.querySelector('.auth-buttons .btn-login').style.display = 'inline-block';
    document.querySelector('.auth-buttons .btn-signup').style.display = 'inline-block';
    document.getElementById('user-info').style.display = 'none';
    
    // Clear chat
    document.getElementById('chatbot').innerHTML = '';
    
    alert('Logged out successfully');
}

// Chat functionality
async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessageToChat(message, 'user');
    input.value = '';
    showLoading(true);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId
            },
            body: JSON.stringify({message})
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addMessageToChat(data.response, 'bot');
        } else {
            addMessageToChat(data.detail, 'bot');
        }
    } catch (error) {
        addMessageToChat('Network error occurred', 'bot');
    }
    
    showLoading(false);
}

function addMessageToChat(message, sender) {
    const chatbot = document.getElementById('chatbot');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message`;
    messageDiv.textContent = message;
    chatbot.appendChild(messageDiv);
    chatbot.scrollTop = chatbot.scrollHeight;
}

async function clearChat() {
    try {
        const response = await fetch('/api/clear-chat', {
            headers: {'session-id': sessionId}
        });
        
        if (response.ok) {
            document.getElementById('chatbot').innerHTML = '';
            showMessage('save-message', 'Chat cleared!', 'success');
        }
    } catch (error) {
        showMessage('save-message', 'Error clearing chat', 'error');
    }
}

async function saveChat() {
    if (!currentUser) {
        showMessage('save-message', 'Please login to save chats', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/save-chat', {
            method: 'POST',
            headers: {
                'session-id': sessionId,
                'username': currentUser
            }
        });
        
        const data = await response.json();
        showMessage('save-message', data.message, response.ok ? 'success' : 'error');
    } catch (error) {
        showMessage('save-message', 'Error saving chat', 'error');
    }
}

// Assessment
async function assessCareer() {
    const q1 = getRadioValue('q1');
    const q2 = getRadioValue('q2');
    const q3 = getRadioValue('q3');
    const q4 = getRadioValue('q4');
    const q5 = getRadioValue('q5');
    
    if (!q1 || !q2 || !q3 || !q4 || !q5) {
        alert('Please answer all questions');
        return;
    }
    
    showLoadingButton('assessment');
    
    try {
        const response = await fetch('/api/assess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId
            },
            body: JSON.stringify({q1, q2, q3, q4, q5})
        });
        
        const data = await response.json();
        document.getElementById('assessment-result').value = data.response;
        
        if (data.updated_history) {
            updateChatHistory(data.history);
        }
    } catch (error) {
        document.getElementById('assessment-result').value = 'Error occurred';
    }
    
    hideLoadingButton('assessment');
}

// Skills Analysis
async function analyzeSkills() {
    const currentSkills = document.getElementById('current-skills').value;
    const targetRole = document.getElementById('target-role').value;
    
    if (!currentSkills || !targetRole) {
        alert('Please fill both fields');
        return;
    }
    
    showLoadingButton('skills');
    
    try {
        const response = await fetch('/api/skills', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId
            },
            body: JSON.stringify({current_skills: currentSkills, target_role: targetRole})
        });
        
        const data = await response.json();
        document.getElementById('skills-result').value = data.response;
        
        if (data.updated_history) {
            updateChatHistory(data.history);
        }
    } catch (error) {
        document.getElementById('skills-result').value = 'Error occurred';
    }
    
    hideLoadingButton('skills');
}

// Resume Tips
async function getResumeTips() {
    const jobRole = document.getElementById('job-role').value;
    const experienceLevel = getRadioValue('experience');
    
    if (!jobRole || !experienceLevel) {
        alert('Please fill both fields');
        return;
    }
    
    showLoadingButton('resume');
    
    try {
        const response = await fetch('/api/resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId
            },
            body: JSON.stringify({job_role: jobRole, experience_level: experienceLevel})
        });
        
        const data = await response.json();
        document.getElementById('resume-result').value = data.response;
        
        if (data.updated_history) {
            updateChatHistory(data.history);
        }
    } catch (error) {
        document.getElementById('resume-result').value = 'Error occurred';
    }
    
    hideLoadingButton('resume');
}

// Market Insights
async function getMarketInsights() {
    const field = document.getElementById('field').value;
    const location = document.getElementById('location').value;
    
    if (!field || !location) {
        alert('Please fill both fields');
        return;
    }
    
    showLoadingButton('market');
    
    try {
        const response = await fetch('/api/market', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId
            },
            body: JSON.stringify({field, location})
        });
        
        const data = await response.json();
        document.getElementById('market-result').value = data.response;
        
        if (data.updated_history) {
            updateChatHistory(data.history);
        }
    } catch (error) {
        document.getElementById('market-result').value = 'Error occurred';
    }
    
    hideLoadingButton('market');
}

// Learning Resources
async function getLearningResources() {
    const skill = document.getElementById('skill-to-learn').value;
    const learningStyle = getRadioValue('learning-style');
    
    if (!skill || !learningStyle) {
        alert('Please fill both fields');
        return;
    }
    
    showLoadingButton('learning');
    
    try {
        const response = await fetch('/api/learning', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId
            },
            body: JSON.stringify({skill, learning_style: learningStyle})
        });
        
        const data = await response.json();
        document.getElementById('learning-result').value = data.response;
        
        if (data.updated_history) {
            updateChatHistory(data.history);
        }
    } catch (error) {
        document.getElementById('learning-result').value = 'Error occurred';
    }
    
    hideLoadingButton('learning');
}

// Utility functions
function getRadioValue(name) {
    const radio = document.querySelector(`input[name="${name}"]:checked`);
    return radio ? radio.value : null;
}

function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `message ${type === 'success' ? 'success' : 'error'}`;
    setTimeout(() => {
        element.textContent = '';
        element.className = 'message';
    }, 5000);
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

function showLoadingButton(service) {
    const button = document.querySelector(`#${service}-service .submit-btn`);
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    button.disabled = true;
}

function hideLoadingButton(service) {
    const button = document.querySelector(`#${service}-service .submit-btn`);
    const icons = {
        'assessment': 'fas fa-search',
        'skills': 'fas fa-chart-line',
        'resume': 'fas fa-magic',
        'market': 'fas fa-chart-pie',
        'learning': 'fas fa-book'
    };
    const texts = {
        'assessment': 'Get Career Recommendations',
        'skills': 'Analyze Skills Gap',
        'resume': 'Get Resume Tips',
        'market': 'Get Market Insights',
        'learning': 'Find Resources'
    };
    button.innerHTML = `<i class="${icons[service]}"></i> ${texts[service]}`;
    button.disabled = false;
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function updateChatHistory(history) {
    const chatbot = document.getElementById('chatbot');
    chatbot.innerHTML = '';
    history.forEach(([user, bot]) => {
        addMessageToChat(user, 'user');
        addMessageToChat(bot, 'bot');
    });
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Smooth scrolling for navigation
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
    
    // Password strength indicator
    const passwordInput = document.getElementById('signup-password');
    if (passwordInput) {
        passwordInput.addEventListener('input', updatePasswordStrength);
    }
});