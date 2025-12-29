# Tasks for AI/Spec-Driven Book Creation

## Feature: Physical AI & Humanoid Robotics Book

## Reference: `constitution.md` + `specs/001-physical-ai-book/spec.md` + `specs/001-physical-ai-book/plan.md`

**Generated**: 2025-12-30
**Clarifications Applied**: FR-021 (hardware requirements), FR-022 (troubleshooting sections), FR-023 (pinned versions)

---

## Objective

This document outlines the detailed, executable tasks for creating the "Physical AI & Humanoid Robotics" book, organized by user story and development phase.

---

## Phase 1 — Setup (Project Initialization)

- [X] T001 Create Docusaurus skeleton project and configure `docusaurus.config.js` and `sidebar.js`.
- [X] T002 Establish initial `docs/`, `src/`, and `static/` folder structures.
- [ ] T003 Create the GitHub repository and configure `main` and `gh-pages` branches. (FAILED: Permissions error. User needs to create manually or provide a token with 'repo' scope).
- [X] T004 Implement the GitHub Actions CI/CD workflow for automated Docusaurus builds and deployments (`.github/workflows/deploy.yml`).
- [X] T005 Create a shared Markdown bibliography file (`bibliography.md`).

---

## Phase 2 — Foundational (Blocking prerequisites for all user stories)

- [X] T006 Document the detailed architecture sketch for the book structure, Docusaurus hierarchy, content pipeline, and toolchain interactions in `specs/001-physical-ai-book/plan.md`.
- [X] T007 Confirm the high-level module and chapter organization based on `spec.md` and `constitution.md`.
- [X] T008 Create Markdown templates that enforce the uniform chapter structure (`.specify/templates/chapter-template.md`).
- [X] T009 [P] Create chapter structure template with required elements: learning objectives, key concepts, introduction, sub-sections with proper hierarchy, code examples with language identifiers, citations in APA style, summary, and review questions (`templates/chapter-template.md`).
- [X] T010 [P] Set up image directory structure in `static/img/book/` with subdirectories for each module (`static/img/book/module-1/`, `static/img/book/module-2/`, `static/img/book/module-3/`, `static/img/book/module-4/`).

---

## Phase 3 — User Stories (in priority order)

### User Story 1 - Physical AI Book Creation (Priority: P1)

**Goal**: The user, as a technical book author, wants to create a comprehensive book on Physical AI and Humanoid Robotics using Spec-Kit Plus and Claude Code, with Docusaurus for publication and GitHub Pages for deployment.

**Independent Test**: The book can be fully specified, planned, and implemented using the defined tools, resulting in a deployable Docusaurus site on GitHub Pages.

**Implementation Tasks**:
- [ ] T011 [US1] Ensure `spec.md` and `plan.md` are detailed enough to generate further specifications for modules and chapters (`specs/001-physical-ai-book/spec.md`, `specs/001-physical-ai-book/plan.md`).
- [ ] T012 [US1] Set up a workflow for Claude Code to assist in generating initial content drafts based on chapter specs and research findings.
- [ ] T013 [US1] Define human author review and editing process for accuracy, clarity, and technical rigor.
- [ ] T014 [US1] Implement a process for committing approved changes to feature branches.
- [X] T015 [US1] Ensure Docusaurus builds the static site without errors.
- [ ] T016 [US1] Verify that GitHub Actions deploys the static site to GitHub Pages correctly.
- [X] T017 [US1] Create Preface and Appendix chapters: "Preface" (`docs/preface.md`), "Appendix: Hardware, Tools, and Lab Setup" (`docs/appendix.md`).

### User Story 2 - ROS 2 Robotic Nervous System (Priority: P1)

**Goal**: The user, as a robotics student, wants to understand ROS 2 fundamentals as the control backbone of humanoid robots through clear explanations, Python examples, URDF details, and real-time control concepts.

**Independent Test**: Students can build working ROS 2 nodes and understand the control architecture of humanoids based on the module's content.

**Implementation Tasks**:
- [X] T018 [US2] Create `spec.md` for Module 1: "The Robotic Nervous System (ROS 2)" in `specs/001-physical-ai-book/module1/spec.md`.
- [X] T019 [US2] Write Chapter 1: "Introduction to Physical AI & Robotics Foundations" in `docs/module-1/chapter-1.md`.
- [X] T020 [P] [US2] Write Chapter 2: "ROS 2 Architecture (Nodes, Topics, Services, Actions, DDS, QoS)" in `docs/module-1/chapter-2.md`.
- [X] T021 [P] [US2] Write Chapter 3: "Building ROS 2 Packages with rclpy (workspaces, nodes, launch files)" in `docs/module-1/chapter-3.md`.
- [X] T022 [P] [US2] Write Chapter 4: "Robot Description Formats (URDF for humanoid robots)" in `docs/module-1/chapter-4.md`.
- [X] T023 [P] [US2] Write Chapter 5: "Real-Time Control Concepts (Controller Manager, PID, Sensor Fusion)" in `docs/module-1/chapter-5.md`.
- [ ] T024 [US2] Ensure all ROS 2 Python examples in Module 1 are runnable and syntactically valid targeting ROS 2 Humble Hawksbill (`docs/module-1/**/*.md`).
- [ ] T025 [US2] Verify all URDF examples in Module 1 are syntactically valid (`docs/module-1/**/*.md`).
- [ ] T026 [US2] Include diagrams and ASCII illustrations where beneficial in Module 1 chapters (`docs/module-1/**/*.md`).
- [ ] T027 [US2] Add at least 3 ROS 2 Python examples per chapter in Module 1 (`docs/module-1/**/*.md`).
- [ ] T028 [US2] Include proper code language identifiers for Python, URDF, and launch files in Module 1 chapters (`docs/module-1/**/*.md`).

### User Story 3 - Digital Twin Simulation (Priority: P2)

**Goal**: The user, as a robotics student, wants to learn simulation workflows using Gazebo and Unity to create robust digital twins for humanoid robots, including sensor simulation and ROS integration.

**Independent Test**: Students can run Gazebo simulations connected to ROS 2, import robots into Unity for visualization, and understand sensor simulation foundations based on the module's content.

**Implementation Tasks**:
- [X] T029 [US3] Create `spec.md` for Module 2: "The Digital Twin (Gazebo & Unity)" in `specs/001-physical-ai-book/module2/spec.md`.
- [X] T030 [P] [US3] Write Chapter 1: "Digital Twins in Physical AI & the Sim-to-Real Gap" in `docs/module-2/chapter-1.md`.
- [X] T031 [P] [US3] Write Chapter 2: "Gazebo Fundamentals (SDF, URDF, Models, Plugins)" in `docs/module-2/chapter-2.md`.
- [X] T032 [P] [US3] Write Chapter 3: "Sensor Simulation (LiDAR, IMUs, Depth Cameras, noise models)" in `docs/module-2/chapter-3.md`.
- [ ] T033 [P] [US3] Write Chapter 4: "Unity for High-Fidelity Robot Visualization" in `docs/module-2/chapter-4.md`.
- [ ] T034 [P] [US3] Write Chapter 5: "Environment & Scenario Building (multi-room navigation, interactions)" in `docs/module-2/chapter-5.md`.
- [ ] T035 [US3] Ensure at least 1 simulation diagram per chapter in Module 2 (`docs/module-2/**/*.md`).
- [ ] T036 [US3] Provide URDF/SDF code examples in Module 2 chapters (`docs/module-2/**/*.md`).
- [ ] T037 [US3] Include Unity scene descriptions (text-based) in Module 2 chapters (`docs/module-2/**/*.md`).
- [ ] T038 [US3] Create installation and setup instructions for Gazebo (physics simulation) and Unity (high-fidelity visualization) in Module 2 chapters (`docs/module-2/**/*.md`).
- [ ] T039 [US3] Demonstrate SDF/URDF usage and conversions in Module 2 chapters (`docs/module-2/**/*.md`).

### User Story 4 - AI-Robot Brain (NVIDIA Isaac) (Priority: P2)

**Goal**: The user, as a robotics student, wants to learn perception, synthetic data creation, navigation, and reinforcement learning for humanoid robotics using NVIDIA Isaac Sim and Isaac ROS.

**Independent Test**: Students can run Isaac Sim scenes with humanoids, configure perception and navigation pipelines, and understand RL-based control workflows based on the module's content.

**Implementation Tasks**:
- [ ] T040 [US4] Create `spec.md` for Module 3: "The AI-Robot Brain (NVIDIA Isaac)" in `specs/001-physical-ai-book/module3/spec.md`.
- [ ] T041 [P] [US4] Write Chapter 1: "NVIDIA Isaac Ecosystem Overview (Sim, ROS, Omniverse)" in `docs/module-3/chapter-1.md`.
- [ ] T042 [P] [US4] Write Chapter 2: "Photorealistic Simulation & Synthetic Data Generation" in `docs/module-3/chapter-2.md`.
- [ ] T043 [P] [US4] Write Chapter 3: "Isaac ROS Perception Pipelines (VSLAM, Depth, Object Detection)" in `docs/module-3/chapter-3.md`.
- [ ] T044 [P] [US4] Write Chapter 4: "Navigation & Path Planning (Nav2 for biped locomotion)" in `docs/module-3/chapter-4.md`.
- [ ] T045 [P] [US4] Write Chapter 5: "Reinforcement Learning & Sim-to-Real Transfer Techniques" in `docs/module-3/chapter-5.md`.
- [ ] T046 [US4] Include diagrams of Isaac ROS graphs in Module 3 chapters (`docs/module-3/**/*.md`).
- [ ] T047 [US4] Provide Nav2 configuration examples with humanoid-specific constraints (bipedal locomotion, balance, step planning) in Module 3 chapters (`docs/module-3/**/*.md`).
- [ ] T048 [US4] Include 2–3 synthetic dataset export examples in Module 3 chapters (`docs/module-3/**/*.md`).
- [ ] T049 [US4] Focus on Isaac Sim + Isaac ROS integration in Module 3 chapters (`docs/module-3/**/*.md`).

### User Story 5 - Vision-Language-Action (VLA) (Priority: P3)

**Goal**: The user, as a robotics student, wants to understand how LLMs, Whisper, and multi-modal AI enable natural interaction and cognitive planning for humanoid robots.

**Independent Test**: Students can build a voice-controlled robot interface, implement LLM task planners, and complete a full VLA-powered Capstone workflow based on the module's content.

**Implementation Tasks**:
- [ ] T050 [US5] Create `spec.md` for Module 4: "Vision-Language-Action (VLA)" in `specs/001-physical-ai-book/module4/spec.md`.
- [ ] T051 [P] [US5] Write Chapter 1: "Introduction to VLA Robotics" in `docs/module-4/chapter-1.md`.
- [ ] T052 [P] [US5] Write Chapter 2: "Voice-to-Action Pipeline (Whisper → Intent → ROS 2 Actions)" in `docs/module-4/chapter-2.md`.
- [ ] T053 [P] [US5] Write Chapter 3: "Cognitive Planning Using LLMs" in `docs/module-4/chapter-3.md`.
- [ ] T054 [P] [US5] Write Chapter 4: "Multi-Modal Perception (Vision + Language + Sensor Fusion)" in `docs/module-4/chapter-4.md`.
- [ ] T055 [P] [US5] Write Chapter 5: "Capstone Project: The Autonomous Humanoid" in `docs/module-4/chapter-5.md`.
- [ ] T056 [US5] Include 2 end-to-end logic diagrams in Module 4 chapters (`docs/module-4/**/*.md`).
- [ ] T057 [US5] Include example planning prompts in Module 4 chapters (`docs/module-4/**/*.md`).
- [ ] T058 [US5] Include ROS 2 action server/client examples in Module 4 chapters (`docs/module-4/**/*.md`).
- [ ] T059 [US5] Implement Whisper + Open Source LLM (e.g., Llama 3) for VLA system in Module 4 chapters (`docs/module-4/**/*.md`).

---

## Final Phase — Polish & Cross-Cutting Concerns

- [ ] T060 Conduct Automated Checks (Accuracy, Clarity, Reproducibility, Formatting Consistency, Plagiarism) using defined tools.
- [ ] T061 Conduct Human Checks (Technical Rigor, Content Quality, Formatting Consistency, Proofreading).
- [ ] T062 Integrate all chapters into the Docusaurus project.
- [ ] T063 Perform a comprehensive end-to-end quality assurance pass.
- [ ] T064 Generate and provide instructions for exporting the book to PDF format.
- [ ] T065 Ensure all functional requirements (FR-001 to FR-023) are met.
- [ ] T066 Ensure all success criteria (SC-001 to SC-010) are met.
- [ ] T067 Verify that all citations follow APA format and are traceable to credible sources.
- [ ] T068 Confirm the book meets Flesch-Kincaid Grade level 9–12 for writing clarity.
- [ ] T069 Ensure the book adheres to the specified length (30,000–50,000 words) and chapter count (10–20).

---

## New Tasks from Clarifications (2025-12-30)

### FR-021: Hardware Requirements per Module

- [X] T070 [P] Create docs/appendix/hardware-requirements.md with consolidated hardware matrices
- [X] T071 [P] Add hardware requirements section to docs/module-1/index.md (CPU: 4 cores, RAM: 8GB min)
- [X] T072 [P] Add hardware requirements section to docs/module-2/index.md (GPU: GTX 1060 min)
- [X] T073 [P] Add hardware requirements section to docs/module-3/index.md (GPU: RTX 2070 required)
- [X] T074 [P] Add hardware requirements section to docs/module-4/index.md (GPU: RTX 3060 12GB min)

### FR-022: Troubleshooting Sections per Module

- [X] T075 [US2] Create docs/module-1/troubleshooting.md with common ROS 2 issues
- [X] T076 [US3] Create docs/module-2/troubleshooting.md with Gazebo/Unity issues
- [X] T077 [US4] Create docs/module-3/troubleshooting.md with Isaac Sim issues
- [X] T078 [US5] Create docs/module-4/troubleshooting.md with VLA/LLM issues

### FR-023: Pinned Tool Versions

- [X] T079 Create docs/appendix/tools-setup.md with pinned versions: ROS 2 Humble, Gazebo Harmonic, Unity 2022 LTS, Isaac Sim 2023.1
- [X] T080 Verify all code examples target pinned versions (ROS 2 Humble Hawksbill)
- [X] T081 Verify all Gazebo examples use Gazebo Harmonic (not Classic) - Fixed chapter-1.md, chapter-2.md
- [X] T082 Verify all Unity examples use Unity 2022 LTS with Unity Robotics Hub - Fixed chapter-1.md, chapter-4.md
- [X] T083 Verify all Isaac Sim examples use Isaac Sim 2023.1.x

---

## Dependencies

The following outlines the completion order of user stories:

1.  **User Story 1** (Physical AI Book Creation) is the overarching goal and depends on the successful completion of all other user stories and foundational tasks.
2.  **User Story 2** (ROS 2 Robotic Nervous System) is foundational for subsequent modules.
3.  **User Story 3** (Digital Twin Simulation) depends on User Story 2.
4.  **User Story 4** (AI-Robot Brain) depends on User Story 2 and User Story 3.
5.  **User Story 5** (Vision-Language-Action) depends on User Story 2, User Story 3, and User Story 4.

## Parallel Execution Examples

-   **Phase 1: Setup**
    -   Tasks T001, T002, T003, T004 can be executed in parallel.
-   **Phase 2: Foundational**
    -   Tasks T009, T010 can be executed in parallel.
-   **User Story 2: ROS 2 Robotic Nervous System**
    -   Tasks T020, T021, T022, T023 (chapter writing) can be executed in parallel once the preceding tasks are complete.
-   **User Story 3: Digital Twin Simulation**
    -   Tasks T030, T031, T032, T033, T034 (chapter writing) can be executed in parallel once the preceding tasks are complete.
-   **User Story 4: AI-Robot Brain**
    -   Tasks T041, T042, T043, T044, T045 (chapter writing) can be executed in parallel once the preceding tasks are complete.
-   **User Story 5: Vision-Language-Action**
    -   Tasks T051, T052, T053, T054, T055 (chapter writing) can be executed in parallel once the preceding tasks are complete.

## Implementation Strategy

The implementation will follow an MVP-first, incremental delivery approach. User Story 1 (Physical AI Book Creation) will serve as the guiding objective, with core foundational elements being established first. Subsequent user stories (Module 1 through 4) will be developed and integrated sequentially, ensuring that each module builds upon the previous one. Testing and quality assurance will be continuous throughout the development lifecycle.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 83 |
| **Setup Tasks (Phase 1)** | 5 |
| **Foundational Tasks (Phase 2)** | 5 |
| **US1 Tasks (Book Infrastructure)** | 7 |
| **US2 Tasks (ROS 2 Module)** | 11 |
| **US3 Tasks (Digital Twin Module)** | 11 |
| **US4 Tasks (Isaac Module)** | 10 |
| **US5 Tasks (VLA Module)** | 10 |
| **Polish Tasks (Final Phase)** | 10 |
| **New Clarification Tasks (FR-021/022/023)** | 14 |
| **Parallelizable Tasks** | ~45 (54%) |

### MVP Scope (Recommended)

Complete through **User Story 2 (ROS 2 Module)** for MVP:
- Setup (T001-T005) + Foundational (T006-T010) + US1 (T011-T017) + US2 (T018-T028)
- Delivers: Complete book infrastructure + ROS 2 module
- Validates: End-to-end Docusaurus workflow, code example testing

### Pinned Tool Versions (FR-023)

| Tool | Version |
|------|---------|
| ROS 2 | Humble Hawksbill (LTS) |
| Gazebo | Harmonic |
| Unity | 2022 LTS |
| Isaac Sim | 2023.1.x |
| Python | 3.10+ |
