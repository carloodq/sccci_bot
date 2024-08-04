import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
import pandas as pd
from datetime import datetime
import time
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage
)




# streamlit_app.py

import hmac
import streamlit as st


def ask_sccci(domanda_seg, info_scuola, chat_history):

    model_name = "gpt-3.5-turbo"
    chat_seg = ChatOpenAI(model_name=model_name, temperature=0)
    domanda_seg = f"""You are the receptionist of SCBCH, a museum with the objective of promoting Chinese culture in Singapore.
                    You have this information about the museum: {info_scuola}

                    Answer the following question.

                    Question:{domanda_seg}

                    Conversation so far: {chat_history}

                    Respond in a coincise and direct way.
                    If you don't know the answer, say you don't know.
                    """

    response = chat_seg([HumanMessage(content=domanda_seg)]).content
    return response




with open("info.txt", 'r',encoding='utf-8') as fl:
    info_sccc = fl.read()


st.title("SCBCH Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What's the email address of SCBCH?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = ask_sccci(prompt, info_sccc, str(st.session_state.messages))
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

