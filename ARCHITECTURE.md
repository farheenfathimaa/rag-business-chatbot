# 🏗️ RAG Chatbot Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Streamlit - app/ui.py)                    │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Chat Input   │  │ File Upload  │  │ Auth Login   │        │
│  │ (User Query) │  │ (Admin Only) │  │ (Role Select)│        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│                       (app/main.py)                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Authenticate User (user/admin)                        │  │
│  │ 2. Handle File Uploads (if admin)                        │  │
│  │ 3. Process Chat Query                                    │  │
│  │ 4. Return Response                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         RAG PIPELINE                            │
│                      (rag/chain.py)                             │
│                                                                 │
│  Query → Embeddings → Vector Search → Context → LLM → Answer   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Retriever    │  │ LLM Factory  │  │ Prompts      │        │
│  │ (retriever.py)│  │(llm_factory.py)│ │(prompts.py)  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      VECTOR DATABASE                            │
│                    (FAISS - vector_db/)                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Business 1: urban_threadz/                               │  │
│  │   ├── index.faiss (vector embeddings)                    │  │
│  │   └── index.pkl (metadata)                               │  │
│  │                                                          │  │
│  │ Business 2: client_name/                                 │  │
│  │   ├── index.faiss                                        │  │
│  │   └── index.pkl                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                           │
│                   (ingestion/ingest.py)                         │
│                                                                 │
│  Documents → Load → Chunk → Embed → Store                      │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Loader       │  │ Chunker      │  │ Embedder     │        │
│  │ (loader.py)  │  │ (chunker.py) │  │ (embedder.py)│        │
│  │              │  │              │  │              │        │
│  │ PDF, DOCX,   │  │ Split into   │  │ Sentence     │        │
│  │ TXT support  │  │ 800-char     │  │ Transformers │        │
│  │              │  │ chunks       │  │ (MiniLM)     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS DOCUMENTS                         │
│                    (businesses/{id}/)                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ public_docs/                                             │  │
│  │   ├── brand_info.txt                                     │  │
│  │   ├── product_catalog.txt                                │  │
│  │   └── faq.txt                                            │  │
│  │                                                          │  │
│  │ admin_docs/                                              │  │
│  │   ├── internal_policies.txt                              │  │
│  │   └── tax_documents.txt                                  │  │
│  │                                                          │  │
│  │ business.json (metadata)                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: User Query

```
1. USER TYPES QUERY
   "What's your return policy?"
   │
   ▼
2. AUTHENTICATION CHECK
   Role: "user" (not admin)
   │
   ▼
3. QUERY EMBEDDING
   Convert text → 384-dim vector
   Using: sentence-transformers/all-MiniLM-L6-v2
   │
   ▼
4. VECTOR SEARCH (FAISS)
   Search in: vector_db/urban_threadz/
   Filter: access="public" (user can't see admin docs)
   Retrieve: Top 4 most similar chunks
   │
   ▼
5. CONTEXT ASSEMBLY
   Chunk 1: "30-day return window..."
   Chunk 2: "Items must be unworn..."
   Chunk 3: "Free returns for US..."
   Chunk 4: "Refunds processed within..."
   │
   ▼
6. LLM PROMPT
   Template: "Use ONLY the context below..."
   Context: [4 chunks]
   Question: "What's your return policy?"
   │
   ▼
7. LLM GENERATION (Groq - Llama 3)
   Generate answer based on context
   │
   ▼
8. RESPONSE
   "We offer a 30-day return window. Items must be 
    unworn with original tags. Free returns for US 
    customers. Refunds processed within 7-10 days."
   │
   ▼
9. UI UPDATE
   Display in chat interface
   st.rerun() to refresh UI
```

---

## Data Flow: Admin Query

```
1. ADMIN TYPES QUERY
   "What was our Q4 revenue?"
   │
   ▼
2. AUTHENTICATION CHECK
   Role: "admin" (authenticated)
   │
   ▼
3. QUERY EMBEDDING
   Convert text → 384-dim vector
   │
   ▼
4. VECTOR SEARCH (FAISS)
   Search in: vector_db/urban_threadz/
   Filter: NONE (admin sees all docs)
   Retrieve: Top 4 chunks from public + admin docs
   │
   ▼
5. CONTEXT ASSEMBLY
   Chunk 1: "Q4 2026: $350,000" (from tax_documents.txt)
   Chunk 2: "Annual target: $1,175,000" (from internal_policies.txt)
   Chunk 3: "Revenue targets..." (from internal_policies.txt)
   Chunk 4: "Total Revenue: $1,050,000" (from tax_documents.txt)
   │
   ▼
6. LLM GENERATION
   Answer: "Q4 2026 revenue was $350,000..."
   │
   ▼
7. RESPONSE
   Display in chat (admin-only data)
```

---

## Data Flow: Document Upload (Admin)

```
1. ADMIN UPLOADS FILE
   File: "new_policy.pdf"
   │
   ▼
2. AUTHENTICATION CHECK
   Role: "admin" ✓
   Package: "standard" or "premium" ✓
   │
   ▼
3. FILE VALIDATION
   Extension: .pdf ✓
   Max docs: 3 (standard) ✓
   │
   ▼
4. LOAD DOCUMENT
   PyMuPDFLoader → Extract text
   │
   ▼
5. ADD METADATA
   {
     "business_id": "urban_threadz",
     "access": "admin",
     "source": "new_policy.pdf"
   }
   │
   ▼
6. CHUNK TEXT
   Split into 800-char chunks
   Overlap: 150 chars
   │
   ▼
7. GENERATE EMBEDDINGS
   Each chunk → 384-dim vector
   │
   ▼
8. UPDATE VECTOR DB
   Load existing: vector_db/urban_threadz/
   Add new chunks
   Save updated index
   │
   ▼
9. CONFIRMATION
   "1 document(s) ingested successfully."
```

---

## Access Control Matrix

| User Role | Public Docs | Admin Docs | Upload Docs |
|-----------|-------------|------------|-------------|
| **user**  | ✅ Read     | ❌ No access | ❌ No       |
| **admin** | ✅ Read     | ✅ Read      | ✅ Yes      |

**Implementation**:
- User role → Filter: `{"access": "public"}`
- Admin role → No filter (sees all)

---

## Package Tier Features

| Feature | Basic | Standard | Premium |
|---------|-------|----------|---------|
| **Max Documents** | 1 | 3 | Unlimited |
| **Authentication** | ❌ | ✅ | ✅ |
| **Admin Upload** | ❌ | ✅ | ✅ |
| **API Access** | ❌ | ❌ | ✅ |

**Configuration**: `app/config.py` → `PACKAGE_TYPE`

---

## Technology Stack

### Frontend
- **Streamlit** - Web UI framework
- **Python 3.9+** - Runtime

### Backend
- **LangChain** - RAG orchestration
- **FAISS** - Vector database (CPU version)
- **Sentence Transformers** - Embeddings
- **Groq** - LLM API (primary)
- **Google Gemini** - LLM API (fallback)

### Document Processing
- **PyMuPDF** - PDF loading
- **Docx2txt** - DOCX loading
- **TextLoader** - TXT loading

### Deployment
- **Docker** - Containerization
- **Streamlit Cloud** - Free hosting
- **Git** - Version control

---

## File Structure Explained

```
rag-business-chatbot/
│
├── app/                      # Frontend & application logic
│   ├── main.py              # Entry point, orchestrates everything
│   ├── auth.py              # Login logic (user/admin)
│   ├── ui.py                # Chat interface components
│   └── config.py            # Settings (API keys, package tier)
│
├── rag/                      # RAG pipeline components
│   ├── chain.py             # Combines retriever + LLM
│   ├── retriever.py         # Vector search with access control
│   ├── prompts.py           # LLM prompt templates
│   └── llm_factory.py       # LLM provider selection (Groq/Gemini)
│
├── ingestion/                # Document processing pipeline
│   ├── loader.py            # Load PDF/DOCX/TXT files
│   ├── chunker.py           # Split text into chunks
│   ├── embedder.py          # Generate embeddings
│   └── ingest.py            # Main ingestion script
│
├── businesses/               # Multi-tenant business data
│   └── urban_threadz/       # Example business
│       ├── public_docs/     # User-accessible documents
│       ├── admin_docs/      # Admin-only documents
│       └── business.json    # Business metadata
│
├── vector_db/                # FAISS vector stores
│   └── urban_threadz/       # One DB per business
│       ├── index.faiss      # Vector embeddings
│       └── index.pkl        # Metadata
│
├── utils/                    # Utility functions
│   ├── error_handler.py     # Error logging
│   └── file_utils.py        # File validation
│
├── .env                      # API keys (not in git)
├── .env.example             # Template for .env
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker orchestration
├── setup.sh                 # One-command setup script
└── main.py                  # App entry point
```

---

## Security Architecture

### Authentication
- Simple password-based auth for demo
- Admin password stored in `.env`
- Session-based role tracking

### Access Control
- Document-level access via metadata
- Filter applied at retrieval time
- Users can't access admin documents

### Data Protection
- `.env` in `.gitignore` (never committed)
- API keys stored as environment variables
- No sensitive data in code

### Future Enhancements
- OAuth integration (Google, Microsoft)
- JWT tokens for API access
- Role-based permissions (viewer, editor, admin)
- Audit logging

---

## Scalability Considerations

### Current Limits
- FAISS (CPU): ~1M vectors per business
- Streamlit: Single-threaded
- Free APIs: 14,400 requests/day (Groq)

### Scaling Strategies

**Horizontal Scaling** (Multiple Businesses):
- Each business = separate vector DB
- No cross-contamination
- Easy to add new clients

**Vertical Scaling** (More Documents):
- FAISS can handle millions of vectors
- Chunk size optimization (800 chars)
- Efficient embedding model (MiniLM)

**Performance Optimization**:
- Cache embeddings
- Batch processing for uploads
- Async LLM calls (future)

---

## Cost Analysis

### Free Tier (Current Setup)
- **Groq**: 14,400 requests/day = FREE
- **Streamlit Cloud**: 1 app = FREE
- **FAISS**: Local storage = FREE
- **Sentence Transformers**: Local model = FREE

**Total monthly cost**: $0 💰

### Paid Tier (If Scaling)
- **Groq Pro**: $0.10/1M tokens
- **Pinecone**: $70/month (managed vector DB)
- **Heroku/Railway**: $5-20/month (hosting)
- **OpenAI**: $0.50/1M tokens (GPT-3.5)

**Estimated cost for 100 clients**: $50-100/month

---

## Monitoring & Debugging

### Logs
- Streamlit console output
- `app.log` (error handler)
- Vector DB load confirmations

### Metrics to Track
- Query response time
- Document retrieval accuracy
- LLM token usage
- Error rates

### Debug Mode
```python
# In rag/retriever.py
print("📂 Loading vector store from:", path)
print("✅ Vector store loaded, doc count:", vs.index.ntotal)
```

---

## Future Enhancements

### Short-term
- [ ] API endpoint for programmatic access
- [ ] Multi-language support
- [ ] Custom branding per business
- [ ] Analytics dashboard

### Medium-term
- [ ] Voice input/output
- [ ] Image document support
- [ ] Conversation memory
- [ ] Export chat history

### Long-term
- [ ] Multi-modal RAG (images + text)
- [ ] Fine-tuned models per business
- [ ] Real-time document sync
- [ ] Mobile app

---

**This architecture is designed for:**
✅ Simplicity (easy to understand)
✅ Reusability (multi-tenant)
✅ Scalability (add clients easily)
✅ Cost-efficiency (free tier)
✅ Maintainability (clear separation of concerns)
