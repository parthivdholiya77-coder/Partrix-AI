import streamlit as st
import uuid

from backend.threads.service import ThreadService
from backend.graph.graph import chatbot
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage


def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):

    if not ThreadService.belongs_to_user(
        thread_id,
        st.session_state.user["id"]
    ):
        return []

    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": str(thread_id),
                "user_id": st.session_state.user["id"],
            }
        }
    )

    return state.values.get("messages", [])

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    ThreadService.create(
        thread_id,
        st.session_state.user["id"],
    )
    st.session_state['message_history'] = []

def init_session():

    if not st.session_state.get("user"):
        return

    if "thread_id" not in st.session_state:

        threads = ThreadService.get_all_threads(st.session_state.user["id"])

        if threads:
            st.session_state["thread_id"] = threads[-1]
        else:
            st.session_state["thread_id"] = generate_thread_id()

    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = ThreadService.get_all_threads(
            st.session_state.user["id"]
        )

    add_thread(st.session_state["thread_id"])

    if "message_history" not in st.session_state:
        messages = load_conversation(st.session_state["thread_id"])

        history = []

        for msg in messages:

            # Ignore tool messages
            if isinstance(msg, ToolMessage):
                continue

            if isinstance(msg, HumanMessage):
                history.append(
                    {
                        "role": "user",
                        "content": msg.content,
                    }
                )

            elif isinstance(msg, AIMessage):
                if msg.content:
                    history.append(
                        {
                            "role": "assistant",
                            "content": msg.content,
                        }
                    )

        st.session_state["message_history"] = history