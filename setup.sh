#!/bin/bash

# ===============================
# RAG BUSINESS CHATBOT - SETUP SCRIPT
# ===============================

echo "🚀 Setting up RAG Business Chatbot..."

# Check Python version
echo "📌 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.9+"; exit 1; }

# Install pip if not available
echo "📌 Checking pip..."
python3 -m ensurepip --upgrade 2>/dev/null || echo "pip already installed"

# Upgrade pip
echo "📌 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p vector_db
mkdir -p businesses/urban_threadz/public_docs
mkdir -p businesses/urban_threadz/admin_docs

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ Please edit .env and add your API keys!"
else
    echo "✅ .env file already exists"
fi

# Ingest sample documents
echo "📚 Ingesting sample documents..."
python3 ingestion/ingest.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env and add your GROQ_API_KEY (get it free at https://console.groq.com)"
echo "2. Run: streamlit run main.py"
echo "3. Open browser at: http://localhost:8501"
echo ""
echo "🔐 Default admin password: admin123 (change in .env)"
echo ""
