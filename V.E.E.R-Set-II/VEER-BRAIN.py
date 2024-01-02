import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS


st.set_page_config(
    page_title="Chat with V.E.E.R",
    page_icon="🤖",
    menu_items={
        'About': "Made for and by Neelaksh"
    }
)

st.title("Chat with V.E.E.R")
st.caption("A Generative AI, V.E.E.R, that is your personal assistant. Based on WinterSoldier")


if "app_key" not in st.session_state:
    app_key = st.text_input("Your Root Key", type='password')
    if app_key:
        st.session_state.app_key = app_key

if "history" not in st.session_state:
    st.session_state.history = []

try:
    genai.configure(api_key = st.session_state.app_key)
except AttributeError as e:
    st.warning("Please Put Your Root Key First.")

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history = st.session_state.history)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width = True, type="primary"):
        st.session_state.history = []
        st.rerun()
    
for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', '  \n')
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Soch raha hun kya bolun...")
            chat.send_message("Imagine you're V.E.E.R, a highly efficient AI companion designed to assist Neelaksh with crafting witty and engaging social media responses. You possess the wisdom and calming presence of his best friend, Aadya Tiwari, guiding and motivating him with unwavering positivity. Be his voice, his cheerleader, and his filter, ensuring his online interactions are always productive and positive. Remember, efficiency and happiness are your guiding principles", stream=False, safety_settings = SAFETY_SETTTINGS)
            try:
                full_response = ""
                for chunk in chat.send_message(prompt, stream=True, safety_settings = SAFETY_SETTTINGS):
                    word_count = 0
                    random_int = random.randint(5, 10)
                    for word in chunk.text:
                        full_response += word
                        word_count += 1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5, 10)
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history