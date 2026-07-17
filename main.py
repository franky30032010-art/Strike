import streamlit as st
from groq import Groq

# 1. Page Configuration & Setup
st.set_page_config(page_title="My Custom AI", page_icon="🤖", layout="wide")

# Custom CSS to construct a clean, modern input bar
st.markdown(
    """
    <style>
    .stMainBlockContainer {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding-bottom: 140px !important; 
    }
    
    /* ABSOLUTELY HIDE SKELETON CORES OF THE DEFAULT UPLOADER BOXES */
    .hidden-uploader, div[data-testid="stFileUploader"] {
        display: none !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        opacity: 0 !important;
    }
    
    /* LARGE + ACTION BUTTON DESIGN */
    .plus-action-wrapper {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 100% !important;
    }
    
    .clean-plus-btn {
        background: transparent !important;
        border: none !important;
        font-size: 38px !important; 
        font-weight: 200 !important;
        color: #65676b !important;
        cursor: pointer !important;
        width: 44px !important;
        height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: -6px !important; /* Raises symbol slightly above text baseline */
        transition: transform 0.2s ease, color 0.2s ease;
        padding: 0 !important;
    }
    .clean-plus-btn:hover {
        transform: scale(1.15) rotate(90deg);
        color: #007bff !important;
    }
    
    /* Sleek Text Input Box styling */
    div[data-testid="stTextInput"] {
        margin: 0 !important;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 24px !important;
        padding: 12px 20px !important;
        border: 1px solid #e4e6eb !important;
        background-color: #f0f2f5 !important;
    }
    div[data-testid="stTextInput"] input:focus {
        background-color: #ffffff !important;
        border-color: #007bff !important;
    }
    
    /* Minimalist Pill Send Button */
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 20px !important;
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        padding: 8px 22px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #0056b3 !important;
        color: white !important;
    }
    
    /* Floating Sticky Footer Bar */
    .sticky-footer-bar {
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        max-width: 760px !important;
        width: 92% !important;
        background-color: white !important;
        z-index: 99999 !important;
        padding: 10px 16px !important;
        border-radius: 32px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06) !important;
        border: 1px solid #e4e6eb !important;
    }
    
    /* Remove default streamlit form borders */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    </style>
    
    <script>
    // Safe DOM target selector to trigger the hidden system explorer window
    function clickActualUploader() {
        const fileInput = window.parent.document.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.click();
        }
    }
    </script>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to StrikeAI!")
st.write("This standalone AI chatbot is running completely in the cloud.")

# 2. API Key verification
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Please configure your GROQ_API_KEY in the Streamlit secrets panel.")
    st.stop()

client = Groq(api_key=api_key)

# 3. Handle Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- HORIZONTAL INTEGRATED DESIGN INPUT BAR ---
st.markdown('<div class="sticky-footer-bar">', unsafe_allow_html=True)

with st.form(key="chat_layout_form", clear_on_submit=True):
    
    # Grid columns aligning layout parts seamlessly
    col_plus, col_text, col_btn = st.columns([0.08, 0.78, 0.14], vertical_alignment="center")
    
    with col_plus:
        st.markdown('<div class="plus-action-wrapper">', unsafe_allow_html=True)
        st.markdown('<button type="button" class="clean-plus-btn" onclick="clickActualUploader()">+</button>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_text:
        user_text = st.text_input("Message", placeholder="Ask StrikeAI a question...", label_visibility="collapsed")
        
    with col_btn:
        submit_button = st.form_submit_button("Send")

st.markdown('</div>', unsafe_allow_html=True)

# Functional uploader rendering silently inside the backend thread
with st.sidebar:
    st.markdown('<div class="hidden-uploader">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("HiddenFile", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

# If an asset file is selected, visually prompt a confirmation badge into the feed
if uploaded_file is not None:
    st.info(f"📎 File attached: {uploaded_file.name}")
# -------------------------------------------------------------

# 4. Handle Input & AI Generation
if submit_button and user_text:
    with st.chat_message("user"):
        st.markdown(user_text)
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.chat_message("assistant"):
        persona = (
            "You are StrikeAI, a highly authentic, chill, and slightly witty gaming buddy "
            "created by Franky. Talk like a real teenager or streamer on Discord or Twitch. "
            "Avoid cringe, over-the-top robotic slang like 'Greetings gamer!' or 'That is epic!'. "
            "Instead, keep your answers short, punchy, and casual. Use lowercase occasionally, "
            "casual transitions like 'tbh', 'imo', or 'idk', and talk passionately about game "
            "mechanics, metas, strategies, and patch notes. If someone asks a non-gaming question, "
            "answer it quickly with a sarcastic twist or tie it back to video games."
        )
        
        groq_messages = [{"role": "system", "content": persona}]
        for m in st.session_state.messages:
            groq_messages.append({"role": m["role"], "content": m["content"]})
            
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages
        )
        response_text = completion.choices.message.content
        st.markdown(response_text)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun()
