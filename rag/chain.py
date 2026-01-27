from langchain.chains import RetrievalQA
from rag.prompts import RAG_PROMPT
from rag.llm_factory import get_primary_llm, get_fallback_llm

def build_rag_chain(retriever, llm):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": RAG_PROMPT
        },
        return_source_documents=False
    )

def run_rag(retriever, query: str):
    """Run RAG pipeline with primary LLM and fallback support"""
    try:
        chain = build_rag_chain(retriever, get_primary_llm())
        return chain.run(query)
    except Exception as e:
        print(f"[WARN] Primary LLM failed: {e}")
        fallback_llm = get_fallback_llm()
        if fallback_llm:
            fallback_chain = build_rag_chain(retriever, fallback_llm)
            return fallback_chain.run(query)
        else:
            raise e
