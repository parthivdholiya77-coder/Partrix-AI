import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI

load_dotenv()

# llm = ChatOpenAI(
#     model="gpt-4.1-mini",

# )


@st.cache_resource
def load_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
    )

llm = load_llm()
