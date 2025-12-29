---
id: 001
title: Setup Textbook Constitution
stage: constitution
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["constitution", "setup", "textbook", "physical-ai", "robotics"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

You are an expert AI textbook architect, roboticist, and technical documentation author.

Your mission is to:
- Convert the provided source document into a complete professional textbook website.
- The book will teach a full university-level course on:
  "Physical AI & Humanoid Robotics".
- The output must be:
  - Fully structured
  - Beginner to Advanced level
  - 100% Docusaurus compatible
  - Free from hallucination
  - Based strictly on the provided content

Rules:
- No missing concepts.
- No marketing fluff.
- Prioritize engineering accuracy.
- Use:
  - Clear chapter hierarchy
  - Lessons
  - Code examples
  - Diagrams (described in text)
  - Tables where useful

Website Structure:
- Total Chapters = 5
- Each chapter must be a complete independent learning unit.
- Each chapter must be publishable as a single Docusaurus doc.

Wait for the specification command.

## Response snapshot

Created comprehensive constitution for Physical AI & Humanoid Robotics textbook project with 7 core principles:

1. Content Fidelity - Zero hallucination, all content traceable to source
2. Academic Rigor - University-level standards, beginner to advanced
3. Structural Completeness - Exactly 5 complete, independent chapters
4. Docusaurus Compatibility (NON-NEGOTIABLE) - Valid markdown, proper frontmatter
5. Pedagogical Structure - Consistent teaching architecture across chapters
6. Engineering Focus - Pure technical content, production-quality examples
7. Multi-Modal Learning - Code, tables, diagrams, math notation

Defined chapter structure (10-part fixed architecture), quality gates, workflow, and strict constraints. Constitution establishes foundation for accurate, complete, professional textbook generation.

## Outcome

- ✅ Impact: Project constitution established defining all standards for textbook generation
- 🧪 Tests: none
- 📁 Files: Created .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify with source document to create feature specification
- 🧠 Reflection: Constitution provides clear guardrails for zero-hallucination, Docusaurus-compatible, academically rigorous textbook generation

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A - constitution setup
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Await source document and run /sp.specify to create chapter plan
