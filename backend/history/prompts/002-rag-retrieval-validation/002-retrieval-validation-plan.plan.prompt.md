---
id: 002
title: retrieval-validation-plan
stage: plan
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: 002-rag-retrieval-validation
branch: 002-rag-retrieval-validation
user: Abdul Mannan
command: /sp.plan
labels: ["plan", "rag", "retrieval", "validation", "vector-db", "qdrant", "architecture"]
links:
  spec: specs/002-rag-retrieval-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-rag-retrieval-validation/plan.md
  - specs/002-rag-retrieval-validation/data-model.md
  - specs/002-rag-retrieval-validation/quickstart.md
tests:
  - Plan structure validated (all mandatory sections present)
  - Architecture decision documented (single-file retrieve.main.py)
  - All 4 user stories mapped to implementation phases
  - 30 tasks identified across 5 phases
---

## Prompt

/sp.plan Spec-2: Retrieval and pipeline validation

- create a single file 'retrieve.main.py' in the backend folder
- connect to Qdrant and load existing vector collections
- Accept a test quries and perform top-k similarity search
- valiadate result using returned text, metadata, and  source URLs

## Response snapshot

Successfully created comprehensive implementation plan for RAG Retrieval Validation feature (spec-2) following Spec-Driven Development workflow.

**Feature Branch**: 002-rag-retrieval-validation

**Plan Structure**:

**Technical Context**:
- Building validation script (`retrieve.main.py`) to test RAG retrieval pipeline
- Depends on spec-1 (001-doc-rag-ingestion) - requires existing Qdrant collection with stored embeddings
- Architecture decision: Single-file implementation following main.py pattern from spec-1

**Architecture Decision - Single-File Validation Script**:
- **Decision**: Implement as standalone `retrieve.main.py` following same pattern as `main.py`
- **Rationale**: Consistency with existing codebase, simplicity for 1-2 task scope, easy to execute independently
- **Tradeoffs**: ✅ Simplicity, portability, low overhead | ❌ Some code duplication with main.py, not scalable beyond MVP
- **Alternatives Considered**:
  1. Shared utilities module (rejected: over-engineering for scope)
  2. Integration into main.py (rejected: mixes concerns)
  3. Jupyter notebook (rejected: less reproducible)

**Phase 0: Research & Technical Decisions** (4 research areas):
1. **R1 - Qdrant Query Methods**: Use `client.search()` with query_vector from Cohere embeddings
2. **R2 - Cohere Embedding API**: Use `input_type="search_query"` for queries (asymmetric search)
3. **R3 - Validation Metrics**: Track connection success, query success rate, avg similarity, metadata completeness, execution time
4. **R4 - Test Query Design**: 10 queries in 3 categories (specific, broad, negative)

**Phase 1: Design & Contracts**:
- **Data Model**: 3 entities defined (RetrievalQuery, RetrievalResult, ValidationReport)
- **Core Functions**: 7 function contracts (load_config, validate_connection, embed_query, search_similar_chunks, validate_metadata, run_validation_suite, main)
- **Error Handling**: 4 categories (connection, collection, query, validation errors) with retry strategy
- **Test Queries**: 10 predefined queries (5 specific, 3 broad, 2 negative)

**Phase 2: Implementation Workflow** (30 tasks across 5 phases):
1. **Setup (T001-T005)**: Skeleton, data models, config, retry decorators, test queries
2. **User Story 1 - Connection Validation (T006-T010)**: validate_connection, collection stats, error handling, logging
3. **User Story 2 - Query Execution (T011-T018)**: embed_query, search_similar_chunks, result parsing, logging
4. **User Story 3 - Metadata Validation (T019-T023)**: validate_metadata, URL validation, completeness check
5. **User Story 4 - End-to-End Validation (T024-T030)**: run_validation_suite, metrics aggregation, error tracking, reporting

**Phase 3: Validation & Testing**:
- Unit testing (optional, beyond scope)
- Integration testing (4 required test cases)
- Manual validation checklist (8 items from SC-001 to SC-008)

**Phase 4: Documentation**:
- quickstart.md: Prerequisites, how to run, interpreting reports, troubleshooting
- Code documentation: Module and function docstrings
- README.md update: Validation section

**Non-Functional Requirements**:
- **Performance**: Single query <2s, 10 queries <20s, connection validation <5s
- **Reliability**: 3-attempt retry logic, graceful error handling, structured logging
- **Security**: Credentials from .env only, no hardcoded secrets
- **Maintainability**: Follow main.py conventions, single responsibility, minimal comments

**Dependencies & Risks**:
- **External**: Qdrant Cloud (accessible, contains vectors), Cohere API (available)
- **Internal**: Spec-1 completion (vectors exist), environment config (valid credentials)
- **Risks**: Collection empty (high impact, medium probability), API rate limits (medium/low), metadata mismatch (medium/low)

**Success Criteria Mapping**: All 8 success criteria (SC-001 to SC-008) mapped to implementation tasks

**Acceptance Criteria** (9 items):
1. retrieve.main.py exists and runs without errors
2. Connection validation succeeds and reports stats
3. Test queries return top-5 results with metadata
4. Metadata validation shows 100% completeness
5. Validation suite generates complete report
6. All 8 success criteria verified
7. quickstart.md created
8. data-model.md documents entities
9. Backend README.md updated

**Timeline Estimate**: 30 tasks, ~110 minutes (~2 hours), fits 1-2 task constraint

**Artifacts Created**:

1. **plan.md** (complete implementation plan):
   - Technical context and existing architecture
   - Architecture decision with rationale and tradeoffs
   - Research phase with 4 technical decisions resolved
   - Design phase with data model, function contracts, error handling
   - Implementation workflow with 30 tasks across 5 phases
   - Validation and testing strategy
   - Documentation plan
   - Non-functional requirements
   - Dependencies and risk analysis
   - Success criteria mapping
   - Acceptance criteria
   - Timeline estimate

2. **data-model.md** (complete entity definitions):
   - **RetrievalQuery**: Input specification for semantic search
     - Fields: query_text, top_k, similarity_threshold, query_id, created_at
     - Python dataclass implementation
     - Usage examples and validation rules
   - **RetrievalResult**: Single search result with metadata and score
     - Fields: query_id, chunk_text, source_url, page_title, section_heading, breadcrumb, chunk_index, similarity_score, metadata, rank
     - Qdrant payload schema documentation
     - Validation rules and metadata completeness checks
   - **ValidationReport**: Aggregated metrics and summary
     - Fields: run_id, total_queries, successful_queries, failed_queries, avg_similarity_score, avg_query_time, metadata_completeness, total_results_retrieved, connection_status, collection_stats, errors, started_at, completed_at
     - Computed properties: duration_seconds, success_rate
     - to_summary() method for human-readable report
   - **Relationships**: Query → Results → Report flow diagram
   - **Data Transformations**: Qdrant → RetrievalResult, Results → ValidationReport
   - **Validation & Error Handling**: Field validation, defensive extraction, edge cases
   - **Complete Example**: Full validation flow from query to report

3. **quickstart.md** (comprehensive usage guide):
   - **Overview**: Purpose and when to use validation script
   - **Prerequisites**: Spec-1 completion, environment setup, dependencies
   - **Quick Start**: Single command to run validation
   - **Expected Output**: Complete example validation report
   - **Interpreting Reports**: Section-by-section explanation with "What to check" guidance
   - **Test Queries Explained**: 10 queries categorized by purpose
   - **Troubleshooting**: 7 common errors with symptoms and fixes
     - Missing environment variables
     - Collection not found
     - Cohere API rate limits
     - Low similarity scores
     - Connection timeouts
     - Metadata completeness issues
   - **Customizing Test Queries**: How to edit TEST_QUERIES
   - **Next Steps**: Integration, monitoring, optimization, updates
   - **Configuration Reference**: All environment variables and script parameters
   - **Success Criteria Checklist**: 8-item checklist from spec
   - **Example Workflows**: First-time setup, after updates, debugging
   - **Additional Resources**: Links to spec, plan, data-model, external docs

**Key Design Decisions**:

1. **Single-File Architecture** (retrieve.main.py):
   - Maintains consistency with main.py from spec-1
   - Simplifies execution and understanding
   - Appropriate for validation use case scope
   - Trade-off: Some duplication vs. unnecessary abstraction

2. **Asymmetric Embeddings**:
   - Documents: `input_type="search_document"`
   - Queries: `input_type="search_query"`
   - Follows Cohere best practices for semantic search

3. **Test Query Categories**:
   - 5 specific queries (high similarity expected)
   - 3 broad queries (moderate similarity)
   - 2 negative queries (low similarity expected)
   - Validates both retrieval quality and irrelevant query handling

4. **Validation Metrics**:
   - Connection success (binary)
   - Query success rate (%)
   - Average similarity score (0.0-1.0)
   - Metadata completeness (%)
   - Execution time per query (seconds)
   - Aligned with all 8 success criteria from spec

5. **Error Handling Strategy**:
   - Retry logic for API and DB operations (3 attempts, exponential backoff)
   - Fail fast for connection/config errors
   - Graceful degradation for query failures
   - Comprehensive error reporting in ValidationReport

**Implementation Phases Mapped to User Stories**:

- **Phase 2.1 (Setup)**: Foundation for all user stories
- **Phase 2.2 (T006-T010)**: User Story 1 - Connection Validation
- **Phase 2.3 (T011-T018)**: User Story 2 - Query Execution
- **Phase 2.4 (T019-T023)**: User Story 3 - Metadata Validation
- **Phase 2.5 (T024-T030)**: User Story 4 - End-to-End Validation

**Technical Stack** (reuses spec-1 dependencies):
- Python 3.11+ with dataclasses
- qdrant-client for vector search
- cohere for query embeddings
- python-dotenv for configuration
- tenacity for retry logic
- Structured logging for progress tracking

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation (/sp.tasks) and implementation (/sp.implement)
- 🧪 Tests: Plan structure validated, architecture decision documented, all user stories mapped
- 📁 Files: 3 files created (plan.md, data-model.md, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed task breakdown, then `/sp.implement` to create retrieve.main.py
- 🧠 Reflection: Planning successfully balanced single-file architecture constraint with comprehensive validation requirements. Research phase resolved all technical unknowns upfront. Data model provides clear contracts for implementation. Quickstart guide ensures smooth user experience. Architecture decision maintains consistency with spec-1 while avoiding over-engineering.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed without blockers
- Graders run and results (PASS/FAIL): PASS - All plan sections complete, architecture decision documented with rationale, 30 tasks identified
- Prompt variant (if applicable): Standard /sp.plan workflow with user directive for single-file implementation
- Next experiment (smallest change to try): Proceed to /sp.tasks to generate detailed task breakdown with acceptance criteria
