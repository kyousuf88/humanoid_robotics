# Quickstart Guide: AI-Native Software Development — Full-Length Technical Book

This guide provides a quick overview of how to get started with the project to create the "Physical AI & Humanoid Robotics" book.

## 1. Project Setup

This project uses Spec-Kit Plus, Claude Code, Docusaurus, and GitHub Pages.

### Prerequisites

- **Git**: Ensure Git is installed and configured.
- **Node.js & npm/yarn**: Required for Docusaurus. Install Node.js (LTS version recommended) and either npm or yarn.
- **Python**: For ROS 2 examples and potentially other AI-related scripts.
- **Claude Code CLI**: Ensure the Claude Code CLI is installed and configured.

### Clone the Repository

```bash
git clone [repository-url]
cd humanoid_robotics
```

## 2. Docusaurus Setup (for local development)

Navigate to the root of the Docusaurus project (where `docusaurus.config.js` is located) and install dependencies:

```bash
npm install  # or yarn install
```

### Start Local Development Server

```bash
npm start # or yarn start
```

This will open a local development server in your browser, typically at `http://localhost:3000`.

## 3. Working with Spec-Kit Plus and Claude Code

- **Feature Specification**: Specifications for each module and chapter are located in `specs/001-physical-ai-book/spec.md`.
- **Planning**: Implementation plans (like this one) are in `specs/001-physical-ai-book/plan.md`.
- **Tasks**: Actionable tasks will be generated in `specs/001-physical-ai-book/tasks.md`.
- **Claude Code**: Use the Claude Code CLI to interact with the project, generate content, and manage the workflow.

## 4. Content Generation

Claude Code will assist in writing accurate, reproducible, and well-formatted chapters based on the detailed specifications.

## 5. Deployment

The book is designed to be deployed to GitHub Pages. After content generation and local testing, the Docusaurus build process will generate a static site.

```bash
npm run build # or yarn build
```

Refer to the Docusaurus and GitHub Pages documentation for specific deployment steps. (NEEDS CLARIFICATION: Detailed deployment steps will be added during implementation phase).