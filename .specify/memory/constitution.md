<!--
Sync Impact Report:
Version change: 1.0.0 → 1.0.1 (PATCH: Re-affirmation and consistency check)
Modified principles: None
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .specify/templates/commands/*.md: ✅ updated
Follow-up TODOs: None
-->
# AI-Native Software Development — Full-Length Technical Book Constitution

## Core Principles

### Accuracy
Accuracy through primary source verification (technical docs, standards, academic research).

### Clarity
Clarity for a professional software audience (developers, CS students, AI engineers).

### Reproducibility
All examples MUST run or compile as written.

### Rigor
Peer-reviewed and authoritative sources preferred.

### Consistency
Tone, terminology, structure maintained across all chapters.

### Documentation Quality
Documentation quality matching industry-standard technical books.

## Key Standards

- All factual claims MUST be traceable to sources.
- Citation format: APA style at the end of each chapter.
- Source types: minimum 40% peer-reviewed academic references.
- Plagiarism tolerance: 0%.
- Writing clarity: Flesch-Kincaid Grade 9–12.
- Technical correctness: all code examples MUST be tested and valid.
- File format: Markdown chapters compatible with Docusaurus.
- Deployment-ready: Book MUST build cleanly and deploy on GitHub Pages.

## Project Constraints

- Book length: 30,000–50,000 words.
- Number of chapters: 10–20.
- Minimum 25 credible sources across the full book.
- All images stored under `/static/img/book/`.
- Code blocks MUST include language identifiers.

## Must Use Technologies

- Spec-Kit Plus (constitution, chapter specs, workflow, QA)
- Claude Code for writing and revision
- Docusaurus for book structure and navigation
- GitHub Pages for deployment

## Success Criteria

- All claims verified against reliable sources.
- Zero plagiarism detected.
- Writing style remains consistent with the `/sp.style-guide`.
- Book compiles without warnings or broken links in Docusaurus.
- Successful GitHub Pages deployment.
- Content demonstrates rigor, clarity, and correctness.
- Target readers (engineers, students, practitioners) can learn and reproduce all examples.

## Governance

This constitution supersedes all other practices; Amendments require documentation, approval, and a migration plan. All PRs/reviews MUST verify compliance.

**Version**: 1.0.1 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
