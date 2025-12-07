# Data Model: Physical AI & Humanoid Robotics Book

## Entities

### Book
- **Description**: A complete technical book on Physical AI & Humanoid Robotics.
- **Fields**:
    - `title`: String (e.g., "AI-Native Software Development — Full-Length Technical Book")
    - `author`: String (e.g., "Claude Code")
    - `length`: Range (30,000–50,000 words)
    - `chapters_count`: Range (10–20)
    - `publication_platform`: String (e.g., "Docusaurus, GitHub Pages")
    - `status`: String (e.g., "Draft", "Completed", "Published")
- **Relationships**: Contains Modules.

### Module
- **Description**: A major section of the book, covering a specific aspect of Physical AI.
- **Fields**:
    - `module_id`: String (e.g., "Module 1")
    - `title`: String (e.g., "The Robotic Nervous System (ROS 2)")
    - `objective`: String (summary of module goal)
- **Relationships**: Belongs to a Book, Contains Chapters.

### Chapter
- **Description**: A subdivision of a module, detailing specific concepts or technologies.
- **Fields**:
    - `chapter_id`: String (e.g., "Chapter 1.1")
    - `title`: String (e.g., "Introduction to Physical AI & Robotics Foundations")
    - `content`: Markdown text
    - `code_examples`: List of code snippets
    - `diagrams`: List of image paths
    - `sources`: List of citations
- **Relationships**: Belongs to a Module.

### ROS 2 Node
- **Description**: A process that performs computation, communicating via topics, services, and actions.
- **Fields**:
    - `name`: String
    - `language`: String (e.g., "Python")
    - `functionality`: String
- **Relationships**: Interacts with other Nodes via Topics, Services, Actions.

### URDF (Unified Robot Description Format)
- **Description**: Used for describing robot models.
- **Fields**:
    - `robot_name`: String
    - `links`: List of robot parts (e.g., "body", "arm")
    - `joints`: List of connections between links
    - `physical_properties`: Mass, inertia, collision, visual elements
- **Relationships**: Describes a Digital Twin.

### Digital Twin
- **Description**: A virtual replica of a physical robot, used for simulation.
- **Fields**:
    - `robot_model`: Reference to URDF
    - `simulation_environment`: String (e.g., "Gazebo", "Unity", "Isaac Sim")
    - `sensors`: List of simulated sensors (e.g., LiDAR, IMU)
- **Relationships**: Uses URDF, simulated in Gazebo/Unity/Isaac Sim.

### Gazebo
- **Description**: A 3D robot simulator.
- **Fields**:
    - `version`: String
    - `models`: List of 3D models
    - `plugins`: List of simulation plugins
- **Relationships**: Hosts Digital Twins.

### Unity
- **Description**: A real-time 3D development platform for high-fidelity visualization and simulation.
- **Fields**:
    - `version`: String
    - `scenes`: List of simulation scenes
    - `robot_assets`: List of 3D robot models
- **Relationships**: Hosts Digital Twins.

### NVIDIA Isaac Sim
- **Description**: A scalable robotics simulation application and synthetic data generation tool.
- **Fields**:
    - `version`: String
    - `omniverse_assets`: List of 3D assets
    - `perception_pipelines`: List of Isaac ROS components
- **Relationships**: Hosts Digital Twins, integrates with Isaac ROS.

### Isaac ROS
- **Description**: A collection of hardware-accelerated packages for ROS 2.
- **Fields**:
    - `packages`: List of ROS 2 packages (e.g., `isaac_ros_vslam`)
    - `functionality`: String (e.g., "perception", "navigation")
- **Relationships**: Integrates with NVIDIA Isaac Sim and ROS 2.

### VLA (Vision-Language-Action)
- **Description**: A paradigm for enabling robots to understand and act based on visual and linguistic input.
- **Fields**:
    - `vision_module`: String (e.g., "Object Detection", "VSLAM")
    - `language_module`: String (e.g., "Whisper", "LLM")
    - `action_module`: String (e.g., "ROS 2 Actions", "Manipulator Control")
- **Relationships**: Orchestrates interaction between perception, language, and action.

### LLM (Large Language Model)
- **Description**: Used for cognitive planning and natural language understanding.
- **Fields**:
    - `model_name`: String
    - `task_decomposition_capability`: Boolean
    - `prompt_examples`: List of planning prompts
- **Relationships**: Used by VLA for cognitive planning.

### Whisper
- **Description**: An AI model for voice-to-text transcription.
- **Fields**:
    - `model_size`: String (e.g., "small", "base", "large")
    - `language_support`: List of languages
- **Relationships**: Used by VLA for Voice-to-Action pipeline.

## Validation Rules

### Book-Level Validation
- `length` must be between 30,000 and 50,000 words
- `chapters_count` must be between 10 and 20
- At least 40% of sources must be peer-reviewed academic references
- All content must pass plagiarism check (0% tolerance)
- Flesch-Kincaid grade level must be between 9-12

### Module-Level Validation
- Each module must have a clear `objective`
- Modules must follow the defined thematic structure
- Module titles must align with the spec

### Chapter-Level Validation
- `content` length should be appropriate for 2,000-5,000 words
- Each chapter must have 2-3 learning objectives
- Each chapter must have at least 3 code examples (for ROS 2 modules)
- All `code_examples` must be syntactically valid and tested
- All `diagrams` must be stored under `/static/img/book/`
- All factual claims must map to a source in `sources`

### Citation-Level Validation
- All citations in `sources` must follow APA format
- At least 40% of sources must be peer-reviewed academic references
- All URLs in citations must be valid and accessible

## State Transitions

### Chapter States
- Draft → In Progress: When writing begins
- In Progress → Complete: When initial draft is finished
- Complete → Reviewed: When quality validation is passed
- Reviewed → Published: When integrated into final book

### Module States
- Planned → In Progress: When first chapter starts
- In Progress → Complete: When all chapters are reviewed
- Complete → Published: When integrated into final book

### Book States
- Draft → In Progress: When first module starts
- In Progress → Complete: When all modules are complete
- Complete → Published: When deployed to GitHub Pages