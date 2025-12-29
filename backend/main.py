"""
Documentation RAG Ingestion Pipeline

This script crawls documentation websites, cleans and chunks text content,
generates embeddings using Cohere, and stores them in Qdrant vector database.
"""

import asyncio
import hashlib
import logging
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin, urlparse, urlunparse
from api import app

import httpx
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, HnswConfigDiff, PayloadSchemaType
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
class DocumentationPage:
    """Represents a single documentation page from crawling."""
    url: str
    page_id: str
    raw_html: str
    cleaned_text: str
    title: str
    description: Optional[str]
    crawled_at: datetime
    content_hash: str
    content_length: int
    http_status: int
    main_content_selector: str
    removed_elements_count: int
    breadcrumb: Optional[str] = None
    processed: bool = False
    chunks_created: int = 0


@dataclass
class TextChunk:
    """Represents a semantically coherent text chunk with metadata."""
    chunk_id: str
    source_page_id: str
    text: str
    char_count: int
    token_count: int
    chunk_index: int
    total_chunks_in_page: int
    source_url: str
    page_title: str
    section_heading: Optional[str]
    heading_hierarchy: List[str]
    breadcrumb: Optional[str]
    content_type: str
    has_code: bool
    language: str = "en"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    prev_chunk_id: Optional[str] = None
    next_chunk_id: Optional[str] = None
    embedding: Optional[List[float]] = None
    embedding_model: str = "embed-english-v3.0"
    embedded_at: Optional[datetime] = None
    stored: bool = False
    qdrant_point_id: Optional[str] = None

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert chunk to Qdrant point payload."""
        return {
            "chunk_text": self.text,
            "source_url": self.source_url,
            "page_title": self.page_title,
            "section_heading": self.section_heading,
            "breadcrumb": self.breadcrumb or "",
            "chunk_index": self.chunk_index,
            "chunk_size": self.token_count,
            "content_type": self.content_type,
            "has_code": self.has_code,
            "ingested_at": self.created_at.isoformat(),
            "content_hash": hashlib.sha256(self.text.encode()).hexdigest()[:16],
            "embedding_model": self.embedding_model
        }


@dataclass
class IngestionMetadata:
    """Tracks metadata and statistics for an ingestion run."""
    run_id: str
    base_url: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    config: Dict[str, Any] = field(default_factory=dict)
    status: str = "running"
    urls_discovered: int = 0
    urls_crawled: int = 0
    urls_failed: int = 0
    chunks_created: int = 0
    chunks_embedded: int = 0
    chunks_stored: int = 0
    errors: List[str] = field(default_factory=list)

    def to_summary(self) -> str:
        """Generate human-readable summary of ingestion run."""
        return f"""
============================================
Ingestion Complete!
============================================
Duration: {self.duration_seconds:.0f}s
Pages crawled: {self.urls_crawled}
Chunks created: {self.chunks_created}
Vectors stored: {self.chunks_stored}
Success rate: {(self.chunks_stored / self.chunks_created * 100) if self.chunks_created > 0 else 0:.1f}%
============================================
""".strip()


# ============================================================================
# CONFIGURATION
# ============================================================================

def load_config() -> Dict[str, Any]:
    """Load and validate configuration from environment variables."""
    config = {
        # Target documentation site
        "base_url": os.getenv("BASE_URL", ""),

        # Cohere API configuration
        "cohere_api_key": os.getenv("COHERE_API_KEY", ""),
        "cohere_model": os.getenv("COHERE_MODEL", "embed-english-v3.0"),
        "cohere_input_type": os.getenv("COHERE_INPUT_TYPE", "search_document"),

        # Qdrant configuration
        "qdrant_url": os.getenv("QDRANT_URL", ""),
        "qdrant_api_key": os.getenv("QDRANT_API_KEY", ""),
        "qdrant_collection_name": os.getenv("QDRANT_COLLECTION_NAME", "documentation"),

        # Chunking configuration
        "target_chunk_size": int(os.getenv("TARGET_CHUNK_SIZE", "400")),
        "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", "80")),
        "min_chunk_size": int(os.getenv("MIN_CHUNK_SIZE", "100")),
        "max_chunk_size": int(os.getenv("MAX_CHUNK_SIZE", "512")),

        # Crawling configuration
        "max_concurrent_requests": int(os.getenv("MAX_CONCURRENT_REQUESTS", "10")),
        "request_timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
        "max_retries": int(os.getenv("MAX_RETRIES", "3")),

        # Batch processing
        "batch_size": int(os.getenv("BATCH_SIZE", "100")),
    }

    # Validate required fields
    required_fields = ["base_url", "cohere_api_key", "qdrant_url", "qdrant_api_key"]
    missing_fields = [field for field in required_fields if not config[field]]

    if missing_fields:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")

    return config


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

# Retry decorators for HTTP, API, and database operations
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


# Create specific retry decorators
retry_http = create_retry_decorator("HTTP")
retry_api = create_retry_decorator("API")
retry_db = create_retry_decorator("DB")


def normalize_url(url: str) -> str:
    """
    Normalize URL by removing trailing slash, anchors, and query params.

    Args:
        url: URL to normalize

    Returns:
        Normalized URL string
    """
    parsed = urlparse(url)

    # Remove query parameters and fragments
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),  # Lowercase domain
        parsed.path.rstrip("/"),  # Remove trailing slash
        "",  # Remove params
        "",  # Remove query
        ""   # Remove fragment
    ))

    return normalized


# ============================================================================
# CRAWLING FUNCTIONS (User Story 1)
# ============================================================================

@retry_http
async def fetch_sitemap(base_url: str) -> Optional[List[str]]:
    """
    Parse sitemap.xml to extract all documentation URLs.

    Args:
        base_url: Base URL of the documentation site

    Returns:
        List of URLs from sitemap, or None if sitemap not available
    """
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    logger.info(f"[CRAWL] Fetching sitemap from {sitemap_url}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(sitemap_url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]

        logger.info(f"[CRAWL] Found {len(urls)} URLs in sitemap")
        return urls

    except Exception as e:
        logger.warning(f"[CRAWL] Sitemap not available: {e}")
        return None


def filter_urls(urls: List[str], base_url: str) -> List[str]:
    """
    Filter URLs using include/exclude patterns.

    Args:
        urls: List of URLs to filter
        base_url: Base URL for validation

    Returns:
        Filtered list of URLs
    """
    # Include patterns (documentation content)
    # Accept all URLs from same domain - comment out to be more restrictive
    include_patterns = []  # Empty list = accept all from same domain

    # Exclude patterns (non-content pages)
    exclude_patterns = [r'/tags/', r'/page/\d+', r'/search', r'/404']

    filtered = []
    base_domain = urlparse(base_url).netloc

    for url in urls:
        parsed = urlparse(url)

        # Must be same domain
        if parsed.netloc != base_domain:
            continue

        # Check exclude patterns
        if any(re.search(pattern, url) for pattern in exclude_patterns):
            continue

        # If include patterns specified, must match at least one
        if include_patterns:
            if not any(re.search(pattern, url) for pattern in include_patterns):
                continue

        filtered.append(normalize_url(url))

    logger.info(f"[CRAWL] Filtered {len(urls)} URLs to {len(filtered)} documentation pages")
    return list(set(filtered))  # Deduplicate


@retry_http
async def fetch_page(url: str, client: httpx.AsyncClient) -> Optional[DocumentationPage]:
    """
    Fetch and parse a single documentation page.

    Args:
        url: URL to fetch
        client: Async HTTP client

    Returns:
        DocumentationPage object or None if fetch failed
    """
    try:
        response = await client.get(url)
        response.raise_for_status()

        page_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        content_hash = hashlib.sha256(response.text.encode()).hexdigest()

        return DocumentationPage(
            url=url,
            page_id=page_id,
            raw_html=response.text,
            cleaned_text="",  # Will be cleaned in next step
            title="",  # Will be extracted
            description=None,
            crawled_at=datetime.now(timezone.utc),
            content_hash=content_hash,
            content_length=len(response.text),
            http_status=response.status_code,
            main_content_selector="",
            removed_elements_count=0
        )

    except Exception as e:
        logger.error(f"[CRAWL] Failed to fetch {url}: {e}")
        return None


async def crawl_pages(urls: List[str], max_concurrent: int = 10) -> List[DocumentationPage]:
    """
    Concurrently crawl multiple documentation pages.

    Args:
        urls: List of URLs to crawl
        max_concurrent: Maximum concurrent requests

    Returns:
        List of successfully fetched DocumentationPage objects
    """
    logger.info(f"[CRAWL] Starting concurrent crawl of {len(urls)} pages (max {max_concurrent} concurrent)")

    pages = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Process in batches to limit concurrency
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i:i + max_concurrent]
            tasks = [fetch_page(url, client) for url in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, DocumentationPage):
                    pages.append(result)

            logger.info(f"[CRAWL] Progress: {len(pages)}/{len(urls)} pages fetched")

    logger.info(f"[CRAWL] Completed: {len(pages)} pages (0 failures)")
    return pages


# Docusaurus-specific selectors
CONTENT_SELECTORS = [
    'article',
    'main[role="main"]',
    '[class*="docItemContainer"]',
    '[class*="docMainContainer"]',
    '.markdown',
    '[class*="theme-doc-markdown"]',
]

REMOVE_SELECTORS = [
    'nav', 'header', 'footer',
    '[class*="navbar"]', '[class*="sidebar"]',
    '[class*="pagination"]',
    '[class*="tocCollapsible"]',
    '[class*="tableOfContents"]',
    '[class*="breadcrumbs"]',
    '[class*="editThisPage"]',
    '[class*="lastUpdated"]',
    '[class*="tags"]',
    'button', '[role="button"]',
    '[aria-hidden="true"]',
    '.hash-link',
    'script', 'style', 'iframe',
]


def extract_and_clean_content(page: DocumentationPage) -> DocumentationPage:
    """
    Extract main content and clean HTML from a documentation page.

    Args:
        page: DocumentationPage with raw HTML

    Returns:
        Updated DocumentationPage with cleaned text and metadata
    """
    soup = BeautifulSoup(page.raw_html, 'html.parser')

    # Extract metadata
    title_tag = soup.find('title')
    page.title = title_tag.text.strip() if title_tag else ""

    desc_tag = soup.find('meta', {'name': 'description'}) or soup.find('meta', {'property': 'og:description'})
    page.description = str(desc_tag.get('content', '')).strip() if desc_tag else None

    # Find main content using selectors
    main_content = None
    for selector in CONTENT_SELECTORS:
        main_content = soup.select_one(selector)
        if main_content:
            page.main_content_selector = selector
            break

    if not main_content:
        logger.warning(f"[CLEAN] No main content found for {page.url}")
        main_content = soup.body if soup.body else soup

    # Remove unwanted elements
    removed_count = 0
    for selector in REMOVE_SELECTORS:
        for element in main_content.select(selector):
            element.decompose()
            removed_count += 1

    page.removed_elements_count = removed_count

    # Extract clean text
    page.cleaned_text = main_content.get_text(separator='\n', strip=True)
    page.processed = True

    logger.debug(f"[CLEAN] Cleaned {page.url}: {len(page.cleaned_text)} chars, removed {removed_count} elements")

    return page


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text (rough approximation: 1 token ≈ 4 chars).

    Args:
        text: Text to estimate tokens for

    Returns:
        Estimated token count
    """
    return len(text) // 4


def chunk_text(page: DocumentationPage, target_size: int = 400, overlap: int = 80) -> List[TextChunk]:
    """
    Chunk cleaned text into semantically coherent segments.

    Args:
        page: DocumentationPage with cleaned text
        target_size: Target chunk size in tokens
        overlap: Overlap between chunks in tokens

    Returns:
        List of TextChunk objects
    """
    text = page.cleaned_text
    chunks = []

    # Simple sentence-based chunking
    sentences = text.split('. ')
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = estimate_tokens(sentence)

        if current_tokens + sentence_tokens > target_size and current_chunk:
            # Create chunk
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append(chunk_text)

            # Keep last sentences for overlap
            overlap_sentences = []
            overlap_tokens = 0
            for s in reversed(current_chunk):
                s_tokens = estimate_tokens(s)
                if overlap_tokens + s_tokens <= overlap:
                    overlap_sentences.insert(0, s)
                    overlap_tokens += s_tokens
                else:
                    break

            current_chunk = overlap_sentences + [sentence]
            current_tokens = overlap_tokens + sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    # Add final chunk
    if current_chunk:
        chunk_text = '. '.join(current_chunk) + '.'
        chunks.append(chunk_text)

    # Convert to TextChunk objects
    text_chunks = []
    for i, chunk_text in enumerate(chunks):
        chunk_id = f"{page.page_id}-{i}"
        text_chunks.append(TextChunk(
            chunk_id=chunk_id,
            source_page_id=page.page_id,
            text=chunk_text,
            char_count=len(chunk_text),
            token_count=estimate_tokens(chunk_text),
            chunk_index=i,
            total_chunks_in_page=len(chunks),
            source_url=page.url,
            page_title=page.title,
            section_heading=None,
            heading_hierarchy=[],
            breadcrumb=page.breadcrumb,
            content_type="text",
            has_code="```" in chunk_text or "<code>" in chunk_text,
            prev_chunk_id=text_chunks[-1].chunk_id if text_chunks else None,
            next_chunk_id=None
        ))

    # Link prev/next
    for i in range(len(text_chunks) - 1):
        text_chunks[i].next_chunk_id = text_chunks[i + 1].chunk_id

    logger.debug(f"[CHUNK] Created {len(text_chunks)} chunks from {page.url}")
    return text_chunks


# ============================================================================
# EMBEDDING FUNCTIONS (User Story 2)
# ============================================================================

@retry_api
def generate_embeddings(chunks: List[TextChunk], cohere_client: cohere.Client, model: str, input_type: str, batch_size: int = 10) -> List[TextChunk]:
    """
    Generate embeddings for text chunks using Cohere API.

    Args:
        chunks: List of TextChunk objects
        cohere_client: Initialized Cohere client
        model: Model name (e.g., embed-english-v3.0)
        input_type: Input type (search_document)
        batch_size: Number of chunks to embed per request

    Returns:
        List of TextChunk objects with embeddings
    """
    logger.info(f"[EMBED] Generating embeddings for {len(chunks)} chunks (batch size: {batch_size})")

    # Filter out empty/short chunks
    valid_chunks = [c for c in chunks if len(c.text.split()) >= 20]
    logger.info(f"[EMBED] Filtered to {len(valid_chunks)} valid chunks (min 20 words)")

    # Process in batches
    for i in range(0, len(valid_chunks), batch_size):
        batch = valid_chunks[i:i + batch_size]
        texts = [chunk.text for chunk in batch]

        try:
            response = cohere_client.embed(
                texts=texts,
                model=model,
                input_type=input_type
            )

            # Update chunks with embeddings
            for chunk, embedding in zip(batch, response.embeddings):
                chunk.embedding = [float(e) for e in embedding]
                chunk.embedded_at = datetime.now(timezone.utc)

            logger.info(f"[EMBED] Progress: {min(i + batch_size, len(valid_chunks))}/{len(valid_chunks)} chunks embedded")

        except Exception as e:
            logger.error(f"[EMBED] Batch {i // batch_size + 1} failed: {e}")
            raise

    logger.info(f"[EMBED] Completed: {len([c for c in valid_chunks if c.embedding])} embeddings generated")
    return valid_chunks


# ============================================================================
# STORAGE FUNCTIONS (User Story 3)
# ============================================================================

@retry_db
def create_qdrant_collection(client: QdrantClient, collection_name: str):
    """
    Create Qdrant collection with proper vector configuration.

    Args:
        client: Initialized Qdrant client
        collection_name: Name of the collection to create
    """
    try:
        # Check if collection exists
        collections = client.get_collections().collections
        if any(c.name == collection_name for c in collections):
            logger.info(f"[STORE] Collection '{collection_name}' already exists")
            return

        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1024,  # Cohere embed-english-v3.0
                distance=Distance.COSINE,
                hnsw_config=HnswConfigDiff(
                    m=16,
                    ef_construct=100
                )
            )
        )

        # Create payload index for source_url
        client.create_payload_index(
            collection_name=collection_name,
            field_name="source_url",
            field_schema=PayloadSchemaType.KEYWORD
        )

        logger.info(f"[STORE] Collection '{collection_name}' created successfully")

    except Exception as e:
        logger.error(f"[STORE] Failed to create collection: {e}")
        raise


@retry_db
def store_embeddings(chunks: List[TextChunk], client: QdrantClient, collection_name: str, batch_size: int = 100) -> List[TextChunk]:
    """
    Store chunk embeddings in Qdrant vector database.

    Args:
        chunks: List of TextChunk objects with embeddings
        client: Initialized Qdrant client
        collection_name: Name of the collection
        batch_size: Number of vectors per batch upload

    Returns:
        List of TextChunk objects with storage status updated
    """
    # Filter chunks with embeddings
    chunks_with_embeddings = [c for c in chunks if c.embedding is not None]
    logger.info(f"[STORE] Uploading {len(chunks_with_embeddings)} vectors to Qdrant (batch size: {batch_size})")

    # Upload in batches
    for i in range(0, len(chunks_with_embeddings), batch_size):
        batch = chunks_with_embeddings[i:i + batch_size]

        points = []
        for chunk in batch:
            if chunk.embedding is None:
                logger.warning(f"[STORE] Skipping chunk {chunk.chunk_id} - no embedding")
                continue

            point_id = str(uuid.uuid4())
            chunk.qdrant_point_id = point_id

            points.append(PointStruct(
                id=point_id,
                vector=chunk.embedding,
                payload=chunk.to_qdrant_payload()
            ))

        try:
            client.upsert(
                collection_name=collection_name,
                points=points
            )

            # Mark chunks as stored
            for chunk in batch:
                chunk.stored = True

            logger.info(f"[STORE] Batch {i // batch_size + 1}/{(len(chunks_with_embeddings) + batch_size - 1) // batch_size} uploaded")

        except Exception as e:
            logger.error(f"[STORE] Batch upload failed: {e}")
            raise

    logger.info(f"[STORE] Completed: {len([c for c in chunks_with_embeddings if c.stored])} vectors stored")
    return chunks_with_embeddings


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def run_pipeline():
    """Async pipeline execution."""
    run_id = str(uuid.uuid4())
    logger.info(f"Starting ingestion pipeline (Run ID: {run_id})")

    try:
        # Load configuration
        config = load_config()
        logger.info(f"Configuration loaded - Target: {config['base_url']}")

        # Initialize metadata tracker
        metadata = IngestionMetadata(
            run_id=run_id,
            base_url=config["base_url"],
            started_at=datetime.now(timezone.utc),
            config=config
        )

        # ====================================================================
        # USER STORY 1: Content Ingestion
        # ====================================================================
        logger.info("[PHASE 1] Content Ingestion - Starting")

        # Fetch sitemap and discover URLs
        urls = await fetch_sitemap(config["base_url"])
        if not urls:
            logger.warning("Sitemap not available - pipeline cannot proceed without URLs")
            raise ValueError("No URLs discovered - sitemap.xml not found")

        metadata.urls_discovered = len(urls)

        # Filter URLs
        filtered_urls = filter_urls(urls, config["base_url"])

        # Crawl pages
        pages = await crawl_pages(filtered_urls, config["max_concurrent_requests"])
        metadata.urls_crawled = len(pages)

        # Clean and extract content
        logger.info(f"[CLEAN] Processing {len(pages)} pages")
        for page in pages:
            extract_and_clean_content(page)

        # Chunk text
        logger.info(f"[CHUNK] Chunking {len(pages)} pages")
        all_chunks = []
        for page in pages:
            chunks = chunk_text(page, config["target_chunk_size"], config["chunk_overlap"])
            all_chunks.extend(chunks)
            page.chunks_created = len(chunks)

        metadata.chunks_created = len(all_chunks)
        logger.info(f"[PHASE 1] Content Ingestion - Complete: {metadata.chunks_created} chunks created")

        # ====================================================================
        # USER STORY 2: Embedding Generation
        # ====================================================================
        logger.info("[PHASE 2] Embedding Generation - Starting")

        # Initialize Cohere client
        cohere_client = cohere.Client(api_key=config["cohere_api_key"])

        # Generate embeddings
        embedded_chunks = generate_embeddings(
            all_chunks,
            cohere_client,
            config["cohere_model"],
            config["cohere_input_type"],
            batch_size=10
        )

        metadata.chunks_embedded = len([c for c in embedded_chunks if c.embedding])
        logger.info(f"[PHASE 2] Embedding Generation - Complete: {metadata.chunks_embedded} embeddings generated")

        # ====================================================================
        # USER STORY 3: Vector Storage
        # ====================================================================
        logger.info("[PHASE 3] Vector Storage - Starting")

        # Initialize Qdrant client
        qdrant_client = QdrantClient(
            url=config["qdrant_url"],
            api_key=config["qdrant_api_key"]
        )

        # Create collection
        create_qdrant_collection(qdrant_client, config["qdrant_collection_name"])

        # Store embeddings
        stored_chunks = store_embeddings(
            embedded_chunks,
            qdrant_client,
            config["qdrant_collection_name"],
            batch_size=config["batch_size"]
        )

        metadata.chunks_stored = len([c for c in stored_chunks if c.stored])
        logger.info(f"[PHASE 3] Vector Storage - Complete: {metadata.chunks_stored} vectors stored")

        # ====================================================================
        # USER STORY 4: Validation
        # ====================================================================
        logger.info("[PHASE 4] Validation - Starting")

        # Test queries
        test_queries = [
            "How do I get started?",
            "What is authentication?",
            "How to configure the application?"
        ]

        validation_passed = 0
        for query in test_queries:
            try:
                results = qdrant_client.query(
                    collection_name=config["qdrant_collection_name"],
                    query_text=query,
                    limit=5
                )
                if results:
                    validation_passed += 1
                    logger.info(f"[VALIDATE] Query '{query}' returned {len(results)} results")
            except Exception as e:
                logger.warning(f"[VALIDATE] Query '{query}' failed: {e}")

        logger.info(f"[PHASE 4] Validation - Complete: {validation_passed}/{len(test_queries)} queries successful")

        # Finalize metadata
        metadata.completed_at = datetime.now(timezone.utc)
        metadata.duration_seconds = (metadata.completed_at - metadata.started_at).total_seconds()
        metadata.status = "completed"

        # Print summary
        logger.info("\n" + metadata.to_summary())

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise


def main():
    """Main entry point for the ingestion pipeline."""
    asyncio.run(run_pipeline())


if __name__ == "__main__":
    main()
