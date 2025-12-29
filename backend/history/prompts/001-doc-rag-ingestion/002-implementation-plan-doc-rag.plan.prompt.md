---
id: 002
title: implementation-plan-doc-rag
stage: plan
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: 001-doc-rag-ingestion
branch: 001-doc-rag-ingestion
user: Abdul Mannan
command: /sp.plan
labels: ["plan", "rag", "ingestion", "documentation", "embeddings", "architecture"]
links:
  spec: specs/001-doc-rag-ingestion/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-doc-rag-ingestion/plan.md
  - specs/001-doc-rag-ingestion/research.md
  - specs/001-doc-rag-ingestion/data-model.md
  - specs/001-doc-rag-ingestion/quickstart.md
tests:
  - Phase 0 research completed (4 research agents)
  - Phase 1 design artifacts generated
---

## Prompt

/sp.plan spec-1: URL Ingestion and Embedding pipeline

- In backend folder, initialize project with 'UV', and add a single 'main.py'
- In 'main.py', implement URL fetching,  text cleaning, and chunking
- generate embeddings using cohere models
- store embeddings and metadata in Qdranrt cloud
- Add a 'main()' function to run the full ingestion pipeline end-to-end

## Response snapshot

Created comprehensive implementation plan for Documentation RAG Ingestion System following Spec-Driven Development workflow.

**Phase 0: Research & Technology Decisions**
Launched 4 parallel research agents to investigate:
1. Cohere embedding models → Decision: embed-english-v3.0 (1024 dims, 512 token context)
2. Docusaurus crawling strategy → Decision: Sitemap-first with recursive fallback
3. Text chunking strategy → Decision: Hybrid markdown-aware recursive chunking (400 tokens, 20% overlap)
4. Qdrant configuration → Decision: Cosine distance, HNSW m=16, ef_construct=100, batch size 100

All research findings consolidated in `research.md` with detailed rationale, alternatives considered, and implementation recommendations.

**Phase 1: Design & Contracts**
Generated design artifacts:
1. **data-model.md**: Complete data structures for all 4 entities
   - DocumentationPage (transient, in-memory)
   - TextChunk (persistent, core entity)
   - EmbeddingVector (stored with chunk)
   - IngestionMetadata (run tracking)
   - Validation rules, state transitions, and relationships

2. **quickstart.md**: Developer-ready setup guide
   - Prerequisites and installation steps
   - Environment configuration (.env template)
   - Usage instructions with expected output
   - Troubleshooting guide for common issues
   - Validation procedures

**Implementation Plan Structure**:
- Single-file architecture (backend/main.py) for simplicity
- UV for package management (modern Python tooling)
- Async HTTP with httpx for performance
- Batch processing (100 vectors) for Qdrant uploads
- Comprehensive error handling with retry logic
- Structured logging at each pipeline stage

**Technical Stack Finalized**:
- Python 3.11+, httpx, beautifulsoup4, cohere, qdrant-client, python-dotenv, tenacity
- Cohere embed-english-v3.0 (1024 dimensions)
- Qdrant Cloud free tier (~300MB for 50K chunks)
- LangChain RecursiveCharacterTextSplitter for chunking

**Key Design Decisions**:
1. Sitemap.xml parsing (10-20x faster than recursive crawling)
2. 400-token chunks with 80-token overlap (balances context & precision)
3. Cosine similarity in Qdrant (optimal for normalized Cohere embeddings)
4. Three-tier deduplication (URL, content hash, chunk hash)
5. Rich metadata per chunk (enables filtering, re-ranking, citation)

**Constitution Check**: All gates passed (simplicity, testability, error handling, configuration management, observability)

**Files Created**:
- specs/001-doc-rag-ingestion/plan.md (comprehensive implementation plan)
- specs/001-doc-rag-ingestion/research.md (all technical decisions documented)
- specs/001-doc-rag-ingestion/data-model.md (4 entity definitions with validation)
- specs/001-doc-rag-ingestion/quickstart.md (setup and usage guide)

## Outcome

- ✅ Impact: Complete architectural plan ready for task generation (/sp.tasks) and implementation
- 🧪 Tests: Phase 0 research validated via 4 parallel agents, Phase 1 design artifacts complete
- 📁 Files: 4 planning documents created (plan.md, research.md, data-model.md, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks, then begin TDD cycle
- 🧠 Reflection: Planning phase successfully balanced depth (comprehensive research) with speed (parallel agents), resulting in production-ready architecture

## Evaluation notes (flywheel)

- Failure modes observed: None - all research agents completed successfully, design artifacts validated
- Graders run and results (PASS/FAIL): PASS - Constitution check passed all gates, data model validated
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 (research) + Phase 1 (design)
- Next experiment (smallest change to try): Proceed to /sp.tasks for task breakdown, implement in TDD style
