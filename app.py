import streamlit as st
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Page config
st.set_page_config(page_title="🧠 BlenderBot Chat", page_icon="🤖", layout="centered")

# Custom CSS for chat UI
st.markdown("""
    <style>
    .chat-container {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 12px;
        max-height: 450px;
        overflow-y: auto;
        font-family: 'Segoe UI', sans-serif;
    }
    .message {
        margin-bottom: 16px;
        display: flex;
    }
    .message.bot {
        justify-content: flex-start;
    }
    .message.user {
        justify-content: flex-end;
    }
    .bubble {
        max-width: 80%;
        padding: 12px 16px;
        border-radius: 18px;
        line-height: 1.4;
    }
    .bubble.bot {
        background-color: #e8e8e8;
        color: #111;
        border-bottom-left-radius: 4px;
    }
    .bubble.user {
        background-color: #5fba7d;
        color: white;
        border-bottom-right-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 BlenderBot Chat")

# Load the model
@st.cache_resource
def load_model():
    model_name = "facebook/blenderbot-1B-distill"
    tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# Session state for messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input form
with st.form("chat-form", clear_on_submit=True):
    user_input = st.text_input("💬 Message", "", placeholder="Say something...")
    send = st.form_submit_button("Send")

# Chat logic
if send and user_input:
    inputs = tokenizer([user_input], return_tensors="pt")
    output_ids = model.generate(**inputs)
    bot_reply = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", bot_reply))

# Display chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for sender, msg in st.session_state.chat_history:
    role_class = "user" if sender == "user" else "bot"
    st.markdown(
        f'<div class="message {role_class}"><div class="bubble {role_class}">{msg}</div></div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# Clear button
if st.button("🗑️ Clear Conversation"):
    st.session_state.chat_history = []
