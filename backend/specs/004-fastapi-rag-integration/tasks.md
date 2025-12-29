# Tasks: FastAPI RAG Integration

**Input**: Design documents from `/specs/004-fastapi-rag-integration/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Tests**: Tests are NOT included in this task list as they were not explicitly requested in the feature specification. This implementation follows the direct integration approach without TDD.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/` for Python API, `src/` for React frontend
- Frontend exists and requires NO changes
- All tasks target `backend/` directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup for FastAPI integration

- [x] T001 Update backend/pyproject.toml to add FastAPI and Uvicorn dependencies (fastapi>=0.115.0, uvicorn[standard]>=0.32.0)
- [x] T002 [P] Install new dependencies using uv sync or pip install
- [x] T003 [P] Verify existing .env file contains required variables (OPENROUTER_API_KEY, QDRANT_API_KEY, QDRANT_URL)
- [x] T004 [P] Create backend/tests/ directory structure (test_api.py placeholder for future)

**Checkpoint**: Dependencies installed, environment configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Pydantic models and shared infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create backend/api.py with FastAPI app initialization and CORS middleware configuration for http://localhost:3000
- [x] T006 [P] Define ChatRequest Pydantic model in backend/api.py (question: str with min_length=1, max_length=1000)
- [x] T007 [P] Define ChatResponse Pydantic model in backend/api.py (answer: str, optional sources and metadata fields)
- [x] T008 [P] Define ErrorResponse Pydantic model in backend/api.py (error, message, detail fields)
- [x] T009 Import existing agent from backend/agent.py into backend/api.py for later use

**Checkpoint**: Foundation ready - FastAPI app initialized with models, CORS configured, agent imported

---

## Phase 3: User Story 1 - Query Submission and Response (Priority: P1) 🎯 MVP

**Goal**: Enable developers to submit queries via POST /chat and receive agent-generated responses with document retrieval

**Independent Test**: Send POST request to http://127.0.0.1:8000/chat with {"question": "What are prerequisites?"} and verify 200 OK response with {"answer": "..."}

**Why this is MVP**: This is the core functionality - without query submission and response, there is no integration. Frontend chatbot depends entirely on this endpoint.

### Implementation for User Story 1

- [x] T010 [US1] Create async query_agent() helper function in backend/api.py that invokes the agent from agent.py with a question string
- [x] T011 [US1] Implement POST /chat endpoint in backend/api.py that accepts ChatRequest and calls query_agent()
- [x] T012 [US1] Add response serialization to return ChatResponse with answer field from agent result
- [x] T013 [US1] Add basic try-except error handling for agent execution failures, returning 500 with ErrorResponse
- [x] T014 [US1] Add request logging (log incoming question, response time, status code) using Python logging module
- [x] T015 [US1] Test endpoint manually with curl: `curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"question": "What is physical AI?"}'`

**Checkpoint**: At this point, User Story 1 should be fully functional - frontend can send queries and receive answers

---

## Phase 4: User Story 2 - Error Handling and Validation (Priority: P2)

**Goal**: Provide clear error messages for validation failures, server issues, and agent errors

**Independent Test**: Send malformed requests (empty question, missing fields) and verify appropriate HTTP status codes (422, 400, 500) with descriptive error messages

**Why this priority**: Essential for developer experience and debugging, but the system can function with basic error handling from US1

### Implementation for User Story 2

- [ ] T016 [US2] Add validation for empty/whitespace-only questions in POST /chat, return 400 Bad Request with ErrorResponse
- [ ] T017 [US2] Enhance error handling to catch specific exceptions (TimeoutError, ConnectionError, ValueError) with appropriate HTTP status codes
- [ ] T018 [US2] Add detailed error logging with stack traces for 500 errors in backend/api.py
- [ ] T019 [US2] Create custom HTTPException handlers for agent-specific errors (retrieval failure, LLM API failure) in backend/api.py
- [ ] T020 [US2] Test error scenarios manually: empty question, agent failure simulation, timeout handling
- [ ] T021 [US2] Verify Pydantic validation errors return 422 with detailed field-level error messages (automatic FastAPI behavior - just verify)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - queries succeed with answers, errors fail gracefully with clear messages

---

## Phase 5: User Story 3 - API Documentation Access (Priority: P3)

**Goal**: Enable developers to explore endpoints, schemas, and test interactively via auto-generated docs

**Independent Test**: Navigate to http://127.0.0.1:8000/docs and verify Swagger UI displays /chat endpoint with request/response schemas and "Try it out" functionality

**Why this priority**: Improves developer experience but not required for basic integration - docs are auto-generated by FastAPI

### Implementation for User Story 3

- [ ] T022 [US3] Add title, description, and version metadata to FastAPI app initialization in backend/api.py (title="RAG Chatbot API", version="1.0.0")
- [ ] T023 [US3] Add docstrings to POST /chat endpoint describing parameters, responses, and examples
- [ ] T024 [US3] Add examples to Pydantic models using Config.json_schema_extra for ChatRequest and ChatResponse
- [ ] T025 [US3] Verify /docs endpoint auto-generates correct Swagger UI documentation (visit http://127.0.0.1:8000/docs)
- [ ] T026 [US3] Verify /redoc endpoint provides alternative ReDoc documentation view (visit http://127.0.0.1:8000/redoc)
- [ ] T027 [US3] Test "Try it out" functionality in Swagger UI by submitting a query and verifying real response

**Checkpoint**: All user stories complete - API is functional, robust, and well-documented

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final touches that improve the overall system quality

- [ ] T028 [P] Create GET /health endpoint in backend/api.py that returns health status, agent status, and vector DB connection status
- [ ] T029 [P] Add uvicorn.run() entrypoint to backend/api.py with __name__ == "__main__" block for easy local development (host=127.0.0.1, port=8000, reload=True)
- [ ] T030 [P] Update backend/README.md or create quickstart instructions documenting how to run the API server
- [ ] T031 Perform end-to-end integration test: Start backend (python backend/api.py), start frontend (npm start), open chatbot, send query, verify response
- [ ] T032 Performance verification: Send 10 concurrent requests and verify all complete in < 10 seconds
- [ ] T033 Code cleanup: Remove unused imports, add type hints, ensure consistent code style in backend/api.py

**Checkpoint**: Production-ready API with health checks, documentation, and validated performance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories ⚠️
- **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order: US1 (MVP) → US2 → US3
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories ✅
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Enhances US1 but independently testable ✅
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Documentation for US1/US2 but independently testable ✅

**Critical Path**: Setup → Foundational → US1 (MVP) → US2 → US3 → Polish

### Within Each User Story

- **US1**: query_agent() helper → POST /chat endpoint → response serialization → error handling → logging → manual test
- **US2**: All error handling tasks can run in parallel (T016-T019) → validation test (T020-T021)
- **US3**: All documentation tasks can run in parallel (T022-T024) → verification (T025-T027)

### Parallel Opportunities

**Phase 1 (Setup)**: T002, T003, T004 can run in parallel
**Phase 2 (Foundational)**: T006, T007, T008 can run in parallel (Pydantic models in same file but different classes)
**Phase 4 (US2)**: T016, T017, T018, T019 can run in parallel (different error handling concerns)
**Phase 5 (US3)**: T022, T023, T024 can run in parallel (different documentation aspects)
**Phase 6 (Polish)**: T028, T029, T030 can run in parallel

---

## Parallel Example: User Story 1 (MVP)

**Sequential dependencies** (must run in order):
```
T005 (FastAPI app init)
  → T006, T007, T008, T009 (models and imports - can run in parallel)
  → T010 (query_agent helper)
  → T011 (POST /chat endpoint)
  → T012 (response serialization)
  → T013 (error handling)
  → T014 (logging)
  → T015 (manual test)
```

**No parallel opportunities within US1** due to sequential dependencies (each task builds on previous)

---

## Parallel Example: User Story 2 (Error Handling)

**Parallel opportunities** (independent error handling concerns):
```bash
# Launch error handling tasks together:
Task T016: "Validate empty/whitespace questions"
Task T017: "Catch specific exception types"
Task T018: "Add detailed error logging"
Task T019: "Create custom HTTP exception handlers"

# Then run validation tasks:
Task T020: "Test error scenarios manually"
Task T021: "Verify Pydantic validation errors"
```

---

## Parallel Example: User Story 3 (Documentation)

**Parallel opportunities** (independent documentation updates):
```bash
# Launch documentation tasks together:
Task T022: "Add FastAPI app metadata"
Task T023: "Add endpoint docstrings"
Task T024: "Add Pydantic model examples"

# Then run verification tasks:
Task T025: "Verify Swagger UI"
Task T026: "Verify ReDoc"
Task T027: "Test Swagger Try it out"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - RECOMMENDED

1. Complete Phase 1: Setup (T001-T004) - ~5 minutes
2. Complete Phase 2: Foundational (T005-T009) - ~10 minutes
3. Complete Phase 3: User Story 1 (T010-T015) - ~20 minutes
4. **STOP and VALIDATE**:
   - Run `python backend/api.py`
   - Send test query: `curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"question": "What is physical AI?"}'`
   - Start frontend: `npm start`
   - Open chatbot and send query
   - Verify end-to-end integration works
5. **MVP COMPLETE** - Deploy/demo if ready (total time: ~35 minutes)

### Incremental Delivery

1. **Milestone 1**: Setup + Foundational (T001-T009) → Foundation ready (~15 minutes)
2. **Milestone 2**: Add User Story 1 (T010-T015) → Test independently → **MVP DEPLOYED** (~20 minutes)
3. **Milestone 3**: Add User Story 2 (T016-T021) → Test independently → Error handling complete (~15 minutes)
4. **Milestone 4**: Add User Story 3 (T022-T027) → Test independently → Documentation complete (~10 minutes)
5. **Milestone 5**: Add Polish (T028-T033) → Final validation → **PRODUCTION READY** (~15 minutes)

**Total estimated time**: ~75 minutes (1 hour 15 minutes)

### Parallel Team Strategy

With 2 developers:

1. **Together**: Complete Setup (Phase 1) and Foundational (Phase 2) - ~15 minutes
2. **Developer A**: User Story 1 (MVP) - ~20 minutes
3. **Developer B**: User Story 2 (Error Handling) - can start after Foundation - ~15 minutes
4. **Developer A** (after US1): User Story 3 (Documentation) - ~10 minutes
5. **Both**: Polish and integration testing - ~15 minutes

**Total time with parallelization**: ~45 minutes

---

## Task Count Summary

- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 5 tasks
- **Phase 3 (US1 - MVP)**: 6 tasks ← **CRITICAL PATH**
- **Phase 4 (US2)**: 6 tasks
- **Phase 5 (US3)**: 6 tasks
- **Phase 6 (Polish)**: 6 tasks

**Total**: 33 tasks

**Parallel tasks**: 13 tasks marked with [P]
**Sequential tasks**: 20 tasks (dependencies within stories)

---

## MVP Scope (Recommended First Iteration)

**Minimal Viable Product**: User Story 1 only (15 tasks total)

- Setup (4 tasks): T001-T004
- Foundational (5 tasks): T005-T009
- User Story 1 (6 tasks): T010-T015

**Delivers**: Working API that accepts queries and returns agent responses - frontend chatbot fully functional

**Excludes** (add later):
- Comprehensive error handling (US2)
- API documentation enhancements (US3)
- Health checks and polish (Phase 6)

**Why this is sufficient for MVP**: The frontend chatbot already has basic error handling ("Backend not reachable" fallback). FastAPI provides auto-docs by default. US1 alone enables the core use case.

---

## Validation Checklist

**After US1 (MVP)**:
- [ ] Backend starts without errors: `python backend/api.py`
- [ ] curl test succeeds with 200 OK and valid answer
- [ ] Frontend chatbot receives and displays answers
- [ ] Response time < 10 seconds for typical queries

**After US2 (Error Handling)**:
- [ ] Empty question returns 400 Bad Request
- [ ] Missing field returns 422 Unprocessable Entity
- [ ] Agent failure returns 500 with descriptive error
- [ ] All errors logged with stack traces

**After US3 (Documentation)**:
- [ ] /docs endpoint loads Swagger UI
- [ ] /redoc endpoint loads ReDoc
- [ ] Schemas show request/response examples
- [ ] "Try it out" executes real queries

**After Phase 6 (Polish)**:
- [ ] /health endpoint returns healthy status
- [ ] 10 concurrent requests complete successfully
- [ ] End-to-end integration test passes
- [ ] Code is clean and well-documented

---

## Notes

- **[P]** tasks can run in parallel (different concerns, no file conflicts)
- **[Story]** labels map tasks to user stories for traceability
- Each user story is independently testable
- No frontend changes required - all work in `backend/api.py` (single file ~150 lines)
- Avoid: modifying existing files (agent.py, retrieve_main.py, frontend components)
- Commit strategy: After each user story completion (T015, T021, T027, T033)
- The entire implementation is a single file (`backend/api.py`) with models, endpoints, and error handling
