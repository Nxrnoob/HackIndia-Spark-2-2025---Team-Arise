import streamlit as st
import requests
import os
import time

API_URL = "http://127.0.0.1:5000/search"
DOCUMENTS_DIR = "documents"

# 🚀 Remove Header, Footer, and Deploy Button
st.markdown("""
    <style>
    #MainMenu, header, footer, .stDeployButton, .stAppViewContainer > .stMarkdown:first-child {
        visibility: hidden !important; 
        display: none !important;
    }
    
    /* Sticky Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.95);  /* Matching Streamlit background */
        text-align: center;
        padding: 12px 0;
        font-weight: bold;
        color: black;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        z-index: 9999;
    }
    </style>
    <div class="footer">🚀 Made with ❤️ by Team Arise at HackIndia 2025</div>
""", unsafe_allow_html=True)

st.title("📄 AI-Powered Document Search")

if "results" not in st.session_state:
    st.session_state.results = []

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "is_running" not in st.session_state:
    st.session_state.is_running = False

query = st.text_input("Enter your search query", key="query_input")

col1, col2 = st.columns([4, 1])
search_clicked = col1.button("🔍 Search")
stop_clicked = col2.button("🛑 Stop")

if stop_clicked:
    st.session_state.is_running = False

if search_clicked or (query and st.session_state.last_query != query):
    st.session_state.last_query = query
    st.session_state.is_running = True

    placeholder = st.empty()  # Placeholder for animation
    with placeholder.container():
        st.markdown('<p style="color: green; font-weight: bold;">⚡ Running...</p>', unsafe_allow_html=True)

    response = requests.post(API_URL, json={"query": query})

    if response.status_code == 200:
        results = response.json()
        st.session_state.results = results if results else []
    
    st.session_state.is_running = False
    placeholder.empty()  # Remove animation once done

if st.session_state.results:
    st.subheader("🔍 Search Results:")

    for result in st.session_state.results:
        file_name = result["file"]
        relevance = result["score"]
        summary = result["summary"]

        with st.expander(f"📂 {file_name} (⭐ {relevance}/100)"):
            st.write(f"**Summary:**\n{summary}")

            file_path = os.path.join(DOCUMENTS_DIR, file_name)

            st.markdown(f"📂 **[Open File]({file_path})**", unsafe_allow_html=True)

            with open(file_path, "rb") as f:
                st.download_button(
                    label="📥 Download File",
                    data=f,
                    file_name=file_name,
                    mime="application/octet-stream"
                )

