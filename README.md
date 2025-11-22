# CareerAI - AI-Powered Career Assistant

A modern, responsive web application that provides AI-powered career guidance and professional development tools.

## 🚀 Features

### 🤖 AI-Powered Services
- **AI Chat Assistant** - Get instant career advice and guidance
- **Career Assessment** - Discover your ideal career path with comprehensive questionnaire
- **Skills Analysis** - Identify skill gaps and get personalized learning recommendations
- **Resume Enhancement** - Get expert tips to improve your resume
- **Market Insights** - Stay updated with job market trends and salary information
- **Learning Resources** - Find personalized learning materials based on your style

### 🔐 User Management
- **User Authentication** - Secure signup/login system
- **Password Validation** - Strong password requirements with real-time strength indicator
- **Forgot Password** - Password reset functionality
- **Chat History** - Save and manage your conversation history

### 📱 Modern UI/UX
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Professional Interface** - Clean, modern design inspired by top job portals
- **Interactive Animations** - Smooth transitions and hover effects
- **Modal-based Services** - Organized service access through beautiful modals

### 📄 Additional Pages
- **Contact Us** - Professional contact form with validation
- **Terms & Conditions** - Comprehensive legal documentation
- **About Section** - Company information and feature highlights

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI**: Google Gemini API
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome
- **Responsive**: Mobile-first design approach

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ShivamKawatra/Career_assistant.git
cd Career_assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

4. **Run the application**
```bash
python main.py
```

5. **Open your browser**
Navigate to `http://localhost:8000`

## 🎯 Usage

1. **Sign Up/Login** - Create an account or login to access all features
2. **Choose a Service** - Click on any service card to open the modal
3. **Get AI Guidance** - Fill out forms or chat directly with the AI
4. **Save Your Progress** - Your chat history is automatically saved
5. **Explore Features** - Try different services to get comprehensive career guidance

## 📁 Project Structure

```
Career_assistant/
├── main.py                 # FastAPI backend server
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── README.md              # Project documentation
└── static/
    ├── index.html         # Main homepage
    ├── contact.html       # Contact us page
    ├── terms.html         # Terms & conditions page
    ├── style.css          # Main stylesheet
    └── script.js          # JavaScript functionality
```

## 🔧 API Endpoints

- `POST /api/signup` - User registration
- `POST /api/login` - User authentication
- `POST /api/forgot-password` - Password reset
- `POST /api/chat` - AI chat interaction
- `POST /api/assess` - Career assessment
- `POST /api/skills` - Skills analysis
- `POST /api/resume` - Resume tips
- `POST /api/market` - Market insights
- `POST /api/learning` - Learning resources
- `POST /api/contact` - Contact form submission
- `GET /contact` - Contact page
- `GET /terms` - Terms & conditions page

## 🎨 Design Features

- **Gradient Backgrounds** - Modern gradient hero section
- **Glassmorphism Effects** - Transparent elements with blur effects
- **Floating Animations** - Animated floating cards
- **Responsive Grid** - Adaptive layouts for all screen sizes
- **Professional Typography** - Clean, readable fonts
- **Interactive Elements** - Hover effects and smooth transitions

## 🔒 Security Features

- **Input Validation** - Comprehensive form validation
- **Password Strength** - Real-time password strength indicator
- **Email Validation** - Proper email format checking
- **Session Management** - Secure user session handling
- **Error Handling** - Graceful error management

## 🚀 Deployment

The application is ready for deployment on platforms like:
- **Heroku** - Add Procfile for easy deployment
- **Railway** - Direct deployment from GitHub
- **Vercel** - For static frontend with serverless functions
- **AWS/GCP** - For scalable cloud deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shivam Kawatra**
- GitHub: [@ShivamKawatra](https://github.com/ShivamKawatra)

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Font Awesome for icons
- FastAPI for the excellent web framework
- The open-source community for inspiration

---

⭐ **Star this repository if you found it helpful!**