---
id: module-4-chapter-3
sidebar_position: 3
title: "Chapter 3 - Cognitive Planning Using LLMs"
---

# Chapter 3: Cognitive Planning Using LLMs

## Learning Objectives
- [ ] Understand the role of Large Language Models (LLMs) in robotic cognitive planning
- [ ] Implement LLM-based task decomposition and execution planning for humanoid robots
- [ ] Design effective prompt engineering strategies for robotic applications
- [ ] Integrate LLM-based planning with ROS 2 navigation and manipulation systems
- [ ] Evaluate and optimize LLM-based planning for real-world robotic tasks

## Key Concepts
- [ ] **Large Language Models (LLMs)**: Transformer-based models that understand and generate human language
- [ ] **Cognitive Planning**: High-level reasoning to decompose complex tasks into executable actions
- [ ] **Prompt Engineering**: Designing effective inputs to guide LLM behavior for specific tasks
- [ ] **Task Decomposition**: Breaking down complex goals into simpler, executable subtasks
- [ ] **Plan Execution**: Converting high-level plans into low-level robot commands
- [ ] **Context Management**: Maintaining and updating relevant information during planning

## Introduction

Cognitive planning using Large Language Models (LLMs) represents a paradigm shift in how humanoid robots approach complex task execution. Unlike traditional rule-based planning systems that rely on predefined action sequences, LLMs enable robots to understand natural language commands and generate sophisticated, context-aware plans that adapt to dynamic environments and user needs.

The integration of LLMs with robotic systems allows for more intuitive human-robot interaction, where users can express complex goals in natural language without requiring detailed technical knowledge of robot capabilities. For example, a command like "Please clean up the living room and set the table for dinner" can be decomposed by an LLM into a sequence of navigation, manipulation, and organization tasks.

This chapter explores the architecture of LLM-based cognitive planning systems, focusing on how these models can be leveraged to create intelligent, adaptive planning capabilities for humanoid robots. We'll examine the technical challenges of integrating LLMs with robotic systems, strategies for effective prompt engineering, and methods for ensuring reliable plan execution in real-world environments.

The cognitive planning system acts as a bridge between high-level human intentions and low-level robot actions, enabling robots to understand complex, ambiguous, or multi-step commands and translate them into executable plans. This capability is particularly valuable for humanoid robots that operate in human environments where tasks are often expressed in natural language and require contextual understanding.

## LLM Fundamentals for Robotic Planning

### Overview of LLM Architecture

Large Language Models are built on transformer architectures that excel at understanding and generating human language. These models learn patterns from vast amounts of text data, enabling them to understand context, relationships, and the meaning behind human language. For robotic planning, this linguistic understanding can be leveraged to decompose complex tasks, reason about object affordances, and generate executable action sequences.

The key components of LLMs relevant to robotic planning include:

**Attention Mechanisms**: Allow the model to focus on relevant parts of the input when generating responses, crucial for understanding which aspects of a command are most important.

**Context Windows**: The amount of information the model can consider at once, important for maintaining awareness of the robot's state and environment during planning.

**Reasoning Capabilities**: The model's ability to perform logical reasoning and chain thoughts together, essential for decomposing complex tasks.

### LLM Selection for Robotics

Different LLMs offer various trade-offs in terms of performance, computational requirements, and accessibility:

**Open Source Models**: Models like Llama 2/3, Mistral, and others offer flexibility and cost-effectiveness, suitable for deployment in robotic systems.

**Commercial APIs**: Services like OpenAI's GPT series provide high performance and reliability, though with potential cost and latency considerations.

**Specialized Models**: Models fine-tuned for specific domains may offer better performance for robotic applications.

```python
# LLM interface for robotic planning
import openai
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import time
from typing import Dict, List, Any

class LLMInterface:
    def __init__(self, model_name="gpt-3.5-turbo", api_key=None):
        """
        Initialize LLM interface for robotic planning
        """
        self.model_name = model_name
        self.api_key = api_key

        if api_key:
            openai.api_key = api_key

        # For open source models
        self.tokenizer = None
        self.model = None

        if model_name.startswith("llama") or model_name.startswith("mistral"):
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_plan(self, task_description: str, robot_capabilities: Dict, environment_state: Dict) -> Dict:
        """
        Generate a plan for the given task using LLM
        """
        prompt = self.create_planning_prompt(task_description, robot_capabilities, environment_state)

        if self.api_key:  # Using OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            plan_json = response.choices[0].message.content
        else:  # Using local model
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(inputs, max_length=inputs.shape[1] + 200, temperature=0.3)
            plan_json = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        try:
            # Extract JSON from response (LLM might include additional text)
            plan_json = self.extract_json_from_response(plan_json)
            return json.loads(plan_json)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract structured information
            return self.parse_plan_from_text(plan_json)

    def create_planning_prompt(self, task_description: str, robot_capabilities: Dict, environment_state: Dict) -> str:
        """
        Create a structured prompt for task planning
        """
        prompt = f"""
        You are a cognitive planning system for a humanoid robot. Your task is to decompose complex human commands into executable robot actions.

        Robot Capabilities:
        {json.dumps(robot_capabilities, indent=2)}

        Current Environment State:
        {json.dumps(environment_state, indent=2)}

        Task Description:
        {task_description}

        Please generate a detailed execution plan with the following structure:
        {{
            "task_decomposition": [
                {{
                    "step": 1,
                    "description": "What needs to be done",
                    "action": "specific robot action",
                    "parameters": {{"param1": "value1", ...}},
                    "prerequisites": ["list of conditions that must be met"],
                    "expected_outcome": "what should happen after execution"
                }}
            ],
            "dependencies": [
                {{"from_step": 1, "to_step": 2, "dependency": "reason for dependency"}}
            ],
            "success_criteria": ["list of conditions that indicate successful completion"],
            "failure_modes": ["list of potential failure points"],
            "safety_considerations": ["list of safety considerations"]
        }}

        Respond with only the JSON object, no additional text.
        """
        return prompt

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the LLM
        """
        return """
        You are an expert robotic planning system. You generate detailed, executable plans for humanoid robots.
        Your plans must be realistic given the robot's capabilities and the environment.
        Always respond with valid JSON and nothing else.
        Be specific about actions and parameters.
        Consider safety and feasibility in all plans.
        """

    def extract_json_from_response(self, response: str) -> str:
        """
        Extract JSON from LLM response that might contain additional text
        """
        # Find JSON object in response
        start_idx = response.find('{')
        end_idx = response.rfind('}')

        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            return response[start_idx:end_idx+1]

        return response

    def parse_plan_from_text(self, text_response: str) -> Dict:
        """
        Parse plan from text response if JSON extraction fails
        """
        # This is a fallback method - in practice, you'd want more sophisticated parsing
        return {
            "task_decomposition": [{"step": 1, "description": text_response, "action": "unknown", "parameters": {}}],
            "dependencies": [],
            "success_criteria": ["task completed"],
            "failure_modes": ["parsing failed"],
            "safety_considerations": ["general safety"]
        }
```

### Context Management for Planning

Effective cognitive planning requires maintaining and updating relevant context information, including the robot's current state, environmental conditions, and task history. This context enables the LLM to make informed decisions and generate appropriate plans.

```python
# Context management for LLM-based planning
class PlanningContextManager:
    def __init__(self):
        self.current_task = None
        self.task_history = []
        self.robot_state = {}
        self.environment_state = {}
        self.context_window = []  # Recent interactions for context
        self.max_context_length = 10  # Maximum number of interactions to keep

    def update_robot_state(self, state: Dict):
        """
        Update the robot's current state
        """
        self.robot_state.update(state)
        self.add_to_context(f"Robot state updated: {state}")

    def update_environment_state(self, state: Dict):
        """
        Update the environment state
        """
        self.environment_state.update(state)
        self.add_to_context(f"Environment state updated: {state}")

    def add_to_context(self, interaction: str):
        """
        Add interaction to context window
        """
        self.context_window.append({
            'timestamp': time.time(),
            'interaction': interaction
        })

        # Keep only recent interactions
        if len(self.context_window) > self.max_context_length:
            self.context_window = self.context_window[-self.max_context_length:]

    def get_context_summary(self) -> Dict:
        """
        Get a summary of current context for LLM
        """
        return {
            'current_task': self.current_task,
            'recent_interactions': [ctx['interaction'] for ctx in self.context_window[-5:]],  # Last 5 interactions
            'robot_state': self.robot_state,
            'environment_state': self.environment_state,
            'task_history': self.task_history[-3:]  # Last 3 tasks
        }

    def start_new_task(self, task_description: str):
        """
        Start a new task and update context
        """
        self.current_task = task_description
        self.add_to_context(f"New task started: {task_description}")

    def complete_task(self, success: bool, outcome: str):
        """
        Complete current task and add to history
        """
        if self.current_task:
            task_record = {
                'task': self.current_task,
                'success': success,
                'outcome': outcome,
                'timestamp': time.time()
            }
            self.task_history.append(task_record)
            self.add_to_context(f"Task completed: {self.current_task}, Success: {success}")
            self.current_task = None
```

## Task Decomposition and Execution Planning

### Hierarchical Task Decomposition

Hierarchical task decomposition is a critical capability of LLM-based cognitive planning systems. This approach breaks down complex, high-level goals into sequences of simpler, executable subtasks that the robot can perform. The LLM's understanding of language and common sense reasoning enables it to identify the necessary steps and their dependencies.

For humanoid robots, task decomposition must consider the robot's physical capabilities, environmental constraints, and safety requirements. The decomposition process should generate a plan that is both feasible and efficient.

```python
# Task decomposition using LLM
class TaskDecomposer:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.robot_capabilities = {
            'navigation': {
                'supported': True,
                'max_speed': 0.5,
                'turning_radius': 0.3
            },
            'manipulation': {
                'supported': True,
                'max_payload': 2.0,
                'reachable_workspace': 'cubic meter around robot'
            },
            'perception': {
                'supported': True,
                'object_recognition': True,
                'person_detection': True
            },
            'interaction': {
                'supported': True,
                'speech_output': True,
                'gesture_support': True
            }
        }

    def decompose_task(self, high_level_task: str, environment_state: Dict) -> Dict:
        """
        Decompose a high-level task into executable subtasks
        """
        # Create detailed prompt for task decomposition
        prompt = f"""
        Decompose the following high-level task into specific, executable subtasks for a humanoid robot:

        High-level Task: {high_level_task}

        Robot Capabilities: {json.dumps(self.robot_capabilities, indent=2)}
        Environment State: {json.dumps(environment_state, indent=2)}

        Decompose the task into a sequence of specific actions. Each action should be:
        1. Executable by the robot
        2. Have clear parameters
        3. Include success/failure conditions
        4. Account for dependencies between actions

        Provide the decomposition in this format:
        {{
            "original_task": "{high_level_task}",
            "decomposed_tasks": [
                {{
                    "id": 1,
                    "description": "Clear description of what to do",
                    "action_type": "navigation|manipulation|perception|interaction",
                    "parameters": {{"param1": "value1"}},
                    "preconditions": ["list of conditions that must be true"],
                    "postconditions": ["list of conditions that will be true after execution"],
                    "estimated_duration": "in seconds",
                    "priority": "high|medium|low",
                    "dependencies": [list of task IDs this task depends on]
                }}
            ],
            "overall_plan_constraints": ["list of constraints for the entire plan"],
            "success_criteria": ["list of conditions for overall task success"],
            "failure_recovery": ["list of actions to take if a task fails"]
        }}

        Return only the JSON, no additional text.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in robotic task decomposition. Generate detailed, executable subtasks that consider robot capabilities and environmental constraints. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )

            plan_json = response.choices[0].message.content
            # Extract JSON from response
            start_idx = plan_json.find('{')
            end_idx = plan_json.rfind('}')
            if start_idx != -1 and end_idx != -1:
                plan_json = plan_json[start_idx:end_idx+1]

            return json.loads(plan_json)
        except Exception as e:
            print(f"Error in task decomposition: {e}")
            return self.fallback_decomposition(high_level_task)

    def fallback_decomposition(self, task: str) -> Dict:
        """
        Fallback decomposition if LLM fails
        """
        return {
            "original_task": task,
            "decomposed_tasks": [
                {
                    "id": 1,
                    "description": f"Execute the task: {task}",
                    "action_type": "unknown",
                    "parameters": {},
                    "preconditions": [],
                    "postconditions": [],
                    "estimated_duration": 60,
                    "priority": "medium",
                    "dependencies": []
                }
            ],
            "overall_plan_constraints": [],
            "success_criteria": ["task attempted"],
            "failure_recovery": ["report failure"]
        }

class PlanExecutor:
    def __init__(self, task_decomposer: TaskDecomposer):
        self.decomposer = task_decomposer
        self.current_plan = None
        self.executed_tasks = []
        self.failed_tasks = []
        self.task_dependencies = {}  # Task ID -> list of dependent task IDs

    def execute_plan(self, high_level_task: str, environment_state: Dict) -> Dict:
        """
        Execute a plan for the given high-level task
        """
        # Decompose the task
        plan = self.decomposer.decompose_task(high_level_task, environment_state)
        self.current_plan = plan

        # Build dependency graph
        self.build_dependency_graph(plan)

        # Execute tasks in dependency order
        results = self.execute_tasks_sequentially(plan)

        return {
            "original_task": high_level_task,
            "plan": plan,
            "execution_results": results,
            "success": self.check_plan_success(results, plan.get("success_criteria", []))
        }

    def build_dependency_graph(self, plan: Dict):
        """
        Build a graph of task dependencies
        """
        for task in plan["decomposed_tasks"]:
            task_id = task["id"]
            deps = task.get("dependencies", [])
            self.task_dependencies[task_id] = deps

    def execute_tasks_sequentially(self, plan: Dict) -> List[Dict]:
        """
        Execute tasks in the plan sequentially
        """
        results = []

        # Simple sequential execution - in practice, you might want parallel execution for independent tasks
        for task in plan["decomposed_tasks"]:
            result = self.execute_single_task(task)
            results.append(result)

            if not result["success"]:
                self.failed_tasks.append(task["id"])
                # Check if failure recovery is possible
                recovery_result = self.attempt_failure_recovery(task, result)
                if not recovery_result["success"]:
                    break  # Stop execution if recovery fails

        return results

    def execute_single_task(self, task: Dict) -> Dict:
        """
        Execute a single task
        """
        print(f"Executing task: {task['description']}")

        # Simulate task execution based on action type
        success = True
        execution_time = 0
        details = {}

        if task["action_type"] == "navigation":
            success, execution_time, details = self.execute_navigation_task(task)
        elif task["action_type"] == "manipulation":
            success, execution_time, details = self.execute_manipulation_task(task)
        elif task["action_type"] == "perception":
            success, execution_time, details = self.execute_perception_task(task)
        elif task["action_type"] == "interaction":
            success, execution_time, details = self.execute_interaction_task(task)
        else:
            success = False
            details = {"error": "Unknown action type"}

        result = {
            "task_id": task["id"],
            "task_description": task["description"],
            "action_type": task["action_type"],
            "success": success,
            "execution_time": execution_time,
            "details": details,
            "timestamp": time.time()
        }

        if success:
            self.executed_tasks.append(task["id"])
        else:
            self.failed_tasks.append(task["id"])

        return result

    def execute_navigation_task(self, task: Dict) -> tuple:
        """
        Execute navigation task
        """
        # Simulate navigation execution
        destination = task["parameters"].get("destination", "unknown")
        print(f"Navigating to {destination}")
        time.sleep(2)  # Simulate execution time
        return True, 2.0, {"destination": destination, "path_length": 3.5}

    def execute_manipulation_task(self, task: Dict) -> tuple:
        """
        Execute manipulation task
        """
        # Simulate manipulation execution
        object_name = task["parameters"].get("object", "unknown")
        action = task["parameters"].get("action", "grasp")
        print(f"Manipulating {object_name} with {action}")
        time.sleep(3)  # Simulate execution time
        return True, 3.0, {"object": object_name, "action": action, "success": True}

    def execute_perception_task(self, task: Dict) -> tuple:
        """
        Execute perception task
        """
        # Simulate perception execution
        target = task["parameters"].get("target", "unknown")
        print(f"Perceiving {target}")
        time.sleep(1)  # Simulate execution time
        return True, 1.0, {"target": target, "detection": True, "confidence": 0.95}

    def execute_interaction_task(self, task: Dict) -> tuple:
        """
        Execute interaction task
        """
        # Simulate interaction execution
        interaction_type = task["parameters"].get("type", "unknown")
        print(f"Performing {interaction_type} interaction")
        time.sleep(1)  # Simulate execution time
        return True, 1.0, {"type": interaction_type, "completed": True}

    def attempt_failure_recovery(self, failed_task: Dict, failure_result: Dict) -> Dict:
        """
        Attempt to recover from task failure
        """
        print(f"Attempting recovery for failed task: {failed_task['description']}")

        # Simple recovery strategy - in practice, this would be more sophisticated
        if failed_task["action_type"] == "navigation":
            # Try alternative navigation approach
            print("Trying alternative navigation route...")
            time.sleep(1)
            return {"success": True, "method": "alternative_route"}
        elif failed_task["action_type"] == "manipulation":
            # Try alternative manipulation approach
            print("Trying alternative manipulation approach...")
            time.sleep(1)
            return {"success": True, "method": "alternative_approach"}

        return {"success": False, "method": "no_recovery"}

    def check_plan_success(self, results: List[Dict], success_criteria: List[str]) -> bool:
        """
        Check if the overall plan was successful
        """
        successful_tasks = sum(1 for result in results if result["success"])
        total_tasks = len(results)

        # For now, consider plan successful if most tasks succeeded
        return successful_tasks / total_tasks > 0.7 if total_tasks > 0 else False
```

### Planning with Environmental Constraints

LLM-based planning systems must account for environmental constraints and dynamic conditions. This includes understanding spatial relationships, object affordances, and situational context that affect plan feasibility.

```python
# Environmental constraint-aware planning
class EnvironmentAwarePlanner:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.spatial_reasoning = SpatialReasoningEngine()
        self.object_affordances = ObjectAffordanceDatabase()

    def plan_with_environmental_constraints(self, task: str, environment_state: Dict) -> Dict:
        """
        Generate a plan that considers environmental constraints
        """
        # Analyze environment for constraints
        constraints = self.analyze_environmental_constraints(environment_state)

        # Generate plan considering constraints
        prompt = f"""
        Generate a plan for: {task}

        Environmental Constraints:
        {json.dumps(constraints, indent=2)}

        Current Environment State:
        {json.dumps(environment_state, indent=2)}

        Robot Capabilities:
        {json.dumps(self.get_robot_capabilities(), indent=2)}

        Generate a plan that respects all environmental constraints while achieving the goal.
        Consider:
        1. Spatial relationships and navigation constraints
        2. Object affordances and accessibility
        3. Safety considerations
        4. Efficiency of the plan

        Return in JSON format with the structure from previous examples.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Generate plans that consider environmental constraints, safety, and efficiency. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1200
            )

            plan_json = response.choices[0].message.content
            start_idx = plan_json.find('{')
            end_idx = plan_json.rfind('}')
            if start_idx != -1 and end_idx != -1:
                plan_json = plan_json[start_idx:end_idx+1]

            return json.loads(plan_json)
        except Exception as e:
            print(f"Error in constraint-aware planning: {e}")
            return self.fallback_plan(task)

    def analyze_environmental_constraints(self, environment_state: Dict) -> Dict:
        """
        Analyze environmental constraints from environment state
        """
        constraints = {
            "spatial_constraints": [],
            "object_constraints": [],
            "safety_constraints": [],
            "temporal_constraints": []
        }

        # Analyze spatial constraints
        if "obstacles" in environment_state:
            for obstacle in environment_state["obstacles"]:
                if obstacle.get("is_blocking_path", False):
                    constraints["spatial_constraints"].append({
                        "type": "obstacle",
                        "location": obstacle.get("position"),
                        "size": obstacle.get("size"),
                        "traversable": obstacle.get("traversable", False)
                    })

        # Analyze object constraints
        if "objects" in environment_state:
            for obj in environment_state["objects"]:
                affordances = self.object_affordances.get_affordances(obj.get("type", "unknown"))
                if affordances:
                    constraints["object_constraints"].append({
                        "object": obj.get("name", "unknown"),
                        "type": obj.get("type", "unknown"),
                        "affordances": affordances,
                        "accessibility": self.spatial_reasoning.is_accessible(obj.get("position", [0,0,0]))
                    })

        # Analyze safety constraints
        if "humans" in environment_state:
            for human in environment_state["humans"]:
                constraints["safety_constraints"].append({
                    "type": "human_proximity",
                    "position": human.get("position"),
                    "safety_radius": 0.8  # Keep 0.8m away from humans
                })

        return constraints

    def get_robot_capabilities(self) -> Dict:
        """
        Get robot capabilities for planning
        """
        return {
            "navigation": {
                "min_clearance": 0.3,
                "max_step_height": 0.1,
                "max_slope": 15  # degrees
            },
            "manipulation": {
                "max_reach": 1.2,
                "min_grasp_size": 0.02,  # 2cm minimum
                "max_object_weight": 3.0
            },
            "perception": {
                "min_object_size": 0.05,  # 5cm minimum
                "max_detection_range": 3.0
            }
        }

    def fallback_plan(self, task: str) -> Dict:
        """
        Fallback plan if LLM fails
        """
        return {
            "original_task": task,
            "decomposed_tasks": [
                {
                    "id": 1,
                    "description": f"Attempt to execute: {task}",
                    "action_type": "unknown",
                    "parameters": {},
                    "preconditions": [],
                    "postconditions": [],
                    "estimated_duration": 60,
                    "priority": "medium",
                    "dependencies": [],
                    "environmental_considerations": ["basic safety"]
                }
            ],
            "overall_plan_constraints": [],
            "success_criteria": ["task attempted safely"],
            "failure_recovery": ["stop and request assistance"]
        }

class SpatialReasoningEngine:
    def __init__(self):
        # Initialize spatial reasoning capabilities
        pass

    def is_accessible(self, position: List[float]) -> bool:
        """
        Check if a position is accessible to the robot
        """
        # Simplified accessibility check
        # In practice, this would involve path planning and collision checking
        x, y, z = position
        return z <= 1.5  # Object is within reach height

class ObjectAffordanceDatabase:
    def __init__(self):
        # Predefined affordances for common objects
        self.affordances = {
            "cup": ["grasp", "lift", "move", "place"],
            "book": ["grasp", "lift", "move", "place", "open"],
            "ball": ["grasp", "lift", "move", "place", "roll"],
            "chair": ["move", "sit_on"],
            "table": ["approach", "navigate_around", "place_objects_on"],
            "door": ["approach", "open", "pass_through", "close"]
        }

    def get_affordances(self, object_type: str) -> List[str]:
        """
        Get affordances for an object type
        """
        return self.affordances.get(object_type.lower(), [])
```

## Prompt Engineering for Robotic Applications

### Effective Prompt Design

Prompt engineering is crucial for getting reliable, consistent outputs from LLMs in robotic applications. Well-designed prompts guide the LLM to generate structured, actionable plans that align with the robot's capabilities and environmental constraints.

Key principles for effective robotic planning prompts include:

**Clarity**: Prompts should clearly specify the task, constraints, and expected output format.

**Context**: Provide sufficient context about the robot's capabilities and environment.

**Structure**: Define clear output formats to ensure consistent parsing.

**Examples**: Include examples when possible to guide the LLM's response.

```python
# Advanced prompt engineering for robotic planning
class RoboticPromptEngineer:
    def __init__(self):
        self.system_prompt_templates = {
            "task_decomposition": """You are a cognitive planning system for a humanoid robot. Decompose complex tasks into executable subtasks that consider the robot's capabilities and environmental constraints. Respond with valid JSON only.""",
            "safety_planning": """Generate plans that prioritize safety above all else. Consider human safety, robot safety, and environmental safety. Respond with valid JSON only.""",
            "efficient_planning": """Generate plans that are efficient in terms of time and energy while maintaining safety and task completion. Respond with valid JSON only."""
        }

    def create_task_decomposition_prompt(self, task: str, capabilities: Dict, environment: Dict) -> Dict:
        """
        Create a comprehensive prompt for task decomposition
        """
        # Few-shot examples to guide the LLM
        examples = [
            {
                "task": "Set the table for two people",
                "capabilities": capabilities,
                "environment": environment,
                "plan": {
                    "decomposed_tasks": [
                        {
                            "id": 1,
                            "description": "Navigate to dining table",
                            "action_type": "navigation",
                            "parameters": {"target_location": "dining_table"},
                            "preconditions": ["path_is_clear"],
                            "postconditions": ["robot_at_dining_table"],
                            "estimated_duration": 15
                        },
                        {
                            "id": 2,
                            "description": "Grasp plate from kitchen counter",
                            "action_type": "manipulation",
                            "parameters": {"object": "plate", "location": "kitchen_counter"},
                            "preconditions": ["plate_is_available", "robot_at_kitchen"],
                            "postconditions": ["plate_is_grasped"],
                            "estimated_duration": 10
                        }
                    ]
                }
            }
        ]

        example_str = json.dumps(examples[0], indent=2)

        prompt = f"""
        Task: {task}

        Robot Capabilities:
        {json.dumps(capabilities, indent=2)}

        Environment State:
        {json.dumps(environment, indent=2)}

        Example of expected output format:
        {example_str}

        Decompose the task into executable subtasks following the example format.
        Consider: robot capabilities, environmental constraints, safety, and task dependencies.
        """

        return {
            "system": self.system_prompt_templates["task_decomposition"],
            "user": prompt
        }

    def create_safety_aware_prompt(self, task: str, capabilities: Dict, environment: Dict) -> Dict:
        """
        Create a safety-focused prompt for task planning
        """
        safety_constraints = self.extract_safety_constraints(environment)

        prompt = f"""
        Task: {task}

        Safety Constraints:
        {json.dumps(safety_constraints, indent=2)}

        Robot Capabilities:
        {json.dumps(capabilities, indent=2)}

        Environment State:
        {json.dumps(environment, indent=2)}

        Generate a plan that prioritizes safety while completing the task.
        Consider: human safety, robot safety, environmental safety, and obstacle avoidance.
        Include safety checks and fail-safes in the plan.
        """

        return {
            "system": self.system_prompt_templates["safety_planning"],
            "user": prompt
        }

    def extract_safety_constraints(self, environment: Dict) -> Dict:
        """
        Extract safety constraints from environment
        """
        safety_constraints = {
            "humans_in_environment": len(environment.get("humans", [])),
            "fragile_objects": [obj for obj in environment.get("objects", []) if obj.get("fragile", False)],
            "narrow_spaces": [area for area in environment.get("navigable_areas", []) if area.get("width", 1.0) < 0.8],
            "height_restricted_areas": [area for area in environment.get("navigable_areas", []) if area.get("ceiling_height", 2.5) < 1.8],
            "safety_zones": environment.get("safety_zones", [])
        }

        return safety_constraints

    def optimize_prompt_for_performance(self, base_prompt: str) -> str:
        """
        Optimize prompt for better LLM performance
        """
        # Add clear instructions about output format
        optimized_prompt = f"""
        {base_prompt}

        IMPORTANT:
        1. Respond with only valid JSON, no additional text or explanations
        2. Ensure all required fields are present in the output
        3. Use consistent data types (strings, numbers, booleans)
        4. Keep descriptions concise but informative
        5. Estimate durations in seconds as floating point numbers
        """

        return optimized_prompt

class AdaptivePromptEngineer:
    def __init__(self):
        self.prompt_history = []
        self.success_rates = {}
        self.adaptation_threshold = 0.8  # Adapt if success rate drops below this

    def adapt_prompt_based_on_feedback(self, original_prompt: str, result: Dict, success: bool) -> str:
        """
        Adapt prompt based on execution feedback
        """
        # Record the interaction
        self.prompt_history.append({
            "prompt": original_prompt,
            "result": result,
            "success": success,
            "timestamp": time.time()
        })

        # Calculate success rate for this prompt type
        prompt_type = self.categorize_prompt(original_prompt)
        if prompt_type not in self.success_rates:
            self.success_rates[prompt_type] = []

        self.success_rates[prompt_type].append(success)

        # Adapt if success rate is too low
        recent_successes = self.success_rates[prompt_type][-10:]  # Last 10 attempts
        if len(recent_successes) >= 5:  # Need at least 5 data points
            avg_success = sum(recent_successes) / len(recent_successes)

            if avg_success < self.adaptation_threshold:
                return self.generate_adapted_prompt(original_prompt, result, success)

        return original_prompt

    def categorize_prompt(self, prompt: str) -> str:
        """
        Categorize prompt for tracking success rates
        """
        if "decompose" in prompt.lower():
            return "decomposition"
        elif "safety" in prompt.lower():
            return "safety"
        elif "navigation" in prompt.lower():
            return "navigation"
        elif "manipulation" in prompt.lower():
            return "manipulation"
        else:
            return "general"

    def generate_adapted_prompt(self, original_prompt: str, result: Dict, success: bool) -> str:
        """
        Generate an adapted prompt based on feedback
        """
        if success:
            # If successful, maybe make it more efficient
            return self.make_prompt_more_efficient(original_prompt)
        else:
            # If failed, add more detailed instructions
            return self.add_detailed_instructions(original_prompt, result)

    def make_prompt_more_efficient(self, prompt: str) -> str:
        """
        Make prompt more efficient while maintaining effectiveness
        """
        return f"""
        {prompt}

        OPTIMIZATION HINTS:
        - Focus on the most critical steps for task completion
        - Minimize unnecessary intermediate steps
        - Consider the most direct path to completion
        """

    def add_detailed_instructions(self, prompt: str, result: Dict) -> str:
        """
        Add detailed instructions based on failure patterns
        """
        return f"""
        {prompt}

        DETAILED INSTRUCTIONS:
        - Ensure all preconditions are met before each action
        - Include explicit safety checks
        - Consider alternative approaches if primary method fails
        - Verify postconditions after each action
        - Include error handling and recovery steps
        """
```

### Context-Aware Prompting

Context-aware prompting leverages the current situation, environment, and task history to generate more relevant and effective plans. This approach improves the LLM's ability to generate plans that are appropriate for the specific circumstances.

```python
# Context-aware prompting system
class ContextAwarePrompter:
    def __init__(self):
        self.context_manager = PlanningContextManager()
        self.task_similarity_analyzer = TaskSimilarityAnalyzer()

    def create_context_aware_prompt(self, task: str, environment: Dict, user_preferences: Dict = None) -> Dict:
        """
        Create a prompt that incorporates current context
        """
        # Get current context
        context = self.context_manager.get_context_summary()

        # Find similar past tasks
        similar_tasks = self.task_similarity_analyzer.find_similar_tasks(task, context.get('task_history', []))

        # Create context-aware prompt
        prompt_parts = []

        # Add task
        prompt_parts.append(f"Current Task: {task}")

        # Add context information
        if context.get('robot_state'):
            prompt_parts.append(f"Robot State: {json.dumps(context['robot_state'], indent=2)}")

        if context.get('environment_state'):
            prompt_parts.append(f"Environment State: {json.dumps(environment, indent=2)}")

        # Add user preferences if available
        if user_preferences:
            prompt_parts.append(f"User Preferences: {json.dumps(user_preferences, indent=2)}")

        # Add similar task information
        if similar_tasks:
            prompt_parts.append(f"Similar Past Tasks: {json.dumps(similar_tasks, indent=2)}")
            prompt_parts.append("Consider approaches that worked well for similar tasks, but adapt to current conditions.")

        # Add recent interactions
        if context.get('recent_interactions'):
            prompt_parts.append(f"Recent Interactions: {json.dumps(context['recent_interactions'], indent=2)}")

        full_prompt = "\n\n".join(prompt_parts)

        return {
            "system": self.get_context_aware_system_prompt(),
            "user": full_prompt
        }

    def get_context_aware_system_prompt(self) -> str:
        """
        Get system prompt that emphasizes context awareness
        """
        return """
        You are a context-aware robotic planning system. Consider all provided context including:
        - Current robot and environment state
        - User preferences and history
        - Similar past tasks and their outcomes
        - Recent interactions and current situation

        Generate plans that are tailored to the specific context while maintaining safety and efficiency.
        Respond with valid JSON only.
        """

class TaskSimilarityAnalyzer:
    def __init__(self):
        # In a real implementation, this might use embeddings or more sophisticated similarity measures
        pass

    def find_similar_tasks(self, current_task: str, past_tasks: List[Dict]) -> List[Dict]:
        """
        Find tasks similar to the current task from history
        """
        similar_tasks = []
        current_lower = current_task.lower()

        for past_task in past_tasks:
            past_desc = past_task.get('task', '').lower()

            # Simple keyword-based similarity (in practice, use semantic similarity)
            if self.calculate_task_similarity(current_lower, past_desc) > 0.3:
                similar_tasks.append(past_task)

        return similar_tasks[-3:]  # Return up to 3 most recent similar tasks

    def calculate_task_similarity(self, task1: str, task2: str) -> float:
        """
        Calculate similarity between two tasks (simplified implementation)
        """
        words1 = set(task1.split())
        words2 = set(task2.split())

        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)  # Jaccard similarity
```

## Integration with ROS 2 Systems

### ROS 2 Action Integration

Integrating LLM-based cognitive planning with ROS 2 requires careful coordination between high-level planning and low-level action execution. The system must translate abstract plans into concrete ROS 2 actions while maintaining feedback loops for monitoring and adaptation.

```python
# ROS 2 integration for LLM-based planning
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import threading
import queue

class LLMPlanningROS2Bridge(Node):
    def __init__(self):
        super().__init__('llm_planning_bridge')

        # Initialize LLM components
        self.llm_interface = LLMInterface(model_name="gpt-3.5-turbo")
        self.task_decomposer = TaskDecomposer(self.llm_interface)
        self.plan_executor = PlanExecutor(self.task_decomposer)
        self.context_manager = PlanningContextManager()

        # ROS 2 interfaces
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Publishers and subscribers
        self.task_sub = self.create_subscription(
            String,
            'high_level_tasks',
            self.task_callback,
            10
        )

        self.status_pub = self.create_publisher(
            String,
            'planning_status',
            10
        )

        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10
        )

        # Internal state
        self.current_plan = None
        self.plan_queue = queue.Queue()
        self.execution_thread = None
        self.is_executing = False

    def task_callback(self, msg):
        """
        Callback for high-level tasks
        """
        task_description = msg.data
        self.get_logger().info(f"Received high-level task: {task_description}")

        # Update context
        self.context_manager.start_new_task(task_description)

        # Generate and queue the plan
        environment_state = self.get_current_environment_state()
        plan = self.task_decomposer.decompose_task(task_description, environment_state)

        self.plan_queue.put(plan)

        # Start execution if not already running
        if not self.is_executing:
            self.execution_thread = threading.Thread(target=self.execute_plans)
            self.execution_thread.start()

    def joint_state_callback(self, msg):
        """
        Callback for joint states to update robot state
        """
        robot_state = {
            'joint_positions': dict(zip(msg.name, msg.position)),
            'joint_velocities': dict(zip(msg.name, msg.velocity)),
            'timestamp': msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
        }
        self.context_manager.update_robot_state(robot_state)

    def get_current_environment_state(self):
        """
        Get current environment state from ROS 2 topics
        """
        # This would integrate with perception nodes, TF, etc.
        # For this example, we'll return a simplified state
        return {
            'objects': [
                {'name': 'cup', 'type': 'cup', 'position': [1.0, 0.5, 0.8], 'reachable': True},
                {'name': 'book', 'type': 'book', 'position': [0.8, 0.3, 0.8], 'reachable': True}
            ],
            'navigable_areas': [
                {'name': 'kitchen', 'centroid': [2.0, 1.0], 'traversable': True},
                {'name': 'living_room', 'centroid': [0.0, 0.0], 'traversable': True}
            ],
            'humans': [],  # Would come from perception
            'obstacles': []  # Would come from costmap/ perception
        }

    def execute_plans(self):
        """
        Execute plans from the queue in a separate thread
        """
        self.is_executing = True

        while rclpy.ok() and not self.plan_queue.empty():
            try:
                plan = self.plan_queue.get(timeout=1.0)
                self.execute_single_plan(plan)
            except queue.Empty:
                continue

        self.is_executing = False

    def execute_single_plan(self, plan):
        """
        Execute a single plan
        """
        self.current_plan = plan

        # Publish status
        status_msg = String()
        status_msg.data = f"Executing plan: {plan.get('original_task', 'unknown')}"
        self.status_pub.publish(status_msg)

        # Execute the plan using the executor
        results = self.execute_tasks_sequentially_with_ros2(plan)

        # Update context with results
        success = self.check_plan_success(results, plan.get("success_criteria", []))
        self.context_manager.complete_task(success, f"Plan completed with {len([r for r in results if r['success']])}/{len(results)} tasks successful")

    def execute_tasks_sequentially_with_ros2(self, plan: Dict) -> List[Dict]:
        """
        Execute tasks in the plan using ROS 2 actions
        """
        results = []

        for task in plan["decomposed_tasks"]:
            result = self.execute_single_task_with_ros2(task)
            results.append(result)

            if not result["success"]:
                self.get_logger().warn(f"Task failed: {task['description']}")
                # Consider recovery strategies
                recovery_result = self.attempt_recovery_with_ros2(task, result)
                if not recovery_result["success"]:
                    break  # Stop execution if recovery fails

        return results

    def execute_single_task_with_ros2(self, task: Dict) -> Dict:
        """
        Execute a single task using ROS 2 interfaces
        """
        self.get_logger().info(f"Executing task: {task['description']}")

        if task["action_type"] == "navigation":
            return self.execute_navigation_with_ros2(task)
        elif task["action_type"] == "manipulation":
            return self.execute_manipulation_with_ros2(task)
        elif task["action_type"] == "perception":
            return self.execute_perception_with_ros2(task)
        elif task["action_type"] == "interaction":
            return self.execute_interaction_with_ros2(task)
        else:
            return {
                "task_id": task["id"],
                "task_description": task["description"],
                "action_type": task["action_type"],
                "success": False,
                "execution_time": 0,
                "details": {"error": "Unsupported action type"},
                "timestamp": time.time()
            }

    def execute_navigation_with_ros2(self, task: Dict) -> Dict:
        """
        Execute navigation task using ROS 2 navigation stack
        """
        try:
            # Extract destination from task parameters
            destination = task["parameters"].get("destination")
            if not destination:
                return {
                    "task_id": task["id"],
                    "success": False,
                    "details": {"error": "No destination specified"}
                }

            # Convert destination to PoseStamped (simplified)
            goal_pose = self.create_navigation_goal(destination)

            # Wait for action server
            self.nav_client.wait_for_server()

            # Create and send goal
            goal_msg = NavigateToPose.Goal()
            goal_msg.pose = goal_pose

            future = self.nav_client.send_goal_async(goal_msg)

            # Wait for result (with timeout)
            start_time = time.time()
            while not future.done() and (time.time() - start_time) < 60:  # 60 second timeout
                time.sleep(0.1)

            if not future.done():
                return {
                    "task_id": task["id"],
                    "success": False,
                    "details": {"error": "Navigation timeout"}
                }

            # Process result
            goal_handle = future.result()
            result = goal_handle.get_result_async()

            success = result.result.result == "reached_goal"  # Simplified check

            return {
                "task_id": task["id"],
                "success": success,
                "execution_time": time.time() - start_time,
                "details": {"destination": destination, "result": str(result.result.result)}
            }

        except Exception as e:
            return {
                "task_id": task["id"],
                "success": False,
                "execution_time": time.time(),
                "details": {"error": str(e)}
            }

    def create_navigation_goal(self, destination: str) -> PoseStamped:
        """
        Create a navigation goal from destination name
        """
        # In a real system, this would use a map or location database
        # For this example, we'll use predefined locations
        locations = {
            "kitchen": (2.0, 1.0, 0.0),
            "living_room": (0.0, 0.0, 0.0),
            "bedroom": (-1.0, 2.0, 0.0),
            "dining_table": (1.5, 0.5, 0.0)
        }

        if destination in locations:
            x, y, theta = locations[destination]
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0
            # Set orientation from theta
            from math import cos, sin
            pose.pose.orientation.z = sin(theta / 2.0)
            pose.pose.orientation.w = cos(theta / 2.0)
            return pose
        else:
            # Default pose if location not found
            pose = PoseStamped()
            pose.header.frame_id = "map"
            return pose

    def execute_manipulation_with_ros2(self, task: Dict) -> Dict:
        """
        Execute manipulation task using ROS 2 manipulation interfaces
        """
        # Placeholder for manipulation execution
        # In a real system, this would interface with manipulation action servers
        object_name = task["parameters"].get("object", "unknown")

        # Simulate execution
        time.sleep(3)  # Simulate manipulation time

        return {
            "task_id": task["id"],
            "success": True,
            "execution_time": 3.0,
            "details": {"object": object_name, "action": "grasped", "position": [0.5, 0.5, 0.75]}
        }

    def execute_perception_with_ros2(self, task: Dict) -> Dict:
        """
        Execute perception task using ROS 2 perception interfaces
        """
        # Placeholder for perception execution
        target = task["parameters"].get("target", "unknown")

        # Simulate perception
        time.sleep(1)  # Simulate perception time

        return {
            "task_id": task["id"],
            "success": True,
            "execution_time": 1.0,
            "details": {"target": target, "detected": True, "confidence": 0.95}
        }

    def execute_interaction_with_ros2(self, task: Dict) -> Dict:
        """
        Execute interaction task using ROS 2 interaction interfaces
        """
        # Placeholder for interaction execution
        interaction_type = task["parameters"].get("type", "unknown")

        # Simulate interaction
        time.sleep(1)  # Simulate interaction time

        return {
            "task_id": task["id"],
            "success": True,
            "execution_time": 1.0,
            "details": {"type": interaction_type, "completed": True}
        }

    def attempt_recovery_with_ros2(self, failed_task: Dict, failure_result: Dict) -> Dict:
        """
        Attempt to recover from task failure using ROS 2 interfaces
        """
        self.get_logger().info(f"Attempting recovery for failed task: {failed_task['description']}")

        # Simple recovery strategies
        if failed_task["action_type"] == "navigation":
            # Try alternative navigation approach
            return self.try_alternative_navigation(failed_task)
        elif failed_task["action_type"] == "manipulation":
            # Try alternative manipulation approach
            return self.try_alternative_manipulation(failed_task)

        return {"success": False, "method": "no_recovery_implemented"}

    def try_alternative_navigation(self, task: Dict) -> Dict:
        """
        Try alternative navigation approach
        """
        # In a real system, this might try a different path or approach
        time.sleep(2)  # Simulate alternative approach
        return {"success": True, "method": "alternative_navigation"}

    def try_alternative_manipulation(self, task: Dict) -> Dict:
        """
        Try alternative manipulation approach
        """
        # In a real system, this might try a different grasp or approach angle
        time.sleep(2)  # Simulate alternative approach
        return {"success": True, "method": "alternative_manipulation"}

    def check_plan_success(self, results: List[Dict], success_criteria: List[str]) -> bool:
        """
        Check if the overall plan was successful
        """
        successful_tasks = sum(1 for result in results if result["success"])
        total_tasks = len(results)

        return successful_tasks / total_tasks > 0.7 if total_tasks > 0 else True
```

### Planning Monitoring and Adaptation

Effective LLM-based planning systems must include monitoring capabilities to track plan execution and adapt when conditions change or tasks fail. This requires continuous assessment of progress and the ability to replan when necessary.

```python
# Planning monitoring and adaptation system
class PlanMonitorAndAdapter:
    def __init__(self, ros2_bridge: LLMPlanningROS2Bridge):
        self.ros2_bridge = ros2_bridge
        self.active_monitoring = False
        self.monitoring_thread = None
        self.plan_progress = {}
        self.environment_changes = []
        self.adaptation_needed = False

    def start_monitoring(self):
        """
        Start monitoring plan execution and environment changes
        """
        self.active_monitoring = True
        self.monitoring_thread = threading.Thread(target=self.monitor_execution)
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """
        Stop monitoring
        """
        self.active_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join()

    def monitor_execution(self):
        """
        Monitor plan execution in a separate thread
        """
        while self.active_monitoring:
            # Check for environment changes
            self.detect_environment_changes()

            # Assess plan progress
            self.assess_plan_progress()

            # Check for adaptation needs
            if self.adaptation_needed:
                self.handle_adaptation()

            time.sleep(0.5)  # Monitor every 0.5 seconds

    def detect_environment_changes(self):
        """
        Detect changes in the environment that might affect the plan
        """
        current_env = self.ros2_bridge.get_current_environment_state()

        # Compare with previous environment state
        # This is a simplified example - in practice, you'd have a more sophisticated change detection system
        if hasattr(self, 'previous_environment'):
            changes = self.compare_environments(self.previous_environment, current_env)
            if changes:
                self.environment_changes.append({
                    'timestamp': time.time(),
                    'changes': changes,
                    'impact_assessment': self.assess_change_impact(changes)
                })

        self.previous_environment = current_env

    def compare_environments(self, env1: Dict, env2: Dict) -> List[Dict]:
        """
        Compare two environment states and identify changes
        """
        changes = []

        # Compare objects
        obj_changes = self.compare_object_lists(env1.get('objects', []), env2.get('objects', []))
        if obj_changes:
            changes.extend(obj_changes)

        # Compare humans
        human_changes = self.compare_human_lists(env1.get('humans', []), env2.get('humans', []))
        if human_changes:
            changes.extend(human_changes)

        # Compare obstacles
        obstacle_changes = self.compare_obstacle_lists(env1.get('obstacles', []), env2.get('obstacles', []))
        if obstacle_changes:
            changes.extend(obstacle_changes)

        return changes

    def compare_object_lists(self, list1: List[Dict], list2: List[Dict]) -> List[Dict]:
        """
        Compare two lists of objects
        """
        changes = []

        # Find new objects
        for obj2 in list2:
            found = False
            for obj1 in list1:
                if obj1.get('name') == obj2.get('name'):
                    found = True
                    # Check if properties changed
                    if obj1.get('position') != obj2.get('position'):
                        changes.append({
                            'type': 'object_moved',
                            'object': obj2['name'],
                            'from': obj1['position'],
                            'to': obj2['position']
                        })
                    break
            if not found:
                changes.append({
                    'type': 'object_added',
                    'object': obj2['name'],
                    'position': obj2['position']
                })

        # Find removed objects
        for obj1 in list1:
            found = False
            for obj2 in list2:
                if obj1.get('name') == obj2.get('name'):
                    found = True
                    break
            if not found:
                changes.append({
                    'type': 'object_removed',
                    'object': obj1['name']
                })

        return changes

    def compare_human_lists(self, list1: List[Dict], list2: List[Dict]) -> List[Dict]:
        """
        Compare two lists of humans
        """
        # Similar to object comparison but for humans
        changes = []

        # Implementation would be similar to compare_object_lists
        # For brevity, returning empty list in this example
        return changes

    def compare_obstacle_lists(self, list1: List[Dict], list2: List[Dict]) -> List[Dict]:
        """
        Compare two lists of obstacles
        """
        # Similar to object comparison but for obstacles
        changes = []

        # Implementation would be similar to compare_object_lists
        # For brevity, returning empty list in this example
        return changes

    def assess_change_impact(self, changes: List[Dict]) -> str:
        """
        Assess the impact level of environment changes
        """
        high_impact_keywords = ['blocked_path', 'new_human', 'fragile_object_moved']
        medium_impact_keywords = ['object_moved', 'obstacle_added']

        for change in changes:
            change_type = change.get('type', '')
            if any(keyword in change_type for keyword in high_impact_keywords):
                return 'high'
            elif any(keyword in change_type for keyword in medium_impact_keywords):
                return 'medium'

        return 'low'

    def assess_plan_progress(self):
        """
        Assess the progress of the current plan
        """
        # This would integrate with the ROS2 bridge to get real-time progress
        # For this example, we'll simulate progress assessment
        if self.ros2_bridge.current_plan:
            plan_id = id(self.ros2_bridge.current_plan)

            if plan_id not in self.plan_progress:
                self.plan_progress[plan_id] = {
                    'start_time': time.time(),
                    'tasks_completed': 0,
                    'total_tasks': len(self.ros2_bridge.current_plan.get('decomposed_tasks', [])),
                    'last_update': time.time()
                }

            # In a real system, this would check actual task completion status
            # For simulation, we'll just check if enough time has passed
            progress_info = self.plan_progress[plan_id]
            time_elapsed = time.time() - progress_info['start_time']

            # Flag for adaptation if plan is taking too long or environment changed significantly
            if time_elapsed > 120:  # 2 minutes
                self.adaptation_needed = True

    def handle_adaptation(self):
        """
        Handle plan adaptation when needed
        """
        if not self.ros2_bridge.current_plan:
            return

        self.ros2_bridge.get_logger().info("Adapting current plan due to environment changes or progress issues")

        # Get current state
        current_env = self.ros2_bridge.get_current_environment_state()
        current_robot_state = self.ros2_bridge.context_manager.robot_state

        # Generate adapted plan
        adapted_plan = self.generate_adapted_plan(
            self.ros2_bridge.current_plan,
            current_env,
            current_robot_state
        )

        if adapted_plan:
            # Replace current plan with adapted plan
            self.ros2_bridge.current_plan = adapted_plan
            self.ros2_bridge.get_logger().info("Plan successfully adapted")

        self.adaptation_needed = False

    def generate_adapted_plan(self, original_plan: Dict, current_env: Dict, current_robot_state: Dict) -> Dict:
        """
        Generate an adapted plan based on current conditions
        """
        # Create adaptation prompt
        adaptation_prompt = f"""
        Original Task: {original_plan.get('original_task', 'unknown')}

        Original Plan: {json.dumps(original_plan, indent=2)}

        Current Environment: {json.dumps(current_env, indent=2)}

        Current Robot State: {json.dumps(current_robot_state, indent=2)}

        Environmental Changes: {json.dumps(self.environment_changes[-5:], indent=2)}  # Last 5 changes

        The original plan needs to be adapted due to environmental changes or progress issues.
        Generate an adapted plan that:
        1. Accounts for the current environment and robot state
        2. Completes the original task goal if possible
        3. Incorporates lessons from environmental changes
        4. Maintains safety and efficiency

        Return in the same JSON format as the original plan.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a plan adaptation system. Generate an adapted plan that accounts for environmental changes while maintaining the task goal. Respond with valid JSON only."},
                    {"role": "user", "content": adaptation_prompt}
                ],
                temperature=0.3,
                max_tokens=1200
            )

            plan_json = response.choices[0].message.content
            start_idx = plan_json.find('{')
            end_idx = plan_json.rfind('}')
            if start_idx != -1 and end_idx != -1:
                plan_json = plan_json[start_idx:end_idx+1]

            return json.loads(plan_json)
        except Exception as e:
            self.ros2_bridge.get_logger().error(f"Error in plan adaptation: {e}")
            return None
```

## Best Practices and Optimization

### Performance Optimization

Optimizing LLM-based cognitive planning systems requires balancing planning quality with computational efficiency. Several strategies can improve system performance:

```python
# Performance optimization for LLM-based planning
class OptimizedLLMPlanner:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.plan_cache = {}
        self.cache_size_limit = 100
        self.response_time_threshold = 5.0  # seconds
        self.fallback_enabled = True

    def plan_with_optimization(self, task: str, environment: Dict, use_cache: bool = True) -> Dict:
        """
        Plan with performance optimizations
        """
        # Create cache key
        cache_key = self.create_cache_key(task, environment)

        # Check cache first
        if use_cache and cache_key in self.plan_cache:
            self.llm.get_logger().info("Using cached plan")
            return self.plan_cache[cache_key]

        # Measure response time
        start_time = time.time()

        try:
            # Generate plan
            plan = self.llm.generate_plan(task, self.get_robot_capabilities(), environment)

            response_time = time.time() - start_time

            # Cache the result if it's fast enough
            if response_time < self.response_time_threshold and len(self.plan_cache) < self.cache_size_limit:
                self.plan_cache[cache_key] = plan

            return plan

        except Exception as e:
            if self.fallback_enabled:
                self.llm.get_logger().warn(f"LLM planning failed: {e}, using fallback")
                return self.fallback_plan(task, environment)
            else:
                raise e

    def create_cache_key(self, task: str, environment: Dict) -> str:
        """
        Create a cache key for the given task and environment
        """
        import hashlib
        cache_input = f"{task}_{json.dumps(environment, sort_keys=True)}"
        return hashlib.md5(cache_input.encode()).hexdigest()

    def get_robot_capabilities(self) -> Dict:
        """
        Get robot capabilities for planning
        """
        return {
            "navigation": {"supported": True, "max_speed": 0.5},
            "manipulation": {"supported": True, "max_payload": 2.0},
            "perception": {"supported": True, "object_recognition": True},
            "interaction": {"supported": True, "speech_output": True}
        }

    def fallback_plan(self, task: str, environment: Dict) -> Dict:
        """
        Generate a simple fallback plan when LLM fails
        """
        return {
            "original_task": task,
            "decomposed_tasks": [
                {
                    "id": 1,
                    "description": f"Attempt to execute: {task}",
                    "action_type": "unknown",
                    "parameters": {},
                    "preconditions": [],
                    "postconditions": [],
                    "estimated_duration": 60,
                    "priority": "medium",
                    "dependencies": []
                }
            ],
            "overall_plan_constraints": [],
            "success_criteria": ["task attempted"],
            "failure_recovery": ["report failure"]
        }

class IncrementalPlanner:
    def __init__(self, base_planner: TaskDecomposer):
        self.base_planner = base_planner
        self.current_plan = None
        self.executed_steps = []

    def update_plan_incrementally(self, new_information: Dict) -> Dict:
        """
        Update the current plan incrementally based on new information
        """
        if not self.current_plan:
            return None

        # Create incremental update prompt
        update_prompt = f"""
        Current Plan: {json.dumps(self.current_plan, indent=2)}

        Executed Steps: {json.dumps(self.executed_steps, indent=2)}

        New Information: {json.dumps(new_information, indent=2)}

        Update the plan incrementally to account for the new information.
        Keep completed steps as is, and only modify upcoming steps.
        If new information makes the plan impossible, suggest alternatives.

        Return the updated plan in the same format.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Update the plan incrementally based on new information. Keep completed steps unchanged. Respond with valid JSON only."},
                    {"role": "user", "content": update_prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )

            plan_json = response.choices[0].message.content
            start_idx = plan_json.find('{')
            end_idx = plan_json.rfind('}')
            if start_idx != -1 and end_idx != -1:
                plan_json = plan_json[start_idx:end_idx+1]

            updated_plan = json.loads(plan_json)
            self.current_plan = updated_plan
            return updated_plan
        except Exception as e:
            print(f"Error in incremental planning: {e}")
            return self.current_plan  # Return unchanged plan on error
```

### Safety and Validation

Safety is paramount in LLM-based robotic planning, especially for humanoid robots operating in human environments. Validation mechanisms must ensure that generated plans are safe and appropriate.

```python
# Safety and validation for LLM-based planning
class SafetyValidator:
    def __init__(self):
        self.safety_rules = self.define_safety_rules()

    def define_safety_rules(self) -> Dict:
        """
        Define safety rules for plan validation
        """
        return {
            "navigation": [
                {"rule": "maintain_min_distance_from_humans", "threshold": 0.8},  # meters
                {"rule": "avoid_forbidden_areas", "areas": []},
                {"rule": "respect_navigation_limits", "max_speed": 0.5}
            ],
            "manipulation": [
                {"rule": "check_object_weight", "max_weight": 3.0},  # kg
                {"rule": "avoid_fragile_objects_unless_specified", "default": True},
                {"rule": "maintain_stability_during_manipulation", "required": True}
            ],
            "interaction": [
                {"rule": "respect_personal_space", "distance": 1.0},  # meters
                {"rule": "use_appropriate_gestures", "required": True}
            ]
        }

    def validate_plan(self, plan: Dict, environment: Dict) -> Dict:
        """
        Validate a plan against safety rules
        """
        validation_results = {
            "is_safe": True,
            "violations": [],
            "suggestions": [],
            "confidence": 0.0
        }

        # Check each task in the plan
        for task in plan.get("decomposed_tasks", []):
            task_violations = self.validate_task(task, environment)
            validation_results["violations"].extend(task_violations)

        # Check overall plan constraints
        overall_violations = self.validate_plan_constraints(plan, environment)
        validation_results["violations"].extend(overall_violations)

        # If there are violations, the plan is not safe
        validation_results["is_safe"] = len(validation_results["violations"]) == 0

        # Calculate safety confidence
        total_checks = len(self.safety_rules["navigation"]) + len(self.safety_rules["manipulation"]) + len(self.safety_rules["interaction"])
        passed_checks = total_checks - len(validation_results["violations"])
        validation_results["confidence"] = passed_checks / total_checks if total_checks > 0 else 1.0

        return validation_results

    def validate_task(self, task: Dict, environment: Dict) -> List[Dict]:
        """
        Validate a single task against safety rules
        """
        violations = []

        if task["action_type"] == "navigation":
            violations.extend(self.validate_navigation_task(task, environment))
        elif task["action_type"] == "manipulation":
            violations.extend(self.validate_manipulation_task(task, environment))
        elif task["action_type"] == "interaction":
            violations.extend(self.validate_interaction_task(task, environment))

        return violations

    def validate_navigation_task(self, task: Dict, environment: Dict) -> List[Dict]:
        """
        Validate navigation task against safety rules
        """
        violations = []

        # Check if destination is too close to humans
        destination = task["parameters"].get("destination_position")
        if destination and "humans" in environment:
            for human in environment["humans"]:
                human_pos = human.get("position", [0, 0, 0])
                if destination and self.calculate_distance(destination, human_pos) < 0.8:
                    violations.append({
                        "rule": "maintain_min_distance_from_humans",
                        "task_id": task["id"],
                        "severity": "high",
                        "description": f"Navigation destination too close to human at {human_pos}"
                    })

        return violations

    def validate_manipulation_task(self, task: Dict, environment: Dict) -> List[Dict]:
        """
        Validate manipulation task against safety rules
        """
        violations = []

        target_object_name = task["parameters"].get("object")
        if target_object_name:
            # Find the object in the environment
            target_object = None
            for obj in environment.get("objects", []):
                if obj.get("name") == target_object_name:
                    target_object = obj
                    break

            if target_object:
                # Check object weight
                weight = target_object.get("weight", 0)
                if weight > 3.0:  # 3kg limit
                    violations.append({
                        "rule": "check_object_weight",
                        "task_id": task["id"],
                        "severity": "high",
                        "description": f"Object {target_object_name} weighs {weight}kg, exceeds 3kg limit"
                    })

                # Check if object is fragile
                if target_object.get("fragile", False) and not task.get("is_fragile_handling", False):
                    violations.append({
                        "rule": "avoid_fragile_objects_unless_specified",
                        "task_id": task["id"],
                        "severity": "medium",
                        "description": f"Attempting to manipulate fragile object {target_object_name} without proper handling"
                    })

        return violations

    def validate_interaction_task(self, task: Dict, environment: Dict) -> List[Dict]:
        """
        Validate interaction task against safety rules
        """
        violations = []

        # Check if interaction respects personal space
        target = task["parameters"].get("target")
        if target and target.startswith("human_") and "humans" in environment:
            for human in environment["humans"]:
                if human.get("id") == target:
                    # In a real system, we'd check the interaction distance
                    pass

        return violations

    def validate_plan_constraints(self, plan: Dict, environment: Dict) -> List[Dict]:
        """
        Validate overall plan constraints
        """
        violations = []

        # Check if plan duration is reasonable
        estimated_duration = sum(task.get("estimated_duration", 0) for task in plan.get("decomposed_tasks", []))
        if estimated_duration > 3600:  # More than 1 hour
            violations.append({
                "rule": "reasonable_plan_duration",
                "severity": "medium",
                "description": f"Plan estimated duration {estimated_duration}s exceeds reasonable limit"
            })

        return violations

    def calculate_distance(self, pos1: List[float], pos2: List[float]) -> float:
        """
        Calculate Euclidean distance between two 3D positions
        """
        import math
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
```

## Looking Ahead

The next chapters will build upon this cognitive planning foundation. Chapter 4 will explore multi-modal perception that combines vision and language understanding to enhance the robot's environmental awareness. Chapter 5 will integrate all components in a comprehensive capstone project demonstrating a complete VLA-powered humanoid system.

LLM-based cognitive planning represents a significant advancement in robotic autonomy, enabling robots to understand and execute complex, natural language commands. As these systems mature, we can expect increasingly sophisticated and intuitive interfaces that make robots more accessible and useful in human environments. The combination of LLMs with traditional robotic systems creates powerful hybrid approaches that leverage the strengths of both symbolic and neural processing.

## Citations

- Brown, T., et al. (2020). Language Models are Few-Shot Learners. Advances in Neural Information Processing Systems.
- Achiam, J., et al. (2023). GPT-4 Technical Report. OpenAI.
- Brohan, A., et al. (2022). RVT: Robotic View Transformers for Learning with Partial Observability. Conference on Robot Learning.
- Huang, W., et al. (2022). Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents. International Conference on Machine Learning.

## Summary

This chapter covered cognitive planning using Large Language Models (LLMs) for humanoid robots. We explored LLM fundamentals for robotic planning, implemented task decomposition and execution planning systems, discussed prompt engineering strategies for robotic applications, and detailed integration with ROS 2 systems. The chapter emphasized the importance of context-aware prompting, safety validation, and performance optimization in creating effective LLM-based planning systems. These systems enable humanoid robots to understand complex, natural language commands and generate sophisticated plans for task execution.

## Review Questions/Exercises

1. How do LLMs enable more flexible task decomposition compared to traditional planning systems?
2. What are the key components of effective prompt engineering for robotic applications?
3. Explain the process of integrating LLM-based planning with ROS 2 action servers.
4. Design a safety validation system for LLM-generated robotic plans.
5. How would you implement context-aware planning that adapts to changing environments?

---

**Chapter Specifications:**
- **Expected Length**: 2,000-3,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based implementations showing LLM integration, task decomposition, and ROS 2 interfaces
- **Diagrams/Illustrations**: Text-based architecture diagrams showing planning system components
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides