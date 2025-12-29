# Quickstart Guide: RAG Retrieval Validation

**Feature**: 002-rag-retrieval-validation
**Created**: 2025-12-27
**Purpose**: Quick setup and usage guide for retrieval validation script

---

## Overview

The RAG Retrieval Validation script (`retrieve.main.py`) tests your vector database retrieval pipeline by:
- Connecting to Qdrant and verifying stored embeddings
- Running test queries to retrieve relevant documentation chunks
- Validating metadata completeness and accuracy
- Generating a comprehensive validation report

**Use this when**:
- After completing spec-1 (ingestion pipeline)
- To verify search quality before integrating into applications
- To debug retrieval issues or test configuration changes

---

## Prerequisites

### 1. Completed Spec-1 (Required)

You must have successfully run the ingestion pipeline (spec-1) first:
```bash
# Run from backend/ directory
uv run python main.py
```

**Verify completion**:
- Check output shows: "Ingestion Complete! Vectors stored: XXX"
- Qdrant collection `documentation` exists with vectors

### 2. Environment Setup

Ensure `.env` file exists in `backend/` directory with valid credentials:

```env
# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=documentation

# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here
COHERE_MODEL=embed-english-v3.0
COHERE_INPUT_TYPE=search_query
```

**Important**: `COHERE_INPUT_TYPE` must be `search_query` for retrieval (different from ingestion which uses `search_document`)

### 3. Dependencies Installed

Dependencies from spec-1 are sufficient (already installed):
```bash
# If needed, reinstall with:
uv sync
```

Required packages:
- `qdrant-client>=1.7.0`
- `cohere>=4.40.0`
- `python-dotenv>=1.0.0`
- `tenacity>=8.2.0`

---

## Quick Start

### Run Validation Script

```bash
# From backend/ directory
uv run python retrieve.main.py
```

**Expected Output** (first 30 seconds):
```
[2025-12-27 14:30:00] INFO - Starting RAG Retrieval Validation (Run ID: val-xxx)
[2025-12-27 14:30:00] INFO - Configuration loaded successfully
[2025-12-27 14:30:01] INFO - [CONNECTION] Connecting to Qdrant at https://your-cluster.qdrant.io:6333
[2025-12-27 14:30:02] INFO - [CONNECTION] Successfully connected to collection 'documentation'
[2025-12-27 14:30:02] INFO - [CONNECTION] Collection stats: 312 vectors, 1024 dimensions, COSINE distance
[2025-12-27 14:30:02] INFO - [VALIDATE] Running validation suite with 10 test queries
[2025-12-27 14:30:03] INFO - [QUERY 1/10] "How do I get started?" → 5 results, top score: 0.87
[2025-12-27 14:30:05] INFO - [QUERY 2/10] "What is authentication?" → 5 results, top score: 0.82
...
[2025-12-27 14:30:20] INFO - [VALIDATE] All queries completed successfully
[2025-12-27 14:30:20] INFO -
============================================================
RAG Retrieval Validation Report
============================================================
Run ID: val-2025-12-27-001
Started: 2025-12-27 14:30:00
Completed: 2025-12-27 14:30:20
Duration: 20.0s

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
Avg Query Time: 2.0s

METADATA VALIDATION
============================================================
Metadata Completeness: 100.0%

STATUS
============================================================
✅ All validations passed successfully!
============================================================
```

---

## Interpreting the Validation Report

### Connection Status

```
Status: connected
Collection: documentation
Vector Count: 312
Vector Dimensions: 1024
Distance Metric: COSINE
```

**What to check**:
- ✅ Status: "connected" (if "failed", check .env credentials)
- ✅ Vector Count: >0 (if 0, run main.py first)
- ✅ Vector Dimensions: 1024 (must match Cohere embed-english-v3.0)
- ✅ Distance Metric: COSINE (must match ingestion config)

### Query Metrics

```
Total Queries: 10
Successful: 10
Failed: 0
Success Rate: 100.0%
```

**What to check**:
- ✅ Success Rate: 100% is ideal
- ⚠️ Failed queries >0: Check errors section for details
- ⚠️ Success Rate <80%: May indicate API issues or network problems

### Retrieval Quality

```
Total Results Retrieved: 50
Avg Similarity Score: 0.732
Avg Query Time: 2.0s
```

**What to check**:
- ✅ Avg Similarity Score: >0.7 indicates good retrieval quality (SC-002)
- ⚠️ Avg Score 0.5-0.7: Acceptable but may need tuning
- ❌ Avg Score <0.5: Poor retrieval quality, check:
  - Embedding model consistency (must be embed-english-v3.0)
  - Query relevance to documentation content
  - Collection has sufficient vectors
- ✅ Avg Query Time: <2 seconds per query (SC-004)
- ⚠️ Query Time >2s: Check network latency or Qdrant performance

### Metadata Validation

```
Metadata Completeness: 100.0%
```

**What to check**:
- ✅ 100%: All results have required metadata (SC-003)
- ❌ <100%: Some results missing fields (check errors section)

### Status/Errors

```
✅ All validations passed successfully!
```

or if errors:

```
ERRORS
============================================================
Query 'What is the weather?' failed: Cohere API timeout
Query 'How to cook pasta?' returned 0 results (expected)
```

**What to check**:
- ✅ No errors: Perfect, all validations passed
- ⚠️ Low-scoring queries: Expected for irrelevant queries (e.g., "weather", "pasta")
- ❌ API timeouts: Check Cohere API status or rate limits
- ❌ Connection errors: Check Qdrant accessibility and credentials

---

## Test Queries Explained

The validation script runs 10 predefined queries in 3 categories:

### Category 1: Specific Queries (expect high scores >0.7)
1. "How do I get started with the documentation?"
2. "What is authentication and how does it work?"
3. "How to configure the application settings?"
4. "Explain the API endpoints available"
5. "What are the installation requirements?"

**Purpose**: Verify retrieval of specific documentation topics

### Category 2: Broad Queries (expect moderate scores 0.5-0.7)
6. "Tell me about the main features"
7. "What is this documentation about?"
8. "How does the system work?"

**Purpose**: Test semantic understanding of general questions

### Category 3: Negative Queries (expect low scores <0.5)
9. "What is the weather today?"
10. "How to cook pasta?"

**Purpose**: Verify system doesn't return irrelevant results with high confidence (SC-008)

---

## Troubleshooting

### Error: "Missing required environment variables"

**Symptom**:
```
ValueError: Missing required environment variables: COHERE_API_KEY, QDRANT_API_KEY
```

**Fix**:
1. Check `.env` file exists in `backend/` directory
2. Verify all required fields are present and not empty:
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `QDRANT_COLLECTION_NAME`
   - `COHERE_API_KEY`
3. Ensure no typos in variable names
4. Restart script after updating `.env`

---

### Error: "Collection 'documentation' not found"

**Symptom**:
```
[CONNECTION] Collection 'documentation' does not exist
```

**Fix**:
1. Run ingestion pipeline first: `uv run python main.py`
2. Verify ingestion completed successfully (check for "Ingestion Complete!" message)
3. Check `QDRANT_COLLECTION_NAME` in `.env` matches collection created by main.py
4. Verify Qdrant Cloud console shows collection exists

---

### Error: "Cohere API rate limit exceeded"

**Symptom**:
```
[QUERY 3/10] Failed: cohere.errors.TooManyRequestsError: Rate limit exceeded
```

**Fix**:
1. Wait 60 seconds and retry
2. Check Cohere dashboard for rate limit status
3. Upgrade Cohere plan if hitting limits frequently
4. Reduce number of test queries (edit `TEST_QUERIES` in retrieve.main.py)

---

### Warning: Low Average Similarity Score (<0.5)

**Symptom**:
```
Avg Similarity Score: 0.42
```

**Possible Causes & Fixes**:
1. **Embedding model mismatch**:
   - Verify `COHERE_MODEL=embed-english-v3.0` in .env
   - Check ingestion used same model (check main.py logs)
2. **Query-document mismatch**:
   - Ensure `COHERE_INPUT_TYPE=search_query` for retrieval
   - Ingestion should use `COHERE_INPUT_TYPE=search_document`
3. **Test queries irrelevant to documentation**:
   - Review test queries (lines in retrieve.main.py)
   - Customize queries to match your documentation content
4. **Insufficient vectors**:
   - Check vector count (should be >100 for meaningful results)
   - Re-run ingestion if count is low

---

### Error: "Connection timeout"

**Symptom**:
```
[CONNECTION] Timeout connecting to Qdrant at https://your-cluster.qdrant.io:6333
```

**Fix**:
1. Check internet connection
2. Verify Qdrant cluster is active (check Qdrant Cloud console)
3. Check `QDRANT_URL` format: `https://your-cluster.qdrant.io:6333` (include port)
4. Test connection manually:
   ```python
   from qdrant_client import QdrantClient
   client = QdrantClient(url="YOUR_URL", api_key="YOUR_KEY")
   print(client.get_collections())
   ```

---

### Warning: Metadata Completeness <100%

**Symptom**:
```
Metadata Completeness: 87.5%
ERRORS
============================================================
6 results missing 'section_heading' field
```

**Explanation**:
- Some documentation pages may not have section headings (e.g., single-page docs)
- This is acceptable if only optional fields are missing

**What to check**:
- Required fields (chunk_text, source_url, page_title) should always be present
- Optional fields (section_heading, breadcrumb) may be null
- If required fields missing, re-run ingestion pipeline

---

## Customizing Test Queries

Edit `retrieve.main.py` to customize validation queries:

```python
# Find this section in retrieve.main.py
TEST_QUERIES = [
    "Your custom query 1",
    "Your custom query 2",
    # Add more queries specific to your documentation
]
```

**Best Practices**:
- Include 3-5 specific queries about your documentation topics
- Include 2-3 broad queries to test semantic understanding
- Include 1-2 negative queries to test irrelevant query handling
- Aim for 8-12 total queries (SC-004: 10 queries <20s)

---

## Next Steps

After successful validation:

1. **Integrate Retrieval into Application**:
   - Use `search_similar_chunks()` function as reference
   - Implement query endpoint in your backend
   - Connect to LLM for answer generation

2. **Monitor Retrieval Quality**:
   - Track average similarity scores over time
   - Adjust `top_k` parameter based on use case
   - Set similarity threshold to filter low-quality results

3. **Optimize Performance**:
   - Tune HNSW index parameters if query time >2s
   - Consider caching frequent queries
   - Monitor Cohere API usage and costs

4. **Update Documentation Content**:
   - Re-run ingestion (main.py) when documentation updates
   - Re-run validation to verify search quality
   - Compare validation reports to detect quality changes

---

## Configuration Reference

### Environment Variables (in `.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `QDRANT_URL` | Yes | - | Qdrant cluster URL (include port :6333) |
| `QDRANT_API_KEY` | Yes | - | Qdrant API key from cloud console |
| `QDRANT_COLLECTION_NAME` | Yes | - | Collection name (use "documentation") |
| `COHERE_API_KEY` | Yes | - | Cohere API key from dashboard |
| `COHERE_MODEL` | No | `embed-english-v3.0` | Embedding model (must match ingestion) |
| `COHERE_INPUT_TYPE` | No | `search_query` | Input type for queries |

### Script Configuration (in `retrieve.main.py`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `top_k` | `5` | Number of results per query |
| `similarity_threshold` | `0.0` | Minimum similarity score (0.0 = no filter) |
| `TEST_QUERIES` | 10 queries | List of validation queries |

---

## Success Criteria Checklist

Use this to verify all acceptance criteria (from spec.md):

- [ ] **SC-001**: Connection validation completes <5 seconds
- [ ] **SC-002**: Average similarity score >0.7 for relevant queries
- [ ] **SC-003**: 100% of results have complete metadata (chunk_text, source_url, page_title)
- [ ] **SC-004**: Batch validation of 10 queries completes <20 seconds
- [ ] **SC-005**: Validation report displays all metrics clearly
- [ ] **SC-006**: Source URLs are valid and accessible
- [ ] **SC-007**: Connection failures handled gracefully with clear error messages
- [ ] **SC-008**: Irrelevant queries return low scores (<0.5) or empty results

---

## Example Workflow

### First-Time Setup
```bash
# 1. Ensure ingestion completed
cd backend/
uv run python main.py

# 2. Verify .env has search_query for COHERE_INPUT_TYPE
cat .env | grep COHERE_INPUT_TYPE
# Should show: COHERE_INPUT_TYPE=search_query

# 3. Run validation
uv run python retrieve.main.py

# 4. Review validation report
# Check success rate, avg similarity, metadata completeness
```

### After Documentation Updates
```bash
# 1. Re-run ingestion
uv run python main.py

# 2. Re-run validation
uv run python retrieve.main.py

# 3. Compare reports
# Check if avg similarity score changed
# Verify vector count increased appropriately
```

### Debugging Poor Retrieval Quality
```bash
# 1. Check collection stats
uv run python -c "
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
load_dotenv()
client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
print(client.get_collection('documentation'))
"

# 2. Test single query manually
uv run python -c "
from retrieve.main import embed_query, search_similar_chunks
import cohere, os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
load_dotenv()

cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))
qdrant_client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))

query_vector = embed_query('How do I get started?', cohere_client, 'embed-english-v3.0')
results = search_similar_chunks(qdrant_client, 'documentation', query_vector, top_k=5)

for i, r in enumerate(results, 1):
    print(f'{i}. Score: {r.similarity_score:.3f} | {r.page_title}')
"

# 3. Run validation with verbose logging
LOG_LEVEL=DEBUG uv run python retrieve.main.py
```

---

## Additional Resources

- **Specification**: `specs/002-rag-retrieval-validation/spec.md`
- **Implementation Plan**: `specs/002-rag-retrieval-validation/plan.md`
- **Data Model**: `specs/002-rag-retrieval-validation/data-model.md`
- **Ingestion README**: `backend/README.md`
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Cohere Embed API**: https://docs.cohere.com/reference/embed

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review validation report errors section
3. Verify prerequisites completed successfully
4. Check Qdrant and Cohere service status
5. Review spec.md for expected behavior

---

**Last Updated**: 2025-12-27
**Feature**: 002-rag-retrieval-validation
**Status**: Ready for implementation
