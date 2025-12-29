# Research: Documentation RAG Ingestion System

**Feature**: 001-doc-rag-ingestion
**Date**: 2025-12-27
**Phase**: 0 - Research & Technology Decisions

This document consolidates research findings from Phase 0 to resolve all technical unknowns identified in [plan.md](plan.md).

---

## Table of Contents

1. [Cohere Embedding Model Selection](#1-cohere-embedding-model-selection)
2. [Web Crawling Strategy for Docusaurus](#2-web-crawling-strategy-for-docusaurus)
3. [Text Chunking Strategy](#3-text-chunking-strategy)
4. [Qdrant Configuration](#4-qdrant-configuration)
5. [Summary of All Decisions](#summary-of-all-decisions)

---

## 1. Cohere Embedding Model Selection

### Decision: `embed-english-v3.0`

### Model Specifications
- **Vector Dimensions**: 1024 (standard), 384 (light version available)
- **Context Length**: 512 tokens maximum
- **Input Types**: `search_document`, `search_query`, `classification`, `clustering`
- **Distance Metric**: Cosine similarity (vectors are L2-normalized)

### Rationale
1. **Language Optimization**: Exclusively optimized for English text, providing better semantic understanding than multilingual variants for English-only documentation
2. **Adequate Dimensions**: 1024 dimensions provide rich semantic representation while balancing storage and compute costs
3. **Context Window**: 512 tokens accommodates properly chunked documentation (300-400 token chunks with headroom)
4. **Input Type Strategy**: Use `search_document` when embedding chunks, `search_query` when embedding user queries to optimize embedding space for retrieval

### API Considerations
- **Pricing**: Approximately $0.10 per million tokens (verify current rates with Cohere)
- **Rate Limits**: Tier-dependent (typically 100 req/min for trial accounts)
- **Batch Processing**: Support for 10-96 documents per request
- **Retry Strategy**: Implement exponential backoff for rate limit handling

### Alternatives Considered
- **embed-multilingual-v3.0**: Rejected - unnecessary multilingual capability for English-only docs
- **embed-english-light-v3.0** (384 dims): Rejected - prioritizing quality over storage savings

### Implementation Notes
```python
# Pseudo-code for embedding generation
response = cohere.embed(
    texts=["documentation chunk text"],
    model="embed-english-v3.0",
    input_type="search_document",
    embedding_types=["float"]
)
```

---

## 2. Web Crawling Strategy for Docusaurus

### Decision: Sitemap-First with Recursive Fallback

### Approach

**Primary Method: Sitemap.xml Parsing**
- Docusaurus generates `/sitemap.xml` automatically via `@docusaurus/plugin-sitemap`
- Enabled by default in Docusaurus preset-classic (no configuration needed)
- Provides complete, authoritative list of all public URLs
- 10-20x faster than recursive crawling

**Fallback Method: Recursive Link Following**
- Only if sitemap.xml returns 404 or is unavailable
- Maximum depth: 5-7 levels to prevent infinite loops
- Start from base URL and follow internal links

### URL Normalization Rules

```python
# Include patterns (primary documentation)
include_patterns = [
    r'^/docs/',           # Main documentation
    r'^/blog/',           # Blog posts (if needed)
    r'^/tutorial/',       # Tutorials
    r'^/guides/',         # Guides
]

# Exclude patterns (non-content pages)
exclude_patterns = [
    r'/tags/',            # Tag listing pages
    r'/page/\d+',         # Pagination pages
    r'/search',           # Search page
    r'/404',              # Error pages
]

# Normalization
# 1. Remove trailing slashes: /docs/intro/ → /docs/intro
# 2. Remove anchors: /docs/intro#setup → /docs/intro
# 3. Remove query params: /docs/intro?v=1 → /docs/intro
# 4. Lowercase domain, preserve path case
```

### Content Extraction - Docusaurus-Specific Selectors

**Main Content Selectors (Priority Order)**:
```python
CONTENT_SELECTORS = [
    'article',                      # Docusaurus v2+ primary article wrapper
    'main[role="main"]',            # Docusaurus v2+ main content
    '[class*="docItemContainer"]',  # Docusaurus specific doc container
    '[class*="docMainContainer"]',  # Docusaurus main container
    '.markdown',                    # Markdown content wrapper
    '[class*="theme-doc-markdown"]', # Theme markdown wrapper (v2+)
]
```

**Elements to Remove**:
```python
REMOVE_SELECTORS = [
    'nav', 'header', 'footer',                # Navigation structure
    '[class*="navbar"]', '[class*="sidebar"]', # Docusaurus navigation
    '[class*="pagination"]',                   # Pagination controls
    '[class*="tocCollapsible"]',              # Table of contents (duplicate)
    '[class*="tableOfContents"]',             # TOC variations
    '[class*="breadcrumbs"]',                 # Breadcrumb navigation
    '[class*="editThisPage"]',                # Edit page links
    '[class*="lastUpdated"]',                 # Last updated metadata
    '[class*="tags"]',                        # Tag lists
    'button', '[role="button"]',              # Interactive buttons
    '[aria-hidden="true"]',                   # Hidden elements
    '.hash-link',                             # Heading anchor links
    'script', 'style', 'iframe',              # Non-content elements
]
```

### Deduplication Strategy

**Three-Tier Approach**:
1. **URL-Based** (during crawling): Normalize and track seen URLs in set
2. **Content Hash** (after extraction): SHA256 hash of cleaned text to catch duplicate content with different URLs
3. **Chunk-Level** (during storage): Store chunk hashes in Qdrant metadata for incremental updates

### Metadata Extraction

```python
metadata = {
    'source_url': url,
    'title': '<og:title> or <title> or <h1>',
    'description': '<og:description> or <meta name="description">',
    'last_modified': '<meta name="docusaurus_last_update">',
    'crawled_at': datetime.utcnow().isoformat(),
}
```

### Rationale
- **Sitemap reliability**: Docusaurus maintains accurate sitemap, eliminating complex graph traversal
- **Performance**: Single XML file vs hundreds of HTTP requests
- **Canonical URLs**: Sitemap provides authoritative URLs, reducing deduplication complexity
- **Structure awareness**: Docusaurus-specific selectors ensure high-quality content extraction (90%+ non-content removal)

---

## 3. Text Chunking Strategy

### Decision: Hybrid Markdown-Aware Recursive Chunking

### Configuration Parameters

```python
CHUNKING_CONFIG = {
    # Size parameters (in tokens)
    "target_chunk_size": 400,      # Optimal balance of context and precision
    "min_chunk_size": 100,         # Minimum meaningful chunk
    "max_chunk_size": 512,         # Cohere model limit

    # Overlap strategy
    "overlap_tokens": 80,          # 20% overlap (80 tokens for 400-token chunks)
    "overlap_sentences": 1,        # Minimum 1 complete sentence overlap

    # Special content handling
    "preserve_code_blocks": True,
    "max_code_block_tokens": 512,
    "include_parent_heading": True,
    "heading_hierarchy_depth": 3,  # H1 > H2 > H3

    # Quality controls
    "min_meaningful_words": 20,    # Skip chunks with fewer words
}
```

### Chunking Algorithm

1. **Parse Document Structure**: Identify headings, code blocks, lists, tables
2. **Split by Sections**: Respect heading hierarchy (H1, H2, H3)
3. **Recursive Split Within Sections** (if section exceeds target size):
   - First: Split on paragraph boundaries (`\n\n`)
   - Then: Split on sentence boundaries (`. `, `! `, `? `)
   - Finally: Split on word boundaries (` `)
4. **Preserve Special Content**: Keep code blocks, tables, lists intact
5. **Add Overlap**: 20% token overlap (80 tokens) between consecutive chunks

### Handling Special Content

**Code Blocks**:
- Keep entire code blocks together when possible
- If exceeds chunk size, split on function/class boundaries
- Include surrounding context (preceding explanation text)

**Lists**:
- Keep list items with parent list context
- Split long lists between items, never mid-item
- Include list header/introduction

**Tables**:
- Keep small tables intact
- For large tables: include headers with each chunk of rows
- Consider converting to structured text for better embedding

**Headings**:
- Include section heading with its content
- Propagate parent headings (breadcrumb context)
- Example: "Configuration > Environment Variables > API Keys"

### Metadata per Chunk

```python
chunk_metadata = {
    "source_url": str,
    "page_title": str,
    "section_heading": str,
    "heading_hierarchy": List[str],  # Breadcrumb
    "chunk_index": int,              # Position within page (0-indexed)
    "total_chunks": int,             # Total from this page
    "char_count": int,
    "token_count": int,
    "content_type": str,             # "text", "code", "list", "table"
    "timestamp": str,                # ISO 8601
    "has_code": bool,
    "prev_chunk_id": Optional[str],  # For context continuity
    "next_chunk_id": Optional[str],
}
```

### Expected Outcomes
- **Chunks per page**: 5-15 for typical documentation
- **Storage efficiency**: ~70% reduction vs full pages
- **Retrieval quality**: High precision due to semantic coherence
- **Context preservation**: 20% overlap ensures no information loss

### Rationale
- **400-token target**: Balances context (for LLM answers) and precision (for retrieval)
- **20% overlap**: Prevents boundary information loss without excessive duplication
- **Structure awareness**: Respects markdown/HTML structure to preserve semantic meaning
- **Metadata-rich**: Enables better retrieval, filtering, and citation

### Implementation Library
**Recommended**: LangChain RecursiveCharacterTextSplitter with custom enhancements

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,        # Characters (≈ 400 tokens)
    chunk_overlap=400,      # Characters (≈ 80 tokens)
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len,
)
```

---

## 4. Qdrant Configuration

### Decision Summary

| Configuration | Value | Rationale |
|--------------|-------|-----------|
| **Distance Metric** | Cosine | Cohere embeddings are normalized; cosine is standard for semantic search |
| **HNSW `m`** | 16 | Optimal balance of speed and accuracy |
| **HNSW `ef_construct`** | 100 | Good build quality without excessive indexing time |
| **HNSW `ef` (search)** | 128 | High recall for documentation retrieval |
| **Storage** | Default (in-memory) | Free tier handles automatically |
| **Batch Size** | 100 vectors | Sweet spot for throughput and error handling |
| **Collection Name** | "documentation" | Single collection for all docs |
| **Point ID Strategy** | UUID v4 | Ensures uniqueness across ingestion runs |

### Distance Metric: Cosine Similarity

**Why Cosine**:
- Cohere embed-english-v3.0 produces L2-normalized vectors
- Cosine measures angular similarity (direction), not magnitude
- Industry standard for semantic search
- Numerically stable for high-dimensional embeddings

**Alternatives Rejected**:
- **Dot Product**: Equivalent for normalized vectors, but cosine is more explicit
- **Euclidean**: Poor for high dimensions (curse of dimensionality)

### HNSW Index Parameters

**What is HNSW**: Hierarchical Navigable Small World - Qdrant's approximate nearest neighbor search algorithm

**`m=16`** (Number of bi-directional links per node):
- Default and optimal for moderate scale (50K-100K vectors)
- Higher values (32-64) improve recall but double memory usage
- Lower values (4-8) save memory but degrade search quality

**`ef_construct=100`** (Dynamic candidate list size during index building):
- Balances index build time and search quality
- Can increase to 200 if search quality is insufficient
- Higher values slow indexing but improve accuracy

**`ef=128`** (Dynamic candidate list size during search - runtime parameter):
- Higher values improve recall at cost of latency
- For documentation, accuracy > speed, so 128 is appropriate
- Tune based on actual search performance

### Payload Structure

```python
{
    # Source identification
    "source_url": str,
    "page_title": str,

    # Content
    "chunk_text": str,              # Full text for display
    "chunk_index": int,
    "chunk_size": int,

    # Context
    "section_heading": str,
    "breadcrumb": str,              # "Home > API > Auth"

    # Timestamps
    "ingested_at": str,             # ISO 8601
    "content_hash": str,            # SHA256 for dedup

    # Tracking
    "ingestion_run_id": str,        # UUID for batch tracking
    "embedding_model": str,         # "embed-english-v3.0"
}
```

### Batch Upload Strategy

**Batch Size: 100 vectors**

**Why 100**:
- Optimal balance between throughput and error handling
- Small enough to handle network errors gracefully
- Large enough to minimize HTTP request overhead
- Aligns with typical pagination standards

**Implementation Pattern**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

BATCH_SIZE = 100

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def upload_batch(client, collection_name, points):
    client.upsert(collection_name=collection_name, points=points)
```

### Free Tier Capacity Planning

**Qdrant Cloud Free Tier Limits**:
- **Storage**: ~1GB total
- **Collections**: 1-2 collections
- **QPS**: 10-50 queries per second
- **Uptime**: 99% SLA

**Capacity Estimates**:
- **Per Vector**: 1024 dims × 4 bytes (float32) = 4KB
- **With Payload**: ~5-6KB per vector
- **1GB Storage**: ~170,000-200,000 vectors
- **Target (50K chunks)**: ~300MB (30% of free tier) ✅

**Conclusion**: Free tier is more than sufficient for documentation search use case

### Collection Creation Code

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, HnswConfigDiff

client.create_collection(
    collection_name="documentation",
    vectors_config=VectorParams(
        size=1024,  # Cohere embed-english-v3.0
        distance=Distance.COSINE,
        hnsw_config=HnswConfigDiff(
            m=16,
            ef_construct=100,
            full_scan_threshold=10000  # Exact search for <10K vectors
        )
    )
)

# Create payload indexes for filtering
client.create_payload_index(
    collection_name="documentation",
    field_name="source_url",
    field_schema="keyword"
)
```

---

## Summary of All Decisions

### Technology Stack Finalized

| Component | Technology | Specification |
|-----------|-----------|---------------|
| **Embedding Model** | Cohere embed-english-v3.0 | 1024 dims, 512 token context |
| **Vector Database** | Qdrant Cloud (free tier) | Cosine distance, HNSW indexing |
| **Web Crawling** | httpx (async) + BeautifulSoup | Sitemap-first strategy |
| **Chunking** | LangChain RecursiveCharacterTextSplitter | 400 tokens, 20% overlap |
| **Package Manager** | UV | Modern Python dependency management |
| **Retry Logic** | tenacity | Exponential backoff |
| **Environment Config** | python-dotenv | .env file management |

### Key Parameters

```python
# Embedding
EMBEDDING_MODEL = "embed-english-v3.0"
EMBEDDING_DIMENSIONS = 1024
EMBEDDING_INPUT_TYPE = "search_document"

# Chunking
TARGET_CHUNK_SIZE = 400  # tokens
CHUNK_OVERLAP = 80       # tokens (20%)
MIN_CHUNK_SIZE = 100     # tokens
MAX_CHUNK_SIZE = 512     # tokens (model limit)

# Qdrant
DISTANCE_METRIC = "COSINE"
HNSW_M = 16
HNSW_EF_CONSTRUCT = 100
HNSW_EF_SEARCH = 128
BATCH_SIZE = 100  # vectors per upload

# Crawling
SITEMAP_URL_PATTERN = "{base_url}/sitemap.xml"
MAX_CONCURRENT_REQUESTS = 10
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
```

### Design Principles Applied

1. **Simplicity**: Single-file script, minimal dependencies
2. **Reliability**: Retry logic at every external interaction point
3. **Performance**: Async HTTP, batch processing, sitemap-first crawling
4. **Observability**: Structured logging at each pipeline stage
5. **Quality**: Validation step ensures searchable, relevant results

### Next Steps

1. ✅ **Phase 0 Complete**: All technical unknowns resolved
2. **Phase 1**: Generate data-model.md and quickstart.md
3. **Phase 2**: Run `/sp.tasks` to create implementation tasks
4. **Implementation**: Follow TDD cycle (tests → implement → validate)

---

**Research Completed**: 2025-12-27
**All Decisions Documented**: Yes
**Ready for Phase 1 Design**: Yes
