import streamlit as st
from streamlit_chat import message
import google.generativeai as palm

def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]


with st.sidebar:
    palm_api_key = st.text_input('Enter Master Key', key='palm_api_key')
    "Please enter your master key in order to begin using the V.E.E.R. System"



# Adding an title to the app
st.title("V.E.E.R Welcomes you!")

#Initialize message state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "AI assistant", "content": "Say something to get started!"}]  #Update "assistant" to your ai's mindset

# Now, let's create a form to get user input and sent it to the Google’s PaLM API. We will use Streamlit's st.form() to 
# create a form and st.columns() to create two columns. The first column will be used for user input, and the second column 
# Send button.

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt = a.text_input(
        label="Your message:",
        placeholder="Type something...",
        label_visibility="collapsed",
    )

    b.form_submit_button("Send", use_container_width=True)

# Make user input at the left side of the screen, so it looks like a chat app:

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")  # display message on the screen

# Configure Google's PaLM API with your API key and get response from the API:

if user_prompt and palm_api_key:

    palm.configure(api_key=palm_api_key)  # set API key
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    message(user_prompt, is_user=True)
    response = palm.chat(messages=[user_prompt])  # get response from Google's PaLM API
    msg = {"role": "assistant", "content": response.last} 

    # we are using dictionary to store message and its role. 
    # It will be useful later when we want to display chat history on the screen, to show user input at the left and AI's right side of the screen.
    
    st.session_state.messages.append(msg)  # add message to the chat history

    message(msg["content"])  # display message on the screen

# Finally, let's add a button to clear the chat history:

def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]

if len(st.session_state.messages) > 1:
    st.button('Clear Chat', on_click=clear_chat)