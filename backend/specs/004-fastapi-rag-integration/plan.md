# Implementation Plan: FastAPI RAG Integration

**Branch**: `004-fastapi-rag-integration` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-fastapi-rag-integration/spec.md`

## Summary

Build a FastAPI REST API server (`api.py`) that exposes the existing RAG agent (from `agent.py`) as a web service. The frontend (Docusaurus-based chatbot UI) already exists and makes POST requests to `http://127.0.0.1:8000/chat`. The integration connects this existing UI to the backend RAG agent, enabling users to query the Physical AI & Humanoid Robotics textbook through a chat interface accessible on every page.

**Key insight**: The frontend chatbot component is already implemented and configured in the Docusaurus site. It expects a `/chat` endpoint that accepts JSON `{question: string}` and returns `{answer: string}`. The backend task is to create `api.py` that bridges this frontend to the agent in `agent.py`.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.115+, Uvicorn (ASGI server), python-dotenv, openai-agents SDK, existing agent.py and retrieve_main.py modules
**Storage**: SQLite (conversations.db - already used by agent.py for session management)
**Testing**: pytest with httpx (AsyncClient for FastAPI testing)
**Target Platform**: Local development server (Linux/Windows/macOS)
**Project Type**: Web application (existing Docusaurus frontend + new FastAPI backend)
**Performance Goals**: < 10 seconds response time per query, support 10+ concurrent requests
**Constraints**: < 200ms API overhead (excluding agent processing time), CORS enabled for localhost origins
**Scale/Scope**: Single developer local setup, ~100 lines of API code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Since the constitution template is not filled, applying standard best practices:

### Gates

- ✅ **Simplicity**: Single-purpose API file (`api.py`) with minimal dependencies
- ✅ **Testability**: FastAPI provides automatic OpenAPI docs and test client support
- ✅ **Reusability**: Agent functionality remains in `agent.py`; API is a thin wrapper
- ✅ **No Over-Engineering**: Direct integration without unnecessary abstraction layers
- ⚠️ **Test-First**: Will create tests before implementation (Phase 2 tasks)

**Status**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/004-fastapi-rag-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-spec.yaml    # OpenAPI 3.0 specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
hackathon_1-main/
├── backend/
│   ├── api.py                    # NEW: FastAPI server (this feature)
│   ├── agent.py                  # EXISTING: RAG agent from spec-003
│   ├── retrieve_main.py          # EXISTING: Retrieval from spec-002
│   ├── main.py                   # EXISTING: Document ingestion from spec-001
│   ├── conversations.db          # EXISTING: SQLite session storage
│   ├── pyproject.toml            # UPDATE: Add FastAPI dependencies
│   └── tests/
│       ├── test_api.py           # NEW: API endpoint tests
│       └── test_integration.py   # NEW: End-to-end integration tests
│
├── src/
│   ├── components/
│   │   └── Chatbot/
│   │       ├── index.js          # EXISTING: Frontend chatbot UI (NO CHANGES)
│   │       └── styles.module.css # EXISTING: Chatbot styles (NO CHANGES)
│   └── clientModules/
│       └── chatbot.js            # EXISTING: Chatbot injection (NO CHANGES)
│
├── docusaurus.config.js          # EXISTING: Docusaurus config (NO CHANGES)
└── package.json                  # EXISTING: Frontend dependencies (NO CHANGES)
```

**Structure Decision**: Web application architecture is already established. Frontend (Docusaurus + React chatbot) is complete and functional. Backend needs only the API layer (`api.py`) to connect the existing agent to the existing frontend. No frontend changes required - the chatbot UI already makes the correct API calls.

## Complexity Tracking

*No constitutional violations detected. Table omitted per template guidance.*

---

## Phase 0: Research & Architectural Decisions

**Objective**: Resolve all technical unknowns and document architectural decisions

### Research Areas

1. **FastAPI Integration Patterns**
   - How to call async agent functions from FastAPI endpoints
   - Error handling best practices for agent failures
   - CORS configuration for local development
   - Logging integration with existing agent logging

2. **Agent Invocation Strategy**
   - Single-turn vs multi-turn conversation handling
   - Session management alignment with agent.py's SQLiteSession
   - Timeout handling for long-running queries
   - Agent initialization and lifecycle management

3. **Request/Response Format**
   - Exact contract expected by frontend (already known: `{question}` → `{answer}`)
   - Error response format for validation failures
   - Optional metadata (sources, confidence, retrieval context)

4. **Deployment & Development Workflow**
   - Uvicorn configuration for local development
   - Hot reload during development
   - Environment variable management
   - Port configuration (frontend expects 8000)

**Output**: `research.md` with decisions for each area above

---

## Phase 1: Design & Contracts

**Objective**: Define data models and API contracts

### 1. Data Model (`data-model.md`)

Document the request/response schemas and error formats:

**Entities**:
- `ChatRequest`: Input from frontend
- `ChatResponse`: Success response with agent answer
- `ErrorResponse`: Error details with status codes

### 2. API Contracts (`contracts/api-spec.yaml`)

OpenAPI 3.0 specification for:
- `POST /chat`: Main query endpoint
- `GET /health`: Health check endpoint
- `GET /docs`: Auto-generated API documentation (FastAPI default)

### 3. Quickstart Guide (`quickstart.md`)

Developer guide covering:
- Installation and dependency setup
- Starting the FastAPI server
- Testing the integration with the frontend
- Using the interactive API docs
- Troubleshooting common issues

### 4. Agent Context Update

Run agent context update script to document FastAPI usage in project context.

**Output**: `data-model.md`, `contracts/api-spec.yaml`, `quickstart.md`, updated agent context

---

## Phase 2: Task Breakdown (NOT in /sp.plan - deferred to /sp.tasks)

Phase 2 is executed by the `/sp.tasks` command and will generate `tasks.md` with:
- RED phase: Write failing tests for each endpoint
- GREEN phase: Implement api.py to pass tests
- REFACTOR phase: Optimize error handling and logging

---

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design artifacts completion*

Verification results:
- ✅ **API design remains simple**: Single `api.py` file with 3 endpoints, minimal dependencies (FastAPI, Uvicorn)
- ✅ **Agent responsibility separation maintained**: API is a thin wrapper; all RAG logic stays in `agent.py`
- ✅ **Test coverage plan exists**: `data-model.md` and `quickstart.md` define test strategy (unit + integration tests)
- ✅ **No premature optimization**: Stateless single-turn queries, no caching/sessions/advanced features
- ✅ **Clear contracts**: OpenAPI spec, Pydantic models, explicit error handling
- ✅ **Developer-friendly**: Comprehensive quickstart guide, interactive API docs, troubleshooting section

**Status**: ✅ PASSED - Design adheres to simplicity and separation of concerns principles

---

## Dependencies & Integration Points

### Upstream Dependencies
- **spec-001**: Document ingestion → Vector DB must be populated
- **spec-002**: Retrieval pipeline → `retrieve_main.py` must be functional
- **spec-003**: RAG Agent → `agent.py` must be operational

### Integration Points
- **Frontend**: Existing Docusaurus chatbot at `src/components/Chatbot/index.js`
  - Expects: `POST http://127.0.0.1:8000/chat` with `{question: string}`
  - Receives: `{answer: string}` on success, error message on failure

- **Backend Agent**: `agent.py` exports agent creation and run functions
  - Must adapt synchronous FastAPI endpoint to async agent execution
  - Must handle agent errors and convert to HTTP error responses

### Environment Configuration
- `.env` file must contain:
  - `OPENROUTER_API_KEY`: For LLM access
  - `QDRANT_API_KEY`: For vector database access
  - `QDRANT_URL`: Vector database endpoint
  - Additional agent configuration from spec-003

---

## Success Criteria Mapping

| Success Criterion | Design Element |
|-------------------|----------------|
| SC-001: < 10s response time | Async agent invocation, no blocking operations |
| SC-002: 10+ concurrent requests | Uvicorn async workers, FastAPI async endpoints |
| SC-003: 95% success rate | Comprehensive error handling, input validation |
| SC-004: 2-minute debugging | Detailed error messages, structured logging |
| SC-005: 5-minute onboarding | quickstart.md with step-by-step instructions |
| SC-006: Zero-config integration | Sensible defaults, clear .env.example |

---

## Risk Analysis

| Risk | Mitigation |
|------|------------|
| Agent initialization time delays first request | Lazy initialization on startup, health check warmup |
| Frontend-backend CORS issues | Explicit CORS middleware configuration |
| Long queries timeout | Configurable timeout with graceful error response |
| Concurrent request resource contention | Async/await pattern, connection pooling |
| Agent errors crash the API | Try-catch wrapper, return 500 with details |

---

## Notes

**Frontend Status**: The Docusaurus chatbot UI is already fully implemented and expects:
- Endpoint: `http://127.0.0.1:8000/chat`
- Method: POST
- Request: `{"question": "..."}`
- Response: `{"answer": "..."}`
- Error fallback: Displays "Backend not reachable" message

**Implementation Focus**: This feature is backend-only. The task is to create `api.py` that:
1. Initializes FastAPI with CORS
2. Defines `/chat` endpoint matching frontend expectations
3. Invokes agent from `agent.py` with the question
4. Returns the agent's response as JSON
5. Handles errors gracefully with appropriate HTTP status codes

**No Frontend Changes Required**: The chatbot UI and Docusaurus configuration are complete and working as-is.
