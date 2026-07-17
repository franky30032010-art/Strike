import streamlit as st
from groq import Groq

# 1. Page Configuration & Layout Rules
st.set_page_config(page_title="My Custom AI", page_icon="🤖", layout="wide")

# Inject Custom CSS styles directly to layout objects
st.markdown(
    """
    <style>
    .stMainBlockContainer {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding-bottom: 140px !important; 
    }
    
    /* ABSOLUTELY HIDE DEFAULT SKELETON BLOCKS OF THE ORIGINAL UPLOADER BAR */
    .hidden-uploader, div[data-testid="stFileUploader"] {
        display: none !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        opacity: 0 !important;
    }
    
    /* STYLE NATIVE STREAMLIT BUTTON TO RENDER AS A CLEAN LARGE + ICON */
    div[data-testid="stColumn"]:first-child button {
        background-color: transparent !important;
        color: #65676b !important;
        border: none !important;
        font-size: 38px !important;
        font-weight: 200 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 44px !important;
        height: 44px !important;
        line-height: 44px !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: -6px !important; /* Raises plus slightly above entry input field */
        transition: transform 0.2s ease, color 0.2s ease !important;
    }
    
    div[data-testid="stColumn"]:first-child button:hover {
        transform: scale(1.15) rotate(90deg) !important;
        color: #007bff !important;
        background-color: transparent !important;
    }
    div[data-testid="stColumn"]:first-child button:active {
        background-color: transparent !important;
        color: #0056b3 !important;
    }

    /* Sleek Rounded Chat Entry Box */
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
    
    /* Floating Sticky Layout Footer Box */
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
    
    /* Wipe container boundary borders */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to StrikeAI!")
st.write("This standalone AI chatbot is running completely in the cloud.")

# 2. Host Secrets Validation
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Please configure your GROQ_API_KEY in the Streamlit secrets panel.")
    st.stop()

client = Groq(api_key=api_key)

# Initialize Session Triggers
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

# Render conversational interface feed elements
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- OPTIMIZED RE-RENDER FRAGMENT CONTAINER BLOCK ---
@st.fragment
def render_chat_input():
    st.markdown('<div class="sticky-footer-bar">', unsafe_allow_html=True)

    with st.form(key="chat_layout_form", clear_on_submit=True):
        col_plus, col_text, col_btn = st.columns([0.08, 0.78, 0.14], vertical_alignment="center")
        
        with col_plus:
            # Native Streamlit component acting as the click target trigger
            plus_clicked = st.form_submit_button("+")
            if plus_clicked:
                st.session_state.show_uploader = not st.session_state.show_uploader
                st.rerun()
                
        with col_text:
            user_text = st.text_input("Message", placeholder="Ask StrikeAI a question...", label_visibility="collapsed")
            
        with col_btn:
            submit_button = st.form_submit_button("Send")

    st.markdown('</div>', unsafe_allow_html=True)

    # Natively mount or unmount the file widget right on top of the box
    if st.session_state.show_uploader:
        st.markdown("<br><br>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload assets directly to chat", type=["png", "jpg", "jpeg", "txt", "pdf"])
        if uploaded_file is not None:
            st.success(f"📎 File tracking verification: {uploaded_file.name}")
    else:
        uploaded_file = None

    # 4. Handle Text Submission & Execution loops
    if submit_button and user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        
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
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
        # Reset the uploader state visibility on text submission
        st.session_state.show_uploader = False
        st.rerun()

# Execute the Input Function block
render_chat_input()
