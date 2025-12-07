# Implementation Plan: AI/Spec-Driven Book Creation

## Project: AI/Spec-Driven Book Creation Using Docusaurus, Spec-Kit Plus, and Claude Code
## Reference: Constitution + High-Level Book Layout (Iteration 1)

---

## Objective

This technical plan guides the architecture, content creation workflow, research methodology, quality checks, and documentation decisions for writing and publishing the "Physical AI & Humanoid Robotics" book. This plan sets the foundation before detailed chapter specs in Iteration 2.

---

## 1. Architecture Sketch

### Book Structure
The book will follow a modular structure:
- **Modules**: High-level thematic sections (e.g., "The Robotic Nervous System").
- **Chapters**: Subdivisions within modules, focusing on specific concepts or technologies.
- **Content Blocks**: Individual sections within chapters (e.g., learning objectives, key concepts, code examples, diagrams, citations).

### Docusaurus Folder Hierarchy
The Docusaurus project will be structured as follows:
```
├── docs/
│   ├── module-1/
│   │   ├── chapter-1.md
│   │   ├── chapter-2.md
│   │   └── ...
│   ├── module-2/
│   │   ├── chapter-1.md
│   │   └── ...
│   └── ...
├── src/
│   └── components/ (for custom React components, e.g., interactive diagrams)
├── static/
│   ├── img/
│   │   └── book/ (all book images, as per constitution)
│   └── ...
├── docusaurus.config.js
├── sidebar.js
└── ...
```

### Content Delivery Pipeline
1.  **Spec**: Detailed specifications for each module and chapter are created using Spec-Kit Plus.
2.  **Draft**: Claude Code assists in generating initial content drafts based on the chapter specs and research findings.
3.  **Review**: Human author reviews, edits, and refines content for accuracy, clarity, and technical rigor.
4.  **Commit**: Approved changes are committed to a feature branch.
5.  **Build**: Docusaurus builds the static site.
6.  **Deploy**: GitHub Actions deploys the static site to GitHub Pages.

### Toolchain Interactions
-   **Spec-Kit Plus**: Used for defining the `constitution.md`, `spec.md`, `plan.md`, `tasks.md`, `workflow.md`, and `style-guide.md`.
-   **Claude Code**: Functions as an AI assistant for content generation, research extraction, summarization, grammar/consistency checks, and revisions.
-   **GitHub**: Version control for the entire project, hosting the Docusaurus source and managing pull requests.
-   **GitHub Pages**: Static site hosting for the published Docusaurus book.
-   **Docusaurus build engine**: Compiles Markdown files and React components into a static HTML/CSS/JS website.

### Automated Deployment Workflow (GitHub Actions)
A GitHub Actions workflow will be configured to:
1.  Trigger on pushes to the `main` branch or specific release branches.
2.  Install Node.js dependencies.
3.  Build the Docusaurus site.
4.  Deploy the generated static files to the `gh-pages` branch.

### Version Control Flow
-   **Feature Branches**: Each module or major feature (e.g., /sp.spec.module1, /sp.spec.module2) will have its own feature branch (e.g., `001-physical-ai-book`).
-   **Main Branch**: Represents the stable, reviewed version of the book's source code. Merges from feature branches occur after review.
-   **gh-pages Branch**: Automatically updated by GitHub Actions with the built Docusaurus site for public deployment.

---

## 2. Section Structure for Every Chapter

Each chapter will adhere to the following uniform internal structure:

-   **Learning Objectives**: 2-3 concise statements outlining what the reader will learn.
-   **Key Concepts**: A bulleted list of essential terms and ideas introduced in the chapter.
-   **Introduction**: Overview of the chapter's topic and its relevance.
-   **Sub-sections**:
    -   Pattern: `## Main Section Title`, `### Sub-section Title`, `#### Detail Sub-section Title`.
    -   Each sub-section will cover a specific aspect of the chapter's topic, including explanations, code examples, diagrams, and illustrations.
    -   **Code Examples**: Must be Python-based using `rclpy` where applicable (for ROS 2 modules), syntactically valid (URDF/SDF), and runnable. All code blocks MUST include language identifiers.
    -   **Diagrams/Illustrations**: Text-based ASCII diagrams or references to images in `/static/img/book/` for conceptual clarity, simulation setups, and architectural overviews.
-   **Citations**: In-text citations using APA style, with a full bibliography at the end of the chapter.
-   **Summary**: A brief recap of the chapter's main points.
-   **Review Questions/Exercises**: Optional, for reinforcing learning.
-   **Expected Length**: Chapters will aim for 2,000-5,000 words, contributing to the overall book length of 30,000–50,000 words across 10-20 chapters.
-   **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides to ensure accuracy and rigor.

---

## 3. Research Approach (Research-Concurrent Workflow)

The research approach will follow a "research-concurrent" workflow:
-   **Just-in-Time Research**: Research will be conducted while writing each chapter, rather than all upfront, to ensure the most current and relevant information is integrated.
-   **Source Quality**: Prioritize peer-reviewed academic sources (minimum 50% of references), official documentation (ROS 2, Gazebo, Unity, NVIDIA Isaac), and reputable industry whitepapers.
-   **Citation Style**: All citations will follow APA style, as mandated by the Constitution.
-   **Bibliography Management**: A running bibliography file (`bibliography.md` or similar) will be maintained to track all sources used across the book. Integration with Zotero/RefWorks is optional, but citation data must be exportable to APA format.
-   **Claim Verification**: All factual claims will be verified with primary sources to ensure accuracy and reproducibility.
-   **Original Summaries**: Summaries and explanations derived from research will be original and non-plagiarized, reflecting a deep understanding of the source material.
-   **Claude Code for Literature Extraction + Summarization**: Claude Code will be utilized to extract key information from research papers and online articles, and to generate concise, accurate summaries for integration into the book content.

---

## 4. Quality Validation Framework

The book's quality will be ensured through a multi-faceted framework combining automated checks and human review:

### Automated Checks
-   **Accuracy (Factual Verification)**:
    -   **Source Traceability Test**: Each claim must be linked to a verifiable source. Automated checks will flag statements lacking in-text citations.
    -   **Technical Correctness**: Code examples will be automatically tested for syntax errors and execution (e.g., ROS 2 nodes, URDF parsing).
-   **Clarity**:
    -   **Readability Metrics**: Automated tools will calculate Flesch-Kincaid grade levels for each chapter, aiming for a consistent grade 9–12.
    -   **Grammar/Consistency**: Claude Code revisions will be employed for grammar, spelling, and stylistic consistency, supplemented by linting tools for Markdown.
-   **Reproducibility**:
    -   **Code Execution Tests**: Automated scripts will run all code examples to confirm they function as written.
-   **Formatting Consistency**:
    -   **Markdown Linting**: `markdownlint` or similar will enforce consistent Markdown formatting across all chapters.
    -   **Docusaurus Build**: The Docusaurus build process itself will act as a linting step, flagging broken links, image paths, and structural issues.
-   **Plagiarism**:
    -   **Plagiarism Detection**: Automated tools will be used to ensure 0% plagiarism tolerance before finalization.

### Human Checks
-   **Technical Rigor**: Human experts (reviewers) will verify the industry and academic correctness of technical explanations and examples.
-   **Content Quality**: Manual review will focus on logical flow, coherence, depth of explanation, and overall learning effectiveness.
-   **Formatting Consistency**: Visual inspection of the deployed Docusaurus site to ensure consistent rendering across devices and browsers.
-   **Proofreading**: Final human proofreading pass for any subtle errors missed by automated tools.

---

## 5. Decisions Needing Documentation (with Options, Trade-offs, and Chosen Option)

### 5.1 Choice of Docusaurus vs MkDocs vs GitBook
-   **Options**: Docusaurus, MkDocs, GitBook.
-   **Trade-offs**:
    -   **Docusaurus**: Pros: React-based, highly customizable, excellent for technical documentation, built-in versioning, search, blog support. Cons: Steeper learning curve than MkDocs, more overhead for simple sites.
    -   **MkDocs**: Pros: Simple, Python-based, easy to set up, good for basic documentation. Cons: Less customizable, limited features compared to Docusaurus, harder to extend with complex interactive components.
    -   **GitBook**: Pros: User-friendly interface, good for non-technical authors, collaborative features. Cons: Often proprietary, less control over underlying tech stack, can be costly for commercial use.
-   **Chosen Option**: **Docusaurus**.
    -   **Rationale**: Docusaurus aligns perfectly with the need for a highly customizable, technically robust platform suitable for a comprehensive technical book. Its React foundation allows for future interactive components, and its strong documentation features support the structured approach required.

### 5.2 Deployment Pipeline Design
-   **Options**: Manual deployment, CI/CD with GitHub Actions, Netlify/Vercel integration.
-   **Trade-offs**:
    -   **Manual**: Pros: Simple for small projects. Cons: Error-prone, slow, not scalable.
    -   **GitHub Actions**: Pros: Free for public repos, integrated with GitHub, highly customizable, automated. Cons: Requires YAML configuration knowledge.
    -   **Netlify/Vercel**: Pros: Extremely easy setup, good performance, serverless functions. Cons: Potential vendor lock-in, limited customization in free tiers.
-   **Chosen Option**: **CI/CD with GitHub Actions**.
    -   **Rationale**: GitHub Actions provides a robust, free, and integrated solution for automated deployment to GitHub Pages, fulfilling the Constitution's requirement for deployment readiness. It offers granular control and fits within the existing GitHub-centric workflow.

### 5.3 Structure of Modules and Chapters
-   **Options**: Flat structure (all chapters at root), hierarchical structure (modules contain chapters), chronological vs. thematic ordering.
-   **Trade-offs**:
    -   **Flat**: Pros: Simple for small books. Cons: Hard to navigate large, multi-topic books.
    -   **Hierarchical (Modular)**: Pros: Clear organization, easy navigation, reflects logical progression of topics. Cons: Slightly more complex setup initially.
-   **Chosen Option**: **Hierarchical, thematic modules containing chapters**.
    -   **Rationale**: This structure (Modules → Chapters → Content Blocks) directly supports the logical progression of Physical AI concepts as outlined in the `spec.md`, ensuring clarity and ease of navigation for readers.

### 5.4 Citation Management Method
-   **Options**: Manual APA formatting, Zotero/RefWorks integration, Markdown-based citation tools.
-   **Trade-offs**:
    -   **Manual**: Pros: Full control. Cons: Time-consuming, error-prone for large bibliographies.
    -   **Zotero/RefWorks**: Pros: Automated formatting, easy source management. Cons: External tool dependency, potential integration challenges with Docusaurus Markdown.
    -   **Markdown-based tools**: Pros: Native to Markdown workflow. Cons: Less mature, might lack advanced features of dedicated citation managers.
-   **Chosen Option**: **Manual APA formatting with a running bibliography file, supported by Claude Code for formatting assistance**. Zotero/RefWorks is optional for source gathering but final output must be pure Markdown APA.
    -   **Rationale**: While Zotero offers convenience, ensuring seamless integration with Docusaurus and a pure Markdown workflow is paramount. Claude Code can assist with adhering to APA guidelines, and a centralized bibliography file ensures consistency without external tool dependencies for the final render.

### 5.5 Image Generation Workflow
-   **Options**: Manual creation (tools like draw.io, Mermaid.js for diagrams), AI-generated images, combination.
-   **Trade-offs**:
    -   **Manual**: Pros: Precise control, high quality. Cons: Time-consuming.
    -   **AI-generated**: Pros: Fast, diverse styles. Cons: Consistency issues, factual accuracy concerns, need for careful prompting.
    -   **Combination**: Pros: Balance of speed and quality. Cons: Requires managing multiple tools.
-   **Chosen Option**: **Combination of Mermaid.js (for architectural diagrams within Markdown), manual creation for complex illustrations (using standard graphics software), and AI-assisted generation for conceptual images (with strict human review for accuracy)**. All images will be stored in `/static/img/book/`.
    -   **Rationale**: Mermaid.js allows diagrams to be version-controlled directly within Markdown, promoting reproducibility. Manual tools ensure high-quality, precise technical diagrams. AI assistance speeds up conceptual image creation, but requires human oversight to prevent hallucinations.

### 5.6 Whether to Include Interactive Components
-   **Options**: Static content only, simple interactive elements (code sandboxes, collapsible sections), complex simulations/3D models.
-   **Trade-offs**:
    -   **Static**: Pros: Simplest to implement, widest compatibility. Cons: Less engaging.
    -   **Simple Interactive**: Pros: Increased engagement, clearer explanations. Cons: Adds development complexity (React components).
    -   **Complex Simulations**: Pros: Highly immersive. Cons: Significant development effort, performance concerns, browser compatibility.
-   **Chosen Option**: **Initially static content with a plan for simple interactive elements (e.g., live code sandboxes for Python/ROS 2 examples, collapsible sections) in future iterations if deemed beneficial for learning.**
    -   **Rationale**: Prioritizing core content creation and stable deployment (Phase 1-4) is critical. Docusaurus's React foundation allows for adding interactive components later without a major architectural shift, enabling incremental enhancement.

### 5.7 How AI Tools Assist Without Hallucinating
-   **Options**: AI for drafting only, AI for factual extraction (WebFetch), AI for summarization, AI for stylistic/grammar checks.
-   **Trade-offs**:
    -   **Drafting only**: Pros: Speeds up initial writing. Cons: High risk of hallucination if not fact-checked rigorously.
    -   **Factual extraction/summarization**: Pros: Reduces research time, provides structured information. Cons: Still requires human verification of accuracy.
    -   **Stylistic/grammar checks**: Pros: Improves writing quality. Cons: AI might suggest stylistic changes that conflict with the established style guide.
-   **Chosen Option**: **Claude Code will primarily assist with factual extraction (using WebSearch/WebFetch), summarization of research materials, drafting initial content blocks (which will undergo strict human review for accuracy), and performing grammar/consistency checks against the style guide.**
    -   **Rationale**: Leveraging Claude Code for these specific tasks maximizes its utility while mitigating the risk of hallucination through human oversight, source verification, and adherence to the quality framework.

### 5.8 Branching Strategy and Commit Workflow
-   **Options**: GitFlow, GitHub Flow, Trunk-Based Development.
-   **Trade-offs**:
    -   **GitFlow**: Pros: Strict release management. Cons: Complex, overkill for this project.
    -   **GitHub Flow**: Pros: Simple, continuous deployment-friendly. Cons: Less formal release process.
    -   **Trunk-Based**: Pros: Fast iteration, continuous integration. Cons: Requires very high test coverage.
-   **Chosen Option**: **GitHub Flow with feature branches for each module/major feature (`001-physical-ai-book`), merging into `main` after review, and automated deployment to `gh-pages` branch.**
    -   **Rationale**: GitHub Flow is well-suited for a project with continuous content creation and deployment. Feature branches (`001-physical-ai-book`) provide isolation for module development, and merging into `main` ensures a stable base before deployment.

---

## 6. Testing Strategy (Acceptance Tests Aligned with Constitution)

The testing strategy will incorporate both automated and manual checks to ensure all aspects of the book's quality and functionality.

-   ***Source Traceability Test***:
    -   **Description**: Every factual claim in the book must map to a credible, cited source.
    -   **Methodology**: Automated script to check for in-text citations for all factual assertions. Manual review to verify the quality and relevance of cited sources.
    -   **Tools**: Custom Python script, human review.

-   ***APA Citation Test***:
    -   **Description**: All citations and bibliography entries must adhere strictly to APA style guidelines.
    -   **Methodology**: Automated linting of bibliography entries and in-text citation format. Manual spot checks for complex cases.
    -   **Tools**: Zotero/RefWorks export validation (if used), custom regex checks, human review.

-   ***Non-Plagiarism Test***:
    -   **Description**: The book must score 0% plagiarism (excluding correctly cited quotes and common phrases).
    -   **Methodology**: Content will be submitted to a plagiarism detection service before finalization.
    -   **Tools**: Commercial/academic plagiarism detection software.

-   ***Content Quality Test***:
    -   **Description**: Evaluates readability, coherence, logical flow, depth of explanation, and technical accuracy.
    -   **Methodology**: Flesch-Kincaid readability score analysis (automated), peer review by subject matter experts, and editorial review for clarity and engagement.
    -   **Tools**: Readability checkers, human reviewers.

-   ***Technical Deployment Test***:
    -   **Description**: Ensures the Docusaurus project builds correctly and deploys successfully to GitHub Pages.
    -   **Methodology**:
        -   **Docusaurus Build Validation**: Automated execution of `npm run build` within the CI/CD pipeline, checking for zero errors or warnings.
        -   **GitHub Actions Deployment Success**: Verification that the GitHub Actions workflow completes successfully, deploying to the `gh-pages` branch.
        -   **Link and Image Resolution**: Automated check of all internal and external links, and image paths, to ensure no broken references on the deployed site.
    -   **Tools**: GitHub Actions, `docusaurus build`, custom link checker.

-   ***Module Consistency Test***:
    -   **Description**: Verifies that all chapters within a module and across different modules adhere to the defined section structure pattern.
    -   **Methodology**: Automated structural analysis of Markdown files against a predefined template. Manual review for subjective consistency aspects (tone, depth).
    -   **Tools**: Custom script, human review.

-   ***Spec Compliance Test***:
    -   **Description**: Each chapter and module must follow its corresponding `spec.md` exactly, fulfilling all functional requirements and acceptance criteria.
    -   **Methodology**: Manual review of each chapter against its specification, cross-referencing requirements with implemented content.
    -   **Tools**: Human review, `spec.md` documents.

---

## 7. Phase Organization (Mandatory)

#### Phase 1 — Research (Ongoing)
-   **Gather Preliminary Sources**: Identify and collect foundational academic papers, official documentation, and authoritative books relevant to Physical AI, ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA.
-   **Create Shared Citation Library**: Establish a common system (e.g., a shared Markdown bibliography file, potentially backed by Zotero/RefWorks) for managing all research sources in APA format.
-   **Identify Gaps in Existing Literature**: Conduct initial literature reviews to pinpoint areas where current knowledge is sparse or outdated, informing the unique contributions of the book.
-   **Evaluate Toolchain Capabilities**: Confirm the readiness and specific features of Spec-Kit Plus, Claude Code, Docusaurus, GitHub, and GitHub Pages for supporting the entire book creation and deployment workflow.

#### Phase 2 — Foundation
-   **Finalize Architecture**: Document the detailed architecture sketch for the book structure, Docusaurus hierarchy, content pipeline, and toolchain interactions, incorporating all decisions from Section 5.
-   **Lock In Book Layout**: Confirm the high-level module and chapter organization based on the `spec.md` and `constitution.md`.
-   **Set Up Docusaurus Skeleton Project**: Initialize the Docusaurus project, configure `docusaurus.config.js` and `sidebar.js`, and establish the initial `docs/`, `src/`, and `static/` folder structures.
-   **Set Up GitHub Repo + Deployment Pipeline**: Create the GitHub repository, configure `main` and `gh-pages` branches, and implement the GitHub Actions CI/CD workflow for automated Docusaurus builds and deployments.

#### Phase 3 — Analysis
-   **Break Down Each Module into Detailed Chapter Specs**: For each module (ROS 2, Digital Twin, AI-Robot Brain, VLA), create individual `spec.md` files for each chapter, detailing learning objectives, core requirements, key concepts, specific examples, and constraints.
-   **Identify Required Citations and Media**: Based on chapter specs, outline the specific research papers, technical documentation, and images/diagrams needed for each chapter.
-   **Define Chapter Structure Templates**: Create Markdown templates that enforce the uniform chapter structure (Section 2) for consistency across all content.

#### Phase 4 — Synthesis
-   **Write Chapters Using Spec-Kit + Claude Code**: Authors (human and AI) will generate content for each chapter, adhering to the chapter specs and utilizing Claude Code for drafting, research summarization, and initial revisions.
-   **Validate with Quality Framework**: Each completed chapter will undergo thorough validation using the Quality Validation Framework (Section 4), including automated checks (readability, linting, plagiarism) and human review (technical rigor, clarity).
-   **Final Integration + QA**: Integrate all chapters into the Docusaurus project, perform a comprehensive end-to-end quality assurance pass, checking for consistency, broken links, and overall user experience.
-   **Deploy Final Docusaurus Site + PDF**: Build and deploy the final Docusaurus static site to GitHub Pages. Generate and provide instructions for exporting the book to PDF format.
