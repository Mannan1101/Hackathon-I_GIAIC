# Implementation Plan: Documentation RAG Ingestion System

**Branch**: `001-doc-rag-ingestion` | **Date**: 2025-12-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-doc-rag-ingestion/spec.md`

**User Directive**: URL Ingestion and Embedding pipeline - Initialize project with UV, implement URL fetching, text cleaning, chunking, generate embeddings using Cohere models, store in Qdrant cloud, with main() function to run full pipeline end-to-end.

## Summary

This feature implements a complete documentation ingestion pipeline that crawls deployed documentation websites (Docusaurus on Vercel), extracts and cleans text content, chunks it appropriately for embedding models, generates vector embeddings using Cohere's embedding API, and stores the embeddings with metadata in Qdrant vector database. The system is designed as a standalone Python script with modular functions, configuration via environment variables, comprehensive error handling with retries, and validation to ensure all content is successfully indexed and searchable.

**Technical Approach**: Single-file Python script (`main.py`) with clear separation of concerns across functions (crawl, clean, chunk, embed, store, validate), using UV for dependency management, async operations for performance, and structured logging for observability.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- `httpx` (async HTTP client for crawling)
- `beautifulsoup4` (HTML parsing and cleaning)
- `cohere` (embedding generation)
- `qdrant-client` (vector database)
- `python-dotenv` (environment configuration)
- `tenacity` (retry logic)

**Storage**: Qdrant Cloud (vector database, free tier)
**Testing**: pytest with pytest-asyncio for async function testing
**Target Platform**: Local development / Cloud execution (Python runtime)
**Project Type**: Single-script pipeline (backend folder)
**Performance Goals**:
- Process 500 pages in under 30 minutes
- Handle 1000+ chunks per batch
- Embed generation rate limited by Cohere API (respect rate limits)

**Constraints**:
- Qdrant free tier storage limits (~1GB vectors)
- Cohere API rate limits (typically 100 req/min for trial, verify actual limits)
- Network reliability (retry logic required)
- Chunk size must match Cohere model context (512-1024 tokens recommended)

**Scale/Scope**:
- Target: Documentation sites with 100-1000 pages
- Expected chunks: 5000-50000 text segments
- Vector dimensions: 1024 or 4096 (depending on Cohere model choice)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: Constitution file contains placeholder template. Applying general software engineering best practices for evaluation.

### Default Engineering Principles Applied

1. **Simplicity First**: ✅ PASS
   - Single Python file approach minimizes complexity
   - No unnecessary abstractions or frameworks
   - Direct implementation of ingestion pipeline

2. **Testability**: ✅ PASS
   - Each function (crawl, clean, chunk, embed, store) is independently testable
   - Clear inputs/outputs for unit tests
   - Integration test validates end-to-end pipeline

3. **Error Handling**: ✅ PASS
   - Retry logic for HTTP, API, and database operations (FR-007, FR-008, FR-009)
   - Graceful degradation with logging
   - Validation step ensures quality (FR-013)

4. **Configuration Management**: ✅ PASS
   - Environment variables for all credentials and parameters (FR-006)
   - No hardcoded secrets
   - Easy configuration changes without code modification

5. **Observability**: ✅ PASS
   - Structured logging at each pipeline stage (FR-012)
   - Progress metrics and statistics
   - Clear error messages for debugging

**Constitution Check Result**: ✅ ALL GATES PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-doc-rag-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # Single-file ingestion pipeline
├── .env.example         # Environment variable template
├── pyproject.toml       # UV project configuration
├── uv.lock              # UV lock file
└── tests/
    ├── test_crawler.py      # Crawling and URL discovery tests
    ├── test_cleaner.py      # HTML cleaning and text extraction tests
    ├── test_chunker.py      # Text chunking tests
    ├── test_embedder.py     # Embedding generation tests (mocked)
    ├── test_storage.py      # Vector storage tests (mocked)
    └── test_integration.py  # End-to-end pipeline test
```

**Structure Decision**: Single project structure selected. This is a standalone ingestion script that doesn't require web frontend, API endpoints, or multiple services. All functionality is contained in `backend/main.py` with supporting test files in `backend/tests/`. UV is used as the modern Python package manager for faster dependency resolution and installation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All design decisions align with simplicity, testability, and maintainability principles.

---

## Phase 0: Research & Technology Decisions

### Research Tasks

The following research tasks will be executed to resolve technical unknowns and establish best practices:

1. **Cohere Embedding Model Selection**
   - Research: Which Cohere embedding model to use (embed-english-v3.0 vs embed-multilingual-v3.0)
   - Goal: Determine optimal model for English documentation with best performance/cost tradeoff
   - Output: Model choice with dimensions, context length, and performance characteristics

2. **Web Crawling Strategy for Docusaurus**
   - Research: Best practices for crawling Docusaurus sites (sitemap.xml vs recursive link following)
   - Goal: Most reliable method to discover all pages without missing content or hitting duplicates
   - Output: Crawling algorithm with URL normalization and deduplication strategy

3. **HTML Content Extraction**
   - Research: Identifying main content in Docusaurus pages (CSS selectors, content markers)
   - Goal: Reliable extraction of article content while removing navigation, headers, footers
   - Output: BeautifulSoup selectors and cleaning rules for Docusaurus structure

4. **Text Chunking Strategy**
   - Research: Semantic chunking vs fixed-size chunking for documentation
   - Goal: Balance between chunk coherence and optimal embedding quality
   - Output: Chunking algorithm with size limits, overlap strategy, and boundary detection

5. **Qdrant Configuration**
   - Research: Optimal Qdrant collection settings (distance metric, vector index type, HNSW parameters)
   - Goal: Best search quality and performance for documentation retrieval
   - Output: Collection configuration with index parameters and distance metric choice

6. **Rate Limiting and Retry Logic**
   - Research: Cohere API rate limits and best practices for handling them
   - Goal: Robust retry strategy that respects limits and handles transient failures
   - Output: Retry configuration (backoff, max attempts, rate limiting approach)

7. **Async vs Sync Implementation**
   - Research: Performance benefits of async HTTP requests for crawling
   - Goal: Determine if async complexity is justified for performance gains
   - Output: Decision on async implementation with performance benchmarks

### Success Criteria for Phase 0

- All technical unknowns resolved with documented decisions
- Best practices identified for each major component
- Alternatives considered with rationale for final choices
- research.md contains all decisions needed for Phase 1 design

---

## Phase 1: Design Artifacts

### Deliverables

1. **data-model.md**: Data structures for Documentation Page, Text Chunk, Embedding Vector, Ingestion Metadata
2. **contracts/**: No external API contracts (this is a script, not a service)
3. **quickstart.md**: Setup instructions, environment configuration, and usage guide

### Design Requirements

1. **Data Model Design**
   - Define Python dataclasses or TypedDicts for all entities from spec
   - Include validation rules and field constraints
   - Document metadata structure for Qdrant payloads

2. **Pipeline Flow Design**
   - Sequence of operations from URL input to stored vectors
   - Error handling points and retry strategies
   - Logging checkpoints and progress tracking

3. **Configuration Design**
   - Environment variable schema (.env.example)
   - Runtime parameters (chunk size, batch size, retry limits)
   - Feature flags if needed (e.g., skip validation for testing)

### Success Criteria for Phase 1

- Complete data model with all entities and relationships
- Clear pipeline architecture with error boundaries
- Developer-ready quickstart guide
- All design decisions documented with rationale

---

## Phase 2: Task Generation

**Note**: Phase 2 is handled by the `/sp.tasks` command, NOT by `/sp.plan`. This section describes what tasks.md will contain once generated.

### Expected Task Categories

1. **Environment Setup Tasks**
   - Initialize UV project
   - Configure dependencies in pyproject.toml
   - Create .env.example template
   - Setup logging configuration

2. **Core Pipeline Tasks**
   - Implement URL crawling and discovery
   - Implement HTML parsing and text extraction
   - Implement text chunking algorithm
   - Implement embedding generation with Cohere
   - Implement Qdrant storage and indexing

3. **Error Handling Tasks**
   - Add retry logic for HTTP requests
   - Add retry logic for Cohere API calls
   - Add retry logic for Qdrant operations
   - Implement comprehensive logging

4. **Validation Tasks**
   - Implement URL deduplication
   - Implement chunk quality validation
   - Implement vector search validation
   - Add pipeline statistics reporting

5. **Testing Tasks**
   - Write unit tests for each component
   - Write integration test for full pipeline
   - Create test fixtures and mocks
   - Document test scenarios

---

## Implementation Notes

### Key Design Decisions

1. **Single File Architecture**: All pipeline logic in main.py for simplicity. Functions are organized logically (crawl → clean → chunk → embed → store → validate) with clear separation of concerns.

2. **UV Package Manager**: Modern Python dependency management with faster resolution and better reproducibility than pip.

3. **Async HTTP**: Use httpx with async for concurrent page fetching to improve crawl performance.

4. **Batch Processing**: Process embeddings in batches to optimize API usage and respect rate limits.

5. **Incremental Progress**: Log progress at each stage to enable monitoring and debugging of long-running ingestion jobs.

6. **Validation as Final Step**: Perform similarity search test queries to ensure vectors are correctly stored and searchable before declaring success.

### Critical Path

1. Research (Phase 0) → 2. Design (Phase 1) → 3. Implementation (tasks.md) → 4. Testing → 5. Validation

### Risk Mitigation

- **Risk**: Cohere API rate limiting
  - **Mitigation**: Implement exponential backoff, batch requests, monitor rate limit headers

- **Risk**: Qdrant connection failures
  - **Mitigation**: Retry logic with timeouts, validate connection before bulk upload

- **Risk**: Large documentation sites exceed free tier limits
  - **Mitigation**: Add configuration for page limits, estimate storage before ingestion

- **Risk**: Poor chunk quality affects search relevance
  - **Mitigation**: Validation step with test queries, manual review of sample chunks

---

## Next Steps

1. Execute Phase 0 research to resolve all technical decisions
2. Execute Phase 1 design to create data model and quickstart guide
3. Run `/sp.tasks` to generate detailed implementation tasks
4. Begin TDD cycle: write tests → implement → validate
