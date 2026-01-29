from langchain_groq import ChatGroq
#from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GROQ_API_KEY

def get_groq_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

# def get_gemini_llm():
#     return ChatGoogleGenerativeAI(
#         google_api_key=GEMINI_API_KEY,
#         model="gemini-1.5-flash",
#         temperature=0
#     )

def get_primary_llm():
    return get_groq_llm()

def get_fallback_llm():
    return None
