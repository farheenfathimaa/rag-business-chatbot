import streamlit as st
import json
from pathlib import Path

def load_business_config(business_id: str):
    path = Path(f"businesses/{business_id}/business.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_chat_ui(business_config):
    branding = business_config.get("branding", {})

    primary = branding.get("primary_color", "#4CAF50")
    secondary = branding.get("secondary_color", "#1E1E1E")
    accent = branding.get("accent_color", "#C2A875")

    st.markdown(
        f"""
        <style>
        body {{
            background-color: {secondary};
        }}

        .stChatMessage[data-testid="chat-message-assistant"] {{
            background-color: {secondary};
            border-left: 4px solid {accent};
            border-radius: 10px;
            padding: 12px;
        }}

        .stChatMessage[data-testid="chat-message-user"] {{
            background-color: {primary};
            color: white;
            border-radius: 10px;
            padding: 12px;
        }}

        h1 {{
            color: {primary};
        }}

        .stButton>button {{
            background-color: {primary};
            color: white;
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    logo_url = branding.get("logo_url", "https://drive.google.com/uc?id=1HQCR70hdr_s2T1wXGuV8QOVoLG7dLop8")
    business_name = business_config.get("business_name", "Business")
    
    # 🧠 Header
    col1, col2 = st.columns([1, 6])
    with col1:
        if logo_url:
            st.image(logo_url, width=60)
    with col2:
        st.markdown(
            f"<h1 style='margin-top: 10px;'>{business_name} Chatbot</h1>",
            unsafe_allow_html=True
        )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    return st.chat_input("Ask a question about the business...")

def add_message(role, content):
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })
