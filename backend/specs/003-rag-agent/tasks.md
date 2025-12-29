# Tasks: RAG Agent with OpenAI SDK

**Input**: Design documents from `specs/003-rag-agent/`
**Prerequisites**: plan.md, spec.md, data-model.md, quickstart.md

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story this task belongs to (US1, US2, US3)
- File paths: `backend/` directory (single-file architecture: `agent.py`)

---

## Phase 1: Setup

**Purpose**: Create `agent.py` skeleton with basic imports and configuration

- [X] T001 Create `backend/agent.py` with module docstring and imports (openai, retrieve.main, dotenv, json, uuid)
- [X] T002 Add OPENAI_API_KEY and OPENAI_MODEL to `backend/.env` file
- [X] T003 Implement configuration loading in `backend/agent.py` (reuse load_config from spec-2, add OpenAI validation)
- [X] T004 [P] Define system prompt in `backend/agent.py` with strict "retrieved content only" rules
- [X] T005 [P] Define retrieval tool schema in `backend/agent.py` (OpenAI function calling format)

---

## Phase 2: Foundational

**Purpose**: Core tool handler and basic agent initialization

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement `execute_retrieval_tool()` function in `backend/agent.py` calling spec-2 embed_query + search_similar_chunks
- [X] T007 Implement `format_tool_response()` in `backend/agent.py` to convert RetrievalResult to JSON for agent
- [X] T008 Add error handling to tool handler in `backend/agent.py` (try/except returning error messages)
- [X] T009 Initialize OpenAI client in `backend/agent.py` with API key from config
- [X] T010 Implement basic message handling in `backend/agent.py` (create messages array with system prompt)

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Basic Question Answering with Retrieval (Priority: P1) 🎯 MVP

**Goal**: Agent answers questions using retrieved book content only

**Independent Test**: Run agent with question "What are the prerequisites?" and verify retrieval + answer with citations

### Implementation for User Story 1

- [X] T011 [US1] Implement `ask_question()` function in `backend/agent.py` that sends user message to OpenAI
- [X] T012 [US1] Add tool call handling in `backend/agent.py` (detect when agent requests retrieve_documentation)
- [X] T013 [US1] Execute retrieval tool when requested and append tool response to messages in `backend/agent.py`
- [X] T014 [US1] Handle agent's final answer in `backend/agent.py` (extract and return assistant message)
- [X] T015 [US1] Implement single-question CLI mode in `backend/agent.py` (accept question as argument)

**Checkpoint**: Agent can answer single questions using retrieval (SC-001: correct answers, SC-003: off-topic handling)

---

## Phase 4: User Story 2 - Multi-Turn Conversation (Priority: P2)

**Goal**: Agent maintains context across multiple questions

**Independent Test**: Ask "What is Chapter 1 about?" then "What comes next?" and verify context understanding

### Implementation for User Story 2

- [X] T016 [US2] Implement conversation loop in `backend/agent.py` (accept multiple questions in sequence)
- [X] T017 [US2] Add conversation state tracking in `backend/agent.py` (messages array persists across turns)
- [X] T018 [US2] Implement interactive mode in `backend/agent.py` (prompt for questions until 'quit')
- [X] T019 [US2] Add turn counter in `backend/agent.py` to track conversation length

**Checkpoint**: Multi-turn conversations work (SC-002: follow-up questions, SC-007: 10+ turn coherence)

---

## Phase 5: User Story 3 - Source Citations (Priority: P3)

**Goal**: Agent responses include transparent source citations

**Independent Test**: Ask any question and verify response includes "According to Chapter X" or source URLs

### Implementation for User Story 3

- [X] T020 [US3] Update system prompt in `backend/agent.py` to explicitly request citations in answers
- [X] T021 [US3] Enhance tool response formatting in `backend/agent.py` to highlight page_title and section_heading
- [X] T022 [US3] Add citation verification to response handling in `backend/agent.py` (ensure metadata passed to agent)

**Checkpoint**: Answers include source citations (SC-005: 90%+ citation rate)

---

## Phase 6: Polish & Validation

**Purpose**: Final refinements and documentation

- [X] T023 [P] Update `backend/README.md` with "RAG Agent" section describing agent.py usage
- [ ] T024 Test single-question mode: `uv run python agent.py "What are the prerequisites?"`
- [ ] T025 Test interactive mode: conduct 5-turn conversation with follow-up questions
- [ ] T026 Test off-topic handling: ask 3 unrelated questions, verify "I don't have information" responses
- [ ] T027 Verify all 7 success criteria pass (SC-001 to SC-007 per spec.md)

**Checkpoint**: All acceptance criteria met, agent ready for production use

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories are sequential by priority (P1 → P2 → P3) but independent
  - Each story can be tested standalone
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Builds on US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational - Enhances US1/US2 but independently testable

### Within Each User Story

- All implementation tasks are sequential within a story (single file `agent.py`)
- Must complete story's functions before moving to next story
- Each story checkpoint validates independent functionality

### Parallel Opportunities

- **Setup tasks marked [P]** (T004, T005): Can define system prompt and tool schema in parallel
- **Polish tasks marked [P]** (T023): README update independent of testing tasks

**Note**: Limited parallelism due to single-file architecture - most tasks are sequential within the file

---

## Parallel Example: Setup Phase

```bash
# Launch system prompt and tool schema definition together:
Task T004: "Define system prompt in backend/agent.py with strict rules"
Task T005: "Define retrieval tool schema in backend/agent.py for OpenAI"

# These can be written concurrently as separate constants in the file
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T010) - CRITICAL
3. Complete Phase 3: User Story 1 (T011-T015)
4. **STOP and VALIDATE**: Test single-question mode independently
5. Verify SC-001: Agent answers correctly using retrieved content

**MVP Deliverable**: Single-question agent that retrieves and answers using book content only

### Incremental Delivery

1. **Foundation** (Phase 1-2): Basic structure + tool handler → Can execute retrieval
2. **+ User Story 1** (Phase 3): Single questions → Can answer using retrieved content (MVP!)
3. **+ User Story 2** (Phase 4): Multi-turn → Can handle conversations with context
4. **+ User Story 3** (Phase 5): Citations → Can provide transparent source references
5. **+ Polish** (Phase 6): Production-ready agent with documentation

Each increment adds value and is independently testable.

### Sequential Strategy (Single Developer)

With single developer (single-file architecture):

1. Complete Setup + Foundational (T001-T010)
2. Implement User Story 1 (T011-T015) → Test checkpoint
3. Implement User Story 2 (T016-T019) → Test checkpoint
4. Implement User Story 3 (T020-T022) → Test checkpoint
5. Polish and validate (T023-T027)

**Timeline**: ~60 minutes total (per plan.md estimate: 25 + 25 + 10 minutes)

---

## Success Criteria Mapping

| Task Range | User Story | Success Criteria |
|------------|-----------|------------------|
| T011-T015 | US1 | SC-001: Correct answers, SC-003: Off-topic handling, SC-004: <5s response time |
| T016-T019 | US2 | SC-002: Multi-turn context, SC-007: 10+ turn coherence |
| T020-T022 | US3 | SC-005: 90%+ citation rate, SC-006: Tool integration |
| T023-T027 | Polish | All SC-001 to SC-007 verified |

---

## Notes

- **Single-file architecture**: All tasks modify `backend/agent.py` (simpler but limits parallelism)
- **[P] tasks**: Different sections of the file, can be written concurrently
- **[Story] label**: Maps task to user story for traceability and independent testing
- **Checkpoints**: Test each user story independently before proceeding
- **Concise**: Task descriptions focused on specific implementation actions (per user request)
- **File paths**: All tasks reference exact location (`backend/agent.py`)
- **Dependencies**: .env must have valid credentials from spec-1/2 + new OPENAI_API_KEY
- **Code reuse**: Import functions from `retrieve.main.py` (no duplication)

---

## Total Tasks: 27

- **Setup**: 5 tasks (T001-T005)
- **Foundational**: 5 tasks (T006-T010)
- **User Story 1**: 5 tasks (T011-T015)
- **User Story 2**: 4 tasks (T016-T019)
- **User Story 3**: 3 tasks (T020-T022)
- **Polish**: 5 tasks (T023-T027)

**Parallel Opportunities**: 3 tasks can run in parallel (marked with [P])

**MVP Scope**: Phases 1-3 (15 tasks, ~50 minutes) delivers single-question agent

**Full Feature**: All 27 tasks (~60 minutes per plan.md estimate)
