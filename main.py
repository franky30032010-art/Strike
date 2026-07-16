import streamlit as st
from huggingface_hub import InferenceClient

# 1. Title your public webpage
st.set_page_config(page_title="My Custom AI", page_icon="🤖")
st.title("Welcome to StrikeAI!")
st.write("This standalone AI chatbot is running completely in the cloud.")

# 2. Grab the hidden API key from host settings
if "HF_TOKEN" in st.secrets:
    api_key = st.secrets["HF_TOKEN"]
else:
    st.error("Please configure your HF_TOKEN in the Streamlit secrets panel.")
    st.stop()

# Initialize the Hugging Face client using a free Meta Llama model
client = InferenceClient(provider="hf-inference", api_key=api_key)

# 3. Handle Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Handle Input & AI Generation
if user_input := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Send conversation history to the cloud model
    with st.chat_message("assistant"):
        # This gives StrikeAI its unique identity and personality!
        hf_messages = [{"role": "system", "content": "You are StrikeAI, a funny and slightly sarcastic gaming expert. Use casual slang."}]
        
        for m in st.session_state.messages:
            hf_messages.append({"role": m["role"], "content": m["content"]})
            
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct", 
            messages=hf_messages,
            max_tokens=500
        )
        response_text = completion.choices.message.content
        st.markdown(response_text)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
