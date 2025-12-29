"""
RAG Retrieval Validation Script

This script validates the RAG retrieval pipeline by:
1. Connecting to Qdrant and verifying stored embeddings
2. Running test queries to retrieve relevant documentation chunks
3. Validating metadata completeness and accuracy
4. Generating a comprehensive validation report

Usage:
    uv run python retrieve.main.py

Prerequisites:
    - Completed spec-1 (001-doc-rag-ingestion) with vectors in Qdrant
    - Valid .env file with Qdrant and Cohere credentials
"""

import uuid
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

import cohere
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class RetrievalQuery:
    """Represents a semantic search query with parameters."""
    query_text: str
    top_k: int = 5
    similarity_threshold: float = 0.0
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RetrievalResult:
    """Represents a single search result with metadata and score."""
    query_id: str
    chunk_text: str
    source_url: str
    page_title: str
    section_heading: Optional[str]
    breadcrumb: Optional[str]
    chunk_index: int
    similarity_score: float
    metadata: Dict[str, Any]
    rank: int


@dataclass
class ValidationReport:
    """Aggregates validation test results with statistics."""
    run_id: str
    total_queries: int
    successful_queries: int
    failed_queries: int
    avg_similarity_score: float
    avg_query_time: float
    metadata_completeness: float
    total_results_retrieved: int
    connection_status: str
    collection_stats: Dict[str, Any]
    errors: List[str]
    started_at: datetime
    completed_at: datetime

    @property
    def duration_seconds(self) -> float:
        """Calculate total validation duration."""
        return (self.completed_at - self.started_at).total_seconds()

    @property
    def success_rate(self) -> float:
        """Calculate query success rate (0.0-1.0)."""
        if self.total_queries == 0:
            return 0.0
        return self.successful_queries / self.total_queries

    def to_summary(self) -> str:
        """Generate human-readable validation summary report."""
        return f"""
{'='*60}
RAG Retrieval Validation Report
{'='*60}
Run ID: {self.run_id}
Started: {self.started_at.strftime('%Y-%m-%d %H:%M:%S')}
Completed: {self.completed_at.strftime('%Y-%m-%d %H:%M:%S')}
Duration: {self.duration_seconds:.1f}s

CONNECTION STATUS
{'='*60}
Status: {self.connection_status}
Collection: {self.collection_stats.get('collection_name', 'N/A')}
Vector Count: {self.collection_stats.get('vector_count', 0):,}
Vector Dimensions: {self.collection_stats.get('vector_dim', 0)}
Distance Metric: {self.collection_stats.get('distance', 'N/A')}

QUERY METRICS
{'='*60}
Total Queries: {self.total_queries}
Successful: {self.successful_queries}
Failed: {self.failed_queries}
Success Rate: {self.success_rate * 100:.1f}%

RETRIEVAL QUALITY
{'='*60}
Total Results Retrieved: {self.total_results_retrieved}
Avg Similarity Score: {self.avg_similarity_score:.3f}
Avg Query Time: {self.avg_query_time:.2f}s

METADATA VALIDATION
{'='*60}
Metadata Completeness: {self.metadata_completeness * 100:.1f}%

{'ERRORS' if self.errors else 'STATUS'}
{'='*60}
{chr(10).join(self.errors) if self.errors else '✅ All validations passed successfully!'}
{'='*60}
""".strip()


# ============================================================================
# CONFIGURATION
# ============================================================================

def load_config() -> Dict[str, Any]:
    """Load and validate configuration from environment variables."""
    config = {
        # Qdrant configuration
        "qdrant_url": os.getenv("QDRANT_URL", ""),
        "qdrant_api_key": os.getenv("QDRANT_API_KEY", ""),
        "qdrant_collection_name": os.getenv("QDRANT_COLLECTION_NAME", "documentation"),

        # Cohere configuration
        "cohere_api_key": os.getenv("COHERE_API_KEY", ""),
        "cohere_model": os.getenv("COHERE_MODEL", "embed-english-v3.0"),
    }

    # Validate required fields
    required_fields = ["qdrant_url", "qdrant_api_key", "qdrant_collection_name", "cohere_api_key"]
    missing_fields = [field for field in required_fields if not config[field]]

    if missing_fields:
        raise ValueError(f"Missing required environment variables: {', '.join(f.upper() for f in missing_fields)}")

    return config


# ============================================================================
# RETRY DECORATORS
# ============================================================================

def create_retry_decorator(operation_type: str):
    """Create a retry decorator with exponential backoff for specific operation type."""
    def log_retry(retry_state):
        error = retry_state.outcome.exception() if retry_state.outcome else "Unknown error"
        logger.warning(f"[{operation_type}] Retry attempt {retry_state.attempt_number} after error: {error}")

    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
        before_sleep=log_retry
    )


retry_db = create_retry_decorator("DB")
retry_api = create_retry_decorator("API")


# ============================================================================
# TEST QUERIES
# ============================================================================

TEST_QUERIES = [
    # Category 1: Specific queries (expect high similarity >0.7)
    "How do I get started with the documentation?",
    "What is authentication and how does it work?",
    "How to configure the application settings?",
    "Explain the API endpoints available",
    "What are the installation requirements?",

    # Category 2: Broad queries (expect moderate similarity 0.5-0.7)
    "Tell me about the main features",
    "What is this documentation about?",
    "How does the system work?",

    # Category 3: Negative queries (expect low similarity <0.5)
    "What is the weather today?",
    "How to cook pasta?",
]


# ============================================================================
# CORE FUNCTIONS - USER STORY 1: CONNECTION VALIDATION
# ============================================================================

@retry_db
def validate_connection(client: QdrantClient, collection_name: str) -> Dict[str, Any]:
    """
    Verify Qdrant connection and collection metadata.

    Returns:
        dict: Collection statistics including vector_count, vector_dim, distance, collection_exists

    Raises:
        ConnectionError: If Qdrant is unreachable
        ValueError: If collection does not exist
    """
    logger.info(f"[CONNECTION] Connecting to Qdrant collection '{collection_name}'")

    try:
        # Check if collection exists
        collections = client.get_collections().collections
        collection_exists = any(c.name == collection_name for c in collections)

        if not collection_exists:
            raise ValueError(f"Collection '{collection_name}' does not exist. Run main.py first to create vectors.")

        # Get collection metadata
        collection_info = client.get_collection(collection_name)

        # Handle both dict and object access for vector params
        vectors_config = collection_info.config.params.vectors
        if isinstance(vectors_config, dict):
            # If vectors is a dict, get the default vector config
            vector_params = list(vectors_config.values())[0] if vectors_config else None
        else:
            vector_params = vectors_config

        stats = {
            "collection_name": collection_name,
            "collection_exists": True,
            "vector_count": collection_info.points_count,
            "vector_dim": vector_params.size if vector_params else 0,
            "distance": vector_params.distance.name if vector_params and hasattr(vector_params, 'distance') else "UNKNOWN",
        }

        logger.info(
            f"[CONNECTION] Successfully connected to collection '{collection_name}' - "
            f"{stats['vector_count']:,} vectors, {stats['vector_dim']} dimensions, {stats['distance']} distance"
        )

        return stats

    except ValueError as e:
        # Collection doesn't exist - re-raise with original error
        logger.error(f"[CONNECTION] Connection failed: {e}")
        raise
    except Exception as e:
        # Network or auth errors
        logger.error(f"[CONNECTION] Connection failed: {e}")
        raise ConnectionError(
            f"Failed to connect to Qdrant at collection '{collection_name}'. "
            "Check QDRANT_URL, QDRANT_API_KEY in .env and ensure Qdrant is accessible."
        ) from e


# ============================================================================
# CORE FUNCTIONS - USER STORY 2: QUERY EXECUTION
# ============================================================================

# Backward compatibility wrapper for validation suite
_embed_query_original = lambda query_text, cohere_client, model: _embed_query_internal(query_text, cohere_client, model)



# Backward compatibility wrapper for validation suite
_search_similar_chunks_original = lambda client, collection_name, query_vector, top_k=5: _search_similar_chunks_internal(client, collection_name, query_vector, top_k)


# ============================================================================
# CORE FUNCTIONS - USER STORY 3: METADATA VALIDATION
# ============================================================================

def validate_metadata(results: List[RetrievalResult]) -> Dict[str, Any]:
    """
    Validate metadata completeness and URL validity.

    Args:
        results: List of retrieval results to validate

    Returns:
        dict: Validation statistics (completeness, missing_fields, invalid_urls)
    """
    if not results:
        logger.info("[METADATA] No results to validate")
        return {
            "completeness": 1.0,  # Vacuously true
            "total_results": 0,
            "complete_results": 0,
            "missing_fields": [],
            "invalid_urls": []
        }

    required_fields = ["chunk_text", "source_url", "page_title"]
    complete_count = 0
    missing_fields_summary = []
    invalid_urls = []

    for result in results:
        # Check required fields
        missing = []
        for field in required_fields:
            value = getattr(result, field, None)
            if not value or (isinstance(value, str) and not value.strip()):
                missing.append(field)

        if not missing:
            complete_count += 1
        else:
            missing_fields_summary.extend(missing)

        # Validate URL format
        if result.source_url:
            if not (result.source_url.startswith("http://") or result.source_url.startswith("https://")):
                invalid_urls.append(result.source_url)

    completeness = complete_count / len(results) if results else 1.0

    stats = {
        "completeness": completeness,
        "total_results": len(results),
        "complete_results": complete_count,
        "missing_fields": list(set(missing_fields_summary)),  # Unique missing fields
        "invalid_urls": invalid_urls
    }

    logger.info(
        f"[METADATA] Validation complete - "
        f"{completeness * 100:.1f}% completeness ({complete_count}/{len(results)} results)"
    )

    if stats["missing_fields"]:
        logger.warning(f"[METADATA] Missing fields detected: {', '.join(stats['missing_fields'])}")

    if stats["invalid_urls"]:
        logger.warning(f"[METADATA] {len(stats['invalid_urls'])} invalid URLs detected")

    return stats


# ============================================================================
# CORE FUNCTIONS - USER STORY 4: END-TO-END VALIDATION SUITE
# ============================================================================

def run_validation_suite(
    queries: List[str],
    qdrant_client: QdrantClient,
    cohere_client: cohere.Client,
    collection_name: str,
    model: str
) -> ValidationReport:
    """
    Execute all test queries and generate validation report.

    Args:
        queries: List of test query strings
        qdrant_client: Initialized Qdrant client
        cohere_client: Initialized Cohere client
        collection_name: Qdrant collection name
        model: Cohere embedding model

    Returns:
        ValidationReport: Complete validation statistics
    """
    run_id = f"val-{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M%S')}"
    started_at = datetime.now(timezone.utc)

    logger.info(f"[VALIDATE] Running validation suite with {len(queries)} test queries (Run ID: {run_id})")

    all_results = []
    errors = []
    query_times = []
    successful_count = 0

    # Execute all test queries
    for idx, query_text in enumerate(queries, start=1):
        try:
            query_start = datetime.now(timezone.utc)

            # Embed query
            query_vector = _embed_query_original(query_text, cohere_client, model)

            # Search similar chunks
            results = _search_similar_chunks_original(qdrant_client, collection_name, query_vector, top_k=5)

            # Set query_id for all results
            query_id = str(uuid.uuid4())
            for result in results:
                result.query_id = query_id
                all_results.append(result)

            query_time = (datetime.now(timezone.utc) - query_start).total_seconds()
            query_times.append(query_time)
            successful_count += 1

            top_score = results[0].similarity_score if results else 0.0
            logger.info(
                f"[QUERY {idx}/{len(queries)}] \"{query_text[:50]}...\" → "
                f"{len(results)} results, top score: {top_score:.3f}, time: {query_time:.2f}s"
            )

        except Exception as e:
            error_msg = f"Query '{query_text}' failed: {str(e)}"
            errors.append(error_msg)
            logger.error(f"[QUERY {idx}/{len(queries)}] {error_msg}")

    completed_at = datetime.now(timezone.utc)

    # Calculate metrics
    avg_query_time = sum(query_times) / len(query_times) if query_times else 0.0

    similarity_scores = [r.similarity_score for r in all_results]
    avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0

    # Validate metadata
    metadata_stats = validate_metadata(all_results)

    # Get connection stats (already validated earlier)
    collection_stats = {}  # Will be populated by main()

    report = ValidationReport(
        run_id=run_id,
        total_queries=len(queries),
        successful_queries=successful_count,
        failed_queries=len(errors),
        avg_similarity_score=avg_similarity,
        avg_query_time=avg_query_time,
        metadata_completeness=metadata_stats["completeness"],
        total_results_retrieved=len(all_results),
        connection_status="connected",
        collection_stats=collection_stats,
        errors=errors,
        started_at=started_at,
        completed_at=completed_at
    )

    logger.info(f"[VALIDATE] Validation suite complete - {successful_count}/{len(queries)} queries successful")

    return report


def main():
    """Main entry point for validation script."""
    run_id = str(uuid.uuid4())
    logger.info(f"Starting RAG Retrieval Validation (Run ID: {run_id})")

    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")

        # Initialize clients
        qdrant_client = QdrantClient(
            url=config["qdrant_url"],
            api_key=config["qdrant_api_key"]
        )
        cohere_client = cohere.Client(api_key=config["cohere_api_key"])

        # Validate connection
        collection_stats = validate_connection(qdrant_client, config["qdrant_collection_name"])

        # Run validation suite
        report = run_validation_suite(
            queries=TEST_QUERIES,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            collection_name=config["qdrant_collection_name"],
            model=config["cohere_model"]
        )

        # Update report with collection stats
        report.collection_stats = collection_stats

        # Print validation report
        print("\n" + report.to_summary())

        # Exit with appropriate status code
        if report.failed_queries > 0:
            logger.warning(f"Validation completed with {report.failed_queries} failed queries")
            return 1
        else:
            logger.info("✅ All validations passed successfully!")
            return 0

    except Exception as e:
        logger.error(f"Validation failed: {e}", exc_info=True)
        print(f"\n❌ Validation failed: {e}")
        return 1


# ============================================================================
# SIMPLIFIED API FOR AGENT USAGE
# ============================================================================

# ============================================================================
# CLIENT SINGLETON PATTERN
# ============================================================================
# Module-level clients (lazy-initialized on first use)
# This pattern avoids repeated client initialization while maintaining testability

_cohere_client: Optional[cohere.Client] = None
_qdrant_client: Optional[QdrantClient] = None
_config: Optional[Dict[str, Any]] = None


def _get_clients() -> tuple[cohere.Client, QdrantClient, Dict[str, Any]]:
    """
    Get or initialize singleton clients for Cohere and Qdrant.

    Uses lazy initialization pattern to avoid unnecessary client creation.
    Clients are cached at module level for reuse across multiple calls.

    Returns:
        tuple: (cohere_client, qdrant_client, config)

    Raises:
        ValueError: If required configuration is missing
    """
    global _cohere_client, _qdrant_client, _config

    # Initialize config if needed
    if _config is None:
        _config = load_config()

    # Initialize Cohere client if needed
    if _cohere_client is None:
        _cohere_client = cohere.Client(api_key=_config["cohere_api_key"])
        logger.debug("[CLIENT] Initialized Cohere client")

    # Initialize Qdrant client if needed
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=_config["qdrant_url"],
            api_key=_config["qdrant_api_key"]
        )
        logger.debug("[CLIENT] Initialized Qdrant client")

    return _cohere_client, _qdrant_client, _config


# Simplified wrapper functions for agent.py
def embed_query(query_text: str) -> List[float]:
    """
    Simplified wrapper: Generate embedding for query text.

    Args:
        query_text: Natural language query

    Returns:
        list: 1024-dimensional embedding vector
    """
    cohere_client, _, config = _get_clients()
    return _embed_query_internal(query_text, cohere_client, config["cohere_model"])


def search_similar_chunks(query_vector: List[float], top_k: int = 5) -> List[RetrievalResult]:
    """
    Simplified wrapper: Perform semantic search in Qdrant.

    Args:
        query_vector: Query embedding (1024-dim)
        top_k: Number of results to retrieve

    Returns:
        list: RetrievalResult objects sorted by similarity_score (descending)
    """
    _, qdrant_client, config = _get_clients()
    return _search_similar_chunks_internal(
        qdrant_client,
        config["qdrant_collection_name"],
        query_vector,
        top_k
    )


# ============================================================================
# INTERNAL HELPER FUNCTIONS (DRY - Don't Repeat Yourself)
# ============================================================================

@retry_api
def _embed_query_internal(query_text: str, cohere_client: cohere.Client, model: str) -> List[float]:
    """
    Generate embedding for query text using Cohere.

    This is the core implementation used by both the validation suite (_embed_query_original)
    and the simplified public API (embed_query).

    Args:
        query_text: Natural language query
        cohere_client: Initialized Cohere client
        model: Embedding model name (e.g., 'embed-english-v3.0')

    Returns:
        list: 1024-dimensional embedding vector

    Raises:
        Exception: If Cohere API call fails after retries
    """
    try:
        response = cohere_client.embed(
            texts=[query_text],
            model=model,
            input_type="search_query"  # Use search_query for query embeddings
        )
        embeddings = list(response.embeddings)
        return [float(x) for x in embeddings[0]]
    except (IndexError, KeyError) as e:
        # Handle empty response or malformed data
        logger.error(f"[EMBED] Invalid response from Cohere API: {e}")
        raise ValueError(f"Invalid embedding response for query '{query_text[:50]}...'") from e
    except Exception as e:
        # Network, auth, or API errors
        logger.error(f"[EMBED] Failed to embed query '{query_text[:50]}...': {e}")
        raise


@retry_db
def _search_similar_chunks_internal(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    top_k: int = 5
) -> List[RetrievalResult]:
    """
    Perform semantic search in Qdrant.

    This is the core implementation used by both the validation suite (_search_similar_chunks_original)
    and the simplified public API (search_similar_chunks).

    Args:
        client: Initialized Qdrant client
        collection_name: Collection to search
        query_vector: Query embedding (1024-dim)
        top_k: Number of results to retrieve

    Returns:
        list: RetrievalResult objects sorted by similarity_score (descending)

    Raises:
        Exception: If Qdrant search fails after retries
    """
    try:
        # Search Qdrant using query_points API
        search_results = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k
        ).points

        # Handle empty results
        if not search_results:
            logger.warning("[QUERY] No results returned for query")
            return []

        # Convert to RetrievalResult objects
        results = []
        for rank, scored_point in enumerate(search_results, start=1):
            payload = scored_point.payload

            result = RetrievalResult(
                query_id="",  # Will be set by caller
                chunk_text=payload.get("chunk_text", ""),
                source_url=payload.get("source_url", ""),
                page_title=payload.get("page_title", ""),
                section_heading=payload.get("section_heading"),
                breadcrumb=payload.get("breadcrumb"),
                chunk_index=payload.get("chunk_index", 0),
                similarity_score=scored_point.score,
                metadata=payload,
                rank=rank
            )
            results.append(result)

        # Log low-scoring results (helps with debugging)
        if results and all(r.similarity_score < 0.5 for r in results):
            logger.info(
                f"[QUERY] All results have low similarity scores (<0.5), "
                f"top score: {results[0].similarity_score:.3f}"
            )

        return results

    except Exception as e:
        logger.error(f"[QUERY] Search failed: {e}")
        raise


if __name__ == "__main__":
    main()
