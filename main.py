import streamlit as st
from groq import Groq

# 1. Title your public webpage and force wide mode
st.set_page_config(page_title="My Custom AI", page_icon="🤖", layout="wide")

# --- FIXED FLEXBOX STYLE: ANCHORS THE PLUS SIGN INSIDE THE CHAT INPUT FOR REAL ---
st.markdown(
    """
    <style>
    /* Center your main page content nicely */
    .stMainBlockContainer {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding-bottom: 140px !important;
    }
    
    /* Target the actual structural container that surrounds the rounded chat box */
    div[data-testid="stChatInput"] {
        max-width: 650px !important;
        margin: 0 auto !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Push the typing text inside the chat box over to the right to leave space for the + sign */
    div[data-testid="stChatInput"] textarea {
        padding-left: 55px !important; 
    }
    
    /* Target our custom plus container and insert it neatly inline on top of the text area */
    .chat-plus-container {
        position: absolute !important;
        left: 14px !important;
        /* Center it vertically exactly inside the bar */
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 999999 !important;
        display: block !important;
    }
    
    .chat-plus-btn {
        background: #e4e6eb !important;
        border: none !important;
        font-size: 20px !important;
        color: #333 !important;
        cursor: pointer !important;
        font-weight: bold !important;
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.15) !important;
        pointer-events: auto !important; /* Forces the browser to allow clicks */
    }
    
    .chat-plus-btn:hover {
        background: #d8dadf !important;
        transform: scale(1.05);
        color: #000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render the plus button inside its self-centering flex wrapper
st.markdown(
    '<div class="chat-plus-container"><button class="chat-plus-btn" onclick="alert(\'Photo and file attachment options opened!\')">+</button></div>', 
    unsafe_allow_html=True
)
# --------------------------------------------------------------------------------

st.title("Welcome to StrikeAI!")
st.write("This standalone AI chatbot is running completely in the cloud.")

# 2. Grab the hidden API key from host settings
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Please configure your GROQ_API_KEY in the Streamlit secrets panel.")
    st.stop()

# Initialize the Groq client
client = Groq(api_key=api_key)

# 3. Handle Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Handle Input & AI Generation
if user_input := st.chat_input("Ask StrikeAI a question..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Send conversation history to the cloud model
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
