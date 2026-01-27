# 🤖 RAG Business Chatbot - Freelance Template

A production-ready RAG (Retrieval-Augmented Generation) chatbot template for business documents. Perfect for freelance gigs - build custom chatbots for clients in minutes!

## 🎯 What This Does

- **For Users**: Ask questions about business products, policies, FAQs
- **For Admins**: Upload private documents (contracts, tax docs, internal policies) and get instant answers
- **For You**: Reusable template to create 10s of chatbots for different clients with minimal changes

## ✨ Features

- ✅ **Multi-tier packages** (Basic, Standard, Premium) - match your Fiverr gig tiers
- ✅ **Role-based access** - Users see public docs, Admins see everything
- ✅ **Document ingestion** - PDF, DOCX, TXT support
- ✅ **Free LLM APIs** - Uses Groq (14,400 free requests/day)
- ✅ **Vector search** - FAISS for fast semantic search
- ✅ **Easy deployment** - Docker, Streamlit Cloud, or local
- ✅ **Reusable template** - Change business name, swap docs, deploy!

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- Free Groq API key ([Get it here](https://console.groq.com/keys))

### Installation

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd rag-business-chatbot

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Add your API key to .env
# Edit .env and replace: GROQ_API_KEY=your_groq_api_key_here

# 4. Run the app
streamlit run main.py
```

Open browser at `http://localhost:8501` 🎉

## 📦 Package Tiers (Match Your Fiverr Gig)

| Feature | Basic ($75) | Standard ($150) | Premium ($250) |
|---------|-------------|-----------------|----------------|
| Document sources | 1 | 3 | Unlimited |
| User authentication | ❌ | ✅ | ✅ |
| Admin document upload | ❌ | ✅ | ✅ |
| API access | ❌ | ❌ | ✅ |

**To change package tier**: Edit `app/config.py` → `PACKAGE_TYPE = "basic"` / `"standard"` / `"premium"`

## 🏢 Creating a New Business Chatbot

### Method 1: Duplicate Existing Business

```bash
# Copy the template
cp -r businesses/urban_threadz businesses/your_client_name

# Update business ID in app/config.py
BUSINESS_ID = "your_client_name"

# Add client documents
# - Public docs → businesses/your_client_name/public_docs/
# - Admin docs → businesses/your_client_name/admin_docs/

# Ingest documents
python3 ingestion/ingest.py

# Run the app
streamlit run main.py
```

### Method 2: From Scratch

1. Create folder: `businesses/client_name/`
2. Add subfolders: `public_docs/`, `admin_docs/`
3. Add documents (PDF, TXT, DOCX)
4. Create `business.json`:

```json
{
  "business_id": "client_name",
  "business_name": "Client Business Name",
  "industry": "Retail",
  "description": "Brief description",
  "tone": "professional, friendly"
}
```

5. Update `app/config.py` → `BUSINESS_ID = "client_name"`
6. Run `python3 ingestion/ingest.py`
7. Launch: `streamlit run main.py`

## 🔧 Configuration

### API Keys (.env)

```bash
# Primary LLM (FREE - 14,400 requests/day)
GROQ_API_KEY=your_groq_api_key_here

# Fallback LLM (Optional)
GOOGLE_API_KEY=your_gemini_api_key_here

# Admin password
ADMIN_PASSWORD=admin123
```

### Business Settings (app/config.py)

```python
BUSINESS_ID = "urban_threadz"  # Change to your client's ID
PACKAGE_TYPE = "standard"       # basic / standard / premium
```

## 📁 Project Structure

```
rag-business-chatbot/
│
├── app/
│   ├── main.py          # Streamlit app entry point
│   ├── auth.py          # User/Admin authentication
│   ├── ui.py            # Chat interface
│   └── config.py        # Configuration settings
│
├── rag/
│   ├── chain.py         # RAG pipeline
│   ├── retriever.py     # Vector search with access control
│   ├── prompts.py       # LLM prompts
│   └── llm_factory.py   # LLM provider selection
│
├── ingestion/
│   ├── loader.py        # Document loaders (PDF, DOCX, TXT)
│   ├── chunker.py       # Text splitting
│   ├── embedder.py      # Sentence embeddings
│   └── ingest.py        # Main ingestion script
│
├── businesses/
│   └── urban_threadz/   # Example business (clothing brand)
│       ├── public_docs/     # User-accessible documents
│       ├── admin_docs/      # Admin-only documents
│       └── business.json    # Business metadata
│
├── vector_db/           # FAISS vector stores (auto-generated)
│
├── .env                 # API keys (create from .env.example)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker deployment
└── docker-compose.yml   # Docker Compose config
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up --build

# Access at http://localhost:8501
```

## ☁️ Streamlit Cloud Deployment

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Set secrets (Settings → Secrets):

```toml
GROQ_API_KEY = "your_key_here"
ADMIN_PASSWORD = "admin123"
```

5. Deploy! Share the URL with your client 🎉

## 🔍 How It Works

### User Flow
1. User opens chatbot → sees public documents only
2. Asks: "What's your return policy?"
3. RAG retrieves relevant chunks from `public_docs/`
4. LLM generates answer based on retrieved context

### Admin Flow
1. Admin logs in with password
2. Uploads private document (e.g., tax_documents.pdf)
3. Document is chunked, embedded, stored in vector DB
4. Admin asks: "What was our Q4 revenue?"
5. RAG retrieves from both `public_docs/` AND `admin_docs/`
6. LLM generates answer with access to private data

### Technical Flow
```
User Query → Embeddings → Vector Search (FAISS) → 
Retrieve Top 4 Chunks → LLM (Groq/Gemini) → Answer
```

## 🛠️ Troubleshooting

### "Vector store not found" error
```bash
# Re-run ingestion
python3 ingestion/ingest.py
```

### "No module named 'langchain_community'" error
```bash
# Reinstall dependencies
python3 -m pip install -r requirements.txt
```

### Chatbot not responding
- Check `.env` has valid `GROQ_API_KEY`
- Check console for errors
- Verify documents exist in `businesses/{BUSINESS_ID}/public_docs/`

### Admin login not working
- Check `ADMIN_PASSWORD` in `.env`
- Verify `PACKAGE_TYPE` is `"standard"` or `"premium"` in `app/config.py`

## 🎨 Customization for Clients

### 1. Branding
Edit `app/ui.py`:
```python
st.title("📦 Your Client's Chatbot Name")
```

### 2. Tone & Style
Edit `rag/prompts.py`:
```python
template="""
You are a helpful assistant for {client_name}.
Use a {tone} tone when responding.
...
"""
```

### 3. Add More Document Types
Edit `ingestion/loader.py` to support CSV, JSON, etc.

## 💰 Monetization Tips (Fiverr/Upwork)

### Gig Pricing Strategy
- **Basic ($75)**: 1 document source, no auth, 2-day delivery
- **Standard ($150)**: 3 sources, auth, custom UI, 3-day delivery
- **Premium ($250)**: Unlimited sources, API, priority support, 5-day delivery

### Upsells
- Custom branding: +$25
- API integration: +$50
- Monthly maintenance: $30/month
- Additional document sources: $20 each

### Portfolio Piece
Use the Urban Threadz demo:
1. Record 30-second video showing it work
2. Upload to YouTube/Loom
3. Add to Fiverr gig gallery
4. Deploy demo to Streamlit Cloud (free)

## 🔐 Security Best Practices

- ✅ Never commit `.env` to Git (already in `.gitignore`)
- ✅ Use strong admin passwords in production
- ✅ Enable HTTPS for production deployments
- ✅ Regularly update dependencies: `pip install --upgrade -r requirements.txt`
- ✅ Limit file upload sizes (already configured in Streamlit)

## 📊 Free API Recommendations

### Primary: Groq (Recommended)
- **Free tier**: 14,400 requests/day
- **Speed**: Very fast (Llama 3 on custom hardware)
- **Signup**: https://console.groq.com
- **No credit card required**

### Fallback: Google Gemini
- **Free tier**: 60 requests/minute
- **Model**: Gemini 1.5 Flash
- **Signup**: https://makersuite.google.com

### Alternative: Hugging Face Inference API
- **Free tier**: Limited
- **Models**: Many open-source options
- **Signup**: https://huggingface.co

## 🤝 Contributing

This is a freelance template - fork it, customize it, sell it! No attribution required.

## 📄 License

MIT License - Use commercially, modify freely, no warranty.

## 🆘 Support

- **Issues**: Open a GitHub issue
- **Questions**: Check troubleshooting section above
- **Freelance help**: Hire me on Fiverr! (Add your link)

---

**Built with**: LangChain, Streamlit, FAISS, Groq, Python

**Perfect for**: Freelancers, agencies, consultants building custom chatbots for clients

**Time to deploy**: 5 minutes ⚡

**Cost**: $0 (using free APIs) 💰
