import openai
import requests
import streamlit as st
from streamlit_chat import message
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader
import os

os.environ['OPENAI_API_KEY'] = "Add your openAI key"


def generate_vector_db():
    raw_text = TextLoader('medical-data.txt')
    knowledge_base = VectorstoreIndexCreator().from_loaders([raw_text])
    return knowledge_base


def querying_and_response_generation(user_input, knw_base_store):
    knw_base_response = knw_base_store.query(user_input)
    return knw_base_response


def get_input():
    input_text = st.text_input("provide input:", key="input")
    return input_text


def display_in_ui(user_input, kn_base_response):
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if input_from_user:
        st.session_state.past.append(user_input)
        st.session_state.generated.append(kn_base_response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state['generated'][i], key=str(i))
            message(st.session_state['past'][i], key=str(i) + '_user', is_user=True)


knowledge_base_store = generate_vector_db()
st.title("Welcome to Medical BOT")
input_from_user = get_input()
response = querying_and_response_generation(input_from_user, knowledge_base_store)
display_in_ui(input_from_user, response)

