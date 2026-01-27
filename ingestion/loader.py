from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader
import tempfile
import os

def load_document(file_path: str):
    """
    Supports:
    - Streamlit UploadedFile
    - Normal opened files from disk (rb)
    """
    
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return loader.load()