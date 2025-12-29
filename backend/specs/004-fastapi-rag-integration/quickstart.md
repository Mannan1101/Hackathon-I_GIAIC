# Quickstart Guide: FastAPI RAG Integration

**Feature**: 004-fastapi-rag-integration
**Date**: 2025-12-28
**Purpose**: Step-by-step guide for developers to set up and run the FastAPI RAG chatbot integration

---

## Overview

This guide walks you through setting up the complete RAG chatbot system:
- **Backend**: FastAPI server (`api.py`) that exposes the RAG agent as a REST API
- **Frontend**: Existing Docusaurus chatbot UI (already implemented)
- **Integration**: End-to-end testing to verify the connection works

**Time to complete**: ~10 minutes

---

## Prerequisites

Before starting, ensure you have:

✅ **Python 3.11+** installed (`python --version`)
✅ **Node.js 18+** installed (`node --version`)
✅ **uv** package manager installed (or pip/poetry)
✅ **Running Qdrant instance** with ingested textbook data (from spec-001)
✅ **Environment variables** configured (see below)

---

## Step 1: Environment Setup

### 1.1 Navigate to Backend Directory

```bash
cd backend
```

### 1.2 Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# OpenRouter API for LLM access
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Qdrant vector database
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=https://your-qdrant-instance.cloud.qdrant.io

# Optional: Model configuration
LLM_MODEL=deepseek/deepseek-r1-0528:free
```

**Where to get these values:**
- **OPENROUTER_API_KEY**: Sign up at [openrouter.ai](https://openrouter.ai/) and create an API key
- **QDRANT_API_KEY** & **QDRANT_URL**: From your Qdrant cloud dashboard or local instance

### 1.3 Install Backend Dependencies

Using **uv** (recommended):

```bash
uv sync
```

Or using **pip**:

```bash
pip install -r requirements.txt
```

**New dependencies added for this feature:**
- `fastapi>=0.115.0` - Web framework
- `uvicorn[standard]>=0.32.0` - ASGI server

---

## Step 2: Verify Existing Components

Before running the API, verify that the RAG agent and retrieval system work:

### 2.1 Test the RAG Agent (Optional Verification)

```bash
uv run python agent.py "What are the prerequisites for this course?"
```

**Expected output:**
```
The prerequisites for this course include: 1) Basic programming skills in Python...
```

If this works, your agent and retrieval pipeline are functional! ✅

### 2.2 Check Vector Database

Verify Qdrant has ingested documents:

```bash
uv run python -c "from retrieve_main import load_config, get_qdrant_client; config = load_config(); client = get_qdrant_client(config); print(f'Collection exists: {client.collection_exists(config[\"qdrant_collection\"])}')"
```

**Expected output:**
```
Collection exists: True
```

---

## Step 3: Start the Backend API

### 3.1 Run the FastAPI Server

```bash
uv run python api.py
```

Or using Uvicorn directly:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Server is now running!** 🚀

### 3.2 Verify API Health

Open a new terminal and test the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "agent": "initialized",
  "vector_db": "connected",
  "timestamp": "2025-12-28T12:00:00Z"
}
```

---

## Step 4: Test the Chat Endpoint

### 4.1 Send a Test Query (Command Line)

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the prerequisites for this course?"}'
```

**Expected response:**
```json
{
  "answer": "The prerequisites for this course include: 1) Basic programming skills in Python, 2) Linear algebra and calculus fundamentals, 3) Understanding of probability and statistics. No prior robotics experience is required."
}
```

### 4.2 Test Error Handling

**Empty question (should fail):**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": ""}'
```

**Expected response (HTTP 422):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "question"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

---

## Step 5: Explore API Documentation

FastAPI automatically generates interactive API documentation!

### 5.1 Open Swagger UI

Visit: **http://127.0.0.1:8000/docs**

You'll see:
- All available endpoints (`/chat`, `/health`)
- Request/response schemas
- Interactive "Try it out" functionality

### 5.2 Test via Swagger UI

1. Click on **POST /chat**
2. Click **"Try it out"**
3. Enter a question in the request body:
   ```json
   {
     "question": "Explain physical AI"
   }
   ```
4. Click **"Execute"**
5. See the response below!

### 5.3 Alternative: ReDoc Documentation

Visit: **http://127.0.0.1:8000/redoc**

This provides a cleaner, read-only view of the API documentation.

---

## Step 6: Start the Frontend (Docusaurus)

### 6.1 Navigate to Project Root

```bash
cd ..  # Go back to project root (hackathon_1-main/)
```

### 6.2 Install Frontend Dependencies

```bash
npm install
```

### 6.3 Start Docusaurus

```bash
npm start
```

**Expected output:**
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at http://localhost:3000/
```

**Frontend is now running!** 🎉

---

## Step 7: Test End-to-End Integration

### 7.1 Open the Textbook

Visit: **http://localhost:3000**

You should see the Physical AI & Humanoid Robotics textbook homepage.

### 7.2 Open the Chatbot

Look for the **💬 chat icon** in the bottom-right corner of the page.

Click it to open the chatbot interface.

### 7.3 Ask a Question

1. Type a question in the chatbot: `"What are the prerequisites?"`
2. Press **Send**
3. Wait a few seconds for the response

**Expected behavior:**
- User message appears: `"You: What are the prerequisites?"`
- Bot response appears: `"Bot: The prerequisites for this course include..."`

### 7.4 Verify the Integration

The chatbot should:
- ✅ Send questions to `http://127.0.0.1:8000/chat`
- ✅ Receive answers from the RAG agent
- ✅ Display answers in the chat interface
- ✅ Handle errors gracefully (e.g., if backend is down)

---

## Step 8: Development Workflow

### 8.1 Hot Reload

**Backend**: Uvicorn's `--reload` flag automatically reloads when you edit `api.py` or `agent.py`

**Frontend**: Docusaurus auto-reloads when you edit React components

### 8.2 Monitoring Logs

**Backend logs** (in terminal running `api.py`):
```
INFO:     127.0.0.1:63421 - "POST /chat HTTP/1.1" 200 OK
```

**Frontend logs** (in terminal running `npm start`):
```
[SUCCESS] Client bundle compiled successfully
```

### 8.3 Stopping Services

**Stop Backend**: Press `Ctrl+C` in the terminal running `api.py`

**Stop Frontend**: Press `Ctrl+C` in the terminal running `npm start`

---

## Troubleshooting

### Issue: "Backend not reachable" message in chatbot

**Possible causes:**
1. Backend server not running
2. CORS misconfiguration
3. Wrong port (frontend expects 8000)

**Solution:**
```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Check backend logs for CORS errors
# Ensure CORS middleware is configured for http://localhost:3000
```

---

### Issue: "Connection refused" to Qdrant

**Possible causes:**
1. Qdrant instance not running
2. Wrong `QDRANT_URL` in `.env`
3. Invalid `QDRANT_API_KEY`

**Solution:**
```bash
# Verify Qdrant connection
curl -H "api-key: $QDRANT_API_KEY" $QDRANT_URL/collections

# Check .env file values
cat .env | grep QDRANT
```

---

### Issue: Agent returns empty answers

**Possible causes:**
1. Vector database is empty (no documents ingested)
2. Query doesn't match any chunks
3. LLM API key is invalid

**Solution:**
```bash
# Verify documents are ingested (from spec-001)
uv run python main.py  # Re-run ingestion if needed

# Test retrieval directly
uv run python retrieve_main.py "What is physical AI?"

# Verify OpenRouter API key
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models
```

---

### Issue: Slow response times (> 10 seconds)

**Possible causes:**
1. Large number of chunks being retrieved
2. Slow LLM model
3. Network latency to Qdrant/OpenRouter

**Solution:**
```bash
# Check retrieval time in agent logs
# Consider reducing top_k parameter in retrieve_main.py
# Try a faster LLM model (e.g., gpt-3.5-turbo)
```

---

### Issue: CORS errors in browser console

**Symptoms:**
```
Access to fetch at 'http://127.0.0.1:8000/chat' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Solution:**

Ensure `api.py` has CORS middleware configured:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

---

## Next Steps

### Run Tests

```bash
cd backend
pytest tests/test_api.py -v
pytest tests/test_integration.py -v
```

### Explore Advanced Features

- Add source citations to responses (modify `ChatResponse` in `api.py`)
- Implement conversation history (add session management)
- Add response caching (use Redis or in-memory cache)
- Deploy to production (configure Uvicorn for production mode)

### Contribute

- Report issues or suggest improvements
- Extend the chatbot UI with new features
- Optimize retrieval and generation performance

---

## Summary

You've successfully set up the complete RAG chatbot integration! 🎉

**What you've done:**
1. ✅ Configured environment variables
2. ✅ Installed backend and frontend dependencies
3. ✅ Started the FastAPI server
4. ✅ Started the Docusaurus frontend
5. ✅ Tested the end-to-end integration
6. ✅ Verified the chatbot works on the textbook site

**Key URLs:**
- **API Server**: http://127.0.0.1:8000
- **API Docs (Swagger)**: http://127.0.0.1:8000/docs
- **API Docs (ReDoc)**: http://127.0.0.1:8000/redoc
- **Frontend**: http://localhost:3000

**Development Commands:**
```bash
# Backend
cd backend
uv run python api.py

# Frontend
cd ..
npm start

# Run tests
cd backend
pytest -v
```

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Docusaurus Documentation**: https://docusaurus.io/
- **OpenAI Agents SDK**: https://github.com/openai/agents-sdk
- **Qdrant Documentation**: https://qdrant.tech/documentation/

**Need help?** Check the troubleshooting section or consult the API documentation at http://127.0.0.1:8000/docs.
