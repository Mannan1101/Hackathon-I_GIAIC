# Quickstart Guide: Documentation RAG Ingestion System

**Feature**: 001-doc-rag-ingestion
**Date**: 2025-12-27
**Phase**: 1 - Design & Contracts

This guide provides step-by-step instructions for setting up and running the documentation ingestion pipeline.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Validation](#validation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- **Python**: 3.11 or higher
- **UV**: Modern Python package manager ([install instructions](https://github.com/astral-sh/uv))
- **Cohere API Key**: Sign up at [cohere.com](https://cohere.com) and get API key
- **Qdrant Cloud Account**: Create free account at [cloud.qdrant.io](https://cloud.qdrant.io)

### Optional

- **Git**: For version control
- **VS Code** or preferred IDE with Python support

### System Requirements

- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 1GB free space
- **Network**: Stable internet connection for API calls

---

## Installation

### Step 1: Clone or Navigate to Backend Directory

```bash
cd backend/
```

### Step 2: Initialize UV Project

```bash
# Initialize UV if not already done
uv init

# Install dependencies
uv add httpx beautifulsoup4 cohere qdrant-client python-dotenv tenacity pytest pytest-asyncio
```

**Expected `pyproject.toml` dependencies**:
```toml
[project]
name = "doc-rag-ingestion"
version = "0.1.0"
description = "Documentation RAG ingestion pipeline"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.25.0",
    "beautifulsoup4>=4.12.0",
    "cohere>=4.40.0",
    "qdrant-client>=1.7.0",
    "python-dotenv>=1.0.0",
    "tenacity>=8.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
]
```

### Step 3: Verify Installation

```bash
# Check UV installation
uv --version

# Check Python version
uv run python --version

# List installed packages
uv pip list
```

---

## Configuration

### Step 1: Create Environment File

Create `.env` file in the `backend/` directory:

```bash
# Copy from example
cp .env.example .env
```

### Step 2: Configure Environment Variables

Edit `.env` with your credentials and settings:

```env
# ===========================================
# Documentation Ingestion Pipeline Config
# ===========================================

# Target Documentation Site
BASE_URL=https://hackathon-1-eight-pi.vercel.app

# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here
COHERE_MODEL=embed-english-v3.0
COHERE_INPUT_TYPE=search_document

# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=documentation

# Chunking Configuration
TARGET_CHUNK_SIZE=400
CHUNK_OVERLAP=80
MIN_CHUNK_SIZE=100
MAX_CHUNK_SIZE=512

# Crawling Configuration
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
MAX_RETRIES=3

# Batch Processing
BATCH_SIZE=100

# Logging
LOG_LEVEL=INFO
```

### Step 3: Create `.env.example` Template

Create `.env.example` for documentation (without actual credentials):

```env
# ===========================================
# Documentation Ingestion Pipeline Config
# ===========================================

# Target Documentation Site
BASE_URL=https://your-documentation-site.com

# Cohere API Configuration
# Get API key from: https://dashboard.cohere.com/api-keys
COHERE_API_KEY=your_cohere_api_key_here
COHERE_MODEL=embed-english-v3.0
COHERE_INPUT_TYPE=search_document

# Qdrant Cloud Configuration
# Create account at: https://cloud.qdrant.io
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=documentation

# Chunking Configuration (tokens)
TARGET_CHUNK_SIZE=400
CHUNK_OVERLAP=80
MIN_CHUNK_SIZE=100
MAX_CHUNK_SIZE=512

# Crawling Configuration
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
MAX_RETRIES=3

# Batch Processing
BATCH_SIZE=100

# Logging
LOG_LEVEL=INFO
```

### Configuration Parameters Explained

| Parameter | Default | Description |
|-----------|---------|-------------|
| `BASE_URL` | - | Documentation website base URL (required) |
| `COHERE_API_KEY` | - | Cohere API key (required) |
| `COHERE_MODEL` | `embed-english-v3.0` | Embedding model name |
| `COHERE_INPUT_TYPE` | `search_document` | Embedding input type |
| `QDRANT_URL` | - | Qdrant cluster URL (required) |
| `QDRANT_API_KEY` | - | Qdrant API key (required) |
| `QDRANT_COLLECTION_NAME` | `documentation` | Collection name in Qdrant |
| `TARGET_CHUNK_SIZE` | `400` | Target chunk size in tokens |
| `CHUNK_OVERLAP` | `80` | Overlap between chunks (tokens) |
| `MIN_CHUNK_SIZE` | `100` | Minimum chunk size (tokens) |
| `MAX_CHUNK_SIZE` | `512` | Maximum chunk size (tokens) |
| `MAX_CONCURRENT_REQUESTS` | `10` | Concurrent HTTP requests during crawl |
| `REQUEST_TIMEOUT` | `30` | HTTP request timeout (seconds) |
| `MAX_RETRIES` | `3` | Maximum retry attempts for failures |
| `BATCH_SIZE` | `100` | Vectors per batch upload to Qdrant |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

---

## Usage

### Basic Usage

Run the complete ingestion pipeline:

```bash
# Using UV
uv run python main.py

# Or activate UV environment and run
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

### Expected Output

```
[2025-12-27 10:30:00] INFO - Starting ingestion pipeline
[2025-12-27 10:30:00] INFO - Run ID: 550e8400-e29b-41d4-a716-446655440000
[2025-12-27 10:30:00] INFO - Base URL: https://hackathon-1-eight-pi.vercel.app

[2025-12-27 10:30:01] INFO - [CRAWL] Fetching sitemap.xml...
[2025-12-27 10:30:02] INFO - [CRAWL] Found 47 URLs in sitemap
[2025-12-27 10:30:02] INFO - [CRAWL] Starting concurrent crawl (max 10 requests)...
[2025-12-27 10:30:15] INFO - [CRAWL] Completed: 47 pages (0 failures)

[2025-12-27 10:30:15] INFO - [CHUNK] Processing 47 pages...
[2025-12-27 10:30:18] INFO - [CHUNK] Created 312 chunks

[2025-12-27 10:30:18] INFO - [EMBED] Generating embeddings (batch size: 10)...
[2025-12-27 10:31:23] INFO - [EMBED] Progress: 100/312 chunks (32%)
[2025-12-27 10:32:28] INFO - [EMBED] Progress: 200/312 chunks (64%)
[2025-12-27 10:33:15] INFO - [EMBED] Completed: 312 embeddings

[2025-12-27 10:33:15] INFO - [STORE] Uploading to Qdrant (batch size: 100)...
[2025-12-27 10:33:18] INFO - [STORE] Batch 1/4 uploaded
[2025-12-27 10:33:21] INFO - [STORE] Batch 2/4 uploaded
[2025-12-27 10:33:24] INFO - [STORE] Batch 3/4 uploaded
[2025-12-27 10:33:26] INFO - [STORE] Batch 4/4 uploaded
[2025-12-27 10:33:26] INFO - [STORE] Completed: 312 vectors stored

[2025-12-27 10:33:26] INFO - [VALIDATE] Running test queries...
[2025-12-27 10:33:28] INFO - [VALIDATE] Query 1: "authentication" - Top result: API Reference > Auth
[2025-12-27 10:33:29] INFO - [VALIDATE] Query 2: "getting started" - Top result: Introduction
[2025-12-27 10:33:30] INFO - [VALIDATE] Query 3: "configuration" - Top result: Setup > Config
[2025-12-27 10:33:30] INFO - [VALIDATE] Validation: 3/3 queries successful (100%)

[2025-12-27 10:33:30] INFO - ============================================
[2025-12-27 10:33:30] INFO - Ingestion Complete!
[2025-12-27 10:33:30] INFO - ============================================
[2025-12-27 10:33:30] INFO - Duration: 3m 30s
[2025-12-27 10:33:30] INFO - Pages crawled: 47
[2025-12-27 10:33:30] INFO - Chunks created: 312
[2025-12-27 10:33:30] INFO - Vectors stored: 312
[2025-12-27 10:33:30] INFO - Success rate: 100%
[2025-12-27 10:33:30] INFO - ============================================
```

### Advanced Usage

**Specify custom base URL**:
```bash
uv run python main.py --base-url https://custom-docs-site.com
```

**Enable debug logging**:
```bash
uv run python main.py --log-level DEBUG
```

**Skip validation**:
```bash
uv run python main.py --skip-validation
```

**Dry run (crawl only, don't store)**:
```bash
uv run python main.py --dry-run
```

---

## Validation

### Test Queries

After ingestion completes, test the vector search:

```python
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Search for "authentication"
results = client.query(
    collection_name="documentation",
    query_text="How do I authenticate API requests?",
    limit=5
)

# Print results
for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Title: {result.payload['page_title']}")
    print(f"Section: {result.payload['section_heading']}")
    print(f"Text: {result.payload['chunk_text'][:200]}...")
    print("-" * 80)
```

### Expected Search Results

For query: "How do I authenticate API requests?"

```
Score: 0.887
Title: API Reference - Authentication
Section: Authentication Methods
Text: To authenticate API requests, include your API key in the Authorization header using the Bearer scheme. The API key can be obtained from your account settings...
--------------------------------------------------------------------------------

Score: 0.845
Title: Getting Started - Setup
Section: API Configuration
Text: Before making API calls, you'll need to configure authentication. Generate an API key from the dashboard and add it to your environment variables...
--------------------------------------------------------------------------------
```

### Validation Checklist

- [ ] All URLs from sitemap.xml were crawled
- [ ] No HTTP errors during crawling
- [ ] Chunks created are within size limits (100-512 tokens)
- [ ] All chunks received embeddings
- [ ] All embeddings stored successfully in Qdrant
- [ ] Test queries return relevant results (top 5)
- [ ] No errors in logs (only INFO/WARNING acceptable)

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'cohere'"

**Cause**: Dependencies not installed

**Solution**:
```bash
uv sync
# or
uv add cohere qdrant-client httpx beautifulsoup4 python-dotenv tenacity
```

---

#### 2. "401 Unauthorized" from Cohere API

**Cause**: Invalid or missing API key

**Solution**:
1. Verify API key in `.env` file
2. Check key is active at https://dashboard.cohere.com/api-keys
3. Ensure no extra spaces or quotes around key in `.env`

---

#### 3. "Connection refused" to Qdrant

**Cause**: Incorrect Qdrant URL or API key

**Solution**:
1. Verify `QDRANT_URL` includes protocol (https://) and port (:6333)
2. Check Qdrant cluster is active in cloud console
3. Verify API key has write permissions

---

#### 4. "Rate limit exceeded" from Cohere

**Cause**: Too many API requests too quickly

**Solution**:
1. Reduce `BATCH_SIZE` in `.env` (try 50 instead of 100)
2. Add delay between batches (modify code to add `time.sleep(1)`)
3. Upgrade Cohere plan for higher rate limits

---

#### 5. Chunks not created / "No main content found"

**Cause**: Docusaurus HTML structure doesn't match selectors

**Solution**:
1. Enable DEBUG logging: `LOG_LEVEL=DEBUG` in `.env`
2. Inspect HTML structure of target site
3. Update `CONTENT_SELECTORS` in `main.py` if needed
4. Check if site requires JavaScript rendering (not supported - needs static HTML)

---

#### 6. "Chunk size out of range" error

**Cause**: Chunking parameters don't match content

**Solution**:
1. Adjust `TARGET_CHUNK_SIZE` in `.env` (try 300 or 500)
2. Verify `MIN_CHUNK_SIZE` < `TARGET_CHUNK_SIZE` < `MAX_CHUNK_SIZE`
3. Check that content has enough text (pages with only images won't chunk well)

---

#### 7. Very slow ingestion (>30 min for 500 pages)

**Cause**: Network latency or conservative concurrency settings

**Solution**:
1. Increase `MAX_CONCURRENT_REQUESTS` to 20 (if network is stable)
2. Increase `BATCH_SIZE` to 200 for Qdrant uploads
3. Check network connection speed
4. Run from server closer to APIs (Cohere, Qdrant)

---

### Debug Mode

Enable debug mode for detailed logging:

```bash
# In .env
LOG_LEVEL=DEBUG

# Run with verbose output
uv run python main.py 2>&1 | tee ingestion.log
```

This will create `ingestion.log` with full details for troubleshooting.

---

### Getting Help

**Error Messages**:
- Check error message in console output
- Search error in [Cohere docs](https://docs.cohere.com) or [Qdrant docs](https://qdrant.tech/documentation)

**Logs**:
- Review logs for specific stage where failure occurred (CRAWL, CHUNK, EMBED, STORE)
- Look for HTTP status codes, API errors, or validation failures

**Common Solutions**:
1. Verify all credentials in `.env`
2. Check network connectivity
3. Ensure API rate limits not exceeded
4. Validate target URL is accessible

---

## Next Steps

After successful ingestion:

1. **Test Search Quality**: Run validation queries and check relevance
2. **Tune Parameters**: Adjust chunk size or overlap based on results
3. **Monitor Usage**: Check Cohere API usage and Qdrant storage
4. **Incremental Updates**: Plan strategy for updating docs (re-run full ingestion or detect changes)
5. **Integration**: Connect to RAG application (retrieval, ranking, generation)

---

## Appendix: File Structure

After setup, your directory should look like:

```
backend/
├── main.py                 # Main ingestion script
├── .env                    # Environment variables (do not commit)
├── .env.example            # Template for environment variables
├── pyproject.toml          # UV project configuration
├── uv.lock                 # UV lock file
├── .venv/                  # Virtual environment (auto-created by UV)
└── tests/
    ├── test_crawler.py
    ├── test_cleaner.py
    ├── test_chunker.py
    ├── test_embedder.py
    ├── test_storage.py
    └── test_integration.py
```

---

**Quickstart Created**: 2025-12-27
**Ready for Use**: Yes (after implementation)
