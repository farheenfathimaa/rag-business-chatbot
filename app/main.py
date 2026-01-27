import os
import streamlit as st

from app.auth import login
from app.ui import render_chat_ui, add_message
from app.config import BUSINESS_ID, PACKAGE_FEATURES, PACKAGE_TYPE

from ingestion.ingest import ingest_files
from rag.retriever import get_retriever
from rag.chain import build_rag_chain, run_rag
from utils.error_handler import handle_error

from types import SimpleNamespace

def auto_ingest_existing_docs():
    base_path = f"businesses/{BUSINESS_ID}"

    for access in ["public", "admin"]:
        docs_path = os.path.join(base_path, f"{access}_docs")
        if not os.path.exists(docs_path):
            continue

        files = []
        for filename in os.listdir(docs_path):
            if not filename.lower().endswith((".pdf", ".txt", ".docx")):
                continue

            file_path = os.path.join(docs_path, filename)
            files.append(
                SimpleNamespace(
                    name=filename,
                    read=lambda fp=file_path: open(fp, "rb").read()
                )
            )
        if files:
            ingest_files(files, BUSINESS_ID, access)


def real_rag_answer(query, role):
    try:
        retriever = get_retriever(BUSINESS_ID, role)
        return run_rag(retriever, query)
    except Exception as e:
        handle_error(e)
        return "I couldn't process that request right now."


def run_app():
    st.set_page_config(page_title="RAG Business Chatbot", layout="centered")

    # Auto-ingest once per session
    if "auto_ingested" not in st.session_state:
        auto_ingest_existing_docs()
        st.session_state.auto_ingested = True


    login()
    role = st.session_state.get("role", "user")

    features = PACKAGE_FEATURES[PACKAGE_TYPE]

    # ===============================
    # ADMIN UPLOAD SECTION
    # ===============================
    if role == "admin" and features["admin_docs"]:
        st.subheader("📄 Upload Business Documents")

        uploaded_files = st.file_uploader(
            "Upload PDF / TXT / DOCX files",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True
        )

        if uploaded_files:
            try:
                ingest_files(
                    uploaded_files,
                    BUSINESS_ID,
                    "admin",
                    features["max_docs"]
                )
                st.success(f"{len(uploaded_files)} document(s) ingested successfully.")
            except Exception as e:
                handle_error(e)

    # ===============================
    # CHAT SECTION
    # ===============================
    query = render_chat_ui()

    if query:
        add_message("user", query)
        
        with st.spinner("🤔 Thinking..."):
            answer = real_rag_answer(query, role)
        
        add_message("assistant", answer)
        st.rerun()  # ✅ CRITICAL: Force UI refresh to show new messages
