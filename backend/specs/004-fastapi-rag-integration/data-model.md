# Data Model: FastAPI RAG Integration

**Feature**: 004-fastapi-rag-integration
**Date**: 2025-12-28
**Purpose**: Define request/response schemas and data structures for the FastAPI RAG integration

---

## Overview

The API uses Pydantic models for request validation and response serialization. All models follow the JSON contract expected by the existing frontend chatbot component.

---

## Request Models

### ChatRequest

Represents an incoming query from the frontend chatbot.

**Schema**:
```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's question about the Physical AI & Humanoid Robotics textbook",
        examples=["What are the prerequisites for this course?"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is physical AI?"
            }
        }
```

**Validation Rules**:
- `question` is required (indicated by `...`)
- Minimum length: 1 character (reject empty strings)
- Maximum length: 1000 characters (prevent abuse, reasonable query limit)
- Type: string only

**Validation Errors**:
FastAPI automatically returns HTTP 422 with detailed validation errors:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "question"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

---

## Response Models

### ChatResponse

Represents a successful response from the RAG agent.

**Schema**:
```python
from pydantic import BaseModel, Field

class ChatResponse(BaseModel):
    """Response model for successful chat queries"""
    answer: str = Field(
        ...,
        description="Agent's response to the user's question, generated using RAG",
        examples=["Physical AI refers to artificial intelligence systems that interact with and manipulate the physical world..."]
    )
    sources: list[str] | None = Field(
        default=None,
        description="Optional: List of document chunks used to generate the answer (for citation/transparency)",
        examples=[["Chapter 1: Introduction, p.5", "Chapter 3: Foundations, p.42"]]
    )
    metadata: dict[str, any] | None = Field(
        default=None,
        description="Optional: Additional response metadata (retrieval time, confidence, etc.)",
        examples=[{"retrieval_time_ms": 234, "generation_time_ms": 1523}]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Physical AI refers to AI systems that can perceive, reason about, and interact with the physical world through sensors and actuators.",
                "sources": ["Chapter 1, Section 1.2: Defining Physical AI"],
                "metadata": {
                    "retrieval_time_ms": 150,
                    "generation_time_ms": 1200
                }
            }
        }
```

**Field Descriptions**:
- **`answer`** (required): The agent's textual response
- **`sources`** (optional): Retrieved document chunks for transparency (Phase 2 enhancement)
- **`metadata`** (optional): Performance metrics and debugging info (Phase 2 enhancement)

**MVP Response** (Phase 1):
```json
{
  "answer": "Physical AI refers to..."
}
```

**Enhanced Response** (Future):
```json
{
  "answer": "Physical AI refers to...",
  "sources": ["Chapter 1, p.5", "Chapter 3, p.42"],
  "metadata": {
    "retrieval_time_ms": 150,
    "generation_time_ms": 1200,
    "confidence": 0.92
  }
}
```

---

### ErrorResponse

Represents error details for failed requests.

**Schema**:
```python
from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    """Response model for error cases"""
    error: str = Field(
        ...,
        description="Error type identifier",
        examples=["validation_error", "agent_error", "timeout_error", "server_error"]
    )
    message: str = Field(
        ...,
        description="Human-readable error description for developers",
        examples=["The question field is required"]
    )
    detail: dict[str, any] | None = Field(
        default=None,
        description="Additional error context (stack trace, validation errors, etc.)",
        examples=[{"field": "question", "reason": "Field required"}]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "error": "agent_error",
                "message": "RAG agent failed to process the query",
                "detail": {
                    "agent_exception": "TimeoutError: Query exceeded 30 seconds"
                }
            }
        }
```

**Error Types**:
- **`validation_error`**: Request validation failed (HTTP 422)
- **`agent_error`**: RAG agent execution failed (HTTP 500)
- **`timeout_error`**: Query exceeded time limit (HTTP 504)
- **`retrieval_error`**: Vector DB retrieval failed (HTTP 500)
- **`server_error`**: Unexpected internal error (HTTP 500)

**Example Error Responses**:

**Validation Error (HTTP 422)**:
```json
{
  "error": "validation_error",
  "message": "Question must be between 1 and 1000 characters",
  "detail": {
    "field": "question",
    "provided_length": 0
  }
}
```

**Agent Error (HTTP 500)**:
```json
{
  "error": "agent_error",
  "message": "Failed to retrieve relevant document chunks",
  "detail": {
    "qdrant_error": "Connection refused to vector database"
  }
}
```

**Timeout Error (HTTP 504)**:
```json
{
  "error": "timeout_error",
  "message": "Query processing exceeded 30 second timeout",
  "detail": {
    "elapsed_time_ms": 30500
  }
}
```

---

## Internal Models (Not Exposed via API)

### AgentResult

Internal representation of agent execution results (not sent to frontend).

**Schema**:
```python
from dataclasses import dataclass

@dataclass
class AgentResult:
    """Internal result from agent execution"""
    answer: str
    sources: list[str] = None
    retrieval_time_ms: float = None
    generation_time_ms: float = None
    error: Exception | None = None
```

This model is used internally to capture agent execution details before converting to `ChatResponse`.

---

## Data Flow

### Successful Request Flow

```
Frontend (JSON)          API Layer (Pydantic)       Agent Layer             API Response
─────────────            ───────────────────        ───────────             ─────────────

{                  →     ChatRequest            →   query_agent()       →   ChatResponse
  "question":           .question: str                 ↓                       ↓
  "What is AI?"        (validated)                 AgentResult          {
}                                                   .answer: str           "answer": "..."
                                                    .sources: [...]      }
                                                         ↓
                                                  Transform to
                                                  ChatResponse
```

### Error Request Flow

```
Frontend (JSON)          API Layer (Pydantic)       Error Handling          API Response
─────────────            ───────────────────        ──────────────          ─────────────

{                  →     ChatRequest            →   ValidationError     →   HTTP 422
  "question": ""        .question: ""               (Pydantic)             {
}                       ❌ min_length=1                                       "detail": [...]
                                                                            }

{                  →     ChatRequest            →   Agent Execution     →   HTTP 500
  "question":           .question: str              Exception               ErrorResponse
  "Valid query"        (validated ✓)                ↓                       ↓
}                                                  Try-Catch           {
                                                   ↓                     "error": "agent_error",
                                                   HTTPException         "message": "...",
                                                                         "detail": {...}
                                                                       }
```

---

## Validation Rules Summary

| Field | Type | Required | Min Length | Max Length | Default |
|-------|------|----------|------------|------------|---------|
| `ChatRequest.question` | str | Yes | 1 | 1000 | N/A |
| `ChatResponse.answer` | str | Yes | - | - | N/A |
| `ChatResponse.sources` | list[str] | No | - | - | None |
| `ChatResponse.metadata` | dict | No | - | - | None |
| `ErrorResponse.error` | str | Yes | - | - | N/A |
| `ErrorResponse.message` | str | Yes | - | - | N/A |
| `ErrorResponse.detail` | dict | No | - | - | None |

---

## HTTP Status Code Mapping

| Status Code | Scenario | Response Model | Example |
|-------------|----------|----------------|---------|
| **200 OK** | Successful agent response | `ChatResponse` | `{"answer": "..."}` |
| **400 Bad Request** | Custom validation errors | `ErrorResponse` | Empty question after trim |
| **422 Unprocessable Entity** | Pydantic validation failure | FastAPI auto-generated | Missing required field |
| **500 Internal Server Error** | Agent execution error | `ErrorResponse` | RAG agent crash, retrieval failure |
| **504 Gateway Timeout** | Query timeout | `ErrorResponse` | Query exceeded 30s limit |

---

## JSON Schema Examples

### Successful Chat Request/Response

**Request**:
```json
POST /chat HTTP/1.1
Content-Type: application/json

{
  "question": "What are the prerequisites for this course?"
}
```

**Response**:
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "answer": "The prerequisites for this course include: 1) Basic programming skills in Python, 2) Linear algebra and calculus fundamentals, 3) Understanding of probability and statistics. No prior robotics experience is required."
}
```

### Error Response Example

**Request**:
```json
POST /chat HTTP/1.1
Content-Type: application/json

{
  "question": ""
}
```

**Response**:
```json
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "question"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    }
  ]
}
```

---

## Entity Relationships

```
┌──────────────┐
│   Frontend   │
│  (Chatbot)   │
└──────┬───────┘
       │ POST /chat
       │ ChatRequest
       ↓
┌──────────────┐
│  API Layer   │
│  (FastAPI)   │
└──────┬───────┘
       │ query_agent(question)
       ↓
┌──────────────┐
│ Agent Layer  │
│ (agent.py)   │
└──────┬───────┘
       │ AgentResult
       ↓
┌──────────────┐
│  API Layer   │
│  (FastAPI)   │
└──────┬───────┘
       │ ChatResponse
       ↓
┌──────────────┐
│   Frontend   │
│  (Chatbot)   │
└──────────────┘
```

---

## Future Enhancements

### Multi-Turn Conversations

**Extended ChatRequest**:
```python
class ChatRequest(BaseModel):
    question: str = Field(...)
    session_id: str | None = Field(None, description="Optional conversation session ID")
```

**Extended ChatResponse**:
```python
class ChatResponse(BaseModel):
    answer: str = Field(...)
    session_id: str = Field(..., description="Conversation session identifier")
    turn_number: int = Field(..., description="Turn number in conversation")
```

### Advanced Metadata

**Extended Metadata**:
```python
metadata: dict[str, any] = {
    "retrieval_time_ms": 150,
    "generation_time_ms": 1200,
    "confidence_score": 0.92,
    "chunks_retrieved": 5,
    "chunks_used": 3,
    "model_name": "deepseek/deepseek-r1-0528:free"
}
```

---

## Validation Constraints

### Business Rules

1. **Question Length**: 1-1000 characters (prevents empty queries and abuse)
2. **Response Format**: Always include `answer` field, optional metadata
3. **Error Details**: Include actionable information for debugging
4. **Type Safety**: All fields strictly typed with Pydantic

### Edge Cases

| Edge Case | Handling |
|-----------|----------|
| Empty question `""` | Reject with 422 validation error |
| Whitespace-only question `"   "` | Accept (FastAPI doesn't auto-trim), agent handles |
| Very long question (>1000 chars) | Reject with 422 validation error |
| Special characters in question | Accept (UTF-8 encoding supported) |
| Missing question field | Reject with 422 validation error |
| Extra unknown fields in request | Ignore (Pydantic default behavior) |
| Agent returns empty answer | Return empty string `""` with 200 OK |
| Agent throws exception | Return 500 with ErrorResponse |

---

## Summary

This data model provides:
- ✅ **Type safety** via Pydantic validation
- ✅ **Clear contracts** matching frontend expectations
- ✅ **Automatic documentation** via FastAPI/OpenAPI
- ✅ **Extensibility** for future enhancements (sources, metadata, sessions)
- ✅ **Developer-friendly errors** with detailed validation messages

The minimal MVP contract (`{question}` → `{answer}`) meets the current frontend requirements while allowing for future enhancements without breaking changes.
