# Data Model: RAG Agent with OpenAI SDK

**Feature**: 003-rag-agent
**Created**: 2025-12-27
**Purpose**: Define entities, schemas, and data structures for the RAG agent implementation

---

## Overview

The RAG agent system consists of 4 primary entities:
1. **AgentConfiguration**: Settings for agent behavior and model selection
2. **RetrievalTool**: Function schema for OpenAI function calling
3. **ConversationState**: Runtime state management for multi-turn conversations
4. **ToolResponse**: Structured output from retrieval tool execution

All entities support the 3 user stories from spec.md:
- US1 (P1): Basic question answering with retrieval
- US2 (P2): Multi-turn conversation with context
- US3 (P3): Source citation and transparency

---

## Entity 1: AgentConfiguration

**Purpose**: Configuration for initializing the OpenAI agent with proper behavior constraints

**Attributes**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| model | string | Yes | "gpt-3.5-turbo" | OpenAI model name (gpt-3.5-turbo or gpt-4-turbo) |
| system_prompt | string | Yes | (see below) | Instructions enforcing "retrieved content only" constraint |
| temperature | float | Yes | 0.0 | Model temperature (0.0 for deterministic, factual responses) |
| max_tokens | integer | No | null | Max response length (null = model default) |
| openai_api_key | string | Yes | from .env | OpenAI API key loaded from environment |

**System Prompt** (enforces FR-004: answers using ONLY retrieved chunks):

```
You are a helpful assistant that answers questions about a book using ONLY information retrieved from the documentation. You have access to a retrieval tool that searches the book content.

CRITICAL RULES:
- ALWAYS call the retrieve_documentation tool before answering any question
- ONLY use information from the retrieved chunks in your answers
- If no relevant chunks are found, respond with: "I don't have information about that in the book content"
- NEVER use external knowledge, make assumptions, or invent information
- Include source citations (page titles and section headings) in your answers
- For follow-up questions, you may reference previous answers but still call the tool if new information is needed

RESPONSE FORMAT:
- Answer the user's question directly
- Include inline citations like "(from Chapter 2: Installation)"
- If multiple sources are used, list all relevant chapters/sections
```

**Validation Rules**:
- `model` must be a valid OpenAI model name
- `temperature` must be between 0.0 and 1.0
- `system_prompt` must not be empty
- `openai_api_key` must be valid (40+ character string starting with "sk-")

**Relationships**:
- Used by: ConversationState (references model and prompt)
- Depends on: Environment variables (.env file)

---

## Entity 2: RetrievalTool

**Purpose**: OpenAI function calling tool schema that defines how the agent can query Qdrant

**Tool Definition** (JSON schema for OpenAI API):

```json
{
  "type": "function",
  "function": {
    "name": "retrieve_documentation",
    "description": "Search the book documentation for relevant information based on a question or topic. Returns chunks of text from the book with metadata about their source.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The question or topic to search for in the documentation"
        },
        "top_k": {
          "type": "integer",
          "description": "Number of most relevant chunks to retrieve (default: 5)",
          "default": 5
        },
        "similarity_threshold": {
          "type": "number",
          "description": "Minimum similarity score for results (0.0-1.0, default: 0.0)",
          "default": 0.0
        }
      },
      "required": ["query"]
    }
  }
}
```

**Tool Handler Function Signature** (Python):

```python
def execute_retrieval_tool(
    query: str,
    top_k: int = 5,
    similarity_threshold: float = 0.0
) -> str:
    """
    Execute retrieval tool by calling spec-2 retrieval pipeline.

    Args:
        query: User's question to search for
        top_k: Number of chunks to retrieve
        similarity_threshold: Minimum similarity score

    Returns:
        JSON string with retrieval results formatted for agent consumption
        Format: {"results": [{"chunk_text": "...", "page_title": "...", ...}]}

    Raises:
        Exception: If Qdrant connection fails or retrieval errors occur
    """
```

**Tool Response Schema** (returned to agent):

```json
{
  "results": [
    {
      "chunk_text": "string (content of retrieved chunk)",
      "page_title": "string (e.g., 'Chapter 2: Installation')",
      "section_heading": "string or null (e.g., 'Prerequisites')",
      "source_url": "string (URL to source page)",
      "similarity_score": "float (0.0-1.0)",
      "rank": "integer (1-based ranking)"
    }
  ],
  "total_results": "integer (number of chunks returned)",
  "query": "string (echo of user's query)"
}
```

**Error Response Schema** (on failure):

```json
{
  "error": "string (error message)",
  "query": "string (echo of user's query)"
}
```

**Validation Rules**:
- `query` must not be empty
- `top_k` must be between 1 and 20
- `similarity_threshold` must be between 0.0 and 1.0
- Tool response must be valid JSON

**Relationships**:
- Calls: spec-2 functions (`embed_query`, `search_similar_chunks`)
- Used by: Agent (via OpenAI function calling)
- Returns: ToolResponse entities

---

## Entity 3: ConversationState

**Purpose**: Maintains conversation context across multi-turn interactions (supports US2: multi-turn conversations)

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| session_id | string (UUID) | Yes | Unique identifier for this conversation session |
| messages | list[Message] | Yes | Ordered list of conversation messages (system, user, assistant, tool) |
| retrieval_history | list[ToolCall] | No | Log of all retrieval tool calls made in this session |
| started_at | datetime | Yes | Timestamp when conversation started |
| turn_count | integer | Yes | Number of user questions asked (for tracking SC-007: 10+ turns) |

**Message Sub-Entity**:

```python
@dataclass
class Message:
    role: str              # "system", "user", "assistant", "tool"
    content: str           # Message text
    name: Optional[str]    # Tool name if role="tool"
    tool_calls: Optional[list]  # Tool calls if agent requested them
    timestamp: datetime    # When message was created
```

**ToolCall Sub-Entity** (for retrieval history):

```python
@dataclass
class ToolCall:
    tool_name: str         # Always "retrieve_documentation"
    query: str             # User's question that triggered retrieval
    results_count: int     # Number of chunks returned
    avg_similarity: float  # Average similarity score of results
    timestamp: datetime    # When tool was called
```

**Initialization**:

```python
state = ConversationState(
    session_id=str(uuid.uuid4()),
    messages=[
        Message(role="system", content=SYSTEM_PROMPT, timestamp=datetime.now())
    ],
    retrieval_history=[],
    started_at=datetime.now(),
    turn_count=0
)
```

**State Transitions**:
1. User asks question → append Message(role="user", content=question)
2. Agent requests tool → append tool_calls to messages
3. Tool executes → append Message(role="tool", content=results)
4. Agent responds → append Message(role="assistant", content=answer)
5. Increment turn_count

**Validation Rules**:
- `messages` must start with role="system"
- `messages` must alternate user/assistant roles (with tool calls in between)
- `turn_count` must not exceed 20 (context window protection)

**Relationships**:
- Contains: Multiple Message entities
- Tracks: Multiple ToolCall entities
- Used by: Agent main loop

---

## Entity 4: ToolResponse

**Purpose**: Structured output from retrieval tool execution, formatted for agent consumption

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| results | list[RetrievalResult] | Yes | List of retrieved chunks (from spec-2 dataclass) |
| total_results | integer | Yes | Number of chunks returned |
| query | string | Yes | Echo of user's query |
| error | string or null | No | Error message if retrieval failed |

**RetrievalResult** (imported from spec-2 `retrieve.main.py`):

```python
@dataclass
class RetrievalResult:
    query_id: str              # Not used by agent, but part of spec-2 schema
    chunk_text: str            # Main content for agent to use
    source_url: str            # For citations (US3)
    page_title: str            # For citations (US3)
    section_heading: Optional[str]  # For citations (US3)
    breadcrumb: Optional[str]  # For citations (US3)
    chunk_index: int           # Position in source document
    similarity_score: float    # Relevance score (0.0-1.0)
    metadata: Dict[str, Any]   # Additional metadata from Qdrant
    rank: int                  # 1-based ranking
```

**Formatting for Agent** (JSON serialization):

```python
def format_tool_response(results: list[RetrievalResult], query: str) -> str:
    """
    Convert RetrievalResult objects to JSON string for agent.

    Returns:
        JSON string with results formatted for readability and citation
    """
    return json.dumps({
        "results": [
            {
                "chunk_text": r.chunk_text,
                "page_title": r.page_title,
                "section_heading": r.section_heading,
                "source_url": r.source_url,
                "similarity_score": r.similarity_score,
                "rank": r.rank
            }
            for r in results
        ],
        "total_results": len(results),
        "query": query
    }, indent=2)
```

**Example Output** (what agent sees):

```json
{
  "results": [
    {
      "chunk_text": "Before installing, ensure you have Python 3.11 or higher...",
      "page_title": "Chapter 1: Getting Started",
      "section_heading": "Prerequisites",
      "source_url": "https://hackathon-1-eight-pi.vercel.app/chapter-01",
      "similarity_score": 0.856,
      "rank": 1
    }
  ],
  "total_results": 1,
  "query": "What are the prerequisites?"
}
```

**Validation Rules**:
- If `error` is set, `results` should be empty list
- `total_results` must equal `len(results)`
- Each result must have non-empty `chunk_text`, `page_title`, `source_url`
- `similarity_score` must be between 0.0 and 1.0

**Relationships**:
- Built from: RetrievalResult entities (spec-2)
- Consumed by: Agent via OpenAI function calling
- Supports: US3 (source citations)

---

## Data Flow

**Single Question-Answer Cycle**:

```
1. User Input
   ↓
2. ConversationState.messages.append(user_message)
   ↓
3. OpenAI API Call (with AgentConfiguration + messages + tools)
   ↓
4. Agent decides to call tool: retrieve_documentation(query="...")
   ↓
5. execute_retrieval_tool() → calls spec-2 pipeline
   ↓
6. ToolResponse created from RetrievalResult list
   ↓
7. ConversationState.messages.append(tool_response)
   ↓
8. OpenAI API Call again (with updated messages)
   ↓
9. Agent generates answer using tool results
   ↓
10. ConversationState.messages.append(assistant_message)
    ↓
11. Output to user
```

**Multi-Turn Conversation** (US2):

```
Turn 1: Q1 → Retrieve → A1 → messages=[system, Q1, tool_call, tool_result, A1]
Turn 2: Q2 → Retrieve → A2 → messages=[..., Q2, tool_call, tool_result, A2]
Turn 3: Q3 → (no retrieval, uses context) → A3 → messages=[..., Q3, A3]
```

Agent sees full `messages` array on each turn → understands "Tell me more" refers to previous answer.

---

## Storage & Persistence

**In-Memory Only** (per user constraints: no persistent storage):
- ConversationState exists only during script execution
- When user exits agent.py, conversation is lost
- No database, no file storage

**Environment Variables** (.env file):

```env
# Existing from spec-1/2
QDRANT_URL=https://...
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=documentation
COHERE_API_KEY=...
COHERE_MODEL=embed-english-v3.0

# NEW for spec-3
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo  # Optional, defaults to gpt-3.5-turbo
```

**Configuration Loading**:
- Reuse `load_config()` from spec-2 `retrieve.main.py`
- Add OPENAI_API_KEY validation
- All other config (Qdrant, Cohere) already handled by spec-2

---

## Implementation Notes

**Code Reuse from Spec-2**:
```python
# Import existing dataclasses and functions
from retrieve.main import (
    RetrievalResult,       # Entity for tool responses
    embed_query,           # Generate query embedding
    search_similar_chunks, # Execute Qdrant search
    load_config            # Load .env configuration
)
```

**No New Dataclasses Needed**:
- AgentConfiguration: Simple dict or named tuple (lightweight)
- ConversationState: Use OpenAI SDK's built-in messages array
- ToolResponse: Format as JSON string (no class needed)
- RetrievalResult: Already exists in spec-2

**Simplicity Focus**:
- Minimal entity count (reuse spec-2 where possible)
- No ORM or database models
- No serialization framework (use stdlib json)
- Single-file implementation (`agent.py`)

---

## Success Criteria Coverage

| Entity | Supports Success Criteria |
|--------|---------------------------|
| AgentConfiguration | SC-001 (correct answers via system prompt), SC-003 (off-topic handling) |
| RetrievalTool | SC-006 (tool integration), SC-001 (retrieval quality) |
| ConversationState | SC-002 (multi-turn context), SC-007 (10+ turn coherence) |
| ToolResponse | SC-005 (source citations), SC-001 (answers use retrieved content) |

All entities designed to support minimal implementation (2-3 tasks per user requirement).
