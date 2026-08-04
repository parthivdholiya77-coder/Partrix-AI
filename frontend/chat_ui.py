import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
from frontend.components import copy_button
from langchain_core.messages import AIMessageChunk
from backend.graph.graph import chatbot
from backend.threads.service import ThreadService
from backend.threads.title_generator import generate_thread_title

def render_history():
    for idx, message in enumerate(st.session_state["message_history"]):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            copy_button(message["content"], key=f"copy_hist_{idx}")

def add_user_message(text:str):
    st.session_state["message_history"].append({
        "role": "user",
        "content": text,
    })


def add_ai_message(text:str):
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": text,
    })


def get_chat_config():
    return {
        "configurable": {
            "thread_id": str(st.session_state["thread_id"]),
            "user_id": st.session_state.user["id"],
        },
        "metadata": {
            "thread_id": str(st.session_state["thread_id"]),
            "user_id": st.session_state.user["id"],
        },
        "run_name": "chat_turn",
    }

def handle_user_input():
    user_input = st.chat_input('Type here')

    if user_input:

        is_first_message = len(st.session_state['message_history']) == 0

        if is_first_message:
            title = generate_thread_title(user_input, st.session_state.user["id"])
            ThreadService.rename(
                st.session_state["thread_id"],
                st.session_state.user["id"],
                title,
            )

        add_user_message(user_input)
        with st.chat_message('user'):
            st.markdown(user_input)
            copy_button(user_input, key="copy_user_live")

        config = get_chat_config()
        with st.chat_message("assistant"):
            status_holder = {"box": None}

            def response_stream():
                for message_chunk, metadata in chatbot.stream(
                    {
                        "messages": [HumanMessage(content=user_input)],
                        "user_id": st.session_state.user["id"],
                        "thread_id": str(st.session_state.thread_id),
                    },
                    config=config,
                    stream_mode="messages",
                     ):

                    if "nostream" in metadata.get("tags", []):
                        continue

                    if isinstance(message_chunk, ToolMessage):
                        tool_name = getattr(message_chunk, "name", "tool")
                        if status_holder["box"] is None:
                            status_holder["box"] = st.status(
                                f"🔧 Using `{tool_name}` …", expanded=True
                            )
                        else:
                            status_holder["box"].update(
                                label=f"🔧 Using `{tool_name}` …",
                                state="running",
                                expanded=True,
                            )
                        continue
                    

                    if isinstance(message_chunk, AIMessage):
                        if message_chunk.content:
                            yield message_chunk.content

                    elif isinstance(message_chunk, AIMessageChunk):
                        if message_chunk.content:
                            yield message_chunk.content

                    print(type(message_chunk))
                    print(message_chunk)
                    print(metadata)
                    print("-" * 80)

            ai_message = st.write_stream(response_stream())
            if not ai_message:
                 ai_message = "I couldn't generate a response."

            if status_holder["box"] is not None:
                status_holder["box"].update(
                    label="✅ Tool finished", state="complete", expanded=False
                )

            
            copy_button(ai_message, key="copy_ai_live")


        add_ai_message(ai_message)
        
        if is_first_message:
            st.rerun()

def show_chat():
    render_history()
    handle_user_input()

