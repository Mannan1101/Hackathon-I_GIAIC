# Implementation Plan: RAG Retrieval Validation

**Feature Branch**: `002-rag-retrieval-validation`
**Created**: 2025-12-27
**Status**: Draft
**Dependencies**: Spec-1 (001-doc-rag-ingestion) - Qdrant collection with stored embeddings

---

## Technical Context

### What We're Building

A validation script (`retrieve.main.py`) that tests the RAG retrieval pipeline by:
1. Connecting to Qdrant and verifying the collection exists
2. Executing test queries to retrieve relevant documentation chunks
3. Validating retrieved results (metadata, similarity scores, source URLs)
4. Generating a validation report with success metrics

### What Already Exists (from spec-1)

- **Qdrant Collection**: `documentation` collection with 1024-dim COSINE vectors
- **Stored Metadata**: Each vector has payload with `chunk_text`, `source_url`, `page_title`, `section_heading`, `breadcrumb`, `chunk_index`, `chunk_size`, `content_type`, `has_code`, `ingested_at`, `content_hash`, `embedding_model`
- **Environment Config**: `.env` with Qdrant credentials (QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME)
- **Embedding Model**: Cohere embed-english-v3.0 (1024 dimensions)

### Architecture Decision: Single-File Validation Script

**Decision**: Implement as standalone `retrieve.main.py` following the same architectural pattern as `main.py` from spec-1

**Rationale**:
- Consistency with existing codebase structure
- Single-file architecture makes validation script easy to understand and run
- Self-contained script can be executed independently: `uv run python retrieve.main.py`
- No need for complex module structure for validation use case

**Tradeoffs**:
- ✅ Simplicity: Easy to read, modify, and execute
- ✅ Portability: Can be copied/shared as single file
- ✅ Low overhead: No package structure needed
- ❌ Code reuse: Some duplication with main.py (config loading, retry logic)
- ❌ Scalability: Not suitable if validation grows significantly (acceptable for MVP)

**Alternatives Considered**:
1. **Shared utilities module**: Extract common code from main.py and retrieve.main.py
   - Rejected: Over-engineering for 1-2 task scope; violates YAGNI
2. **Integration into main.py**: Add validation mode flag
   - Rejected: Mixes ingestion and validation concerns; spec-1 already complete
3. **Jupyter notebook**: Interactive validation
   - Rejected: Less reproducible; user requested script format

---

## Phase 0: Research & Technical Decisions

### Research Areas

**R1: Qdrant Query Methods**
- **Question**: What's the best method for semantic search in Qdrant Python client?
- **Status**: ✅ Resolved
- **Decision**: Use `client.search()` with query_vector from Cohere embeddings
- **Rationale**:
  - `search()` returns scored results with metadata
  - Compatible with existing Cohere embed-english-v3.0 embeddings
  - Supports top-k retrieval with similarity scores
- **Reference**: [Qdrant Python Client Docs - Search](https://qdrant.tech/documentation/concepts/search/)

**R2: Cohere Embedding API for Queries**
- **Question**: Should we use `input_type="search_query"` or `input_type="search_document"`?
- **Status**: ✅ Resolved
- **Decision**: Use `input_type="search_query"` for query embeddings
- **Rationale**:
  - Documents were ingested with `input_type="search_document"` (from main.py)
  - Cohere recommends `search_query` for query-side embeddings
  - Asymmetric search: different input types optimize for query vs document encoding
- **Reference**: [Cohere Embed API Docs](https://docs.cohere.com/reference/embed)

**R3: Validation Metrics**
- **Question**: What metrics define successful retrieval validation?
- **Status**: ✅ Resolved
- **Decision**: Track these metrics per spec success criteria (SC-001 to SC-008):
  - Connection success (binary: pass/fail)
  - Collection metadata validation (vector count, dimensions, distance metric)
  - Query success rate (% of queries returning results)
  - Average similarity score (expect >0.7 for relevant queries per SC-002)
  - Metadata completeness (100% of results have required fields per SC-003)
  - Execution time per query (expect <2 seconds per SC-004)
- **Rationale**: Aligns with spec success criteria; measurable and actionable

**R4: Test Query Design**
- **Question**: What test queries validate retrieval quality?
- **Status**: ✅ Resolved
- **Decision**: Use 3 query categories (10 total queries):
  1. **Specific queries** (5): Target known documentation topics
  2. **Broad queries** (3): Test semantic understanding
  3. **Negative queries** (2): Should return low scores or no results
- **Rationale**:
  - Covers SC-002 (relevant queries), SC-008 (irrelevant queries)
  - Small set suitable for 1-2 task timeline
  - Can be expanded later if needed

---

## Phase 1: Design & Contracts

### 1.1 Data Model

See `data-model.md` for complete entity definitions. Key entities:

**RetrievalQuery** (Input):
```python
@dataclass
class RetrievalQuery:
    query_text: str
    top_k: int = 5
    similarity_threshold: float = 0.0
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
```

**RetrievalResult** (Output):
```python
@dataclass
class RetrievalResult:
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

**ValidationReport** (Summary):
```python
@dataclass
class ValidationReport:
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

    def to_summary(self) -> str:
        # Returns formatted validation report
```

### 1.2 Core Functions Contract

**Configuration**:
```python
def load_config() -> Dict[str, Any]:
    """Load Qdrant and Cohere config from .env"""
    # Returns: qdrant_url, qdrant_api_key, qdrant_collection_name,
    #          cohere_api_key, cohere_model, cohere_input_type
```

**Connection Validation** (User Story 1):
```python
def validate_connection(client: QdrantClient, collection_name: str) -> Dict[str, Any]:
    """Verify Qdrant connection and collection metadata"""
    # Returns: collection_exists, vector_count, vector_dim, distance_metric
    # Raises: ConnectionError if Qdrant unreachable
```

**Query Embedding**:
```python
def embed_query(query_text: str, cohere_client: cohere.Client, model: str) -> List[float]:
    """Generate embedding for query text using Cohere"""
    # Returns: 1024-dim embedding vector
    # Uses: input_type="search_query"
```

**Semantic Search** (User Story 2):
```python
def search_similar_chunks(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    top_k: int = 5
) -> List[RetrievalResult]:
    """Perform semantic search in Qdrant"""
    # Returns: List of RetrievalResult sorted by similarity_score (descending)
```

**Metadata Validation** (User Story 3):
```python
def validate_metadata(results: List[RetrievalResult]) -> Dict[str, Any]:
    """Check metadata completeness and validity"""
    # Returns: completeness_score (0.0-1.0), missing_fields, invalid_urls
```

**Batch Query Execution** (User Story 4):
```python
def run_validation_suite(
    queries: List[RetrievalQuery],
    client: QdrantClient,
    cohere_client: cohere.Client,
    collection_name: str,
    config: Dict[str, Any]
) -> ValidationReport:
    """Execute all test queries and generate validation report"""
    # Returns: Complete ValidationReport with all metrics
```

### 1.3 Error Handling Strategy

**Error Categories**:
1. **Connection Errors**: Qdrant unreachable, invalid credentials
   - Handling: Fail fast with clear error message, suggest checking .env
2. **Collection Errors**: Collection not found, empty collection
   - Handling: Report error, suggest running main.py first
3. **Query Errors**: Cohere API failures, rate limits
   - Handling: Retry with exponential backoff (3 attempts), log failures
4. **Validation Errors**: Metadata missing, malformed results
   - Handling: Log warnings, include in validation report, continue execution

**Retry Strategy** (reuse pattern from main.py):
```python
retry_db = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)

retry_api = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
```

### 1.4 Test Queries (Predefined)

**Category 1: Specific Queries** (expect high similarity >0.7):
1. "How do I get started with the documentation?"
2. "What is authentication and how does it work?"
3. "How to configure the application settings?"
4. "Explain the API endpoints available"
5. "What are the installation requirements?"

**Category 2: Broad Queries** (expect moderate similarity 0.5-0.7):
6. "Tell me about the main features"
7. "What is this documentation about?"
8. "How does the system work?"

**Category 3: Negative Queries** (expect low similarity <0.5):
9. "What is the weather today?"
10. "How to cook pasta?"

---

## Phase 2: Implementation Workflow

### 2.1 Setup (Tasks T001-T005)

**T001**: Create `retrieve.main.py` skeleton
- Imports: qdrant-client, cohere, python-dotenv, tenacity, dataclasses, logging
- Module docstring: Purpose and usage
- Logging configuration (same format as main.py)

**T002**: Define data models
- Implement `RetrievalQuery` dataclass
- Implement `RetrievalResult` dataclass
- Implement `ValidationReport` dataclass with `to_summary()` method

**T003**: Implement `load_config()` function
- Load environment variables from .env
- Validate required fields: QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, COHERE_API_KEY
- Return config dictionary

**T004**: Implement retry decorators
- `retry_db` for Qdrant operations
- `retry_api` for Cohere operations
- Same configuration as main.py (3 attempts, exponential backoff)

**T005**: Define test queries list
- Create `TEST_QUERIES` constant with 10 predefined queries
- Include category labels for reporting

### 2.2 User Story 1 - Connection Validation (Tasks T006-T010)

**T006**: Implement `validate_connection()` function
- Initialize Qdrant client
- Check collection exists
- Retrieve collection metadata (vector count, dimensions, distance metric)
- Return validation results dictionary

**T007**: Implement collection statistics retrieval
- Get total vector count
- Get collection configuration (vector_dim, distance)
- Compare with expected values (1024-dim, COSINE)

**T008**: Add connection error handling
- Catch connection errors with clear messages
- Suggest troubleshooting steps (check .env, Qdrant status)
- Log connection details (URL, collection name)

**T009**: Implement connection validation logging
- Log connection attempt
- Log collection statistics
- Log validation success/failure

**T010**: Test connection validation
- Acceptance: Connection succeeds <5 seconds (SC-001)
- Acceptance: Reports correct vector count and dimensions
- Acceptance: Handles connection failures gracefully (SC-007)

### 2.3 User Story 2 - Query Execution (Tasks T011-T018)

**T011**: Implement `embed_query()` function
- Initialize Cohere client
- Generate embedding with `input_type="search_query"`
- Return 1024-dim vector
- Add retry logic with `@retry_api`

**T012**: Implement `search_similar_chunks()` function
- Use `client.search()` with query_vector
- Set limit=top_k
- Extract results with scores and payloads
- Convert to `RetrievalResult` objects

**T013**: Implement result parsing
- Extract chunk_text, source_url, page_title from payload
- Extract metadata fields (section_heading, breadcrumb, chunk_index)
- Include similarity_score from search result
- Set rank based on position in results

**T014**: Add query execution logging
- Log query text
- Log number of results returned
- Log top result's similarity score
- Log execution time

**T015**: Handle empty results
- Detect when search returns no results
- Log warning with query text
- Include in validation report

**T016**: Handle low-scoring results
- Detect when all results have score <0.5
- Log info message (expected for negative queries)
- Include in validation report

**T017**: Implement single-query execution wrapper
- Combine embed_query() + search_similar_chunks()
- Track execution time
- Return RetrievalResult list + metrics

**T018**: Test query execution
- Acceptance: Specific queries return top-5 results (FR-003)
- Acceptance: Results ranked by similarity score (FR-004)
- Acceptance: Avg similarity >0.7 for relevant queries (SC-002)
- Acceptance: Query executes <2 seconds (SC-004, FR-010)

### 2.4 User Story 3 - Metadata Validation (Tasks T019-T023)

**T019**: Implement `validate_metadata()` function
- Check required fields present: source_url, page_title, chunk_text (FR-005)
- Check optional fields: section_heading, breadcrumb, chunk_index
- Calculate completeness percentage

**T020**: Implement URL validation
- Check source_url format (valid URL structure)
- Log any malformed URLs
- Track count of valid vs invalid URLs

**T021**: Implement metadata completeness check
- Track missing fields per result
- Calculate overall completeness score
- Return validation statistics

**T022**: Add metadata validation logging
- Log completeness percentage
- Log missing fields if any
- Warn on metadata issues

**T023**: Test metadata validation
- Acceptance: 100% of results have required fields (SC-003, FR-005)
- Acceptance: source_url points to valid documentation (SC-006, FR-009)
- Acceptance: chunk_index and other metadata accurate

### 2.5 User Story 4 - End-to-End Validation (Tasks T024-T030)

**T024**: Implement `run_validation_suite()` function
- Initialize ValidationReport
- Execute all test queries sequentially
- Aggregate results and metrics
- Handle errors gracefully

**T025**: Implement query loop
- Iterate through TEST_QUERIES
- Execute each query with timing
- Collect all RetrievalResult objects
- Track successes and failures

**T026**: Implement metrics aggregation
- Calculate total_queries, successful_queries, failed_queries
- Calculate avg_similarity_score across all results
- Calculate avg_query_time
- Calculate metadata_completeness

**T027**: Implement error tracking
- Collect error messages from failed queries
- Include in ValidationReport.errors
- Continue execution on individual query failures

**T028**: Implement `ValidationReport.to_summary()` method
- Format report header with run_id and timestamps
- Display connection status and collection stats
- Display query metrics (success rate, avg scores)
- Display metadata validation results
- List any errors encountered

**T029**: Implement main() entry point
- Load config
- Validate connection
- Run validation suite
- Print validation report
- Exit with appropriate status code (0=success, 1=failure)

**T030**: Test end-to-end validation
- Acceptance: 10 queries complete <20 seconds total (SC-004)
- Acceptance: Validation report shows all metrics (SC-005)
- Acceptance: Handles failed queries with clear errors (SC-005, FR-006)
- Acceptance: All 4 user stories validated successfully

---

## Phase 3: Validation & Testing

### 3.1 Unit Testing (Optional - beyond 1-2 task scope)

If time permits, create `test_retrieve.py`:
- Test `embed_query()` with mock Cohere client
- Test `search_similar_chunks()` with mock Qdrant client
- Test `validate_metadata()` with sample results
- Test `ValidationReport.to_summary()` formatting

### 3.2 Integration Testing (Required)

**Test Case 1: Connection Validation**
- Prerequisite: Qdrant collection exists with vectors from spec-1
- Expected: Connection succeeds, reports vector count >0
- Expected: Dimensions=1024, distance=COSINE

**Test Case 2: Specific Query Retrieval**
- Query: "How do I get started?"
- Expected: Top-5 results returned
- Expected: Avg similarity >0.7
- Expected: All results have complete metadata

**Test Case 3: Negative Query Handling**
- Query: "What is the weather today?"
- Expected: Results returned (if any) have low scores <0.5
- Expected: No errors, handled gracefully

**Test Case 4: End-to-End Suite**
- Run all 10 test queries
- Expected: All queries execute without errors
- Expected: Validation report generated
- Expected: Total time <20 seconds

### 3.3 Manual Validation Checklist

Before marking feature complete:
- [ ] `retrieve.main.py` runs without errors: `uv run python retrieve.main.py`
- [ ] Connection validation passes (SC-001)
- [ ] Specific queries return relevant results (SC-002)
- [ ] All metadata fields present (SC-003)
- [ ] Batch validation completes in time (SC-004)
- [ ] Validation report displays correctly (SC-005)
- [ ] Source URLs are valid (SC-006)
- [ ] Connection errors handled gracefully (SC-007)
- [ ] Negative queries handled correctly (SC-008)

---

## Phase 4: Documentation

### 4.1 Quickstart Guide

Create `specs/002-rag-retrieval-validation/quickstart.md`:
- Prerequisites: Spec-1 completed, .env configured
- How to run: `uv run python retrieve.main.py`
- How to interpret validation report
- Troubleshooting common issues

### 4.2 Code Documentation

- Module docstring: Purpose, usage, dependencies
- Function docstrings: Parameters, returns, raises
- Inline comments for complex logic (minimal, code should be self-documenting)

### 4.3 Update README

Add section to backend/README.md:
- "Validation" section describing retrieve.main.py
- Link to spec-2 documentation
- Example output from validation report

---

## Non-Functional Requirements

### Performance

- **Latency**: Single query <2 seconds (SC-004, FR-010)
- **Throughput**: 10 queries in <20 seconds (SC-004)
- **Connection**: Validation <5 seconds (SC-001)

### Reliability

- **Retry Logic**: 3 attempts for API and DB operations
- **Error Handling**: Graceful degradation, clear error messages
- **Logging**: Structured logs for all operations

### Security

- **Credentials**: Load from .env only, never hardcode
- **API Keys**: Use environment variables
- **No Secrets in Logs**: Redact API keys in log output

### Maintainability

- **Code Style**: Follow main.py conventions
- **Single Responsibility**: Each function has one clear purpose
- **DRY**: Reuse retry decorators and config patterns
- **Comments**: Minimal, only where logic is non-obvious

---

## Dependencies & Risks

### External Dependencies

1. **Qdrant Cloud**: Must be accessible and contain vectors from spec-1
   - Risk: Collection empty or deleted
   - Mitigation: Connection validation fails fast with clear message

2. **Cohere API**: Must be available for query embeddings
   - Risk: Rate limits or API downtime
   - Mitigation: Retry logic with exponential backoff

3. **Environment Config**: .env must have valid credentials
   - Risk: Missing or invalid credentials
   - Mitigation: Config validation fails fast at startup

### Internal Dependencies

1. **Spec-1 Completion**: Vectors must exist in Qdrant
   - Risk: Spec-1 not run or failed
   - Mitigation: Connection validation detects empty collection

2. **Consistent Embedding Model**: Must use same model as ingestion (embed-english-v3.0)
   - Risk: Model mismatch causes poor retrieval
   - Mitigation: Document model requirement in quickstart

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Qdrant collection empty | High (validation fails) | Medium | Connection validation detects and reports |
| Cohere API rate limit | Medium (queries fail) | Low | Retry logic, reduce query count if needed |
| Metadata schema mismatch | Medium (validation fails) | Low | Defensive metadata extraction with defaults |
| Query embeddings fail | High (no results) | Low | Retry logic, fail fast with clear error |
| Network latency >2s | Low (metrics miss target) | Medium | Acceptable for validation use case |

---

## Success Criteria Mapping

| Success Criterion | Implementation | Verification |
|-------------------|----------------|--------------|
| SC-001: Connection <5s | `validate_connection()` with timing | Integration test |
| SC-002: Similarity >0.7 | Track avg_similarity_score in ValidationReport | Test queries |
| SC-003: 100% metadata | `validate_metadata()` checks all fields | Metadata validation |
| SC-004: 10 queries <20s | `run_validation_suite()` with timing | End-to-end test |
| SC-005: Validation report | `ValidationReport.to_summary()` | Manual review |
| SC-006: Valid URLs | URL format validation in `validate_metadata()` | Manual spot check |
| SC-007: Error handling | Try/except with clear messages | Connection failure test |
| SC-008: Low score handling | Log results <0.5, no errors | Negative query test |

---

## Acceptance Criteria

**This feature is complete when**:

1. ✅ `retrieve.main.py` exists and runs without errors
2. ✅ Connection validation succeeds and reports collection stats (User Story 1)
3. ✅ Test queries return top-5 results with metadata (User Story 2)
4. ✅ Metadata validation shows 100% completeness (User Story 3)
5. ✅ Validation suite generates complete report (User Story 4)
6. ✅ All 8 success criteria (SC-001 to SC-008) verified
7. ✅ `quickstart.md` created with usage instructions
8. ✅ `data-model.md` documents all entities
9. ✅ Backend README.md updated with validation section

**Out of Scope** (will NOT be implemented):
- LLM reasoning or answer generation
- Chatbot or conversational UI
- FastAPI backend or REST API
- Re-embedding or re-ingestion
- Query optimization or re-ranking
- Caching or advanced performance optimization
- Authentication or access control
- Production deployment configuration

---

## Timeline Estimate

**Total Tasks**: 30 tasks (T001-T030)
**Target**: 1-2 tasks (per spec constraint)

**Task Breakdown**:
- Setup: 5 tasks (T001-T005) - ~15 min
- User Story 1: 5 tasks (T006-T010) - ~20 min
- User Story 2: 8 tasks (T011-T018) - ~30 min
- User Story 3: 5 tasks (T019-T023) - ~20 min
- User Story 4: 7 tasks (T024-T030) - ~25 min

**Total Estimated Time**: ~110 minutes (~2 hours)
**Fits Timeline**: Yes, can be completed in 1-2 focused work sessions

---

## Next Steps

After plan approval:

1. **Generate Tasks**: Run `/sp.tasks` to create `tasks.md` with detailed task breakdown
2. **Implement**: Run `/sp.implement` to execute all tasks and create `retrieve.main.py`
3. **Test**: Execute `uv run python retrieve.main.py` to validate end-to-end
4. **Document**: Verify all documentation (quickstart, data-model) is complete
5. **Commit**: Create PR with implementation and documentation

---

**Plan Status**: Ready for review
**Next Command**: `/sp.tasks` to generate detailed task breakdown
