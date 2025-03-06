import streamlit as st
import requests
import os

API_URL_SEARCH = "http://127.0.0.1:5000/search"
API_URL_UPLOAD = "http://127.0.0.1:5000/upload"
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

st.title("📄 AI-Powered Document Search & Retrieval Assistant ")

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

uploaded_file = st.file_uploader("📂 Upload a document (PDF, DOCX, PPTX, TXT)", type=["pdf", "docx", "pptx", "txt"])

if uploaded_file:
    with st.spinner("Uploading file..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(API_URL_UPLOAD, files={"file": uploaded_file})
        
        if response.status_code == 200:
            st.success("✅ File uploaded successfully!")
        else:
            st.error("❌ Failed to upload file.")

if stop_clicked:
    st.session_state.is_running = False

if search_clicked or (query and st.session_state.last_query != query):
    st.session_state.last_query = query
    st.session_state.is_running = True

    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<p style="color: green; font-weight: bold;">⚡ Running...</p>', unsafe_allow_html=True)

    response = requests.post(API_URL_SEARCH, json={"query": query})

    if response.status_code == 200:
        results = response.json()
        st.session_state.results = results if results else []
    
    st.session_state.is_running = False
    placeholder.empty()

if st.session_state.results:
    st.subheader("🔍 Search Results:")

    for result in st.session_state.results:
        file_name = result["file"]
        relevance = result["score"]
        summary = result["summary"]

        with st.expander(f"📂 {file_name} (⭐ {relevance}/100)"):
            st.write(f"**Summary:**\n{summary}")

