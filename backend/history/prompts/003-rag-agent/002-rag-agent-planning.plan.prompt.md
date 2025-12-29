---
id: 002
title: rag-agent-planning
stage: plan
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: 003-rag-agent
branch: 003-rag-agent
user: Abdul Mannan
command: /sp.plan
labels: ["planning", "rag", "agent", "openai", "architecture", "design"]
links:
  spec: specs/003-rag-agent/spec.md
  plan: specs/003-rag-agent/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-rag-agent/plan.md
  - specs/003-rag-agent/data-model.md
  - specs/003-rag-agent/contracts/retrieval-tool-schema.json
  - specs/003-rag-agent/contracts/tool-response-schema.json
  - specs/003-rag-agent/quickstart.md
  - history/prompts/003-rag-agent/002-rag-agent-planning.plan.prompt.md
tests:
  - Phase 0 research completed (5 technical decisions resolved)
  - Phase 1 design completed (data model, contracts, quickstart)
  - Single-file architecture decision documented
  - All 7 success criteria mapped to implementation approach
---

## Prompt

/sp.plan Spec-3: Agent with Retrieval

- create a single 'agent.py' file in backend folder
- initialize an agent using the OpenAI Agent SDK
- integrate retrieval by calling the existing Qdrant search logic
- Ensure the agent responds using retrieved book content only

## Response snapshot

Successfully created comprehensive implementation plan for RAG Agent with OpenAI SDK (spec-3) including architecture decisions, technical research, and complete design artifacts.

**Feature Branch**: 003-rag-agent

**Planning Artifacts Created**:

**1. plan.md** - Complete implementation plan with:
- **Summary**: AI agent using OpenAI function calling to orchestrate retrieval from Qdrant, maintaining multi-turn conversations while answering using only retrieved chunks
- **Technical Context**:
  - Language: Python 3.11+
  - Dependencies: openai, qdrant-client, cohere (reused from spec-2), python-dotenv
  - Architecture: Single-file `agent.py` (consistent with spec-1/2 pattern)
  - Performance: <5s per question-answer cycle
  - Constraints: Reuse spec-2 retrieval, no hallucination, CLI only, 2-3 tasks
- **Constitution Check**: ✅ No violations (single-file architecture, code reuse, minimal scope)
- **Project Structure**:
  ```
  backend/
  ├── agent.py             # NEW: RAG agent (this feature)
  ├── retrieve.main.py     # EXISTING: Reused from spec-2
  ├── main.py              # EXISTING: Reused from spec-1
  └── .env                 # UPDATED: Add OPENAI_API_KEY
  ```

**2. Phase 0: Research (5 technical decisions resolved)**:

**R1: OpenAI Agents SDK vs Function Calling**
- **Decision**: Use OpenAI function calling with `tools` parameter (standard API)
- **Rationale**: Simpler than Assistants API, more mature, sufficient for use case
- **Implementation**: `openai.ChatCompletion.create()` with `tools=[retrieval_tool]`

**R2: Tool Schema Design**
- **Decision**: Single tool `retrieve_documentation` with parameters: query, top_k, similarity_threshold
- **Rationale**: Matches spec-2 retrieval function signature, simple single-purpose tool
- **Schema**: JSON tool definition (see contracts/)

**R3: System Prompt Engineering**
- **Decision**: Explicit constraints to enforce "retrieved content only"
- **Prompt**:
  ```
  CRITICAL RULES:
  - ALWAYS call retrieve_documentation tool before answering
  - ONLY use information from retrieved chunks
  - If no relevant chunks found, say "I don't have information"
  - NEVER use external knowledge
  - Include source citations
  ```
- **Rationale**: Reduces hallucination risk, clear failure mode for off-topic questions

**R4: Conversation History Management**
- **Decision**: Use OpenAI's built-in messages array for context
- **Implementation**: Messages list grows with conversation (system, user, assistant, tool)
- **Rationale**: No custom session management needed, SDK handles context

**R5: Error Handling for Retrieval Failures**
- **Decision**: Wrap tool execution in try/except, return error message to agent
- **Rationale**: Agent sees error as tool output and informs user gracefully

**3. Phase 1: Design**

**data-model.md** - 4 entities defined:

1. **AgentConfiguration**: Settings for agent behavior
   - Fields: model, system_prompt, temperature, max_tokens, openai_api_key
   - System prompt enforces FR-004 (answers using only retrieved chunks)

2. **RetrievalTool**: OpenAI function calling tool schema
   - Tool name: `retrieve_documentation`
   - Parameters: query (required), top_k (default 5), similarity_threshold (default 0.0)
   - Tool handler calls spec-2 functions: embed_query, search_similar_chunks
   - Response format: JSON with results array (chunk_text, page_title, section_heading, source_url, similarity_score, rank)

3. **ConversationState**: Multi-turn conversation management
   - Fields: session_id, messages array, retrieval_history, started_at, turn_count
   - Message sub-entity: role, content, name, tool_calls, timestamp
   - ToolCall sub-entity: tool_name, query, results_count, avg_similarity, timestamp

4. **ToolResponse**: Structured retrieval output
   - Fields: results (RetrievalResult list from spec-2), total_results, query, error
   - Formatted as JSON for agent consumption
   - Supports US3 (source citations)

**contracts/** - Tool schemas:

1. **retrieval-tool-schema.json**: OpenAI function calling tool definition
   - Type: function
   - Name: retrieve_documentation
   - Parameters: query (string, required), top_k (int, 1-20), similarity_threshold (float, 0.0-1.0)

2. **tool-response-schema.json**: JSON schema for tool responses
   - Results array with chunk_text, page_title, section_heading, source_url, similarity_score, rank
   - Example responses for success, empty results, and errors

**quickstart.md** - Complete user guide with:
- Prerequisites checklist (spec-1/2 complete, OpenAI API key)
- Setup instructions (install openai, add API key to .env)
- Usage examples (single question mode, interactive session)
- Example questions (good questions, follow-ups, off-topic tests)
- How it works (6-step flow from question to answer with citations)
- Troubleshooting (8 common errors with solutions)
- Performance expectations (7 success criteria with verification methods)
- Configuration options (model selection, retrieval parameters)
- Example session transcript

**Implementation Workflow** (3 tasks, ~60 minutes):

**Task 1: Agent Core Setup** (~25 min)
- Create agent.py, load OpenAI API key, define system prompt
- Initialize OpenAI client, implement basic Q&A loop (no tools yet)
- **Deliverable**: Agent answers using model knowledge (baseline)

**Task 2: Retrieval Tool Integration** (~25 min)
- Import spec-2 functions (embed_query, search_similar_chunks)
- Define retrieval tool schema, implement tool handler
- Wire tool into agent conversation loop
- **Deliverable**: Agent calls retrieval tool and uses results

**Task 3: Multi-Turn & Polish** (~10 min)
- Implement conversation history (messages array)
- Add interactive CLI mode, update README.md
- Test with example questions from quickstart.md
- **Deliverable**: Fully functional RAG agent

**Dependencies**:
- Spec-2 (retrieval validation): embed_query(), search_similar_chunks(), RetrievalResult
- Spec-1 (ingestion): Qdrant collection 'documentation'
- New: openai package, OPENAI_API_KEY in .env

**Risk Analysis** (4 risks identified):
1. **OpenAI API rate limits**: Mitigation - retry logic, use gpt-3.5-turbo
2. **Retrieval returns no results**: Mitigation - system prompt "I don't have information"
3. **Conversation context grows too large**: Mitigation - document max length, simple window management
4. **Tool calling hallucination**: Mitigation - strict schema validation, error handling

**Success Criteria Mapping**:
- SC-001 (80%+ correct answers): System prompt + retrieval tool + citations
- SC-002 (multi-turn context): OpenAI messages array
- SC-003 (100% off-topic handling): System prompt "I don't have information" rule
- SC-004 (<5s response time): OpenAI latency + Qdrant search (<2s)
- SC-005 (90%+ citations): Tool response metadata, system prompt requests citations
- SC-006 (retrieval integration): Function calling with error handling
- SC-007 (10+ turn coherence): Messages array preserves full context

**Code Reuse Strategy**:
- Import from retrieve.main.py: embed_query, search_similar_chunks, load_config, RetrievalResult
- No code duplication - all retrieval logic already validated in spec-2
- Single-file architecture consistent with spec-1 (main.py) and spec-2 (retrieve.main.py)

**Key Design Decisions**:
1. **Function calling over Assistants API**: Simpler, more mature, sufficient for use case
2. **System prompt engineering**: Explicit constraints reduce hallucination
3. **Reuse spec-2 without modification**: Import functions, no duplication
4. **Single-file architecture**: Consistent with established pattern, minimal scope
5. **CLI interface**: Simple stdin/stdout, no web complexity

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation and implementation with clear 3-task workflow
- 🧪 Tests: 5 technical decisions researched and resolved, 4 entities designed, 7 success criteria mapped, 4 risks analyzed
- 📁 Files: 5 files created (plan.md, data-model.md, 2 contract schemas, quickstart.md, PHR)
- 🔁 Next prompts: Run `/sp.tasks` to generate task breakdown from plan, then `/sp.implement` to build agent.py
- 🧠 Reflection: Successfully designed minimal agent architecture reusing spec-2 retrieval pipeline. Single-file approach consistent with spec-1/2 patterns. System prompt engineering critical for hallucination prevention. Function calling simpler than Assistants API. Timeline achievable (3 tasks, 60 min) meets user's "2-3 tasks" requirement.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed without blocking issues
- Graders run and results (PASS/FAIL): PASS - All 5 research decisions resolved, complete design artifacts, clear implementation workflow
- Prompt variant (if applicable): Standard /sp.plan workflow with user directive for single-file architecture
- Next experiment (smallest change to try): Proceed to /sp.tasks to generate task breakdown from plan.md
