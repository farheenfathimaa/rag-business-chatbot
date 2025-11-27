import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 1. SETUP & CONFIGURATION
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Urban Threadz AI", page_icon="🧵", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color: #ffffff;}
    .stChatInput {position: fixed; bottom: 30px;}
    </style>
    """, unsafe_allow_html=True)

# 2. HELPER FUNCTIONS

def load_customer_data():
    """Loads the static JSON data for customer queries."""
    with open("data/brand_data.json", "r") as f:
        return json.load(f)

def process_admin_pdf(uploaded_file):
    """Processes uploaded PDF for the Admin RAG system."""
    # Save file temporarily to disk
    with open("temp_admin_doc.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load and split the PDF
    loader = PyPDFLoader("temp_admin_doc.pdf")
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(pages)
    
    # Create Vector Database (The "Brain")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🧵 Urban Threadz")
    st.write("AI-Powered Retail Assistant")
    st.divider()
    
    mode = st.radio("Select Interface:", 
                    ["🛍️ Customer Support", "🔐 Admin Dashboard"],
                    captions=["For shoppers", "For business owners"])
    
    st.divider()
    st.caption("Powered by Google Gemini & LangChain")

    # Clear chat history when switching modes
    if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
        st.session_state.messages = []
        st.session_state.current_mode = mode

# 4. MAIN APP LOGIC

if mode == "🛍️ Customer Support":
    st.header("Welcome to Urban Threadz! 🧢")
    st.write("I can help you with product details, sizing, and order info.")
    
    # Load Brand Knowledge
    brand_data = load_customer_data()
    brand_context = json.dumps(brand_data)

    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

    # Display Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask about hoodies, shipping, or returns..."):
        # Show User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_prompt = f"""
                You are a helpful sales assistant for 'Urban Threadz', a streetwear brand.
                Use the following JSON data to answer the user's question accurately.
                
                DATA: {brand_context}
                
                RULES:
                1. Be friendly and cool (streetwear vibe).
                2. If the user asks about a product, mention the price and stock status.
                3. If the info isn't in the JSON, say you don't know and suggest emailing support.
                4. Keep answers concise.
                
                USER QUESTION: {prompt}
                """
                response = llm.invoke(system_prompt)
                st.markdown(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})

elif mode == "🔐 Admin Dashboard":
    st.header("📊 Business Intelligence Hub")
    
    # Authentication (Simple)
    password = st.text_input("Enter Admin Key", type="password")
    
    if password == "admin123":
        st.success("Access Granted")
        
        # File Upload Area
        st.subheader("Document Analysis (RAG)")
        uploaded_file = st.file_uploader("Upload a Business PDF (Tax, Policy, Reports)", type="pdf")
        
        # Process PDF if uploaded
        if uploaded_file:
            if "vector_store" not in st.session_state:
                with st.spinner("Reading and indexing document..."):
                    st.session_state.vector_store = process_admin_pdf(uploaded_file)
                st.toast("Document processed successfully!", icon="✅")
            
            # Admin Chat Interface
            if "admin_messages" not in st.session_state:
                st.session_state.admin_messages = []

            for msg in st.session_state.admin_messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            if prompt := st.chat_input("Ask a question about the uploaded document..."):
                st.session_state.admin_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # RAG Answer Generation
                with st.chat_message("assistant"):
                    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
                    
                    # Create Retrieval Chain
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=st.session_state.vector_store.as_retriever()
                    )
                    
                    response = qa_chain.run(prompt)
                    st.markdown(response)
                    st.session_state.admin_messages.append({"role": "assistant", "content": response})
        else:
            st.info("👆 Please upload a PDF document to start analyzing.")
            
    elif password:
        st.error("Invalid Admin Key")