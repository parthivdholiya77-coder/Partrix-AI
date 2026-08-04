import streamlit as st
from backend.threads.service import ThreadService
from frontend.session import reset_chat, load_conversation
from frontend.pdf_upload import render_pdf_upload
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

def show_sidebar():

    
    st.sidebar.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #10A37F, #1DB954);
            color: white;
            padding: 14px;
            border-radius: 12px;
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 10px;
            box-shadow: 0 4px 10px rgba(16,163,127,0.3);
        ">
            🤖 Partrix AI
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.divider()
    if st.sidebar.button(
        "➕ New Chat",
        use_container_width=True,
    ):
        reset_chat()
    st.sidebar.divider()

    render_pdf_upload(st.session_state.user["id"])

    st.sidebar.divider()

    st.sidebar.header('My Conversations')

    search_query = st.sidebar.text_input(
        "🔍 Search",
        placeholder="Search conversations...",
    )

    st.sidebar.subheader("💬 Conversations")

    threads_with_titles = [
        (tid, ThreadService.get_title(tid, st.session_state.user["id"]))
        for tid in st.session_state["chat_threads"][::-1]
    ]

    if search_query:
        threads_with_titles = [
            (tid, title) for tid, title in threads_with_titles
            if search_query.lower() in title.lower()
        ]
    current_thread = st.session_state.get("thread_id")

    for thread_id, thread_label in threads_with_titles:
        is_active = thread_id == current_thread

        button_label = (
            f"▶ {thread_label}"
            if is_active
            else thread_label
        )
        col1, col2 = st.sidebar.columns([4, 1])

        with col1:
            if st.button(
                button_label,
                key=f"open_{thread_id}",
                use_container_width=True,
            ):

                st.session_state["thread_id"] = thread_id

                messages = load_conversation(thread_id)

                temp_messages = []

                for msg in messages:

                    if isinstance(msg, ToolMessage):
                        continue

                    if isinstance(msg, HumanMessage):
                        temp_messages.append(
                            {
                                "role": "user",
                                "content": msg.content,
                            }
                        )

                    elif isinstance(msg, AIMessage):

                        if getattr(msg, "tool_calls", None):
                            continue

                        if not msg.content:
                            continue

                        temp_messages.append(
                            {
                                "role": "assistant",
                                "content": msg.content,
                            }
                        )

                st.session_state["message_history"] = temp_messages
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"delete_{thread_id}"):
                ThreadService.delete(thread_id, st.session_state.user["id"])
                st.session_state['chat_threads'].remove(thread_id)

                if st.session_state['thread_id'] == thread_id:
                    reset_chat()

                st.rerun()

    if search_query and not threads_with_titles:
        st.sidebar.caption("No matching conversations found.")

    st.sidebar.divider()

    with st.sidebar.popover(f"👤 {st.session_state.user['username']}", use_container_width=True):

        st.write(f"**Username:** {st.session_state.user['username']}")

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            st.session_state.logged_in = False
            st.session_state.user = None

            st.session_state.message_history = []
            st.session_state.chat_threads = []

            st.session_state.pop("thread_id", None)
            st.session_state.pop("editing_thread", None)

            st.rerun()


    