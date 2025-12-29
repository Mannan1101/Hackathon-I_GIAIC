# Tasks: Documentation RAG Ingestion System

**Input**: Design documents from `/specs/001-doc-rag-ingestion/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Note**: Tests are NOT explicitly required by the specification, so test tasks are NOT included. The focus is on implementation with validation through the built-in validation step (User Story 4).

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files/areas, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- File paths reference `backend/` directory

## Path Conventions

Project uses single-file architecture per plan.md:
- **Main implementation**: `backend/main.py`
- **Environment**: `backend/.env`, `backend/.env.example`
- **Configuration**: `backend/pyproject.toml`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize UV project and basic structure

- [X] T001 Initialize UV project in backend/ directory with Python 3.11+
- [X] T002 [P] Create pyproject.toml with project metadata and dependencies (httpx, beautifulsoup4, cohere, qdrant-client, python-dotenv, tenacity)
- [X] T003 [P] Create .env.example template with all required environment variables per quickstart.md
- [X] T004 [P] Create main.py skeleton with import statements and basic structure
- [X] T005 Install dependencies using UV sync command

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Implement data models (DocumentationPage, TextChunk, EmbeddingVector, IngestionMetadata) in main.py using dataclasses from data-model.md
- [X] T007 [P] Implement configuration loader function to read .env variables into config dict in main.py
- [X] T008 [P] Implement structured logging setup with configurable LOG_LEVEL in main.py
- [X] T009 [P] Implement retry decorator using tenacity for HTTP, API, and database operations in main.py
- [X] T010 [P] Implement URL normalization function (remove trailing slash, anchors, query params) in main.py
- [X] T011 Implement IngestionMetadata tracker initialization and summary generation in main.py
- [X] T012 Implement main() entry point function that orchestrates pipeline stages in main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Content Ingestion (Priority: P1) 🎯 MVP

**Goal**: Crawl documentation website, extract and clean text content, chunk into semantically meaningful segments

**Independent Test**: Provide a documentation URL, run ingestion process, verify content chunks exist with proper metadata

### Implementation for User Story 1

- [ ] T013 [P] [US1] Implement sitemap.xml parser function to extract URLs from {base_url}/sitemap.xml in main.py
- [ ] T014 [P] [US1] Implement recursive link crawler as fallback (max depth 5-7 levels) if sitemap unavailable in main.py
- [ ] T015 [P] [US1] Implement URL filtering function using include/exclude patterns from research.md in main.py
- [ ] T016 [P] [US1] Implement content hash deduplication tracking (SHA256 of URLs and cleaned text) in main.py
- [ ] T017 [US1] Implement async HTTP fetch function using httpx with retry logic and timeout (30s) in main.py
- [ ] T018 [US1] Implement concurrent page crawling function (max 10 concurrent requests) using asyncio in main.py
- [ ] T019 [P] [US1] Implement BeautifulSoup content extraction using Docusaurus-specific selectors from research.md in main.py
- [ ] T020 [P] [US1] Implement HTML cleaning function to remove navigation, headers, footers using REMOVE_SELECTORS in main.py
- [ ] T021 [P] [US1] Implement metadata extraction (title, description, breadcrumb) from HTML in main.py
- [ ] T022 [US1] Implement DocumentationPage creation from fetched and cleaned content in main.py
- [ ] T023 [US1] Implement text chunking function using hybrid markdown-aware recursive strategy (400 tokens, 20% overlap) in main.py
- [ ] T024 [US1] Implement TextChunk creation with all metadata fields from data-model.md in main.py
- [ ] T025 [US1] Implement chunk validation (100-512 tokens, min 20 words, content type classification) in main.py
- [ ] T026 [US1] Implement logging for crawl progress (pages discovered, fetched, failed) in main.py
- [ ] T027 [US1] Implement logging for chunk creation progress (chunks created per page, total chunks) in main.py
- [ ] T028 [US1] Integrate crawl, clean, and chunk functions into main pipeline in main.py

**Checkpoint**: At this point, User Story 1 should crawl pages and create chunks - verify by logging chunk count and sample metadata

---

## Phase 4: User Story 2 - Embedding Generation (Priority: P2)

**Goal**: Convert text chunks to vector embeddings using Cohere API with retry logic for rate limits

**Independent Test**: Provide text chunks, generate embeddings, verify each chunk receives valid 1024-dim vector

### Implementation for User Story 2

- [ ] T029 [P] [US2] Implement Cohere client initialization with API key from environment in main.py
- [ ] T030 [P] [US2] Implement batch embedding function (embed 10-96 chunks per request) using cohere.embed() in main.py
- [ ] T031 [US2] Implement exponential backoff retry logic for Cohere API rate limits (429 errors) in main.py
- [ ] T032 [US2] Implement empty/short chunk filtering (skip chunks with <20 words) before embedding in main.py
- [ ] T033 [US2] Implement embedding vector validation (1024 dimensions, all floats) in main.py
- [ ] T034 [US2] Implement TextChunk update with embedding data (vector, embedded_at timestamp) in main.py
- [ ] T035 [US2] Implement logging for embedding progress (batches processed, chunks embedded, API calls) in main.py
- [ ] T036 [US2] Integrate embedding generation into main pipeline after chunking in main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should work - verify chunks have embeddings by logging sample vectors

---

## Phase 5: User Story 3 - Vector Storage (Priority: P3)

**Goal**: Store embeddings and metadata in Qdrant vector database with proper indexing

**Independent Test**: Store embeddings with metadata, perform vector similarity search, verify relevant chunks retrieved

### Implementation for User Story 3

- [ ] T037 [P] [US3] Implement Qdrant client initialization with URL and API key from environment in main.py
- [ ] T038 [P] [US3] Implement collection creation function with VectorParams (size=1024, distance=COSINE, HNSW m=16, ef_construct=100) in main.py
- [ ] T039 [P] [US3] Implement collection existence check to avoid re-creating existing collection in main.py
- [ ] T040 [P] [US3] Implement TextChunk to Qdrant point conversion (UUID, vector, payload) using to_qdrant_payload() in main.py
- [ ] T041 [US3] Implement batch upload function (100 vectors per batch) with retry logic in main.py
- [ ] T042 [US3] Implement progress tracking for batch uploads (batch N/total) in main.py
- [ ] T043 [US3] Implement TextChunk update with storage status (stored=True, qdrant_point_id) in main.py
- [ ] T044 [US3] Implement payload index creation for source_url and ingestion_run_id fields in main.py
- [ ] T045 [US3] Implement logging for storage progress (batches uploaded, total vectors stored) in main.py
- [ ] T046 [US3] Integrate vector storage into main pipeline after embedding in main.py

**Checkpoint**: All user stories 1-3 should work - verify vectors stored in Qdrant by checking collection size

---

## Phase 6: User Story 4 - Validation & Verification (Priority: P4)

**Goal**: Verify ingestion pipeline completed successfully and stored content is searchable with relevant results

**Independent Test**: Run validation queries, check statistics match expected counts, verify search returns relevant chunks

### Implementation for User Story 4

- [ ] T047 [P] [US4] Implement test query list (3-5 queries related to known documentation topics) in main.py
- [ ] T048 [P] [US4] Implement vector search function using Qdrant query with test queries in main.py
- [ ] T049 [US4] Implement search result validation (check top 5 results for relevance) in main.py
- [ ] T050 [US4] Implement ingestion statistics calculation (pages crawled, chunks created, embeddings generated, vectors stored) in main.py
- [ ] T051 [US4] Implement success rate calculation (chunks_stored / chunks_created) in main.py
- [ ] T052 [US4] Implement validation pass/fail logic (100% storage success, test queries return results) in main.py
- [ ] T053 [US4] Implement final summary report generation with IngestionMetadata.to_summary() in main.py
- [ ] T054 [US4] Implement logging for validation results (queries run, success rate, final status) in main.py
- [ ] T055 [US4] Integrate validation into main pipeline as final step in main.py

**Checkpoint**: Complete pipeline with validation - verify final summary shows 100% success and test queries work

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finalize implementation with error handling, configuration, and documentation

- [ ] T056 [P] Implement comprehensive error handling for all pipeline stages (crawl, chunk, embed, store, validate) in main.py
- [ ] T057 [P] Implement graceful shutdown and cleanup (finalize IngestionMetadata, close connections) in main.py
- [ ] T058 [P] Add command-line argument parsing (--base-url, --log-level, --skip-validation, --dry-run) in main.py
- [ ] T059 [P] Verify .env.example contains all variables with descriptions per quickstart.md
- [ ] T060 Create README.md with quickstart instructions referencing specs/001-doc-rag-ingestion/quickstart.md
- [ ] T061 Run full ingestion pipeline test using quickstart.md validation procedure
- [ ] T062 Verify all success criteria from spec.md are met (SC-001 through SC-010)
- [ ] T063 Code cleanup and add inline comments for complex logic sections in main.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3 → P4)
  - Limited parallelization due to single-file architecture (main.py)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Content Ingestion**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2) - Embedding Generation**: Depends on US1 chunks being created
- **User Story 3 (P3) - Vector Storage**: Depends on US2 embeddings being generated
- **User Story 4 (P4) - Validation**: Depends on US3 vectors being stored

### Within Each User Story

- Implementation order: Data structures → Functions → Integration → Logging
- Each story must be completed before moving to next priority
- Validate intermediate outputs (e.g., chunk count, embedding dimensions, storage count)

### Parallel Opportunities

**Limited parallelization due to single-file architecture:**

- Phase 1 Setup: Tasks T002, T003, T004 can be worked on in parallel (different files)
- Phase 2 Foundational: Tasks T006-T010 can be worked on in parallel (different functions in main.py)
- Within User Story 1: Tasks T013-T016, T019-T021 can be worked on in parallel (different functions)
- Within User Story 2: Tasks T029, T030 can be worked on in parallel
- Within User Story 3: Tasks T037-T040 can be worked on in parallel
- Within User Story 4: Tasks T047-T048 can be worked on in parallel
- Phase 7 Polish: Tasks T056-T059 can be worked on in parallel

**Note**: While functions can be developed in parallel, integration into main.py must be sequential within each user story.

---

## Parallel Example: User Story 1

```bash
# Launch function implementations in parallel (different functions):
Task T013: "Implement sitemap.xml parser function"
Task T014: "Implement recursive link crawler as fallback"
Task T015: "Implement URL filtering function"
Task T016: "Implement content hash deduplication tracking"

# These functions can be developed simultaneously and then integrated sequentially
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T028)
4. **STOP and VALIDATE**: Test crawling, extraction, and chunking independently
5. Deploy/demo if ready (chunks are created and validated)

### Incremental Delivery

1. **Setup + Foundational** → Foundation ready
2. **Add User Story 1** → Test independently → Chunks created ✓
3. **Add User Story 2** → Test independently → Embeddings generated ✓
4. **Add User Story 3** → Test independently → Vectors stored in Qdrant ✓
5. **Add User Story 4** → Test independently → Validation passes ✓
6. **Add Polish** → Production-ready system

Each story adds value and can be validated independently.

### Sequential Implementation (Recommended for Single Developer)

1. Team completes Setup + Foundational together
2. Complete User Story 1 → Verify chunks created
3. Complete User Story 2 → Verify embeddings added to chunks
4. Complete User Story 3 → Verify vectors in Qdrant
5. Complete User Story 4 → Verify validation passes
6. Complete Polish → Production-ready

---

## Validation Checkpoints

### After User Story 1 (Content Ingestion)
- [ ] Sitemap.xml is parsed successfully or fallback crawler works
- [ ] All pages are crawled (verify count matches sitemap)
- [ ] Content is cleaned (90%+ non-content removal per SC-002)
- [ ] Chunks are created (5-15 per page, 100-512 tokens per SC-003)
- [ ] Logging shows progress: "Created X chunks from Y pages"

### After User Story 2 (Embedding Generation)
- [ ] All chunks have embeddings (100% per SC-004)
- [ ] Embeddings are 1024 dimensions
- [ ] Retry logic handles rate limits gracefully (per SC-008)
- [ ] Logging shows: "Generated X embeddings in Y batches"

### After User Story 3 (Vector Storage)
- [ ] All embeddings stored in Qdrant (100% per SC-005)
- [ ] Collection configured correctly (COSINE distance, HNSW indexing)
- [ ] Payload includes all metadata fields from data-model.md
- [ ] Logging shows: "Stored X vectors in Y batches"

### After User Story 4 (Validation)
- [ ] Test queries return relevant results (top 5 per SC-006)
- [ ] Statistics report matches actual counts
- [ ] Validation passes (100% success rate)
- [ ] Final summary logged with run_id, duration, metrics

---

## Success Criteria Mapping

Each task maps to success criteria from spec.md:

| Success Criteria | Related Tasks |
|------------------|---------------|
| **SC-001**: All pages crawled | T013-T018 |
| **SC-002**: 90%+ non-content removed | T019-T020 |
| **SC-003**: Chunks 100-512 tokens | T023-T025 |
| **SC-004**: 100% chunks embedded | T029-T036 |
| **SC-005**: 100% embeddings stored | T037-T046 |
| **SC-006**: Top 5 results relevant | T047-T049 |
| **SC-007**: <30 min for 500 pages | T017-T018 (async crawling) |
| **SC-008**: Graceful error recovery | T009, T031, T041, T056 |
| **SC-009**: Progress logging | T026-T027, T035, T042, T045, T054 |
| **SC-010**: Environment config | T003, T007 |

---

## Notes

- **[P]** tasks = different functions/files, can develop in parallel (limited by single-file architecture)
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently testable via validation checkpoint
- Single-file architecture (main.py) limits parallelization - focus on sequential story completion
- Commit after completing each user story or logical group of tasks
- Stop at any checkpoint to validate story independently before proceeding
- **MVP = User Story 1 alone** provides crawling, cleaning, and chunking - can be used without embeddings/storage for analysis

---

## Task Count Summary

- **Total Tasks**: 63
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 7 tasks
- **Phase 3 (User Story 1)**: 16 tasks
- **Phase 4 (User Story 2)**: 8 tasks
- **Phase 5 (User Story 3)**: 10 tasks
- **Phase 6 (User Story 4)**: 9 tasks
- **Phase 7 (Polish)**: 8 tasks

**Parallel Opportunities**: 21 tasks marked [P] can be developed in parallel (different functions/files)

**Suggested MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1) = 28 tasks for minimal viable product

---

**Tasks Generated**: 2025-12-27
**Ready for Implementation**: Yes
**Estimated Completion** (sequential, single developer): Phases 1-3 (MVP) = 2-3 days; Full implementation = 4-5 days
