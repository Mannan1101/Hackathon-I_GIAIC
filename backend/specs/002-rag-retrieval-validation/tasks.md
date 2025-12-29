# Tasks: RAG Retrieval Validation

**Input**: Design documents from `specs/002-rag-retrieval-validation/`
**Prerequisites**: plan.md, spec.md, data-model.md, quickstart.md

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story this task belongs to (US1, US2, US3, US4)
- File paths: `backend/` directory (single-file architecture: `retrieve.main.py`)

---

## Phase 1: Setup

**Purpose**: Create `retrieve.main.py` skeleton and basic structure

- [x] T001 Create `backend/retrieve.main.py` with module docstring and imports (qdrant-client, cohere, python-dotenv, tenacity, dataclasses, logging)
- [x] T002 Configure logging in `backend/retrieve.main.py` (same format as main.py: `[%(asctime)s] %(levelname)s - %(message)s`)
- [x] T003 [P] Define `RetrievalQuery` dataclass in `backend/retrieve.main.py` with fields: query_text, top_k, similarity_threshold, query_id, created_at
- [x] T004 [P] Define `RetrievalResult` dataclass in `backend/retrieve.main.py` with fields: query_id, chunk_text, source_url, page_title, section_heading, breadcrumb, chunk_index, similarity_score, metadata, rank
- [x] T005 [P] Define `ValidationReport` dataclass in `backend/retrieve.main.py` with fields: run_id, total_queries, successful_queries, failed_queries, avg_similarity_score, avg_query_time, metadata_completeness, total_results_retrieved, connection_status, collection_stats, errors, started_at, completed_at

---

## Phase 2: Foundational

**Purpose**: Core infrastructure for all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Implement `load_config()` function in `backend/retrieve.main.py` to load QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, COHERE_API_KEY, COHERE_MODEL from .env
- [x] T007 Validate required environment variables in `load_config()` (raise ValueError if missing)
- [x] T008 [P] Create `retry_db` decorator in `backend/retrieve.main.py` for Qdrant operations (3 attempts, exponential backoff 2-10s)
- [x] T009 [P] Create `retry_api` decorator in `backend/retrieve.main.py` for Cohere operations (3 attempts, exponential backoff 2-10s)
- [x] T010 Define `TEST_QUERIES` list in `backend/retrieve.main.py` with 10 queries: 5 specific, 3 broad, 2 negative

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Vector Database Connection Validation (Priority: P1) 🎯 MVP

**Goal**: Verify Qdrant connection and collection exists with correct metadata

**Independent Test**: Run connection validation, verify it reports vector count >0, dimensions=1024, distance=COSINE in <5 seconds

### Implementation for User Story 1

- [x] T011 [US1] Implement `validate_connection()` function in `backend/retrieve.main.py` to initialize Qdrant client and check collection exists
- [x] T012 [US1] Add collection metadata retrieval in `validate_connection()` (vector count, dimensions, distance metric)
- [x] T013 [US1] Add connection error handling in `validate_connection()` with clear error messages (connection failures, collection not found)
- [x] T014 [US1] Add logging for connection validation in `backend/retrieve.main.py` ([CONNECTION] prefix: attempt, stats, success/failure)
- [x] T015 [US1] Return collection stats dictionary from `validate_connection()` with keys: collection_name, vector_count, vector_dim, distance, collection_exists

**Checkpoint**: Connection validation works independently (SC-001: <5 seconds)

---

## Phase 4: User Story 2 - Query-Based Retrieval Testing (Priority: P2)

**Goal**: Execute semantic search queries and return ranked results with metadata

**Independent Test**: Run test query "How do I get started?", verify top-5 results returned with avg similarity >0.7 in <2 seconds

### Implementation for User Story 2

- [x] T016 [US2] Implement `embed_query()` function in `backend/retrieve.main.py` to generate embeddings with Cohere (input_type="search_query")
- [x] T017 [US2] Add `@retry_api` decorator to `embed_query()` for API resilience
- [x] T018 [US2] Implement `search_similar_chunks()` function in `backend/retrieve.main.py` using client.search() with query_vector
- [x] T019 [US2] Add `@retry_db` decorator to `search_similar_chunks()` for database resilience
- [x] T020 [US2] Parse Qdrant search results in `search_similar_chunks()` and convert to `RetrievalResult` objects (extract payload fields, similarity score, rank)
- [x] T021 [US2] Add logging for query execution in `backend/retrieve.main.py` ([QUERY] prefix: query text, result count, top score, execution time)
- [x] T022 [US2] Handle empty results case in `search_similar_chunks()` (return empty list, log warning)
- [x] T023 [US2] Handle low-scoring results case (<0.5) in `search_similar_chunks()` (log info message, include in results)

**Checkpoint**: Query execution returns ranked results (SC-002: avg similarity >0.7, SC-004: <2s per query)

---

## Phase 5: User Story 3 - Metadata and Source Verification (Priority: P3)

**Goal**: Validate retrieved chunks have complete metadata and valid source URLs

**Independent Test**: Execute query, verify 100% of results have chunk_text, source_url, page_title fields present

### Implementation for User Story 3

- [x] T024 [US3] Implement `validate_metadata()` function in `backend/retrieve.main.py` to check required fields (chunk_text, source_url, page_title) in all results
- [x] T025 [US3] Calculate metadata completeness percentage in `validate_metadata()` (count of complete results / total results)
- [x] T026 [US3] Add URL format validation in `validate_metadata()` (check source_url is valid URL structure)
- [x] T027 [US3] Track missing fields per result in `validate_metadata()` (return list of missing field names)
- [x] T028 [US3] Add logging for metadata validation in `backend/retrieve.main.py` ([METADATA] prefix: completeness %, missing fields, invalid URLs)

**Checkpoint**: Metadata validation works (SC-003: 100% completeness, SC-006: valid URLs)

---

## Phase 6: User Story 4 - End-to-End Pipeline Validation (Priority: P4)

**Goal**: Run comprehensive validation suite with all test queries and generate report

**Independent Test**: Execute 10 test queries, verify validation report shows success rate, avg metrics, completes in <20 seconds

### Implementation for User Story 4

- [x] T029 [US4] Implement `run_validation_suite()` function in `backend/retrieve.main.py` to execute all TEST_QUERIES
- [x] T030 [US4] Initialize `ValidationReport` in `run_validation_suite()` with run_id and timestamps
- [x] T031 [US4] Add query execution loop in `run_validation_suite()` (iterate TEST_QUERIES, call embed_query + search_similar_chunks, track timing)
- [x] T032 [US4] Collect all `RetrievalResult` objects in `run_validation_suite()` across all queries
- [x] T033 [US4] Handle query failures in `run_validation_suite()` (catch exceptions, add to errors list, continue execution)
- [x] T034 [US4] Calculate metrics in `run_validation_suite()` (total_queries, successful_queries, failed_queries, avg_similarity_score, avg_query_time)
- [x] T035 [US4] Call `validate_metadata()` in `run_validation_suite()` and add metadata_completeness to report
- [x] T036 [US4] Implement `ValidationReport.to_summary()` method in `backend/retrieve.main.py` to format human-readable report (connection status, query metrics, retrieval quality, metadata validation, errors)
- [x] T037 [US4] Implement `main()` entry point in `backend/retrieve.main.py` (load_config, validate_connection, run_validation_suite, print summary)
- [x] T038 [US4] Add `if __name__ == "__main__"` block in `backend/retrieve.main.py` to call main()

**Checkpoint**: End-to-end validation suite works (SC-004: 10 queries <20s, SC-005: report displays all metrics)

---

## Phase 7: Polish & Validation

**Purpose**: Final checks and documentation

- [x] T039 [P] Verify `backend/retrieve.main.py` syntax with `python -m py_compile backend/retrieve.main.py`
- [ ] T040 [P] Test connection validation: run `uv run python backend/retrieve.main.py` with valid .env, verify connection succeeds
- [ ] T041 Test specific query: verify query "How do I get started?" returns avg similarity >0.7
- [ ] T042 Test negative query: verify query "What is the weather?" returns low scores <0.5 or empty results (SC-008)
- [ ] T043 Test error handling: run with invalid Qdrant URL, verify graceful error message (SC-007)
- [ ] T044 Verify all 8 success criteria pass (SC-001 to SC-008 per spec.md)
- [x] T045 [P] Update `backend/README.md` with "Validation" section describing retrieve.main.py usage

**Checkpoint**: All acceptance criteria met, validation script ready for use

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories are sequential by priority (P1 → P2 → P3 → P4) due to single-file architecture
  - Each story builds on previous validation capabilities
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Uses connection from US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational - Validates results from US2 but independently testable
- **User Story 4 (P4)**: Can start after Foundational - Integrates all previous stories into suite

### Within Each User Story

- All implementation tasks are sequential within a story (single file `retrieve.main.py`)
- Must complete story's functions before moving to next story
- Each story checkpoint validates independent functionality

### Parallel Opportunities

- **Setup tasks marked [P]** (T003, T004, T005): Can define dataclasses in parallel
- **Foundational tasks marked [P]** (T008, T009): Can create retry decorators in parallel
- **Polish tasks marked [P]** (T039, T040, T045): Can run syntax check, connection test, README update in parallel

**Note**: Limited parallelism due to single-file architecture - most tasks are sequential within the file

---

## Parallel Example: Setup Phase

```bash
# Launch all dataclass definitions together:
Task T003: "Define RetrievalQuery dataclass in backend/retrieve.main.py"
Task T004: "Define RetrievalResult dataclass in backend/retrieve.main.py"
Task T005: "Define ValidationReport dataclass in backend/retrieve.main.py"

# These can be written concurrently as separate class definitions
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T010) - CRITICAL
3. Complete Phase 3: User Story 1 (T011-T015)
4. **STOP and VALIDATE**: Test connection validation independently
5. Verify SC-001: Connection completes <5 seconds

**MVP Deliverable**: Connection validation script that verifies Qdrant collection exists

### Incremental Delivery

1. **Foundation** (Phase 1-2): Basic structure + config → Can load environment
2. **+ User Story 1** (Phase 3): Connection validation → Can verify collection exists (MVP!)
3. **+ User Story 2** (Phase 4): Query execution → Can retrieve relevant chunks
4. **+ User Story 3** (Phase 5): Metadata validation → Can verify data quality
5. **+ User Story 4** (Phase 6): Full validation suite → Can run comprehensive tests
6. **+ Polish** (Phase 7): Production-ready validation script

Each increment adds value and is independently testable.

### Sequential Strategy (Single Developer)

With single developer (single-file architecture):

1. Complete Setup + Foundational (T001-T010)
2. Implement User Story 1 (T011-T015) → Test checkpoint
3. Implement User Story 2 (T016-T023) → Test checkpoint
4. Implement User Story 3 (T024-T028) → Test checkpoint
5. Implement User Story 4 (T029-T038) → Test checkpoint
6. Polish and validate (T039-T045)

**Timeline**: ~110 minutes total (per plan.md estimate)

---

## Success Criteria Mapping

| Task Range | User Story | Success Criteria |
|------------|-----------|------------------|
| T011-T015 | US1 | SC-001: Connection validation <5s |
| T016-T023 | US2 | SC-002: Avg similarity >0.7, SC-004: Query <2s, FR-003: Top-k results, FR-004: Similarity scores |
| T024-T028 | US3 | SC-003: 100% metadata, SC-006: Valid URLs, FR-005: Complete metadata |
| T029-T038 | US4 | SC-004: 10 queries <20s, SC-005: Validation report, SC-007: Error handling, SC-008: Negative queries |
| T039-T045 | Polish | All SC-001 to SC-008 verified |

---

## Notes

- **Single-file architecture**: All tasks modify `backend/retrieve.main.py` (simpler but limits parallelism)
- **[P] tasks**: Different sections of the file, can be written concurrently
- **[Story] label**: Maps task to user story for traceability and independent testing
- **Checkpoints**: Test each user story independently before proceeding
- **Concise**: Task descriptions focused on specific implementation actions
- **File paths**: All tasks reference exact location (`backend/retrieve.main.py`)
- **Dependencies**: .env must have valid credentials from spec-1 (001-doc-rag-ingestion)
- **Testing**: Validation script validates itself by running test queries

---

## Total Tasks: 45

- **Setup**: 5 tasks (T001-T005)
- **Foundational**: 5 tasks (T006-T010)
- **User Story 1**: 5 tasks (T011-T015)
- **User Story 2**: 8 tasks (T016-T023)
- **User Story 3**: 5 tasks (T024-T028)
- **User Story 4**: 10 tasks (T029-T038)
- **Polish**: 7 tasks (T039-T045)

**Parallel Opportunities**: 6 tasks can run in parallel (marked with [P])

**MVP Scope**: Phases 1-3 (15 tasks, ~45 minutes) delivers connection validation

**Full Feature**: All 45 tasks (~110 minutes per plan.md estimate)
