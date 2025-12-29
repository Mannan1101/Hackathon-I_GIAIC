# Documentation RAG Ingestion Pipeline

Complete pipeline for crawling documentation websites, generating embeddings, and storing them in Qdrant vector database.

## Quick Start

### 1. Prerequisites

- Python 3.11+
- UV package manager ([install instructions](https://github.com/astral-sh/uv))
- Cohere API key ([get it here](https://dashboard.cohere.com/api-keys))
- Qdrant Cloud account ([sign up](https://cloud.qdrant.io))

### 2. Setup

```bash
# Dependencies are already installed
# If needed, reinstall with:
uv sync
```

### 3. Configuration

Create a `.env` file in the `backend/` directory (copy from `.env.example`):

```env
# Target Documentation Site
BASE_URL=https://hackathon-1-eight-pi.vercel.app

# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here
COHERE_MODEL=embed-english-v3.0
COHERE_INPUT_TYPE=search_document

# Qdrant Cloud Configuration
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

### 4. Run the Pipeline

```bash
uv run python main.py
```

## What It Does

The pipeline executes 4 phases:

1. **Content Ingestion**: Crawls sitemap.xml, extracts clean text, chunks content
2. **Embedding Generation**: Generates 1024-dim embeddings using Cohere embed-english-v3.0
3. **Vector Storage**: Stores embeddings in Qdrant with COSINE distance and HNSW indexing
4. **Validation**: Runs test queries to verify search quality

## Expected Output

```
[2025-12-27 15:30:00] INFO - Starting ingestion pipeline (Run ID: ...)
[2025-12-27 15:30:00] INFO - Configuration loaded - Target: https://hackathon-1-eight-pi.vercel.app
[2025-12-27 15:30:00] INFO - [PHASE 1] Content Ingestion - Starting
[2025-12-27 15:30:01] INFO - [CRAWL] Fetching sitemap from ...
[2025-12-27 15:30:02] INFO - [CRAWL] Found 47 URLs in sitemap
...
[2025-12-27 15:33:30] INFO -
============================================
Ingestion Complete!
============================================
Duration: 210s
Pages crawled: 47
Chunks created: 312
Vectors stored: 312
Success rate: 100.0%
============================================
```

## Architecture

- **Single-file implementation**: All logic in `main.py` (852 lines)
- **Async HTTP**: Concurrent crawling using httpx and asyncio
- **Retry logic**: Exponential backoff for all external operations
- **Batch processing**: Efficient embedding generation and vector storage
- **Structured logging**: Progress tracking at each pipeline stage

## Troubleshooting

### "Missing required environment variables"
- Ensure `.env` file exists with all required fields
- Check API keys are valid and active

### "Sitemap not available"
- Verify BASE_URL is accessible
- Check if site has sitemap.xml at `/sitemap.xml`

### "Rate limit exceeded" (Cohere)
- Reduce batch size or add delays between requests
- Upgrade Cohere plan for higher rate limits

### "Connection refused" (Qdrant)
- Verify QDRANT_URL includes protocol (https://) and port (:6333)
- Check Qdrant cluster is active

## Validation

After ingestion, validate the retrieval pipeline with the validation script:

```bash
uv run python retrieve.main.py
```

**What it does**:
- Connects to Qdrant and verifies stored vectors
- Runs 10 test queries to test semantic search quality
- Validates metadata completeness (source URLs, page titles)
- Generates comprehensive validation report

**Expected output**:
```
============================================================
RAG Retrieval Validation Report
============================================================
Run ID: val-2025-12-27-001
Duration: 18.5s

CONNECTION STATUS
============================================================
Status: connected
Collection: documentation
Vector Count: 312
Vector Dimensions: 1024
Distance Metric: COSINE

QUERY METRICS
============================================================
Total Queries: 10
Successful: 10
Failed: 0
Success Rate: 100.0%

RETRIEVAL QUALITY
============================================================
Total Results Retrieved: 50
Avg Similarity Score: 0.732
Avg Query Time: 1.85s

METADATA VALIDATION
============================================================
Metadata Completeness: 100.0%

STATUS
============================================================
✅ All validations passed successfully!
============================================================
```

**Troubleshooting**: See `specs/002-rag-retrieval-validation/quickstart.md` for detailed usage and troubleshooting.

## RAG Agent

After ingestion and validation, use the RAG agent to ask questions about the book content.

### Setup

1. Install OpenAI package:
```bash
uv pip install openai
```

2. Add OpenAI API key to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### Usage

**Single question mode**:
```bash
uv run python agent.py "What are the prerequisites?"
```

**Interactive mode** (multi-turn conversation):
```bash
uv run python agent.py
```

### Features

- **Retrieval-augmented answers**: Agent uses ONLY retrieved book content (no hallucination)
- **Source citations**: Responses include page titles and section references
- **Multi-turn conversations**: Maintains context across follow-up questions
- **Off-topic handling**: Gracefully responds "I don't have information" for unrelated questions

### Example Session

```bash
$ uv run python agent.py

RAG Agent - Ask questions about the book content
Type 'quit' or 'exit' to end the session

You: What are the prerequisites?
[Retrieving information from documentation...]
Agent: According to Chapter 1: Getting Started, the prerequisites include:
- Python 3.11 or higher
- Git installed on your system
- Internet access to download dependencies

(Source: Chapter 1: Getting Started: Prerequisites)

You: How do I install it?
[Retrieving information from documentation...]
Agent: Based on Chapter 2: Installation, the installation process is:
1. Clone the repository: git clone <repo-url>
2. Navigate to the project directory
3. Run the setup script: ./setup.sh

(Source: Chapter 2: Installation)

You: quit
Session ended. Asked 2 questions. Thank you!
```

### Documentation

See full documentation in `specs/003-rag-agent/`:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `data-model.md` - Data structures
- `quickstart.md` - Detailed usage guide
- `tasks.md` - Implementation tasks (27 tasks)

## Next Steps

After successful agent setup:

1. Test with various question types (factual, synthesis, off-topic)
2. Monitor OpenAI API usage and costs
3. Tune retrieval parameters (top_k, similarity_threshold)
4. Integrate with larger application if needed

## Documentation

See full documentation in `specs/001-doc-rag-ingestion/`:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `research.md` - Technical decisions
- `data-model.md` - Data structures
- `quickstart.md` - Detailed setup guide
- `tasks.md` - Implementation tasks (63 tasks)
