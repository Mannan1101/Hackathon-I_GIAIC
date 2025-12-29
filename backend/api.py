"""
FastAPI RAG Integration

This module provides a REST API server that exposes the RAG agent as a web service.
The frontend Docusaurus chatbot sends POST requests to /chat and receives agent responses.

Features:
- POST /chat: Submit questions and receive RAG-powered answers
- CORS enabled for localhost:3000 (Docusaurus dev server)
- Auto-generated API documentation at /docs and /redoc

Usage:
    python api.py
    # Server runs on http://127.0.0.1:8000
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import existing agent from agent.py
from agent import create_agent, load_config
from agents import Runner

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Configure CORS for Docusaurus frontend (localhost:3000 and other common ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's question about the Physical AI & Humanoid Robotics textbook"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the prerequisites for this course?"
            }
        }


class ChatResponse(BaseModel):
    """Response model for successful chat queries"""
    answer: str = Field(
        ...,
        description="Agent's response to the user's question, generated using RAG"
    )
    sources: Optional[list[str]] = Field(
        default=None,
        description="Optional: List of document chunks used to generate the answer"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional: Additional response metadata (retrieval time, confidence, etc.)"
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


class ErrorResponse(BaseModel):
    """Response model for error cases"""
    error: str = Field(
        ...,
        description="Error type identifier"
    )
    message: str = Field(
        ...,
        description="Human-readable error description for developers"
    )
    detail: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error context"
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


# Helper Functions

async def query_agent(question: str) -> str:
    """
    Invoke the RAG agent with a single question.

    Args:
        question: User's question as a string

    Returns:
        Agent's answer as a string

    Raises:
        Exception: If agent execution fails
    """
    try:
        # Load configuration and create a new agent instance for this query
        config = load_config()
        agent = create_agent(config)

        # Execute the query using Runner (stateless, no session persistence)
        result = await Runner.run(agent, question)

        # Extract the final answer from RunResult object
        if result and hasattr(result, 'final_output') and result.final_output:
            return result.final_output

        # Fallback: convert result to string if final_output is None or empty
        return str(result) if result else "No response generated"

    except Exception as e:
        logger.error(f"Agent execution failed: {e}", exc_info=True)
        raise


# API Endpoints

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint for querying the RAG agent.

    Accepts a question and returns the agent's answer with optional sources and metadata.
    """
    import time
    start_time = time.time()

    try:
        # Log incoming request
        logger.info(f"Received query: {request.question[:100]}...")

        # Call the agent
        answer = await query_agent(request.question)

        # Calculate response time
        elapsed_ms = (time.time() - start_time) * 1000

        # Log successful response
        logger.info(f"Query completed in {elapsed_ms:.0f}ms with status 200")

        # Return response
        return ChatResponse(answer=answer)

    except Exception as e:
        # Log error
        elapsed_ms = (time.time() - start_time) * 1000
        logger.error(f"Query failed after {elapsed_ms:.0f}ms: {e}", exc_info=True)

        # Return 500 error with details
        raise HTTPException(
            status_code=500,
            detail={
                "error": "agent_error",
                "message": f"RAG agent failed to process the query: {str(e)}",
                "detail": {"exception": str(e)}
            }
        )


# Startup validation
@app.on_event("startup")
async def startup_validation():
    """Validate configuration and dependencies on server startup."""
    try:
        logger.info("Validating configuration...")
        config = load_config()
        logger.info("✅ Configuration validated successfully")

        # Test agent creation
        logger.info("Testing agent initialization...")
        agent = create_agent(config)
        logger.info("✅ Agent initialized successfully")

        logger.info("🚀 Server is ready to accept requests")
    except Exception as e:
        logger.error(f"❌ Startup validation failed: {e}")
        logger.error("Please check your .env file and ensure all required variables are set")
        raise


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify server is running."""
    return {
        "status": "healthy",
        "service": "RAG Chatbot API",
        "timestamp": datetime.now().isoformat()
    }


# Development Server Entrypoint

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting RAG Chatbot API server...")
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
