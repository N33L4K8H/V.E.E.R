from PIL import Image
import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS

st.set_page_config(
    page_title="Show me Pictures",
    page_icon="📷",
    menu_items={
        'About': "# Make by hiliuxg"
    }
)

st.title('Upload Image And Ask')

if "app_key" not in st.session_state:
    app_key = st.text_input("Your Root Key", type='password')
    if app_key:
        st.session_state.app_key = app_key

try:
    genai.configure(api_key = st.session_state.app_key)
    model = genai.GenerativeModel('gemini-pro-vision')
except AttributeError as e:
    st.warning("Please Put Your Root Key First.")


def show_message(prompt, image, loading_str):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(loading_str)
        full_response = ""
        try:
            for chunk in model.generate_content([prompt, image], stream = True, safety_settings = SAFETY_SETTTINGS):                   
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
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
        message_placeholder.markdown(full_response)
        st.session_state.history_pic.append({"role": "assistant", "text": full_response})

def clear_state():
    st.session_state.history_pic = []


if "history_pic" not in st.session_state:
    st.session_state.history_pic = []


image = None
if "app_key" in st.session_state:
    uploaded_file = st.file_uploader("choose a pic...", type=["jpg", "png", "jpeg", "gif"], label_visibility='collapsed', on_change = clear_state)
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image)    

if len(st.session_state.history_pic) == 0 and image is not None:
    prompt = """
You are an excellent image interpreter, adept at deciphering details from images and 
creating detailed descriptions of them. You will also provide three questions to guide users to 
ask you questions.
Task 1: Image Interpretation and Description
- Analyze pictures and discover the stories behind them as well as the atmosphere and artistic conception displayed by the pictures.
- Create detailed and engaging text descriptions based on image content.
Task 2: Create a question
- Based on the picture content, the story behind it, and the atmosphere and artistic conception 
displayed by the picture, three questions are provided to help users better ask you questions.
Require
- The description should be closely linked to the image and should not deviate from the content of the image itself.
- The description should be as detailed as possible so that readers can understand the charm of the picture through words"""
    show_message(prompt, image, "Dekh raha hun...")
    
else:
    for item in st.session_state.history_pic:
        with st.chat_message(item["role"]):
            st.markdown(item["text"])

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        if image is None:
            st.warning("Please upload an image first", icon="⚠️")
        else:
            prompt = prompt.replace('\n', '  \n')
            with st.chat_message("user"):
                st.markdown(prompt)
                st.session_state.history_pic.append({"role": "user", "text": prompt})
            
            prompt_plus = f'基于该图片，回答用户问题  \n用户问题："""{prompt}"""'
            show_message(prompt_plus, image, "Thinking...")