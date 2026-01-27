# 🚀 Quick Start: Create Chatbot for New Client

## 5-Minute Setup for New Business

### Step 1: Duplicate Template (30 seconds)

```bash
# Copy the Urban Threadz template
cp -r businesses/urban_threadz businesses/my_new_client

# Rename folders if needed
cd businesses/my_new_client
```

### Step 2: Add Client Documents (2 minutes)

```bash
# Add public documents (accessible to all users)
# Examples: product catalogs, FAQs, return policies, contact info
cp /path/to/client/public_doc.pdf public_docs/

# Add admin documents (accessible only to business owner)
# Examples: tax docs, contracts, internal policies, financial reports
cp /path/to/client/admin_doc.pdf admin_docs/
```

**Supported formats**: PDF, TXT, DOCX

### Step 3: Update Configuration (1 minute)

Edit `app/config.py`:

```python
# Change this line:
BUSINESS_ID = "my_new_client"  # ← Your client's folder name

# Choose package tier:
PACKAGE_TYPE = "standard"  # basic / standard / premium
```

### Step 4: Update Business Metadata (1 minute)

Edit `businesses/my_new_client/business.json`:

```json
{
  "business_id": "my_new_client",
  "business_name": "My Client's Business Name",
  "industry": "Retail / Healthcare / Finance / etc.",
  "description": "Brief description of the business",
  "tone": "professional, friendly, technical, casual",
  "target_audience": "Who uses this chatbot",
  "contact": {
    "email": "support@client.com",
    "phone": "1-800-XXX-XXXX",
    "address": "123 Main St, City, State"
  }
}
```

### Step 5: Ingest Documents (30 seconds)

```bash
# Run ingestion script
python3 ingestion/ingest.py
```

**Expected output**:
```
Ingesting admin docs...
Ingesting public docs...
✅ Ingestion completed
```

### Step 6: Test Locally (30 seconds)

```bash
# Run the app
streamlit run main.py
```

Open browser at `http://localhost:8501`

**Test queries**:
- "What products/services do you offer?"
- "What's your contact information?"
- "What's your return/refund policy?"

**Test admin access**:
1. Login as admin (password from `.env`)
2. Upload a test document
3. Ask questions about the uploaded document

### Step 7: Deploy to Client (1 minute)

**Option A: Streamlit Cloud (Easiest)**
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect repo
4. Add secrets (GROQ_API_KEY, ADMIN_PASSWORD)
5. Share URL with client

**Option B: Docker**
```bash
docker-compose up --build
```

**Option C: Heroku / Railway / Render**
- Follow platform-specific deployment guides
- Set environment variables
- Deploy!

---

## 📋 Checklist for Each New Client

- [ ] Copy `businesses/urban_threadz` to `businesses/client_name`
- [ ] Add client documents to `public_docs/` and `admin_docs/`
- [ ] Update `BUSINESS_ID` in `app/config.py`
- [ ] Update `business.json` with client info
- [ ] Run `python3 ingestion/ingest.py`
- [ ] Test locally with `streamlit run main.py`
- [ ] Verify user queries work
- [ ] Verify admin login works
- [ ] Deploy to production
- [ ] Share URL + admin password with client
- [ ] Invoice client 💰

---

## 🎨 Optional Customizations

### Change Chatbot Title
Edit `app/ui.py`:
```python
st.title("📦 [Client Name] AI Assistant")
```

### Change Welcome Message
Edit `app/ui.py`:
```python
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "assistant",
        "content": "👋 Welcome to [Client Name]! How can I help you today?"
    }]
```

### Customize Prompt Tone
Edit `rag/prompts.py`:
```python
template="""
You are a helpful AI assistant for [Client Name].
Use a [professional/friendly/technical] tone.
...
"""
```

### Add Logo
Edit `app/ui.py`:
```python
st.image("businesses/client_name/logo.png", width=200)
st.title("Client Name Chatbot")
```

---

## 💰 Pricing Guide

### Basic Package ($75)
- 1 document source
- No authentication
- Public chatbot only
- 2-day delivery

**Setup**: Skip admin_docs, set `PACKAGE_TYPE = "basic"`

### Standard Package ($150)
- Up to 3 document sources
- User + Admin authentication
- Admin can upload documents
- Custom branding
- 3-day delivery

**Setup**: Use both public_docs and admin_docs, set `PACKAGE_TYPE = "standard"`

### Premium Package ($250)
- Unlimited document sources
- User + Admin authentication
- Admin document upload
- Custom branding
- API access (future feature)
- Priority support
- 5-day delivery

**Setup**: Full features, set `PACKAGE_TYPE = "premium"`

---

## 🔄 Managing Multiple Clients

### Recommended Folder Structure

```
rag-business-chatbot/
├── businesses/
│   ├── client1_clothing/
│   ├── client2_restaurant/
│   ├── client3_law_firm/
│   ├── client4_dental/
│   └── client5_gym/
```

### Switching Between Clients

Just change one line in `app/config.py`:

```python
BUSINESS_ID = "client1_clothing"  # Switch to any client
```

### Deploying Multiple Clients

**Option 1: Separate Deployments** (Recommended)
- Create separate GitHub repos for each client
- Deploy each to its own Streamlit Cloud instance
- Each client gets their own URL

**Option 2: Single Deployment with Dropdown**
- Add business selector in UI
- Let users choose which business to chat with
- Good for demo/portfolio

---

## 🛠️ Troubleshooting

### "Vector store not found"
```bash
# Re-run ingestion
python3 ingestion/ingest.py
```

### "No documents found"
- Check files exist in `businesses/{BUSINESS_ID}/public_docs/`
- Verify file extensions: `.pdf`, `.txt`, `.docx`
- Check file permissions (readable)

### Chatbot gives generic answers
- Documents may not be ingested properly
- Check vector_db/{BUSINESS_ID}/ folder exists
- Re-run ingestion script

### Admin can't login
- Check `ADMIN_PASSWORD` in `.env`
- Verify `PACKAGE_TYPE` is `"standard"` or `"premium"`
- Restart Streamlit app

---

## 📊 Time Estimates

| Task | Time |
|------|------|
| Copy template | 30 sec |
| Add documents | 2 min |
| Update config | 1 min |
| Ingest documents | 30 sec |
| Test locally | 1 min |
| Deploy | 2-5 min |
| **Total** | **7-10 min** |

**With practice, you can deploy a new client chatbot in under 10 minutes!**

---

## 🎯 Success Metrics

Track these for each client:

- ✅ Documents ingested successfully
- ✅ User queries return relevant answers
- ✅ Admin login works
- ✅ Admin document upload works
- ✅ Deployed to production
- ✅ Client can access chatbot
- ✅ Client satisfied (5-star review!)
- ✅ Payment received 💰

---

**You're ready to build chatbots for 10s of clients! 🚀**
