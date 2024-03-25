#from openai import OpenAI
import streamlit as st
import google.generativeai as genai
#from google.cloud import language_v1
import time
import random
from .env load key

key()

#with st.sidebar:
  #  openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
   # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
   # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
   # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


st.title("💬 Finserv")
#st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I'm Finserv your Financial Services Policy Expert. I can help you with summarising legislative documents, creating detailed study guides and exam material for staff training and ensure accurate conveyance of information."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

#if prompt := st.chat_input():
    #if not openai_api_key:
        #st.info("Please add your OpenAI API key to continue.")
        #st.stop()

    # client = OpenAI(api_key=openai_api_key)
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_message("user").write(prompt)
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg)


st.session_state.app_key = 'AIzaSyA5FcQ8pyNtFQ569nsZEto02hesrVmUha0'

# if "app_key" not in st.session_state:
#     app_key = st.text_input("Please enter your Gemini API Key", type='password')
#     if app_key:
#         st.session_state.app_key = app_key
        

if "history" not in st.session_state:
    st.session_state.history = []

try:
    genai.configure(api_key = st.session_state.app_key)
except AttributeError as e:
    st.warning("Please Put Your Gemini API Key First")

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history = st.session_state.history)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = []
        st.rerun()

for message in chat.history:
    role ="assistant" if message.role == 'model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', ' \n')
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                full_response = ""
                for chunk in chat.send_message(prompt, stream=True):
                    word_count = 0
                    random_int = random.randint(5,10)
                    for word in chunk.text:
                        full_response+=word
                        word_count+=1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5,10)
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history
