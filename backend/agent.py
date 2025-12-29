"""
RAG Agent with OpenAI Agents SDK

This module implements an AI agent using the OpenAI Agents SDK to orchestrate
retrieval operations over book content stored in Qdrant. The agent answers questions
using ONLY retrieved chunks from the documentation, preventing hallucination.

Features:
- Single-question CLI mode
- Interactive multi-turn conversations with SQLiteSession
- Source citations in responses
- Graceful handling of off-topic questions

Usage:
    # Single question
    uv run python agent.py "What are the prerequisites?"

    # Interactive session
    uv run python agent.py

Dependencies:
- openai-agents: OpenAI Agents SDK for agent orchestration
- retrieve.main: Retrieval pipeline from spec-2 (embed_query, search_similar_chunks)
- python-dotenv: Environment variable loading
"""

import os
import sys
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, SQLiteSession, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI

# Import retrieval functions from spec-2
from retrieve_main import embed_query, search_similar_chunks, load_config as load_retrieval_config

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="openai/gpt-4o-mini"
)


set_tracing_disabled(True)  # Disable tracing for simplicity
def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.

    Reuses retrieval configuration from spec-2 and adds OpenAI-specific settings.

    Returns:
        Dict containing all configuration values

    Raises:
        ValueError: If required environment variables are missing
    """
    # Load environment variables from .env file
    load_dotenv()

    # Load retrieval configuration from spec-2 (Qdrant, Cohere)
    retrieval_config = load_retrieval_config()
    
    

    if not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("Missing OPENROUTER_API_KEY in .env")

    return {
        **retrieval_config
    }

   


# Agent instructions with strict "retrieved content only" rules
AGENT_INSTRUCTIONS = """You are a helpful assistant that answers questions about a book using ONLY information retrieved from the documentation.

CRITICAL RULES:
1. ALWAYS call the retrieve_documentation tool before answering any question
2. ONLY use information from the retrieved chunks in your answers
3. If no relevant chunks are found or the similarity scores are too low, say "I don't have information about that in the book content"
4. NEVER use external knowledge or make assumptions beyond the retrieved content
5. Include source citations in your answers (mention the page titles and section headings from the retrieved chunks)
6. Be direct and factual - focus on answering the user's question using the retrieved information

When you receive retrieval results:
- Check if any results were returned
- Review the similarity scores (higher is more relevant)
- Use the chunk_text as your primary source
- Cite the page_title and section_heading when providing information

Example response format:
"According to [page_title], [answer using chunk_text].

(Source: [page_title]: [section_heading])"
"""


# Retrieval tool as a function_tool decorator
@function_tool
def retrieve_documentation(query: str, top_k: int = 5, similarity_threshold: float = 0.0) -> str:
    """Search the book documentation for relevant information based on a question or topic.

    Returns chunks of text from the book with metadata about their source (page titles,
    section headings, URLs). Use this tool BEFORE answering any question to retrieve
    factual information from the book content.

    Args:
        query: The question or topic to search for in the documentation. Should be the
               user's question or a rephrased version focused on key concepts.
        top_k: Number of most relevant chunks to retrieve. Increase if more context is
               needed for complex questions. Default: 5
        similarity_threshold: Minimum similarity score for results (0.0-1.0). Lower values
                            return more results but may be less relevant. Default: 0.0

    Returns:
        JSON string containing retrieval results with chunks, metadata, and similarity scores
    """
    try:
        # Embed the query using Cohere (from spec-2)
        print(f"[Retrieving information for: {query}...]")
        query_embedding = embed_query(query)

        # Search Qdrant for similar chunks (from spec-2)
        results = search_similar_chunks(query_embedding, top_k=top_k)

        # Filter by similarity threshold if specified
        if similarity_threshold > 0.0:
            results = [r for r in results if r.similarity_score >= similarity_threshold]

        # Format results as structured data
        formatted_results = []
        for rank, result in enumerate(results, start=1):
            formatted_results.append({
                "chunk_text": result.chunk_text,
                "page_title": result.page_title,
                "section_heading": result.section_heading,
                "source_url": result.source_url,
                "similarity_score": round(result.similarity_score, 3),
                "rank": rank
            })

        import json
        response = {
            "results": formatted_results,
            "total_results": len(formatted_results),
            "query": query,
            "error": None
        }

        return json.dumps(response, indent=2)

    except Exception as e:
        import json
        return json.dumps({
            "results": [],
            "total_results": 0,
            "query": query,
            "error": f"Retrieval failed: {str(e)}"
        }, indent=2)


def create_agent(config: Dict[str, Any]) -> Agent:
    """
    Create an Agent instance with retrieval tool.

    Uses the OpenAI Agents SDK to create an agent with:
    - Instructions for answering questions using ONLY retrieved content
    - retrieve_documentation function tool
    - Configured model and settings

    Args:
        config: Configuration dict containing model and API settings

    Returns:
        Initialized Agent instance ready to answer questions
    """
    # Set OpenAI API key from config
    

    # Create agent with instructions and retrieval tool
    agent = Agent(
        name="Book RAG Agent",
        instructions=AGENT_INSTRUCTIONS,
        tools=[retrieve_documentation],
        model = model

    )

    return agent


def single_question_mode(question: str):
    """
    CLI mode for asking a single question and exiting.

    Uses Runner.run_sync for synchronous execution without async/await.

    Usage: python agent.py "What are the prerequisites?"

    Args:
        question: The user's question
    """
    try:
        # Load configuration
        config = load_config()

        # Create agent
        agent = create_agent(config)

        # Ask question using synchronous runner
        print(f"\nQuestion: {question}\n")
        result = Runner.run_sync(agent, question)

        # Print answer
        print(f"\nAnswer: {result.final_output}\n")

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def interactive_mode_async():
    """
    Async implementation of interactive CLI mode for multi-turn conversations.

    Uses SQLiteSession to maintain conversation context across multiple questions.
    Type 'quit' or 'exit' to end the session.
    """
    try:
        # Load configuration
        config = load_config()

        # Create agent
        agent = create_agent(config)

        # Create persistent session for conversation memory
        session = SQLiteSession("interactive_session", "conversations.db")

        # Turn counter
        turn_count = 0

        # Welcome message
        print("\nRAG Agent - Ask questions about the book content")
        print("Type 'quit' or 'exit' to end the session\n")

        # Conversation loop
        while True:
            # Get user input
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n")
                break

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            # Skip empty input
            if not user_input:
                continue

            # Increment turn counter
            turn_count += 1

            # Ask question using async runner with session
            try:
                result = await Runner.run(agent, user_input, session=session)
                print(f"Agent: {result.final_output}\n")
            except Exception as e:
                print(f"Error processing question: {e}\n", file=sys.stderr)

        # Session summary
        print(f"Session ended. Asked {turn_count} questions. Thank you!")

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def interactive_mode():
    """
    Interactive CLI mode for multi-turn conversations.

    Wraps the async implementation for easy calling from main().
    """
    asyncio.run(interactive_mode_async())


def main():
    """
    Main entry point for the agent.

    Supports two modes:
    1. Single-question mode: python agent.py "Your question"
    2. Interactive mode: python agent.py
    """
    if len(sys.argv) > 1:
        # Single-question mode
        question = " ".join(sys.argv[1:])
        single_question_mode(question)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
