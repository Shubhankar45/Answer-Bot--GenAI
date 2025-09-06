from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import time
import datetime

# Load environment variables
load_dotenv()
api_key = os.getenv("api_key")

# Configure the API
genai.configure(api_key=api_key)

# Page Configuration
st.set_page_config(
    page_title="AnswerBot - AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for completely new design with no margins and proper padding
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* New CSS Variables with modern color palette */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #06b6d4;
        --accent: #f59e0b;
        --success: #10b981;
        --error: #ef4444;
        --warning: #f97316;
        
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #334155;
        --bg-glass: rgba(51, 65, 85, 0.8);
        --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --text-accent: #e2e8f0;
        
        --border: #475569;
        --border-light: #64748b;
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);
        
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
        --gradient-secondary: linear-gradient(135deg, #f59e0b 0%, #10b981 100%);
        --gradient-accent: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        --gradient-hero: linear-gradient(135deg, #6366f1 0%, #06b6d4 0%, #f59e0b 100%);
    }
    
    /* Base styles */
    .stApp {
        background: var(--bg-gradient);
        color: var(--text-primary);
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    /* Main container with new design */
    .main-container {
        background: transparent;
        padding: 0;
        margin: 0;
        width: 100%;
        max-width: none;
        position: relative;
        overflow: hidden;
    }
    
    /* Hero section with new design */
    .hero-section {
        text-align: center;
        padding: 2rem 1rem 2rem;
        position: relative;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
        margin: 0;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        background: var(--gradient-hero);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.025em;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        position: relative;
    }
    
    .hero-title::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: var(--gradient-primary);
        border-radius: 2px;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin: 0.5rem auto 0.5rem auto;
        max-width: 500px;
        line-height: 1.5;
        opacity: 0.9;
    }
    
    .hero-badge {
        display: inline-block;
        background: var(--gradient-primary);
        color: white;
        padding: 0.25rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: var(--shadow-md);
        margin: 0;
    }
    
    /* Stats grid with new card design */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 0;
        padding: 2rem 1rem;
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stat-card {
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-xl);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-icon {
        font-size: 2.25rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .stat-number {
        font-size: 2.75rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stat-label {
        font-size: 0.9375rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.8;
    }
    
    /* Chat section with new design */
    .chat-section {
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        margin: 0;
        position: relative;
        text-align: center;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: var(--shadow-lg);
    }
    
    .chat-header {
        text-align: center;
        margin: 0;
        padding: 0;
    }
    
    .chat-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
        background: var(--gradient-secondary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chat-subtitle {
        color: var(--text-secondary);
        font-size: 1.0625rem;
        opacity: 0.8;
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* Input styling with new design */
    .stTextArea > div {
        text-align: center;
        max-width: 700px;
        margin: 0 auto;
        padding: 1rem 0;
    }
    
    .stTextArea > div > div > textarea {
        background: var(--bg-secondary) !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.25rem 1.5rem !important;
        font-size: 1.0625rem !important;
        color: var(--text-primary) !important;
        font-weight: 400 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Poppins', sans-serif !important;
        resize: vertical !important;
        min-height: 100px !important;
        box-shadow: var(--shadow-md) !important;
        text-align: left !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1), var(--shadow-lg) !important;
        background: var(--bg-primary) !important;
        transform: scale(1.01) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted) !important;
        text-align: center !important;
    }
    
    /* Button styling with new design */
    .stButton {
        text-align: center;
        max-width: 700px;
        margin: 0 auto;
        padding: 0.5rem 0;
    }
    
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.25rem 3rem !important;
        font-size: 1.1875rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        max-width: 500px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 0 !important;
        font-family: 'Poppins', sans-serif !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        display: block !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-xl) !important;
        background: var(--gradient-accent) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Response container with new design */
    .response-container {
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0;
        position: relative;
        box-shadow: var(--shadow-lg);
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        text-align: left;
    }
    
    .response-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 0 1rem 0;
        padding: 0 0 0.75rem 0;
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .response-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--primary);
        font-weight: 600;
        font-size: 1.1875rem;
    }
    
    .response-meta {
        display: flex;
        gap: 1rem;
        font-size: 0.8125rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .response-text {
        color: var(--text-primary);
        font-size: 1.0625rem;
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
        font-weight: 400;
    }
    
    /* Loading animation with new design */
    .loading-container {
        text-align: center;
        padding: 2rem 1rem;
        color: var(--text-secondary);
        margin: 0 auto;
        max-width: 500px;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 60px;
        height: 60px;
        border: 4px solid rgba(99, 102, 241, 0.2);
        border-radius: 50%;
        border-top-color: var(--primary);
        animation: spin 1s ease-in-out infinite;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-glow);
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Error styling with new design */
    .error-container {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0;
        position: relative;
        box-shadow: var(--shadow-lg);
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        text-align: left;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        
        .hero-subtitle {
            font-size: 1rem;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
            padding: 1.5rem 0.5rem;
        }
        
        .stat-number {
            font-size: 2.25rem;
        }
        
        .chat-title {
            font-size: 1.75rem;
        }
        
        .chat-section {
            padding: 1.5rem 1rem;
            margin: 0;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--gradient-secondary);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Hero section with new design - header starts from top
st.markdown("""
<div class="hero-section" style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; text-align: center; background: none; min-height: 0;">
    <h1 class="hero-title" style="margin: 0 auto;">🚀 AnswerBot</h1>
    <br>
    <p class="hero-subtitle" style="max-width: 600px; margin: 0 auto 1rem auto;">
        Your intelligent AI companion powered by cutting-edge language models.<br>
        Experience the future of AI assistance with lightning-fast responses.
    </p>
    <div class="hero-badge" style="margin-top: 0.5rem;">Powered by Gemini 2.5</div>
</div>
""", unsafe_allow_html=True)

# Stats section with new design
current_time = datetime.datetime.now().strftime("%H:%M")
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card">
        <span class="stat-icon">📊</span>
        <div class="stat-number">{st.session_state.query_count}</div>
        <div class="stat-label">Questions Asked</div>
    </div>
    <div class="stat-card">
        <span class="stat-icon">💬</span>
        <div class="stat-number">{len(st.session_state.chat_history)}</div>
        <div class="stat-label">Chat History</div>
    </div>
    <div class="stat-card">
        <span class="stat-icon">⏰</span>
        <div class="stat-number">{current_time}</div>
        <div class="stat-label">Current Time</div>
        </div>
    <div class="stat-card">
        <span class="stat-icon">⚡</span>
        <div class="stat-number">99.9%</div>
        <div class="stat-label">Uptime</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat section with new design
st.markdown("""
<div class="chat-section" style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: none; text-align: center;">
    <div class="chat-header" style="background: none; text-align: center;">
        <h2 class="chat-title" style="margin: 0 auto;">💬 Start Your Conversation</h2>
        <p class="chat-subtitle" style="margin: 0 auto;">Ask me anything and I'll provide you with a detailed, intelligent response</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Center align chat input and button, remove borders via custom CSS
st.markdown("""
<style>
.centered-input textarea {
    margin: 0 auto !important;
    display: block !important;
    border: none !important;
    box-shadow: none !important;
    background: var(--bg-card, #334155) !important;
    border-radius: 1rem !important;
    color: var(--text-primary, #fff) !important;
    font-size: 1.1rem !important;
    padding: 1.2rem !important;
    width: 100% !important;
    max-width: 600px !important;
}
.centered-btn button {
    margin: 0 auto !important;
    display: block !important;
    border: none !important;
    box-shadow: none !important;
    background: var(--primary, #6366f1) !important;
    color: #fff !important;
    border-radius: 2rem !important;
    font-size: 1.1rem !important;
    padding: 0.75rem 2.5rem !important;
    font-weight: 600 !important;
    transition: background 0.2s;
}
.centered-btn button:hover {
    background: var(--primary-dark, #4f46e5) !important;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="centered-input">', unsafe_allow_html=True)
    request = st.text_area(
        "Your question:",
        height=100,
        placeholder="Type your question here... (e.g., 'Explain quantum computing', 'Write a Python function', 'Create a marketing strategy')",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered-btn">', unsafe_allow_html=True)
    btn = st.button("🚀 Get AI Response", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Response handling
if btn and request.strip():
    start_time = time.time()
    
    # Show loading animation
    with st.empty():
        st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div style="font-size: 1.1875rem; font-weight: 500;">🤔 AI is analyzing your question...</div>
            <div style="margin-top: 0.5rem; color: var(--text-muted);">This may take a few moments</div>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            time.sleep(0.8)  # Simulate processing time
            
            # Configure model
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Generate response
            response = model.generate_content(request)
            
            # Calculate response time
            response_time = round(time.time() - start_time, 2)
            
            # Update session state
            st.session_state.query_count += 1
            
            # Save to history
            chat_item = {
                "question": request,
                "answer": response.text,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "response_time": response_time
            }
            st.session_state.chat_history.append(chat_item)
            
            # Clear loading and show response
            st.empty()
            
            # Enhanced response display
            timestamp_str = datetime.datetime.now().strftime("%H:%M:%S")
            
            st.markdown(f"""
            <div class="response-container">
                <div class="response-header">
                    <div class="response-title">
                        <span>🎯</span>
                        <span>AI Response</span>
                    </div>
                    <div class="response-meta">
                        <span>⏱️ {response_time}s</span>
                        <span>🤖 Gemini 2.5</span>
                        <span>🕐 {timestamp_str}</span>
                    </div>
                </div>
                <div class="response-text">{response.text}</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f"""
            <div class="error-container">
                <div class="response-header">
                    <div class="response-title">
                        <span>❌</span>
                        <span>Error Occurred</span>
                    </div>
                    <div class="response-meta">
                        <span>⏱️ {round(time.time() - start_time, 2)}s</span>
                    </div>
                </div>
                <div style="font-size: 1.0625rem; margin-bottom: 0.75rem;"><strong>Error Details:</strong> {str(e)}</div>
                <div style="font-size: 0.9375rem; opacity: 0.8; line-height: 1.5;">
                    <strong>Troubleshooting:</strong><br>
                    • Check your API key configuration<br>
                    • Verify internet connection<br>
                    • Try a different question<br>
                    • Contact support if issue persists
                </div>
            </div>
            """, unsafe_allow_html=True)

elif btn and not request.strip():
    st.error("⚠️ Please enter a question before submitting!")

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer with new design - no margins, proper padding
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; color: var(--text-muted); margin: 0;">
    <p style="font-size: 1.0625rem; font-weight: 500; margin: 0;">✨ Built with Streamlit & Google Gemini AI • Modern UI Design • Privacy-First</p>
    <p style="margin-top: 0.5rem; font-size: 0.8125rem; opacity: 0.7; margin-bottom: 0;">Experience the future of AI assistance</p>
</div>
""", unsafe_allow_html=True)
