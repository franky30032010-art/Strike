import streamlit as st
from groq import Groq

# 1. Title your public webpage
st.set_page_config(page_title="My Custom AI", page_icon="🤖")
st.title("Welcome to StrikeAI!")
st.write("This standalone AI chatbot is running completely in the cloud.")

# --- NEW: ADVANCED INTEGRATED PLUS BUTTON STYLING ---
# This code injects a functional plus button directly into the native chat input bar!
st.markdown(
    """
    <style>
    /* Make room for the message space centering */
    .stMainBlockContainer {
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    /* Restyle the main chat input bar wrapper to fit our plus button */
    div[data-testid="stChatInput"] {
        max-width: 600px !important;
        margin: 0 auto !important;
        position: relative !important;
    }
    div[data-testid="stChatInput"] textarea {
        padding-left: 45px !important; /* Push placeholder text to the right for the + sign */
    }
    /* Style our custom overlay plus button */
    .chat-plus-btn {
        position: absolute;
        left: 15px;
        bottom: 12px;
        z-index: 1000;
        background: none;
        border: none;
        font-size: 24px;
        color: #555;
        cursor: pointer;
        font-weight: 300;
        line-height: 1;
        transition: transform 0.2s ease;
    }
    .chat-plus-btn:hover {
        transform: scale(1.15);
        color: #000;
    }
    </style>
    
    <script>
    // Simple script to handle clicking our custom inline plus button
    function triggerHiddenUpload() {
        const uploader = window.parent.document.querySelector('input[type="file"]');
        if (uploader) {
            uploader.click();
        } else {
            alert("Open the sidebar on the left to manage files!");
        }
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Render the interactive inline plus sign anchor visually
st.markdown('<button class="chat-plus-btn" onclick="triggerHiddenUpload()">+</button>', unsafe_allow_html=True)
# -----------------------------------------------------

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

# --- KEEPING AN OPTIONAL SIDEBAR FOR VISUAL ATTACHMENTS ---
with st.sidebar:
    st.header("Attachments")
    uploaded_file = st.file_uploader("Upload a screenshot (PNG, JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Screenshot", use_container_width=True)

# 4. Handle Input & AI Generation (Using native clean input bar!)
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
