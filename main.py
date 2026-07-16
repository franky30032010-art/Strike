import streamlit as st
from groq import Groq

# 1. Title your public webpage and force wide mode
st.set_page_config(page_title="My Custom AI", page_icon="🤖", layout="wide")

# Custom CSS to force the uploader to lock to the bottom right above the input bar
st.markdown(
    """
    <style>
    .stMainBlockContainer {
        max-width: 700px !important;
        margin: 0 auto !important;
        padding-bottom: 220px !important; /* Extra padding so chat text clears the bottom layout */
    }
    
    /* Target the file uploader and glue it directly to the sticky bottom of the webpage */
    div[data-testid="stFileUploader"] {
        position: fixed !important;
        bottom: 110px !important; /* Floats perfectly above the 60px stChatInput bar */
        left: 50% !important;
        transform: translateX(-50%) !important;
        max-width: 650px !important;
        width: 100% !important;
        z-index: 99999 !important;
        background-color: white !important;
        padding: 5px 0 !important;
    }
    
    /* Shrink the box to make it sleek and small */
    div[data-testid="stFileUploader"] section {
        padding: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# --- UPDATED: RE-POSITIONED COMPACT BOTTOM UPLOADER ---
# label_visibility="collapsed" hides the bulky instruction text to save space
uploaded_file = st.file_uploader("+ Add screenshot or file:", type=["png", "jpg", "jpeg"], label_visibility="visible")

if uploaded_file is not None:
    st.image(uploaded_file, caption="Attached File Preview", width=200)
# -------------------------------------------------------------

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
    st.rerun()
