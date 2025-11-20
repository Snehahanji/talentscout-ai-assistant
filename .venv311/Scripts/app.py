import streamlit as st
import os
from datetime import datetime
import json
import re
from groq import Groq
import time

# Page configuration
st.set_page_config(
    page_title="TalentScout AI Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with more animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 2rem auto;
        max-width: 900px;
    }
    
    .stChatMessage {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        animation: slideIn 0.3s ease-out;
        transition: transform 0.2s;
    }
    
    .stChatMessage:hover {
        transform: translateX(5px);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.9);
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        animation: pulse 1s infinite;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
    }
    
    .progress-bar {
        height: 8px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.5s ease;
    }
    
    .typing-indicator {
        display: inline-block;
        animation: blink 1.4s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 1; }
    }
    
    .success-badge {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .warning-badge {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'candidate_data' not in st.session_state:
    st.session_state.candidate_data = {}
if 'conversation_stage' not in st.session_state:
    st.session_state.conversation_stage = 'greeting'
if 'tech_stack' not in st.session_state:
    st.session_state.tech_stack = []
if 'questions_asked' not in st.session_state:
    st.session_state.questions_asked = 0
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = []
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

# Enhanced system prompt
SYSTEM_PROMPT = """You are an intelligent and friendly AI Hiring Assistant for TalentScout, a leading technology recruitment agency. Your role is to conduct initial candidate screening with professionalism, warmth, and efficiency.

CONVERSATION STAGES:
1. GREETING: Welcome candidates warmly, explain your purpose, and build rapport
2. INFO_GATHERING: Collect essential details one at a time for natural flow:
   - Full Name
   - Email Address (validate format)
   - Phone Number
   - Years of Experience (must be a number)
   - Desired Position(s)
   - Current Location
3. TECH_STACK: Ask about their technical skills, programming languages, frameworks, databases, and tools
4. TECHNICAL_QUESTIONS: Generate 3-5 relevant, challenging technical questions based on their tech stack and experience level
5. CLOSING: Thank them, explain next steps, and wish them well

CRITICAL RULES:
✅ Stay focused on recruitment screening - politely redirect off-topic conversations
✅ Be conversational and warm - you're representing TalentScout's brand
✅ Ask ONE question at a time for better user experience
✅ Validate information formats (email must have @, phone must be numeric, experience must be a number)
✅ Generate technical questions that are:
   - Specific to mentioned technologies
   - Mix of conceptual understanding and practical application
   - Appropriately challenging based on years of experience
   - Focused on real-world scenarios, not trivia
✅ If user says "bye", "goodbye", "exit", "quit", or "no thanks", gracefully end the conversation
✅ NEVER ask for sensitive data like SSN, passwords, or financial information
✅ If you notice missing or invalid information, politely ask for correction

ADAPTIVE QUESTIONING:
- Junior (0-2 years): Focus on fundamentals and basic concepts
- Mid-level (3-5 years): Include architecture decisions and best practices
- Senior (6+ years): Advanced patterns, system design, leadership scenarios

PERSONALITY:
- Professional yet approachable
- Patient and encouraging
- Clear and concise
- Enthusiastic about technology
- Respectful of candidate's time

Current conversation stage: {stage}
Candidate data collected: {data}
Tech stack mentioned: {tech_stack}"""

def initialize_groq_client():
    """Initialize Groq client with API key"""
    api_key = os.getenv('GROQ_API_KEY') or st.secrets.get('GROQ_API_KEY', '')
    if not api_key:
        st.error("⚠️ GROQ_API_KEY not found! Please set it in .streamlit/secrets.toml or environment variables.")
        st.stop()
    return Groq(api_key=api_key)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number"""
    pattern = r'^\+?[\d\s\-\(\)]{10,}$'
    return re.match(pattern, phone) is not None

def extract_candidate_info(messages):
    """Extract candidate information from conversation using AI"""
    # Simple extraction - in production, you'd use NER or more sophisticated parsing
    data = {}
    for msg in messages:
        content = msg.get('content', '').lower()
        # This is simplified - the AI handles actual extraction
        if '@' in content and 'email' not in data:
            words = content.split()
            for word in words:
                if '@' in word and validate_email(word):
                    data['email'] = word
                    break
    return data

def get_ai_response(user_message):
    """Get response from Groq AI with enhanced context"""
    try:
        client = initialize_groq_client()
        
        # Prepare system prompt with current context
        system_prompt = SYSTEM_PROMPT.format(
            stage=st.session_state.conversation_stage,
            data=json.dumps(st.session_state.candidate_data, indent=2),
            tech_stack=", ".join(st.session_state.tech_stack) if st.session_state.tech_stack else "None yet"
        )
        
        # Prepare messages for API
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(st.session_state.messages)
        messages.append({"role": "user", "content": user_message})
        
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"I apologize, but I'm having trouble processing your message. Please try again. Error: {str(e)}"

def detect_conversation_end(message):
    """Detect if user wants to end conversation"""
    end_keywords = ['bye', 'goodbye', 'exit', 'quit', 'no thanks', 'not interested']
    return any(keyword in message.lower() for keyword in end_keywords)

def save_candidate_data():
    """Save candidate data to JSON file with enhanced metadata"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"candidate_data_{timestamp}.json"
        
        session_duration = (datetime.now() - st.session_state.session_start).total_seconds()
        
        with open(filename, 'w') as f:
            json.dump({
                'candidate_data': st.session_state.candidate_data,
                'tech_stack': st.session_state.tech_stack,
                'conversation': st.session_state.messages,
                'metadata': {
                    'timestamp': timestamp,
                    'session_duration_seconds': session_duration,
                    'total_messages': len(st.session_state.messages),
                    'conversation_stage': st.session_state.conversation_stage
                }
            }, f, indent=2)
        
        return filename
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return None

def calculate_progress():
    """Calculate conversation progress percentage"""
    stages = ['greeting', 'info_gathering', 'tech_stack', 'technical_questions', 'closing']
    current_index = stages.index(st.session_state.conversation_stage) if st.session_state.conversation_stage in stages else 0
    return int((current_index / len(stages)) * 100)

# Header
st.markdown("<h1>🎯 TalentScout AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Intelligent Recruitment Companion - Enhanced Edition</p>", unsafe_allow_html=True)

# Progress bar
progress = calculate_progress()
st.markdown(f"""
<div class='progress-bar'>
    <div class='progress-fill' style='width: {progress}%'></div>
</div>
<p style='text-align: center; color: white; font-size: 0.9rem;'>Progress: {progress}% Complete</p>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Session Dashboard")
    
    # Session timer
    elapsed = (datetime.now() - st.session_state.session_start).total_seconds()
    minutes, seconds = divmod(int(elapsed), 60)
    st.markdown(f"<div class='stat-card'><h4>⏱️ {minutes}m {seconds}s</h4><p>Session Time</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='stat-card'><h3>{len(st.session_state.messages)//2}</h3><p>Messages</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><h3>{len(st.session_state.candidate_data)}</h3><p>Data Points</p></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Candidate Profile")
    
    if st.session_state.candidate_data:
        for key, value in st.session_state.candidate_data.items():
            # Validate and show status
            is_valid = True
            if key == 'email':
                is_valid = validate_email(value)
            elif key == 'phone':
                is_valid = validate_phone(value)
            
            status = "✅" if is_valid else "⚠️"
            st.markdown(f"{status} **{key.replace('_', ' ').title()}:** {value}")
        
        if st.session_state.tech_stack:
            st.markdown("**Tech Stack:**")
            for tech in st.session_state.tech_stack:
                st.markdown(f"<span class='success-badge'>{tech}</span>", unsafe_allow_html=True)
    else:
        st.info("No data collected yet - Let's get started! 🚀")
    
    st.markdown("---")
    st.markdown("### 🎯 Stage")
    st.markdown(f"<span class='warning-badge'>{st.session_state.conversation_stage.replace('_', ' ').title()}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.messages = []
            st.session_state.candidate_data = {}
            st.session_state.conversation_stage = 'greeting'
            st.session_state.tech_stack = []
            st.session_state.session_start = datetime.now()
            st.rerun()
    
    with col2:
        if st.button("💾 Export", use_container_width=True) and st.session_state.candidate_data:
            filename = save_candidate_data()
            if filename:
                st.success(f"Saved!")
                # Offer download
                with open(filename, 'r') as f:
                    st.download_button(
                        label="⬇️ Download",
                        data=f.read(),
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True
                    )

# Main chat interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display initial greeting if no messages
if len(st.session_state.messages) == 0:
    initial_greeting = """👋 **Welcome to TalentScout!**

I'm your AI Hiring Assistant, and I'm excited to learn more about you and your technical expertise!

**What we'll cover today:**
1. 📝 Basic information about you
2. 💼 Your professional background
3. 💻 Your technical skills and preferred technologies
4. 🎯 A few technical questions to showcase your expertise

**This process typically takes 5-10 minutes.**

Don't worry - you can type "bye" or "exit" at any time if you need to leave. Your progress will be saved!

Let's get started! What's your full name? 😊"""
    
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Check for conversation end
    if detect_conversation_end(prompt):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        farewell_message = """Thank you so much for your time today! 🙏

**Here's what happens next:**
✅ Our recruitment team will review your profile within 24-48 hours
✅ If you're a strong match, we'll reach out via email for next steps
✅ Technical interviews are typically scheduled within 3-5 business days
✅ We'll keep you updated throughout the entire process

Your information has been securely saved, and we're excited about the possibility of working together!

**Tips while you wait:**
- Keep your phone handy - we might call!
- Check your email (including spam folder)
- Feel free to explore our website for more opportunities

Best of luck with your job search! 🌟

*You can start a new session anytime by clicking the "Reset" button.*"""
        
        st.session_state.messages.append({"role": "assistant", "content": farewell_message})
        st.session_state.conversation_stage = 'closing'
        
        # Save data
        save_candidate_data()
        st.rerun()
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response with typing indicator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Update stage intelligently based on conversation
    if len(st.session_state.messages) > 4 and st.session_state.conversation_stage == 'greeting':
        st.session_state.conversation_stage = 'info_gathering'
    elif len(st.session_state.candidate_data) >= 5 and st.session_state.conversation_stage == 'info_gathering':
        st.session_state.conversation_stage = 'tech_stack'
    
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Footer with enhanced info
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<p style='text-align: center; color: white;'>🔒 Secure & Private</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='text-align: center; color: white;'>⚡ Powered by Groq LLaMA 3.3</p>", unsafe_allow_html=True)
with col3:
    st.markdown("<p style='text-align: center; color: white;'>🎨 Built with Streamlit</p>", unsafe_allow_html=True)