# 🎯 TalentScout AI Hiring Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent, AI-powered chatbot for automated candidate screening and technical assessment**

[Demo Video](#demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Prompt Engineering](#prompt-engineering)
- [Architecture](#architecture)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

TalentScout AI Hiring Assistant is a sophisticated chatbot designed to revolutionize the initial candidate screening process for technology recruitment. Powered by advanced Large Language Models (LLaMA 3.3 70B via Groq), it conducts intelligent conversations with candidates, gathering essential information and administering customized technical assessments based on their declared tech stack.

### Why This Project?

- **Efficiency**: Automates the time-consuming initial screening process
- **Consistency**: Ensures every candidate gets a standardized, fair assessment
- **Intelligence**: Adapts technical questions based on candidate's experience and skills
- **Scale**: Can handle multiple candidates simultaneously without quality degradation

---

## ✨ Key Features

### 🎨 Modern, Eye-Catching UI
- **Glassmorphic Design**: Beautiful gradient backgrounds with frosted-glass effect components
- **Smooth Animations**: Slide-in animations for messages and interactive elements
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Stats**: Live dashboard showing conversation progress and collected data

### 🤖 Intelligent Conversation Flow
- **Context-Aware**: Maintains conversation context throughout the session
- **Natural Language**: Human-like interactions that feel genuine and engaging
- **Smart Navigation**: Guides candidates through screening stages naturally
- **Fallback Handling**: Gracefully manages unexpected inputs and keeps conversation on track

### 📊 Comprehensive Data Collection
Automatically gathers:
- Full Name
- Email Address (with validation)
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Technical Skills & Tech Stack

### 🎯 Dynamic Technical Assessment
- **Adaptive Questions**: Generates 3-5 technical questions tailored to declared tech stack
- **Difficulty Scaling**: Adjusts question complexity based on years of experience
- **Diverse Coverage**: Tests conceptual understanding and practical application
- **Real-world Focus**: Questions that assess actual job-relevant skills

### 🔒 Security & Privacy
- **Data Encryption**: All sensitive information handled securely
- **GDPR Compliant**: Follows data privacy best practices
- **Local Storage**: Candidate data stored locally in JSON format
- **No Sensitive Data**: Never requests SSN, passwords, or financial information

### 🚪 Conversation Control
- **Natural Exit**: Recognizes keywords like "bye", "exit", "quit"
- **Graceful Closing**: Thanks candidates and explains next steps
- **Session Management**: Easy reset and new session initialization
- **Data Export**: Save conversation and candidate data as JSON

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit**: Interactive web application framework
- **Custom CSS**: Advanced styling with animations and gradients
- **Responsive Design**: Mobile-first approach

### Backend
- **Python 3.8+**: Core programming language
- **Groq API**: Lightning-fast LLM inference
- **LLaMA 3.3 70B**: State-of-the-art language model

### Data Management
- **JSON**: Structured data storage
- **Session State**: In-memory conversation management

### Development Tools
- **Git**: Version control
- **Python-dotenv**: Environment variable management

---

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/talentscout-ai-assistant.git
cd talentscout-ai-assistant
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.streamlit/secrets.toml` file in the project directory:

```bash
mkdir .streamlit
```

Add your Groq API key to `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

**Alternative**: Set as environment variable:

**Windows:**
```bash
set GROQ_API_KEY=your_groq_api_key_here
```

**macOS/Linux:**
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

---

## ⚙️ Configuration

### Getting Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into `.streamlit/secrets.toml`

### Customization Options

You can customize the chatbot by modifying `app.py`:

- **Color Scheme**: Edit the CSS gradient colors (lines 20-30)
- **LLM Model**: Change model in `get_ai_response()` function
- **System Prompt**: Modify `SYSTEM_PROMPT` to adjust chatbot behavior
- **Conversation Stages**: Add/remove stages in session state initialization

---

## 🚀 Usage

### Running Locally

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Chatbot

1. **Start Conversation**: The chatbot greets you automatically
2. **Provide Information**: Answer questions about your background and experience
3. **Declare Tech Stack**: Specify your programming languages, frameworks, and tools
4. **Technical Assessment**: Answer 3-5 tailored technical questions
5. **Complete Session**: Review next steps and exit gracefully

### Keyboard Shortcuts

- Type "bye", "goodbye", "exit", or "quit" to end conversation anytime
- Click "Start New Session" to reset and begin fresh
- Click "Export Data" to save candidate information

---

## 📁 Project Structure

```
talentscout-ai-assistant/
│
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore rules
│
├── .streamlit/
│   └── secrets.toml               # API keys (not committed)
│
├── candidate_data_*.json          # Saved candidate data (generated)
│
└── assets/                        # (Optional) Screenshots and demo videos
    ├── screenshot1.png
    ├── screenshot2.png
    └── demo_video.mp4
```

---

## 🧠 Prompt Engineering

### Prompt Design Philosophy

The chatbot's intelligence stems from carefully crafted prompts that guide the LLM through structured conversation stages while maintaining natural, human-like interactions.

### System Prompt Components

1. **Role Definition**: Establishes chatbot's identity and purpose
2. **Conversation Stages**: Clear progression from greeting to closing
3. **Rules & Constraints**: Boundaries to keep conversation focused
4. **Context Injection**: Dynamic data about current stage and collected information
5. **Quality Guidelines**: Standards for question generation and interaction

### Key Prompt Engineering Techniques

#### 1. **Stage-Based Prompting**
```python
SYSTEM_PROMPT = """You are an AI Hiring Assistant for TalentScout.

CONVERSATION STAGES:
1. GREETING: Welcome candidates warmly
2. INFO_GATHERING: Collect essential details
3. TECH_STACK: Ask about technical skills
4. TECHNICAL_QUESTIONS: Generate relevant questions
5. CLOSING: Thank and explain next steps

Current stage: {stage}
"""
```

**Why it works**: Gives the model clear context about where it is in the conversation, preventing confusion and maintaining logical flow.

#### 2. **Context Injection**
```python
system_prompt = SYSTEM_PROMPT.format(
    stage=st.session_state.conversation_stage,
    data=json.dumps(st.session_state.candidate_data, indent=2)
)
```

**Why it works**: Provides the model with accumulated candidate information, enabling contextual responses and preventing repetitive questions.

#### 3. **Constraint-Based Guidance**
```
IMPORTANT RULES:
- Stay focused on recruitment screening only
- Ask one question at a time
- Validate information formats
- Generate challenging but fair questions
```

**Why it works**: Sets clear boundaries that prevent the model from going off-topic or behaving inappropriately.

#### 4. **Few-Shot Learning Patterns**
```
When generating technical questions:
- Make them specific to mentioned technologies
- Include mix of conceptual and practical questions
- Ensure questions test real-world application
- Adapt difficulty based on experience
```

**Why it works**: Provides concrete examples of desired behavior without explicit few-shot examples, leveraging the model's pre-trained knowledge.

#### 5. **Fallback Mechanisms**
```python
def detect_conversation_end(message):
    end_keywords = ['bye', 'goodbye', 'exit', 'quit']
    return any(keyword in message.lower() for keyword in end_keywords)
```

**Why it works**: Programmatic fallbacks handle edge cases that prompts alone can't reliably manage.

### Handling Diverse Tech Stacks

The prompt is designed to handle various technologies:

- **Programming Languages**: Python, JavaScript, Java, C++, etc.
- **Frameworks**: React, Django, Spring Boot, etc.
- **Databases**: PostgreSQL, MongoDB, Redis, etc.
- **Tools**: Docker, Kubernetes, Git, etc.

**Technique**: Open-ended prompt structure allows model to generate relevant questions for any technology without hardcoded rules.

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Streamlit UI  │ ← User Interface Layer
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Session State  │ ← State Management
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Groq API      │ ← LLM Inference
│  (LLaMA 3.3)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  JSON Storage   │ ← Data Persistence
└─────────────────┘
```

### Component Breakdown

#### 1. **UI Layer (Streamlit)**
- Renders chat interface
- Handles user input
- Displays messages with animations
- Shows real-time stats and candidate data

#### 2. **State Management**
```python
st.session_state.messages          # Chat history
st.session_state.candidate_data    # Collected information
st.session_state.conversation_stage # Current stage
```

**Purpose**: Maintains conversation context across reruns and user interactions.

#### 3. **LLM Integration (Groq)**
```python
def get_ai_response(user_message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
    )
    return response.choices[0].message.content
```

**Purpose**: Generates intelligent, context-aware responses using state-of-the-art language model.

#### 4. **Data Persistence**
```python
def save_candidate_data():
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
```

**Purpose**: Stores candidate information and conversation history for future reference.

### Design Decisions

#### Why Groq + LLaMA 3.3?
- **Speed**: Sub-second response times with Groq's LPU architecture
- **Quality**: LLaMA 3.3 70B provides excellent conversational ability
- **Cost**: Free tier sufficient for development and demos

#### Why Streamlit?
- **Rapid Development**: Build interactive UIs with pure Python
- **Built-in Components**: Chat interface, state management, layouts
- **Easy Deployment**: Multiple hosting options (Streamlit Cloud, Heroku, AWS)

#### Why Session State?
- **Simplicity**: No need for external database for demo
- **Performance**: In-memory operations are lightning-fast
- **Privacy**: Data doesn't leave the user's session

---

## 🎢 Challenges & Solutions

### Challenge 1: Maintaining Conversation Context

**Problem**: LLMs are stateless and don't remember previous messages without explicit context.

**Solution**: 
- Store entire conversation history in `st.session_state.messages`
- Include all messages in each API call
- Inject current conversation stage and collected data into system prompt

```python
messages = [{"role": "system", "content": system_prompt}]
messages.extend(st.session_state.messages)  # Full history
messages.append({"role": "user", "content": user_message})
```

### Challenge 2: Preventing Off-Topic Conversations

**Problem**: LLMs can easily go off-topic if not properly constrained.

**Solution**:
- Clear role definition in system prompt
- Explicit rules about staying focused on recruitment
- Programmatic detection of conversation-ending keywords
- Fallback messages to redirect users back on track

### Challenge 3: Generating Relevant Technical Questions

**Problem**: Generic questions don't effectively assess candidate skills.

**Solution**:
- Dynamic prompt engineering based on declared tech stack
- Experience-level adaptation instructions
- Mix of conceptual and practical question types
- Real-world application focus

### Challenge 4: UI Performance with Long Conversations

**Problem**: Streamlit reruns entire script on each interaction, which can slow down with many messages.

**Solution**:
- Efficient session state management
- Conditional rendering
- Groq's fast inference (< 1 second response time)
- Minimal DOM manipulation

### Challenge 5: Data Privacy & Security

**Problem**: Handling sensitive candidate information securely.

**Solution**:
- Local JSON storage (no external database)
- No collection of sensitive data (SSN, passwords)
- Clear data handling disclosure
- GDPR-compliant practices
- User control over data export

### Challenge 6: API Key Management

**Problem**: Securely storing API keys without exposing them in code.

**Solution**:
- Use Streamlit secrets management
- Environment variable support
- `.gitignore` for sensitive files
- Clear setup instructions in README

---

## 🚀 Future Enhancements

### Planned Features

#### 1. **Advanced Analytics Dashboard**
- Candidate pipeline visualization
- Skill distribution charts
- Response time analytics
- Success rate tracking

#### 2. **Multilingual Support**
- Automatic language detection
- Support for 10+ languages
- Culturally appropriate interactions

#### 3. **Sentiment Analysis**
- Real-time emotion detection
- Engagement scoring
- Candidate confidence assessment

#### 4. **Resume Parsing Integration**
- Upload PDF/DOCX resumes
- Auto-extract information
- Pre-fill candidate data

#### 5. **Video Interview Scheduling**
- Calendar integration
- Automated email notifications
- Time zone handling

#### 6. **Advanced Question Bank**
- Industry-specific questions
- Difficulty progression
- Coding challenge integration

#### 7. **HR Dashboard**
- Candidate comparison view
- Bulk data export
- Interview notes and ratings

#### 8. **Cloud Deployment**
- AWS Lambda deployment guide
- Docker containerization
- Kubernetes orchestration

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Update README with new features
- Test thoroughly before submitting

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Groq** for providing lightning-fast LLM inference
- **Meta AI** for the LLaMA 3.3 model
- **Streamlit** for the amazing framework
- **TalentScout** (fictional) for the assignment inspiration

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/talentscout-ai-assistant/issues) page
2. Create a new issue with detailed description
3. Contact via email

---

<div align="center">

**Made with ❤️ and ☕ for TalentScout**

⭐ Star this repo if you find it helpful!

</div>