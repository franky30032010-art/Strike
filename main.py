import streamlit as st
from groq import Groq

# 1. Title your public webpage and force wide mode
st.set_page_config(page_title="My Custom AI", page_icon="🤖", layout="wide")

# Custom CSS to design a stacked layout at the bottom of the screen
st.markdown(
    """
    <style>
    .stMainBlockContainer {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding-bottom: 220px !important; 
    }
    
    /* COMPLETELY HIDE THE BULKY DEFAULT STREAMLIT UPLOADER WIDGET */
    .hidden-uploader {
        display: none !important;
    }
    
    /* CENTERED TOP ROW FOR THE ATTACHMENT PLUS BUTTON */
    .attachment-row {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-bottom: 8px !important;
    }
    
    /* STYLE OUR SIMPLE, LARGE PLUS BUTTON */
    .clean-plus-btn {
        background: transparent !important;
        border: none !important;
        font-size: 36px !important; /* Made larger */
        font-weight: 300 !important;
        color: #65676b !important;
        cursor: pointer !important;
        width: 50px !important;
        height: 50px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.2s ease, color 0.2s ease;
        padding: 0 !important;
    }
    .clean-plus-btn:hover {
        transform: scale(1.2);
        color: #007bff !important;
    }
    
    /* Make the text entry field look sharp and remove margins */
    div[data-testid="stTextInput"] {
        margin: 0 !important;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 20px !important;
        padding: 10px 20px !important;
        border: 1px solid #d8dadf !important;
    }
    
    /* Style the main send button */
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 20px !important;
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #0056b3 !important;
    }
    
    /* Sticky footer bar container that pins everything to the bottom */
    .sticky-footer-bar {
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        max-width: 700px !important;
        width: 100% !important;
        background-color: white !important;
        z-index: 99999 !important;
        padding: 15px 20px !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        border: 1px solid #e4e6eb !important;
    }
    </style>
    
    <script>
    // JavaScript helper script that triggers the file manager when clicking our +
    function clickActualUploader() {
        const fileInput = window.parent.document.querySelector('div.hidden-uploader input[type="file"]');
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

# --- STACKED STICKY FOOTER INTERFACE ---
st.markdown('<div class="sticky-footer-bar">', unsafe_allow_html=True)

with st.form(key="chat_layout_form", clear_on_submit=True):
    
    # ROW 1: Large + Upload Symbol sitting on top
    st.markdown('<div class="attachment-row">', unsafe_allow_html=True)
    st.markdown('<button type="button" class="clean-plus-btn" onclick="clickActualUploader()">+</button>', unsafe_allow_html=True)
    
    # Functional uploader running silently in the background
    st.markdown('<div class="hidden-uploader">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Hidden", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ROW 2: Input box and send button underneath
    input_col, button_col = st.columns([0.85, 0.15], vertical_alignment="center")
    
    with input_col:
        user_text = st.text_input("Message", placeholder="Ask StrikeAI a question...", label_visibility="collapsed")
        
    with button_col:
        submit_button = st.form_submit_button("Send")

st.markdown('</div>', unsafe_allow_html=True)

# If an asset file is uploaded, show its preview box inside the conversation zone
if uploaded_file is not None:
    st.image(uploaded_file, caption="Attached File Preview", width=200)
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
