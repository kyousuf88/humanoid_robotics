# Quickstart Guide: Physical AI & Humanoid Robotics Book

## Overview
This guide will help you get started with contributing to the "Physical AI & Humanoid Robotics" book project. The book is built using Docusaurus and follows the Spec-Kit Plus methodology with Claude Code assistance.

## Prerequisites
- Node.js (v16 or higher)
- Git
- Basic knowledge of Markdown
- Understanding of ROS 2 concepts (helpful but not required)
- Claude Code CLI (for AI-assisted content generation)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [repository-url]
cd humanoid_robotics
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Local Development Server
```bash
npm start
```
This command starts a local development server and opens the book in your browser. Most changes are reflected live without restarting the server.

### 4. Project Structure
```
├── docs/                    # Book content (modules and chapters)
│   ├── module-1/           # ROS 2 module (The Robotic Nervous System)
│   │   ├── chapter-1.md
│   │   └── ...
│   ├── module-2/           # Digital Twin module (Gazebo & Unity)
│   │   ├── chapter-1.md
│   │   └── ...
│   ├── module-3/           # AI-Robot Brain module (NVIDIA Isaac)
│   │   ├── chapter-1.md
│   │   └── ...
│   ├── module-4/           # VLA module (Vision-Language-Action)
│   │   ├── chapter-1.md
│   │   └── ...
│   └── ...
├── src/
│   └── components/         # Custom React components
├── static/
│   └── img/
│       └── book/          # Book images
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js            # Navigation structure
└── package.json           # Project dependencies
```

## Writing Content

### 1. Chapter Template
Each chapter should follow this structure:
```markdown
---
title: Chapter Title
description: Brief description of the chapter
---

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## Introduction
Brief introduction to the topic.

## Main Section Title
Content for the main section.

### Sub-section Title
More detailed content.

## Code Examples
```python
# Python code example using rclpy
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        # Node implementation
```

## Summary
Brief summary of the chapter's content.

## Citations
- In-text citations should follow APA format
- Full bibliography at the end of the chapter
```

### 2. Adding Code Examples
- Use appropriate language identifiers (python, bash, yaml, urdf, etc.)
- Ensure all code examples are tested and runnable
- Include explanatory comments where necessary
- For ROS 2 modules, use `rclpy` for Python examples
- Target ROS 2 Humble Hawksbill (LTS) for compatibility

### 3. Adding Diagrams
- Store all images in `static/img/book/`
- Use descriptive filenames
- Include alt text for accessibility
- Reference images as: `![Alt text](/img/book/filename.png)`

## Quality Standards

### 1. Content Requirements
- Factual claims must be traceable to sources
- Minimum 40% peer-reviewed academic references
- APA citation style required
- Flesch-Kincaid grade level 9-12
- Word count: 2,000-5,000 per chapter

### 2. Technical Requirements
- All code examples must be syntactically valid
- URDF examples must be syntactically valid
- All links and image paths must resolve correctly
- No plagiarism (0% tolerance)

## Spec-Kit Plus Workflow

### 1. Creating New Modules/Chapters
1. Create a specification using the Spec-Kit Plus methodology
2. Define functional requirements and acceptance criteria
3. Plan the content structure
4. Create the actual content following the spec

### 2. Using Claude Code
- Use Claude Code for content generation, research extraction, and summarization
- Always verify AI-generated content for accuracy
- Ensure all AI-assisted content meets quality standards

## Technology Stack

### ROS 2 (Humble Hawksbill LTS)
- Target ROS 2 Humble Hawksbill for long-term support
- Use `rclpy` for Python-based examples
- Include URDF examples for humanoid robots

### Simulation Tools
- **Gazebo**: For physics simulation and sensor simulation
- **Unity**: For high-fidelity visualization
- **NVIDIA Isaac Sim**: For photorealistic simulation and synthetic data generation
- **Isaac ROS**: For hardware-accelerated perception pipelines

### AI Components
- **Whisper**: For voice-to-text transcription
- **Open Source LLM (e.g., Llama 3)**: For cognitive planning and task decomposition
- **VLA (Vision-Language-Action)**: For multi-modal interaction

## Building and Deployment

### 1. Build the Static Site
```bash
npm run build
```
This command generates static content into the `build/` directory.

### 2. Deployment
The site is automatically deployed to GitHub Pages via GitHub Actions when changes are merged to the `main` branch.

## Navigation Architecture

The book follows a hierarchical structure:
- **Modules**: High-level thematic sections (e.g., "The Robotic Nervous System")
- **Chapters**: Subdivisions within modules focusing on specific concepts
- **Content Blocks**: Individual sections within chapters (learning objectives, key concepts, code examples, diagrams, citations)

## Common Commands
- `npm start` - Start local development server
- `npm run build` - Build static site
- `npm run serve` - Serve the built site locally
- `npm run docusaurus` - Display Docusaurus CLI options

## Getting Help
- Check the `specs/001-physical-ai-book/` directory for detailed specifications
- Review the constitution file for project principles and standards
- Contact the project maintainers for technical questions