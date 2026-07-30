import os
import streamlit as st
from backend.rag.service import ingest_pdf

UPLOAD_DIR = "backend/uploads"


def render_pdf_upload(user_id: int):

    with st.sidebar.form("pdf_upload_form"):

        uploaded_file = st.file_uploader(
            "📄 Upload PDF",
            type=["pdf"],
        )

        submitted = st.form_submit_button("Upload")

    if not submitted:
        return

    if uploaded_file is None:
        st.sidebar.warning("Please choose a PDF.")
        return

    try:
        user_folder = os.path.join(
            UPLOAD_DIR,
            str(user_id),
            str(st.session_state.thread_id),
        )
        os.makedirs(user_folder, exist_ok=True)

        file_path = os.path.join(
            user_folder,
            uploaded_file.name,
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.sidebar.spinner("📄 Indexing PDF..."):
            ingest_pdf(
                file_path=file_path,
                user_id=user_id,
                thread_id=str(st.session_state.thread_id),
            )

        st.sidebar.success("✅ PDF indexed successfully!")

    except Exception as e:
        st.sidebar.exception(e)