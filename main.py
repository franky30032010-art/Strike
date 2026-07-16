import streamlit as st
from groq import Groq

# 1. Title your public webpage
st.set_page_config(page_title="My Custom AI", page_icon="🤖", layout="wide")

# Custom CSS to handle centering and formatting
st.markdown(
    """
    <style>
    .stMainBlockContainer {
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    /* Hide default upload labels to keep the inline layout tight */
    div[data-testid="stFileUploader"] label {
        display: none;
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

# --- INLINE TYPING BAR LAYOUT WITH UPLOADER ---
# Create a form at the bottom so pressing enter submits both the file and the text
with st.form(key="chat_form", clear_on_submit=True):
    # Split the area into three columns: a wide text bar, an upload slot, and a submit button
    col1, col2, col3 = st.columns([6, 2, 1], vertical_alignment="bottom")
    
    with col1:
        user_text = st.text_input("Message...", placeholder="Ask StrikeAI a question...", label_visibility="collapsed")
        
    with col2:
        uploaded_file = st.file_uploader("Upload", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        
    with col3:
        submit_button = st.form_submit_button("Send")

# Display the uploaded file if present
if uploaded_file is not None:
    st.image(uploaded_file, caption="Attached Screenshot", width=300)

# 4. Handle Input & AI Generation
if submit_button and user_text:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_text)
    st.session_state.messages.append({"role": "user", "content": user_text})
    
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
