import streamlit as st

from backend.database.models import create_tables
from frontend.auth_ui import show_auth_page
from frontend.session import init_session
from frontend.sidebar import show_sidebar
from frontend.chat_ui import show_chat

st.set_page_config(
    page_title="Partrix AI",
    page_icon="🤖",      # Optional
    layout="wide"
)


# Create database tables
create_tables()

# ---------------- Authentication State ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- Login ---------------- #

if not st.session_state.logged_in:
    show_auth_page()
    st.stop()

# ---------------- Chat Initialization ---------------- #

init_session()

# ---------------- UI ---------------- #

show_sidebar()
show_chat()