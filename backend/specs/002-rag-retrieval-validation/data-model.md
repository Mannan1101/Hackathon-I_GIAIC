# Data Model: RAG Retrieval Validation

**Feature**: 002-rag-retrieval-validation
**Created**: 2025-12-27
**Purpose**: Define data structures for retrieval validation system

---

## Overview

This document defines the data models used in the RAG retrieval validation pipeline. All models are implemented as Python dataclasses for type safety and clarity.

---

## Core Entities

### 1. RetrievalQuery

**Purpose**: Represents a semantic search query with parameters

**Lifecycle**: Created at query time → Used for embedding generation → Used for Qdrant search

**Fields**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query_text` | `str` | Yes | - | Natural language query text |
| `top_k` | `int` | No | `5` | Number of results to retrieve |
| `similarity_threshold` | `float` | No | `0.0` | Minimum similarity score (0.0-1.0) |
| `query_id` | `str` | No | `uuid.uuid4()` | Unique identifier for this query |
| `created_at` | `datetime` | No | `datetime.utcnow()` | Query creation timestamp |

**Python Implementation**:
```python
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class RetrievalQuery:
    """Represents a semantic search query with parameters."""
    query_text: str
    top_k: int = 5
    similarity_threshold: float = 0.0
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
```

**Usage Example**:
```python
# Specific query with defaults
query1 = RetrievalQuery(query_text="How do I get started?")

# Custom top-k and threshold
query2 = RetrievalQuery(
    query_text="What is authentication?",
    top_k=10,
    similarity_threshold=0.5
)
```

**Validation Rules**:
- `query_text` must be non-empty string
- `top_k` must be positive integer (typically 1-20)
- `similarity_threshold` must be in range [0.0, 1.0]

---

### 2. RetrievalResult

**Purpose**: Represents a single search result with chunk content, metadata, and similarity score

**Lifecycle**: Created from Qdrant search response → Used for metadata validation → Included in ValidationReport

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query_id` | `str` | Yes | ID of the query that produced this result |
| `chunk_text` | `str` | Yes | Retrieved text chunk content |
| `source_url` | `str` | Yes | URL of the documentation page |
| `page_title` | `str` | Yes | Title of the documentation page |
| `section_heading` | `Optional[str]` | No | Section heading where chunk appears |
| `breadcrumb` | `Optional[str]` | No | Navigation breadcrumb (e.g., "Docs > API > Auth") |
| `chunk_index` | `int` | Yes | Index of this chunk within the page (0-based) |
| `similarity_score` | `float` | Yes | Cosine similarity score (0.0-1.0) |
| `metadata` | `Dict[str, Any]` | Yes | Full payload from Qdrant (for debugging) |
| `rank` | `int` | Yes | Position in search results (1-based) |

**Python Implementation**:
```python
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class RetrievalResult:
    """Represents a single search result with metadata and score."""
    query_id: str
    chunk_text: str
    source_url: str
    page_title: str
    section_heading: Optional[str]
    breadcrumb: Optional[str]
    chunk_index: int
    similarity_score: float
    metadata: Dict[str, Any]
    rank: int
```

**Usage Example**:
```python
result = RetrievalResult(
    query_id="a1b2c3d4",
    chunk_text="To get started, first install the dependencies...",
    source_url="https://docs.example.com/getting-started",
    page_title="Getting Started Guide",
    section_heading="Installation",
    breadcrumb="Docs > Getting Started > Installation",
    chunk_index=2,
    similarity_score=0.87,
    metadata={
        "chunk_size": 380,
        "content_type": "text",
        "has_code": True,
        "ingested_at": "2025-12-27T10:30:00Z",
        "content_hash": "abc123def456",
        "embedding_model": "embed-english-v3.0"
    },
    rank=1
)
```

**Validation Rules**:
- `chunk_text` must be non-empty
- `source_url` must be valid URL format
- `similarity_score` must be in range [0.0, 1.0]
- `rank` must be positive integer
- `chunk_index` must be non-negative integer

**Metadata Schema** (from Qdrant payload):
```python
{
    "chunk_text": str,           # Same as top-level field
    "source_url": str,            # Same as top-level field
    "page_title": str,            # Same as top-level field
    "section_heading": str | None,
    "breadcrumb": str,
    "chunk_index": int,
    "chunk_size": int,            # Token count
    "content_type": str,          # "text", "code", "mixed"
    "has_code": bool,
    "ingested_at": str,           # ISO 8601 timestamp
    "content_hash": str,          # First 16 chars of SHA-256
    "embedding_model": str        # "embed-english-v3.0"
}
```

---

### 3. ValidationReport

**Purpose**: Aggregates validation test results with statistics and metrics

**Lifecycle**: Initialized at validation start → Updated during query execution → Finalized with summary → Displayed to user

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `run_id` | `str` | Yes | Unique identifier for this validation run |
| `total_queries` | `int` | Yes | Total number of queries executed |
| `successful_queries` | `int` | Yes | Number of queries that completed successfully |
| `failed_queries` | `int` | Yes | Number of queries that failed |
| `avg_similarity_score` | `float` | Yes | Average similarity score across all results |
| `avg_query_time` | `float` | Yes | Average execution time per query (seconds) |
| `metadata_completeness` | `float` | Yes | Percentage of results with complete metadata (0.0-1.0) |
| `total_results_retrieved` | `int` | Yes | Total number of results retrieved across all queries |
| `connection_status` | `str` | Yes | Status of Qdrant connection ("connected", "failed") |
| `collection_stats` | `Dict[str, Any]` | Yes | Qdrant collection metadata |
| `errors` | `List[str]` | Yes | List of error messages encountered |
| `started_at` | `datetime` | Yes | Validation start timestamp |
| `completed_at` | `datetime` | Yes | Validation completion timestamp |

**Python Implementation**:
```python
from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime

@dataclass
class ValidationReport:
    """Aggregates validation test results with statistics."""
    run_id: str
    total_queries: int
    successful_queries: int
    failed_queries: int
    avg_similarity_score: float
    avg_query_time: float
    metadata_completeness: float
    total_results_retrieved: int
    connection_status: str
    collection_stats: Dict[str, Any]
    errors: List[str]
    started_at: datetime
    completed_at: datetime

    @property
    def duration_seconds(self) -> float:
        """Calculate total validation duration."""
        return (self.completed_at - self.started_at).total_seconds()

    @property
    def success_rate(self) -> float:
        """Calculate query success rate (0.0-1.0)."""
        if self.total_queries == 0:
            return 0.0
        return self.successful_queries / self.total_queries

    def to_summary(self) -> str:
        """Generate human-readable validation summary report."""
        return f"""
{'='*60}
RAG Retrieval Validation Report
{'='*60}
Run ID: {self.run_id}
Started: {self.started_at.strftime('%Y-%m-%d %H:%M:%S')}
Completed: {self.completed_at.strftime('%Y-%m-%d %H:%M:%S')}
Duration: {self.duration_seconds:.1f}s

CONNECTION STATUS
{'='*60}
Status: {self.connection_status}
Collection: {self.collection_stats.get('collection_name', 'N/A')}
Vector Count: {self.collection_stats.get('vector_count', 0):,}
Vector Dimensions: {self.collection_stats.get('vector_dim', 0)}
Distance Metric: {self.collection_stats.get('distance', 'N/A')}

QUERY METRICS
{'='*60}
Total Queries: {self.total_queries}
Successful: {self.successful_queries}
Failed: {self.failed_queries}
Success Rate: {self.success_rate * 100:.1f}%

RETRIEVAL QUALITY
{'='*60}
Total Results Retrieved: {self.total_results_retrieved}
Avg Similarity Score: {self.avg_similarity_score:.3f}
Avg Query Time: {self.avg_query_time:.2f}s

METADATA VALIDATION
{'='*60}
Metadata Completeness: {self.metadata_completeness * 100:.1f}%

{'ERRORS' if self.errors else 'STATUS'}
{'='*60}
{chr(10).join(self.errors) if self.errors else '✅ All validations passed successfully!'}
{'='*60}
""".strip()
```

**Usage Example**:
```python
report = ValidationReport(
    run_id="val-2025-12-27-001",
    total_queries=10,
    successful_queries=9,
    failed_queries=1,
    avg_similarity_score=0.73,
    avg_query_time=1.2,
    metadata_completeness=1.0,
    total_results_retrieved=45,
    connection_status="connected",
    collection_stats={
        "collection_name": "documentation",
        "vector_count": 312,
        "vector_dim": 1024,
        "distance": "COSINE"
    },
    errors=["Query 'What is the weather?' failed: Cohere API timeout"],
    started_at=datetime(2025, 12, 27, 14, 30, 0),
    completed_at=datetime(2025, 12, 27, 14, 30, 15)
)

print(report.to_summary())
```

**Collection Stats Schema**:
```python
{
    "collection_name": str,      # e.g., "documentation"
    "vector_count": int,          # Total vectors in collection
    "vector_dim": int,            # e.g., 1024
    "distance": str,              # e.g., "COSINE"
    "indexed": bool,              # HNSW index status
    "collection_exists": bool     # True if collection found
}
```

**Validation Rules**:
- `total_queries` = `successful_queries` + `failed_queries`
- `avg_similarity_score` in range [0.0, 1.0]
- `avg_query_time` must be positive
- `metadata_completeness` in range [0.0, 1.0]
- `connection_status` in {"connected", "failed", "timeout"}
- `completed_at` >= `started_at`

---

## Relationships

```
RetrievalQuery (1) ──produces──> (N) RetrievalResult
                                       │
                                       │ aggregated_into
                                       ▼
ValidationReport (1) ──summarizes──> (N) RetrievalResult
```

**Flow**:
1. User defines `RetrievalQuery` with query text
2. System generates embedding for query
3. Qdrant search returns matching chunks
4. Each chunk converted to `RetrievalResult`
5. All results aggregated into `ValidationReport`
6. Report displayed with `to_summary()` method

---

## Data Transformations

### From Qdrant Search Response to RetrievalResult

**Qdrant Response Structure**:
```python
[
    ScoredPoint(
        id="uuid-1234",
        score=0.87,
        payload={
            "chunk_text": "To get started...",
            "source_url": "https://docs.example.com/start",
            "page_title": "Getting Started",
            "section_heading": "Installation",
            "breadcrumb": "Docs > Getting Started",
            "chunk_index": 2,
            # ... other metadata
        }
    ),
    # ... more results
]
```

**Transformation Logic**:
```python
def qdrant_result_to_retrieval_result(
    scored_point,
    query_id: str,
    rank: int
) -> RetrievalResult:
    """Convert Qdrant ScoredPoint to RetrievalResult."""
    payload = scored_point.payload

    return RetrievalResult(
        query_id=query_id,
        chunk_text=payload["chunk_text"],
        source_url=payload["source_url"],
        page_title=payload["page_title"],
        section_heading=payload.get("section_heading"),
        breadcrumb=payload.get("breadcrumb"),
        chunk_index=payload["chunk_index"],
        similarity_score=scored_point.score,
        metadata=payload,
        rank=rank
    )
```

### From List[RetrievalResult] to ValidationReport Metrics

**Aggregation Logic**:
```python
def aggregate_results_to_report(
    results: List[RetrievalResult],
    queries: List[RetrievalQuery],
    connection_stats: Dict[str, Any],
    errors: List[str],
    started_at: datetime,
    completed_at: datetime
) -> ValidationReport:
    """Aggregate results into validation report."""

    # Calculate metrics
    total_queries = len(queries)
    failed_queries = len(errors)
    successful_queries = total_queries - failed_queries

    similarity_scores = [r.similarity_score for r in results]
    avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0

    # Check metadata completeness
    required_fields = ["chunk_text", "source_url", "page_title"]
    complete_count = sum(
        1 for r in results
        if all(getattr(r, field, None) for field in required_fields)
    )
    metadata_completeness = complete_count / len(results) if results else 1.0

    # Calculate average query time (would be tracked during execution)
    avg_query_time = (completed_at - started_at).total_seconds() / total_queries

    return ValidationReport(
        run_id=str(uuid.uuid4()),
        total_queries=total_queries,
        successful_queries=successful_queries,
        failed_queries=failed_queries,
        avg_similarity_score=avg_similarity,
        avg_query_time=avg_query_time,
        metadata_completeness=metadata_completeness,
        total_results_retrieved=len(results),
        connection_status=connection_stats.get("status", "unknown"),
        collection_stats=connection_stats,
        errors=errors,
        started_at=started_at,
        completed_at=completed_at
    )
```

---

## Validation & Error Handling

### RetrievalQuery Validation

**Invalid Examples**:
```python
# Empty query text
RetrievalQuery(query_text="")  # Should raise ValueError

# Negative top_k
RetrievalQuery(query_text="test", top_k=-5)  # Should raise ValueError

# Invalid threshold
RetrievalQuery(query_text="test", similarity_threshold=1.5)  # Should raise ValueError
```

**Validation Function**:
```python
def validate_retrieval_query(query: RetrievalQuery) -> None:
    """Validate RetrievalQuery fields."""
    if not query.query_text.strip():
        raise ValueError("query_text cannot be empty")

    if query.top_k <= 0:
        raise ValueError(f"top_k must be positive, got {query.top_k}")

    if not 0.0 <= query.similarity_threshold <= 1.0:
        raise ValueError(
            f"similarity_threshold must be in [0.0, 1.0], got {query.similarity_threshold}"
        )
```

### RetrievalResult Validation

**Defensive Metadata Extraction**:
```python
def extract_metadata_safely(payload: Dict[str, Any], field: str, default=None):
    """Safely extract metadata field with default fallback."""
    value = payload.get(field, default)
    if value is None and field in ["chunk_text", "source_url", "page_title"]:
        logger.warning(f"Required field '{field}' missing from payload")
    return value
```

### ValidationReport Edge Cases

**Empty Results**:
```python
# If no results retrieved
report = ValidationReport(
    # ... other fields ...
    total_results_retrieved=0,
    avg_similarity_score=0.0,  # No results to average
    metadata_completeness=1.0  # Vacuously true (100% of 0 results complete)
)
```

**All Queries Failed**:
```python
report = ValidationReport(
    # ... other fields ...
    total_queries=10,
    successful_queries=0,
    failed_queries=10,
    success_rate=0.0,
    errors=[...list of 10 error messages...]
)
```

---

## Example: Complete Validation Flow

```python
# Step 1: Create queries
queries = [
    RetrievalQuery(query_text="How do I get started?"),
    RetrievalQuery(query_text="What is authentication?"),
    RetrievalQuery(query_text="What is the weather?")  # Negative query
]

# Step 2: Execute queries and collect results
all_results = []
errors = []
started_at = datetime.utcnow()

for query in queries:
    try:
        # Embed query
        query_vector = embed_query(query.query_text, cohere_client, model)

        # Search Qdrant
        search_results = client.search(
            collection_name="documentation",
            query_vector=query_vector,
            limit=query.top_k
        )

        # Convert to RetrievalResult
        for rank, scored_point in enumerate(search_results, start=1):
            result = qdrant_result_to_retrieval_result(
                scored_point, query.query_id, rank
            )
            all_results.append(result)

    except Exception as e:
        errors.append(f"Query '{query.query_text}' failed: {str(e)}")

completed_at = datetime.utcnow()

# Step 3: Generate validation report
report = aggregate_results_to_report(
    results=all_results,
    queries=queries,
    connection_stats=connection_stats,
    errors=errors,
    started_at=started_at,
    completed_at=completed_at
)

# Step 4: Display report
print(report.to_summary())
```

**Expected Output**:
```
============================================================
RAG Retrieval Validation Report
============================================================
Run ID: val-2025-12-27-001
Started: 2025-12-27 14:30:00
Completed: 2025-12-27 14:30:08
Duration: 8.2s

CONNECTION STATUS
============================================================
Status: connected
Collection: documentation
Vector Count: 312
Vector Dimensions: 1024
Distance Metric: COSINE

QUERY METRICS
============================================================
Total Queries: 3
Successful: 3
Failed: 0
Success Rate: 100.0%

RETRIEVAL QUALITY
============================================================
Total Results Retrieved: 15
Avg Similarity Score: 0.687
Avg Query Time: 2.73s

METADATA VALIDATION
============================================================
Metadata Completeness: 100.0%

STATUS
============================================================
✅ All validations passed successfully!
============================================================
```

---

## Summary

**Key Data Models**:
1. **RetrievalQuery**: Input specification for semantic search
2. **RetrievalResult**: Single search result with metadata and score
3. **ValidationReport**: Aggregated metrics and summary

**Data Flow**: Query → Embedding → Search → Results → Report

**Validation**: All models include field validation and error handling

**Next Steps**: Use these models in `retrieve.main.py` implementation (see `plan.md`)
