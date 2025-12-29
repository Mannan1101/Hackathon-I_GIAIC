# Implementation Plan: RAG Agent with OpenAI SDK

**Branch**: `003-rag-agent` | **Date**: 2025-12-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-rag-agent/spec.md`
**User Directive**: "create a single 'agent.py' file in backend folder - initialize an agent using the OpenAI Agent SDK - integrate retrieval by calling the existing Qdrant search logic - Ensure the agent responds using retrieved book content only"

---

## Summary

Build an AI agent using OpenAI Agents SDK that answers questions about book content by orchestrating retrieval from Qdrant. The agent will call retrieval tools that reuse existing validated retrieval pipeline from spec-2, maintain multi-turn conversation context, and generate answers using only retrieved chunks without hallucination.

**Technical Approach** (from research):
- Single-file architecture (`agent.py`) consistent with spec-1/2 pattern
- OpenAI Agents SDK with function calling for retrieval tool integration
- Reuse spec-2 retrieval functions (embed_query, search_similar_chunks) without modification
- System prompt engineering to enforce "retrieved content only" constraint
- Conversation history management via OpenAI SDK built-in context

---

## Technical Context

**Language/Version**: Python 3.11+ (consistent with spec-1/2)
**Primary Dependencies**:
- openai (OpenAI Agents SDK / function calling)
- qdrant-client (reused from spec-2)
- cohere (reused from spec-2)
- python-dotenv (reused from spec-2)

**Storage**: Qdrant Cloud (existing 'documentation' collection from spec-1)
**Testing**: Manual CLI testing (per user constraints - no automated test framework)
**Target Platform**: Command-line interface (local Python execution)
**Project Type**: Single-file CLI script (backend/agent.py)
**Performance Goals**: <5 seconds per question-answer cycle (SC-004)
**Constraints**:
- Must reuse spec-2 retrieval pipeline without modification
- Answers must use ONLY retrieved chunks (no hallucination)
- No web UI, FastAPI, authentication (per spec out-of-scope)
- Minimal scope: 2-3 implementation tasks

**Scale/Scope**:
- Single developer user per session
- 10-15 turn conversations typical
- 5-10 questions per session
- 34 embedded chunks in Qdrant (from current ingestion)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Status**: Template constitution not populated - using project-wide development best practices

**Development Principles Applied**:
1. ✅ **Single-file architecture**: Consistent with spec-1 (main.py) and spec-2 (retrieve.main.py) patterns
2. ✅ **Code reuse**: Reuses spec-2 retrieval functions via import, no duplication
3. ✅ **Minimal scope**: User requested 2-3 tasks, single file agent.py delivers this
4. ✅ **CLI interface**: Simple command-line execution (`uv run python agent.py`)
5. ✅ **Testable**: Each user story has independent test criteria

**No Violations**: All design decisions align with simplicity and reuse principles

---

## Project Structure

### Documentation (this feature)

```text
specs/003-rag-agent/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (entities and schemas)
├── quickstart.md        # Phase 1 output (user guide)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── agent.py             # NEW: RAG agent with OpenAI SDK (this feature)
├── retrieve.main.py     # EXISTING: Retrieval validation from spec-2 (REUSED)
├── main.py              # EXISTING: Ingestion pipeline from spec-1
├── .env                 # UPDATED: Add OPENAI_API_KEY
└── README.md            # UPDATED: Add agent usage section
```

**Structure Decision**: Single-file CLI script at backend/agent.py following established pattern from spec-1/2. No new directories or packages needed - keeps implementation minimal and consistent.

**Reuse Strategy**:
- Import retrieval functions from `retrieve.main.py`: `embed_query()`, `search_similar_chunks()`
- Import configuration loading from `retrieve.main.py`: `load_config()`
- Reuse dataclasses from `retrieve.main.py`: `RetrievalResult`
- No code duplication - all retrieval logic already validated in spec-2

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - complexity tracking not required.

---

## Phase 0: Research & Technical Decisions

### Research Areas

**R1: OpenAI Agents SDK vs Function Calling API**
- **Question**: Should we use OpenAI Agents SDK (beta) or standard function calling?
- **Status**: ✅ Resolved
- **Decision**: Use OpenAI function calling with `tools` parameter (standard API)
- **Rationale**:
  - User specified "OpenAI Agents SDK" but current stable approach is function calling
  - OpenAI's Assistants API (agents) requires thread management and file storage
  - Function calling is simpler, more mature, and sufficient for our use case
  - Supports same capability: agent decides when to call retrieval tool
- **Alternative**: If user specifically wants Assistants API, would need thread/run management
- **Implementation**: Use `openai.ChatCompletion.create()` with `tools=[retrieval_tool]`

**R2: Tool Schema Design for Retrieval**
- **Question**: How should we structure the retrieval tool schema for OpenAI?
- **Status**: ✅ Resolved
- **Decision**: Single tool `retrieve_documentation` with parameters:
  ```json
  {
    "name": "retrieve_documentation",
    "description": "Search the book documentation for relevant information",
    "parameters": {
      "query": "string (user's question)",
      "top_k": "integer (default 5)",
      "similarity_threshold": "float (default 0.0)"
    }
  }
  ```
- **Rationale**:
  - Simple single-purpose tool matches spec-2 retrieval function signature
  - Agent can control top_k if more context needed
  - Default threshold 0.0 returns results, agent judges relevance
- **Reference**: [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

**R3: System Prompt Engineering**
- **Question**: How do we enforce "retrieved content only" constraint?
- **Status**: ✅ Resolved
- **Decision**: Use explicit system prompt with strict instructions:
  ```
  You are a helpful assistant that answers questions about a book using ONLY
  information retrieved from the documentation. You have access to a retrieval
  tool that searches the book content.

  CRITICAL RULES:
  - ALWAYS call the retrieval tool before answering any question
  - ONLY use information from retrieved chunks in your answers
  - If no relevant chunks are found, say "I don't have information about that"
  - NEVER use external knowledge or make assumptions
  - Include source citations (page titles, sections) in your answers
  ```
- **Rationale**:
  - Explicit constraints reduce hallucination risk
  - "ALWAYS call tool" ensures retrieval happens
  - Clear failure mode ("I don't have information") for off-topic questions
- **Testing**: Validate with SC-003 (off-topic questions)

**R4: Conversation History Management**
- **Question**: How do we maintain multi-turn conversation context?
- **Status**: ✅ Resolved
- **Decision**: Use OpenAI's built-in messages array for context
- **Implementation**:
  ```python
  messages = [
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": "question 1"},
      {"role": "assistant", "content": "answer 1"},
      {"role": "user", "content": "question 2"},  # Follow-up
      # ... agent adds tool calls and responses automatically
  ]
  ```
- **Rationale**:
  - No custom session management needed - SDK handles it
  - Messages list grows with conversation
  - Agent sees full history when deciding tool usage
- **Constraint**: Memory grows linearly - acceptable for 10-15 turn conversations

**R5: Error Handling for Retrieval Failures**
- **Question**: What happens when Qdrant is unavailable or retrieval fails?
- **Status**: ✅ Resolved
- **Decision**: Wrap tool execution in try/except, return error message to agent
- **Implementation**:
  ```python
  def retrieval_tool_handler(query, top_k=5):
      try:
          results = search_similar_chunks(...)
          return format_results(results)
      except Exception as e:
          return f"Error retrieving documentation: {str(e)}"
  ```
- **Rationale**:
  - Agent sees error as tool output and can inform user gracefully
  - Matches SC-006 requirement (graceful failure with error messages)
  - Prevents script crash on transient Qdrant issues

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions.

**Key Entities**:
1. **Agent Configuration**: System prompt, model name, temperature
2. **Tool Definition**: Retrieval tool schema (name, description, parameters)
3. **Conversation State**: Messages array, retrieval history
4. **Tool Response**: Formatted retrieval results (chunk text + metadata)

### API Contracts

See [contracts/](contracts/) for OpenAPI/JSON schemas.

**Agent-to-Retrieval Tool Contract**:
- **Input**: query (string), top_k (int), similarity_threshold (float)
- **Output**: JSON array of results with chunk_text, page_title, section_heading, source_url, similarity_score
- **Error**: String error message on failure

**User-to-Agent Interface** (CLI):
- **Input**: Text question via stdin or command-line argument
- **Output**: Agent answer to stdout with source citations
- **Modes**:
  - Single question: `uv run python agent.py "What are the prerequisites?"`
  - Interactive session: `uv run python agent.py` (enter questions in loop)

### Quickstart Guide

See [quickstart.md](quickstart.md) for complete usage instructions, troubleshooting, and examples.

---

## Implementation Workflow

### Estimated Timeline: ~60 minutes (2-3 tasks)

**Task 1: Agent Core Setup** (~25 min)
- Create `backend/agent.py` with imports
- Load OpenAI API key from .env
- Define system prompt and model configuration
- Initialize OpenAI client
- Implement basic question-answer loop (single turn, no tools yet)
- **Deliverable**: Agent can answer questions using only model knowledge (before tool integration)

**Task 2: Retrieval Tool Integration** (~25 min)
- Import retrieval functions from `retrieve.main.py`
- Define retrieval tool schema for OpenAI function calling
- Implement tool handler function (calls embed_query + search_similar_chunks)
- Format tool responses for agent consumption (JSON with metadata)
- Wire tool into agent conversation loop
- **Deliverable**: Agent calls retrieval tool and uses results in answers

**Task 3: Multi-Turn & Polish** (~10 min)
- Implement conversation history management (messages array)
- Add interactive CLI mode for multi-turn sessions
- Update README.md with agent usage section
- Test with example questions from quickstart.md
- **Deliverable**: Fully functional RAG agent ready for user testing

**Total**: 60 minutes for 3 tasks (meets user's "2-3 tasks" requirement)

---

## Dependencies

### Prerequisites (must exist before implementation)

1. **Spec-2 (002-rag-retrieval-validation)**: MUST be complete
   - `retrieve.main.py` with functions: `embed_query()`, `search_similar_chunks()`, `load_config()`
   - Dataclass: `RetrievalResult`
   - Validated retrieval pipeline working end-to-end

2. **Spec-1 (001-doc-rag-ingestion)**: MUST be complete
   - Qdrant collection `'documentation'` with embedded book chunks
   - `.env` file with QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY

3. **Environment Setup**:
   - Python 3.11+ installed
   - UV package manager installed
   - Dependencies from spec-1/2 (qdrant-client, cohere, python-dotenv)

### New Dependencies

- **openai** (Python package): `uv pip install openai`
- **OPENAI_API_KEY**: Add to `.env` file (obtain from [OpenAI Platform](https://platform.openai.com/api-keys))

---

## Risk Analysis

### Risk 1: OpenAI API Rate Limits
- **Probability**: Medium (if user makes many rapid queries)
- **Impact**: Agent fails with 429 error
- **Mitigation**:
  - Use retry logic with exponential backoff
  - Document rate limits in quickstart.md
  - Start with gpt-3.5-turbo (higher rate limits than gpt-4)

### Risk 2: Retrieval Returns No Results
- **Probability**: High (for off-topic questions - expected behavior per SC-003)
- **Impact**: Agent must respond gracefully without hallucinating
- **Mitigation**:
  - System prompt explicitly instructs "say I don't have information"
  - Tool handler returns empty results gracefully
  - Test with negative queries to validate behavior

### Risk 3: Conversation Context Grows Too Large
- **Probability**: Low (typical sessions 10-15 turns)
- **Impact**: Token limit exceeded, context truncation
- **Mitigation**:
  - Document max conversation length in quickstart.md
  - Implement simple context window management if needed (keep last N messages)
  - Not critical for MVP - out of scope per "minimal" requirement

### Risk 4: Tool Calling Hallucination
- **Probability**: Medium (LLM might invent tool calls or parameters)
- **Impact**: Invalid tool execution, errors
- **Mitigation**:
  - Strict tool schema validation
  - Error handling returns clear messages to agent
  - Test with edge cases (malformed queries)

---

## Success Criteria Mapping

| Success Criterion | Implementation Approach | Validation Method |
|-------------------|------------------------|-------------------|
| SC-001: 80%+ questions answered correctly | System prompt + retrieval tool + citation enforcement | Manual testing with 10 questions from quickstart.md |
| SC-002: Multi-turn context handling | OpenAI messages array maintains history | Test 5-turn conversation with "tell me more" follow-ups |
| SC-003: 100% off-topic questions handled | System prompt rule: "I don't have information" | Test 5 unrelated questions (e.g., "What's the weather?") |
| SC-004: <5s response time | OpenAI API latency + Qdrant search (<2s from spec-2) | Measure end-to-end time for 10 questions |
| SC-005: 90%+ citation rate | Tool response includes metadata, system prompt requests citations | Review 20 answers, count source mentions |
| SC-006: Retrieval tool integration | Function calling with error handling | Test 20 tool calls, verify success or graceful errors |
| SC-007: 10+ turn coherence | Messages array preserves full context | 15-turn conversation test, verify relevance maintained |

---

## Next Steps

1. **Phase 0 Output**: Create `research.md` documenting R1-R5 technical decisions ✅ (inline above)
2. **Phase 1 Output**: Create `data-model.md` with entity schemas
3. **Phase 1 Output**: Create `contracts/` directory with tool schema
4. **Phase 1 Output**: Create `quickstart.md` with usage examples
5. **Phase 2**: Run `/sp.tasks` to generate implementation task breakdown from this plan
6. **Phase 3**: Run `/sp.implement` to execute 3 tasks and build agent.py
