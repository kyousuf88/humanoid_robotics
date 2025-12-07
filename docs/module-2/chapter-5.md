# Chapter 5: Environment & Scenario Building (multi-room navigation, interactions)

## Learning Objectives
- [ ] Understand how to create complex multi-room environments for humanoid robot navigation
- [ ] Learn to implement interactive scenarios with dynamic obstacles and tasks
- [ ] Master environment design principles for realistic humanoid robot testing
- [ ] Implement navigation scenarios with varying complexity levels

## Key Concepts
- **Multi-room Navigation**: Techniques for navigating between different rooms and spaces
- **Dynamic Obstacles**: Moving objects and obstacles that affect robot navigation
- **Interactive Scenarios**: Environments with objects that the robot can interact with
- **Environment Complexity**: Gradually increasing difficulty in navigation scenarios
- **Task-Oriented Navigation**: Navigation tasks that require object interaction or manipulation

## Introduction

Creating realistic and challenging environments is crucial for developing robust humanoid robots capable of operating in real-world settings. Multi-room navigation scenarios provide the necessary complexity to test and refine navigation algorithms, obstacle avoidance systems, and human-robot interaction capabilities. This chapter explores the design and implementation of complex environments that challenge humanoid robots with realistic navigation tasks and interactive scenarios.

The complexity of humanoid robot navigation increases significantly when moving from simple, single-room environments to multi-room scenarios with dynamic obstacles, interactive objects, and complex navigation tasks. These environments must simulate real-world challenges such as door navigation, furniture avoidance, human interaction, and task-oriented navigation where the robot must perform specific actions in different rooms.

## Multi-Room Environment Design

### Architectural Planning

Designing multi-room environments for humanoid robots requires careful consideration of architectural elements that affect navigation and interaction:

1. **Doorways and Passages**: Door widths must accommodate the robot's dimensions with sufficient clearance for navigation. Standard doorways are typically 32-36 inches wide, but humanoid robots may require wider passages for safe navigation.

2. **Room Layouts**: Common room layouts include:
   - Living spaces with furniture arrangements
   - Kitchen environments with appliances and counters
   - Office spaces with desks and equipment
   - Bedroom environments with beds and dressers

3. **Floor Transitions**: Different floor materials (carpet, hardwood, tile) can affect robot locomotion and require different control strategies.

### Gazebo Environment Implementation

Creating multi-room environments in Gazebo involves using SDF (Simulation Description Format) to define the world structure:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="multi_room_house">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Living Room -->
    <model name="living_room_walls">
      <pose>0 0 0 0 0 0</pose>
      <static>true</static>
      <link name="wall_link">
        <collision name="front_wall_collision">
          <geometry>
            <box>
              <size>10 0.2 2.5</size>
            </box>
          </geometry>
        </collision>
        <visual name="front_wall_visual">
          <geometry>
            <box>
              <size>10 0.2 2.5</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Kitchen Area -->
    <model name="kitchen_counter">
      <pose>2 -3 0 0 0 0</pose>
      <static>true</static>
      <link name="counter_link">
        <collision name="counter_collision">
          <geometry>
            <box>
              <size>1.5 0.6 0.9</size>
            </box>
          </geometry>
        </collision>
        <visual name="counter_visual">
          <geometry>
            <box>
              <size>1.5 0.6 0.9</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.6 0.6 1</ambient>
            <diffuse>0.6 0.6 0.6 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Interactive Objects -->
    <model name="table">
      <pose>-1 1 0 0 0 0</pose>
      <static>true</static>
      <link name="table_link">
        <collision name="table_collision">
          <geometry>
            <box>
              <size>1.2 0.8 0.75</size>
            </box>
          </geometry>
        </collision>
        <visual name="table_visual">
          <geometry>
            <box>
              <size>1.2 0.8 0.75</size>
            </box>
          </geometry>
          <material>
            <ambient>0.7 0.5 0.3 1</ambient>
            <diffuse>0.7 0.5 0.3 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

### Unity Environment Implementation

For Unity environments, we create multi-room scenarios using 3D models and prefabs:

```csharp
using UnityEngine;
using System.Collections.Generic;

public class MultiRoomEnvironment : MonoBehaviour
{
    [Header("Room Configuration")]
    public List<GameObject> rooms = new List<GameObject>();
    public List<GameObject> doorways = new List<GameObject>();
    public List<GameObject> interactiveObjects = new List<GameObject>();

    [Header("Navigation Configuration")]
    public float robotRadius = 0.5f;
    public float doorWidth = 0.8f;
    public float clearanceDistance = 0.3f;

    [Header("Dynamic Obstacles")]
    public List<GameObject> dynamicObstacles = new List<GameObject>();

    void Start()
    {
        SetupEnvironment();
        ConfigureNavigation();
        InitializeInteractiveObjects();
    }

    void SetupEnvironment()
    {
        // Create room boundaries
        foreach (GameObject room in rooms)
        {
            // Add navigation mesh to room
            NavMeshSurface surface = room.AddComponent<NavMeshSurface>();
            surface.collectObjects = CollectObjects.Children;
            surface.BuildNavMesh();
        }

        // Configure doorways for humanoid navigation
        foreach (GameObject doorway in doorways)
        {
            ConfigureDoorway(doorway);
        }
    }

    void ConfigureDoorway(GameObject doorway)
    {
        // Ensure doorway width accommodates humanoid robot
        BoxCollider doorwayCollider = doorway.GetComponent<BoxCollider>();
        if (doorwayCollider != null)
        {
            if (doorwayCollider.size.x < doorWidth)
            {
                doorwayCollider.size = new Vector3(doorWidth, doorwayCollider.size.y, doorwayCollider.size.z);
            }
        }

        // Add doorway component for navigation
        DoorwayComponent doorwayComp = doorway.AddComponent<DoorwayComponent>();
        doorwayComp.robotRadius = robotRadius;
        doorwayComp.clearanceDistance = clearanceDistance;
    }

    void ConfigureNavigation()
    {
        // Set up NavMesh for humanoid navigation
        NavMeshBuildSettings buildSettings = new NavMeshBuildSettings();
        buildSettings.agentTypeID = 0;
        buildSettings.agentRadius = robotRadius;
        buildSettings.agentHeight = 1.5f; // Humanoid height
        buildSettings.agentSlope = 45.0f;
        buildSettings.agentClimb = 0.5f;
        buildSettings.minRegionArea = 2.0f;
        buildSettings.overrideVoxelSize = true;
        buildSettings.voxelSize = 0.1f;

        // Build navigation mesh
        NavMeshBuilder.BuildNavMesh();
    }

    void InitializeInteractiveObjects()
    {
        foreach (GameObject obj in interactiveObjects)
        {
            // Add interaction components
            InteractionComponent interaction = obj.AddComponent<InteractionComponent>();
            interaction.SetAsInteractable();
        }
    }
}

// Component for handling doorway navigation
public class DoorwayComponent : MonoBehaviour
{
    public float robotRadius = 0.5f;
    public float clearanceDistance = 0.3f;

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Robot"))
        {
            CheckDoorwayClearance(other.transform.position);
        }
    }

    void CheckDoorwayClearance(Vector3 robotPosition)
    {
        float effectiveWidth = CalculateEffectiveWidth();
        float requiredWidth = (robotRadius * 2) + (clearanceDistance * 2);

        if (effectiveWidth < requiredWidth)
        {
            Debug.LogWarning("Doorway too narrow for humanoid robot navigation");
        }
    }

    float CalculateEffectiveWidth()
    {
        BoxCollider doorwayCollider = GetComponent<BoxCollider>();
        if (doorwayCollider != null)
        {
            return doorwayCollider.size.x;
        }
        return 0.0f;
    }
}

// Component for handling object interactions
public class InteractionComponent : MonoBehaviour
{
    public bool isInteractable = true;
    public string interactionType = "pickup"; // pickup, push, activate

    public void SetAsInteractable()
    {
        isInteractable = true;
        // Add visual indicator for interactable objects
        AddInteractionIndicator();
    }

    void AddInteractionIndicator()
    {
        // Add visual indicator (e.g., outline, icon) for interactable objects
        GameObject indicator = new GameObject("InteractionIndicator");
        indicator.transform.SetParent(transform);
        indicator.transform.localPosition = Vector3.zero;

        // Add visual effect
        var renderer = GetComponent<Renderer>();
        if (renderer != null)
        {
            // Add outline or highlight effect
            Material outlineMat = new Material(Shader.Find("Sprites/Default"));
            outlineMat.color = Color.yellow;
            renderer.materials = new Material[] { renderer.material, outlineMat };
        }
    }

    public bool CanInteract(GameObject robot)
    {
        // Check if robot is in range and interaction is possible
        float distance = Vector3.Distance(robot.transform.position, transform.position);
        return distance <= 1.5f && isInteractable;
    }

    public void ExecuteInteraction(GameObject robot)
    {
        if (CanInteract(robot))
        {
            switch (interactionType)
            {
                case "pickup":
                    PickupInteraction(robot);
                    break;
                case "push":
                    PushInteraction(robot);
                    break;
                case "activate":
                    ActivateInteraction(robot);
                    break;
            }
        }
    }

    void PickupInteraction(GameObject robot)
    {
        // Handle pickup interaction
        Debug.Log("Pickup interaction with " + gameObject.name);
    }

    void PushInteraction(GameObject robot)
    {
        // Handle push interaction
        Debug.Log("Push interaction with " + gameObject.name);
    }

    void ActivateInteraction(GameObject robot)
    {
        // Handle activate interaction
        Debug.Log("Activate interaction with " + gameObject.name);
    }
}
```

## Dynamic Obstacles and Moving Elements

### Simulating Dynamic Obstacles

Dynamic obstacles are crucial for realistic environment testing. They simulate moving humans, pets, or other moving objects:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, Twist
from gazebo_msgs.srv import SpawnEntity, DeleteEntity
from std_msgs.msg import Float64
import math
import random

class DynamicObstacleSimulator(Node):
    def __init__(self):
        super().__init__('dynamic_obstacle_simulator')

        # Parameters for obstacle movement
        self.declare_parameter('num_obstacles', 3)
        self.declare_parameter('movement_type', 'random_walk')  # random_walk, patrol, follow_path

        self.num_obstacles = self.get_parameter('num_obstacles').value
        self.movement_type = self.get_parameter('movement_type').value

        # Timer for updating obstacle positions
        self.timer = self.create_timer(0.1, self.update_obstacles)

        # Store obstacle information
        self.obstacles = []
        self.spawn_obstacles()

    def spawn_obstacles(self):
        """Spawn dynamic obstacles in the simulation"""
        spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        while not spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn service not available, waiting again...')

        for i in range(self.num_obstacles):
            obstacle_name = f'dynamic_obstacle_{i}'

            # Create a simple sphere model for the obstacle
            obstacle_xml = f"""
            <sdf version="1.6">
              <model name="{obstacle_name}">
                <pose>0 0 0.5 0 0 0</pose>
                <link name="link">
                  <pose>0 0 0 0 0 0</pose>
                  <collision name="collision">
                    <geometry>
                      <sphere>
                        <radius>0.3</radius>
                      </sphere>
                    </geometry>
                  </collision>
                  <visual name="visual">
                    <geometry>
                      <sphere>
                        <radius>0.3</radius>
                      </sphere>
                    </geometry>
                    <material>
                      <ambient>1 0 0 1</ambient>
                      <diffuse>1 0 0 1</diffuse>
                    </material>
                  </visual>
                  <inertial>
                    <mass>1.0</mass>
                    <inertia>
                      <ixx>0.4</ixx>
                      <iyy>0.4</iyy>
                      <izz>0.4</izz>
                    </inertia>
                  </inertial>
                </link>
              </model>
            </sdf>
            """

            # Random starting position
            start_x = random.uniform(-3.0, 3.0)
            start_y = random.uniform(-3.0, 3.0)

            request = SpawnEntity.Request()
            request.name = obstacle_name
            request.xml = obstacle_xml
            request.initial_pose.position.x = start_x
            request.initial_pose.position.y = start_y
            request.initial_pose.position.z = 0.5
            request.robot_namespace = ''

            future = spawn_client.call_async(request)
            self.obstacles.append({
                'name': obstacle_name,
                'x': start_x,
                'y': start_y,
                'target_x': start_x,
                'target_y': start_y,
                'speed': random.uniform(0.1, 0.5),
                'last_update': self.get_clock().now()
            })

    def update_obstacles(self):
        """Update positions of dynamic obstacles"""
        current_time = self.get_clock().now()

        for obstacle in self.obstacles:
            if self.movement_type == 'random_walk':
                self.random_walk_movement(obstacle, current_time)
            elif self.movement_type == 'patrol':
                self.patrol_movement(obstacle, current_time)
            elif self.movement_type == 'follow_path':
                self.follow_path_movement(obstacle, current_time)

    def random_walk_movement(self, obstacle, current_time):
        """Move obstacle in random directions"""
        # Change target position randomly every 2-5 seconds
        time_diff = (current_time - obstacle['last_update']).nanoseconds / 1e9
        if time_diff > random.uniform(2.0, 5.0):
            obstacle['target_x'] = obstacle['x'] + random.uniform(-2.0, 2.0)
            obstacle['target_y'] = obstacle['y'] + random.uniform(-2.0, 2.0)
            obstacle['last_update'] = current_time

        # Move toward target
        dx = obstacle['target_x'] - obstacle['x']
        dy = obstacle['target_y'] - obstacle['y']
        distance = math.sqrt(dx*dx + dy*dy)

        if distance > 0.1:  # If not at target
            # Normalize direction vector
            dx /= distance
            dy /= distance

            # Move at constant speed
            obstacle['x'] += dx * obstacle['speed'] * 0.1  # 0.1 is dt
            obstacle['y'] += dy * obstacle['speed'] * 0.1

            # Update position in gazebo (this would require a service call in practice)
            self.update_gazebo_position(obstacle['name'], obstacle['x'], obstacle['y'])

    def patrol_movement(self, obstacle, current_time):
        """Move obstacle between predefined waypoints"""
        # Define patrol waypoints
        waypoints = [
            {'x': -3.0, 'y': -2.0},
            {'x': 3.0, 'y': -2.0},
            {'x': 3.0, 'y': 2.0},
            {'x': -3.0, 'y': 2.0}
        ]

        # Move to next waypoint
        current_waypoint = int((current_time.nanoseconds / 1e9) // 5) % len(waypoints)
        target = waypoints[current_waypoint]

        dx = target['x'] - obstacle['x']
        dy = target['y'] - obstacle['y']
        distance = math.sqrt(dx*dx + dy*dy)

        if distance > 0.1:
            dx /= distance
            dy /= distance
            obstacle['x'] += dx * obstacle['speed'] * 0.1
            obstacle['y'] += dy * obstacle['speed'] * 0.1

            self.update_gazebo_position(obstacle['name'], obstacle['x'], obstacle['y'])

    def follow_path_movement(self, obstacle, current_time):
        """Move obstacle along a predefined path"""
        # Define a circular path
        radius = 2.0
        center_x, center_y = 0.0, 0.0
        time_factor = (current_time.nanoseconds / 1e9) * 0.5  # Adjust speed

        obstacle['x'] = center_x + radius * math.cos(time_factor)
        obstacle['y'] = center_y + radius * math.sin(time_factor)

        self.update_gazebo_position(obstacle['name'], obstacle['x'], obstacle['y'])

    def update_gazebo_position(self, name, x, y):
        """Update the position of an entity in Gazebo"""
        # In a real implementation, this would call Gazebo's set_entity_state service
        pass

def main(args=None):
    rclpy.init(args=args)
    node = DynamicObstacleSimulator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Interactive Scenarios and Tasks

### Task-Oriented Navigation

Creating scenarios where humanoid robots must perform specific tasks in different rooms requires careful planning:

```csharp
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public class TaskOrientedNavigation : MonoBehaviour
{
    [Header("Navigation Tasks")]
    public List<NavigationTask> tasks = new List<NavigationTask>();

    [Header("Robot Reference")]
    public GameObject robot;

    [Header("Task Completion")]
    public int completedTasks = 0;
    public int totalTasks = 0;

    private Queue<NavigationTask> taskQueue = new Queue<NavigationTask>();
    private NavigationTask currentTask;
    private bool isTaskActive = false;

    void Start()
    {
        InitializeTasks();
        SetupTaskQueue();
        StartNextTask();
    }

    void InitializeTasks()
    {
        // Define navigation tasks
        totalTasks = tasks.Count;

        // Example tasks:
        tasks.Add(new NavigationTask
        {
            taskName = "Go to kitchen and find the table",
            destination = new Vector3(2.0f, -3.0f, 0.0f),
            taskType = TaskType.Navigation,
            description = "Navigate to the kitchen area and locate the table object"
        });

        tasks.Add(new NavigationTask
        {
            taskName = "Move to living room and find the couch",
            destination = new Vector3(-1.0f, 1.0f, 0.0f),
            taskType = TaskType.Navigation,
            description = "Navigate to the living room and locate the couch object"
        });

        tasks.Add(new NavigationTask
        {
            taskName = "Navigate through hallway to bedroom",
            destination = new Vector3(-4.0f, 0.0f, 0.0f),
            taskType = TaskType.Navigation,
            description = "Navigate through the hallway to reach the bedroom"
        });
    }

    void SetupTaskQueue()
    {
        // Add all tasks to queue
        foreach (NavigationTask task in tasks)
        {
            taskQueue.Enqueue(task);
        }
    }

    void StartNextTask()
    {
        if (taskQueue.Count > 0)
        {
            currentTask = taskQueue.Dequeue();
            isTaskActive = true;
            Debug.Log("Starting task: " + currentTask.taskName);

            // Send navigation goal to robot
            SendNavigationGoal(currentTask.destination);
        }
        else
        {
            Debug.Log("All tasks completed!");
            isTaskActive = false;
        }
    }

    void SendNavigationGoal(Vector3 destination)
    {
        // Send navigation goal to robot's navigation system
        if (robot != null)
        {
            NavMeshAgent agent = robot.GetComponent<NavMeshAgent>();
            if (agent != null)
            {
                agent.SetDestination(destination);
            }
        }
    }

    void Update()
    {
        if (isTaskActive && robot != null)
        {
            CheckTaskCompletion();
        }
    }

    void CheckTaskCompletion()
    {
        if (Vector3.Distance(robot.transform.position, currentTask.destination) < 1.0f)
        {
            // Task completed
            completedTasks++;
            Debug.Log("Task completed: " + currentTask.taskName);

            // Wait a moment before starting next task
            StartCoroutine(WaitForNextTask());
            isTaskActive = false;
        }
    }

    IEnumerator WaitForNextTask()
    {
        yield return new WaitForSeconds(2.0f); // Wait 2 seconds before next task
        StartNextTask();
    }
}

[System.Serializable]
public class NavigationTask
{
    public string taskName;
    public Vector3 destination;
    public TaskType taskType;
    public string description;
    public bool completed = false;
}

public enum TaskType
{
    Navigation,
    Interaction,
    ObjectSearch,
    PathFollowing
}
```

### Scenario Complexity Grading

Different scenarios can be graded by complexity to provide progressive challenges:

```python
#!/usr/bin/env python3

class ScenarioComplexityGrader:
    """
    Grade navigation scenarios by complexity level for humanoid robots
    """

    def __init__(self):
        self.complexity_levels = {
            'beginner': {
                'max_rooms': 1,
                'obstacles': 0,
                'interactions': 0,
                'navigation_difficulty': 1
            },
            'intermediate': {
                'max_rooms': 2,
                'obstacles': 2,
                'interactions': 1,
                'navigation_difficulty': 3
            },
            'advanced': {
                'max_rooms': 3,
                'obstacles': 5,
                'interactions': 2,
                'navigation_difficulty': 5
            },
            'expert': {
                'max_rooms': 4,
                'obstacles': 10,
                'interactions': 3,
                'navigation_difficulty': 7
            }
        }

    def calculate_complexity_score(self, scenario_config):
        """
        Calculate complexity score based on scenario configuration
        """
        score = 0

        # Room complexity (more rooms = higher complexity)
        score += scenario_config.get('num_rooms', 1) * 10

        # Obstacle complexity (more obstacles = higher complexity)
        score += scenario_config.get('num_obstacles', 0) * 5

        # Interaction complexity (more interactions = higher complexity)
        score += scenario_config.get('num_interactions', 0) * 15

        # Path complexity (narrow passages, tight spaces)
        score += scenario_config.get('narrow_passages', 0) * 8

        # Dynamic elements (moving obstacles, changing environment)
        score += scenario_config.get('dynamic_elements', 0) * 12

        # Task complexity (multiple objectives, sequential tasks)
        score += scenario_config.get('task_complexity', 1) * 7

        return score

    def grade_scenario(self, scenario_config):
        """
        Grade scenario based on complexity score
        """
        score = self.calculate_complexity_score(scenario_config)

        if score <= 25:
            return 'beginner'
        elif score <= 50:
            return 'intermediate'
        elif score <= 75:
            return 'advanced'
        else:
            return 'expert'

    def generate_scenario_for_level(self, target_level):
        """
        Generate a scenario configuration for a specific complexity level
        """
        if target_level not in self.complexity_levels:
            return None

        config = self.complexity_levels[target_level].copy()

        # Generate specific parameters based on level
        if target_level == 'beginner':
            config.update({
                'rooms': ['living_room'],
                'obstacles': [],
                'interactions': [],
                'tasks': ['navigate_to_target']
            })
        elif target_level == 'intermediate':
            config.update({
                'rooms': ['living_room', 'kitchen'],
                'obstacles': ['chair', 'small_table'],
                'interactions': ['find_object'],
                'tasks': ['navigate_between_rooms', 'locate_object']
            })
        elif target_level == 'advanced':
            config.update({
                'rooms': ['living_room', 'kitchen', 'bedroom'],
                'obstacles': ['chair', 'table', 'plant', 'box'],
                'interactions': ['find_object', 'navigate_narrow_space'],
                'tasks': ['navigate_complex_path', 'find_object', 'return_to_start']
            })
        elif target_level == 'expert':
            config.update({
                'rooms': ['living_room', 'kitchen', 'bedroom', 'bathroom'],
                'obstacles': ['chair', 'table', 'plant', 'box', 'person', 'pet', 'cart'],
                'interactions': ['find_object', 'navigate_narrow_space', 'avoid_moving_obstacle'],
                'tasks': ['multi_room_navigation', 'dynamic_obstacle_avoidance', 'object_interaction']
            })

        return config

# Example usage
def main():
    grader = ScenarioComplexityGrader()

    # Example scenario configuration
    example_scenario = {
        'num_rooms': 3,
        'num_obstacles': 5,
        'num_interactions': 2,
        'narrow_passages': 2,
        'dynamic_elements': 3,
        'task_complexity': 4
    }

    complexity_score = grader.calculate_complexity_score(example_scenario)
    grade = grader.grade_scenario(example_scenario)

    print(f"Scenario complexity score: {complexity_score}")
    print(f"Scenario grade: {grade}")

    # Generate scenario for specific level
    intermediate_scenario = grader.generate_scenario_for_level('intermediate')
    print(f"\nIntermediate scenario: {intermediate_scenario}")

if __name__ == '__main__':
    main()
```

## Environment Validation and Testing

### Validation Techniques

Validating multi-room environments ensures they're suitable for humanoid robot testing:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
import numpy as np
from scipy.spatial import distance
import math

class EnvironmentValidator(Node):
    """
    Validate multi-room environments for humanoid robot navigation
    """

    def __init__(self):
        super().__init__('environment_validator')

        # Publishers for validation results
        self.marker_pub = self.create_publisher(MarkerArray, 'validation_markers', 10)
        self.path_pub = self.create_publisher(Path, 'validation_path', 10)

        # Parameters for validation
        self.declare_parameter('robot_radius', 0.5)
        self.declare_parameter('min_door_width', 0.8)
        self.declare_parameter('min_corridor_width', 1.2)

        self.robot_radius = self.get_parameter('robot_radius').value
        self.min_door_width = self.get_parameter('min_door_width').value
        self.min_corridor_width = self.get_parameter('min_corridor_width').value

        # Timer for periodic validation
        self.timer = self.create_timer(5.0, self.validate_environment)

        self.get_logger().info('Environment validator initialized')

    def validate_environment(self):
        """
        Perform comprehensive environment validation
        """
        self.get_logger().info('Starting environment validation...')

        validation_results = {
            'door_widths': self.check_door_widths(),
            'corridor_widths': self.check_corridor_widths(),
            'navigation_paths': self.validate_navigation_paths(),
            'obstacle_clearance': self.check_obstacle_clearance(),
            'accessibility': self.validate_accessibility()
        }

        # Publish validation markers
        self.publish_validation_markers(validation_results)

        # Log validation summary
        self.log_validation_summary(validation_results)

    def check_door_widths(self):
        """
        Check if all doors are wide enough for humanoid navigation
        """
        # In simulation, we would query Gazebo for door models
        # For this example, we'll simulate door validation
        doors = self.get_door_models()
        narrow_doors = []

        for door in doors:
            width = self.calculate_door_width(door)
            if width < self.min_door_width:
                narrow_doors.append({
                    'name': door['name'],
                    'width': width,
                    'position': door['position'],
                    'required': self.min_door_width
                })

        return narrow_doors

    def check_corridor_widths(self):
        """
        Check if corridors are wide enough for humanoid navigation
        """
        # Simulate corridor width checking
        corridors = self.get_corridor_regions()
        narrow_corridors = []

        for corridor in corridors:
            width = self.calculate_corridor_width(corridor)
            if width < self.min_corridor_width:
                narrow_corridors.append({
                    'region': corridor['name'],
                    'width': width,
                    'required': self.min_corridor_width
                })

        return narrow_corridors

    def validate_navigation_paths(self):
        """
        Validate that navigation paths exist between all rooms
        """
        # Check connectivity between rooms
        rooms = self.get_rooms()
        connectivity_matrix = self.build_connectivity_matrix(rooms)

        unreachable_rooms = []
        for room in rooms:
            if not self.is_reachable_from_start(room, connectivity_matrix):
                unreachable_rooms.append(room['name'])

        return {
            'connectivity_matrix': connectivity_matrix,
            'unreachable_rooms': unreachable_rooms,
            'valid_paths': len(unreachable_rooms) == 0
        }

    def check_obstacle_clearance(self):
        """
        Check if obstacles maintain safe clearance for humanoid robots
        """
        obstacles = self.get_obstacles()
        invalid_clearances = []

        for obstacle in obstacles:
            clearance = self.calculate_obstacle_clearance(obstacle)
            if clearance < self.robot_radius:
                invalid_clearances.append({
                    'obstacle': obstacle['name'],
                    'clearance': clearance,
                    'required': self.robot_radius
                })

        return invalid_clearances

    def validate_accessibility(self):
        """
        Validate that all areas are accessible to humanoid robots
        """
        # Check for areas that are too small for humanoid navigation
        small_areas = []

        # In a real implementation, this would check for:
        # - Narrow passages
        # - Low ceiling areas
        # - Stairs or level changes
        # - Areas with insufficient turning space

        return small_areas

    def get_door_models(self):
        """
        Get door models from simulation (simulated implementation)
        """
        # This would normally query Gazebo for door models
        return [
            {'name': 'living_room_door', 'position': (0, 2.5, 0)},
            {'name': 'kitchen_door', 'position': (2, -1, 0)},
            {'name': 'bedroom_door', 'position': (-2, 1, 0)}
        ]

    def calculate_door_width(self, door):
        """
        Calculate door width (simulated implementation)
        """
        # Simulate different door widths
        import random
        return random.uniform(0.6, 1.2)  # Random width between 0.6 and 1.2 meters

    def get_corridor_regions(self):
        """
        Get corridor regions from simulation (simulated implementation)
        """
        return [
            {'name': 'hallway_1', 'bounds': (-1, -0.5, 1, 0.5)},
            {'name': 'hallway_2', 'bounds': (1.5, -2.5, 2.5, -1.5)}
        ]

    def calculate_corridor_width(self, corridor):
        """
        Calculate corridor width (simulated implementation)
        """
        bounds = corridor['bounds']
        width = bounds[2] - bounds[0]  # x2 - x1
        return width

    def get_rooms(self):
        """
        Get room models from simulation (simulated implementation)
        """
        return [
            {'name': 'living_room', 'position': (0, 0, 0)},
            {'name': 'kitchen', 'position': (2, -3, 0)},
            {'name': 'bedroom', 'position': (-3, 0, 0)},
            {'name': 'bathroom', 'position': (-1, -2, 0)}
        ]

    def build_connectivity_matrix(self, rooms):
        """
        Build connectivity matrix between rooms (simulated implementation)
        """
        # Simulate room connectivity
        connectivity = {}
        for room in rooms:
            connectivity[room['name']] = []

        # Add some connections
        connectivity['living_room'].append('kitchen')
        connectivity['living_room'].append('bedroom')
        connectivity['kitchen'].append('living_room')
        connectivity['bedroom'].append('living_room')
        connectivity['bathroom'].append('bedroom')
        connectivity['bedroom'].append('bathroom')

        return connectivity

    def is_reachable_from_start(self, target_room, connectivity_matrix):
        """
        Check if a room is reachable from the starting room (simulated implementation)
        """
        # Simulate reachability check
        start_room = 'living_room'
        visited = set()
        queue = [start_room]

        while queue:
            current = queue.pop(0)
            if current == target_room['name']:
                return True
            if current not in visited:
                visited.add(current)
                for neighbor in connectivity_matrix.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return False

    def get_obstacles(self):
        """
        Get obstacle models from simulation (simulated implementation)
        """
        return [
            {'name': 'table_1', 'position': (-1, 1, 0)},
            {'name': 'chair_1', 'position': (0.5, 0.5, 0)},
            {'name': 'plant_1', 'position': (2, -2, 0)}
        ]

    def calculate_obstacle_clearance(self, obstacle):
        """
        Calculate clearance around an obstacle (simulated implementation)
        """
        # Simulate clearance calculation
        import random
        return random.uniform(0.3, 1.0)

    def publish_validation_markers(self, validation_results):
        """
        Publish visualization markers for validation results
        """
        marker_array = MarkerArray()
        marker_id = 0

        # Mark narrow doors
        for door in validation_results['door_widths']:
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "narrow_doors"
            marker.id = marker_id
            marker.type = Marker.TEXT_VIEW_FACING
            marker.action = Marker.ADD

            marker.pose.position.x = door['position'][0]
            marker.pose.position.y = door['position'][1]
            marker.pose.position.z = 1.0
            marker.pose.orientation.w = 1.0

            marker.scale.z = 0.3
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0

            marker.text = f"Narrow Door: {door['width']:.2f}m"
            marker_array.markers.append(marker)
            marker_id += 1

        # Mark invalid clearances
        for clearance in validation_results['obstacle_clearance']:
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "invalid_clearances"
            marker.id = marker_id
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD

            marker.pose.position.x = 0.0  # Would get actual position in real implementation
            marker.pose.position.y = 0.0
            marker.pose.position.z = 0.5
            marker.pose.orientation.w = 1.0

            marker.scale.x = 0.2
            marker.scale.y = 0.2
            marker.scale.z = 0.2
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 0.5

            marker.text = f"Insufficient clearance: {clearance['clearance']:.2f}m"
            marker_array.markers.append(marker)
            marker_id += 1

        self.marker_pub.publish(marker_array)

    def log_validation_summary(self, validation_results):
        """
        Log validation summary
        """
        self.get_logger().info("=== Environment Validation Summary ===")

        if validation_results['door_widths']:
            self.get_logger().warn(f"Found {len(validation_results['door_widths'])} narrow doors")
            for door in validation_results['door_widths']:
                self.get_logger().warn(f"  - {door['name']}: {door['width']:.2f}m (min: {door['required']:.2f}m)")
        else:
            self.get_logger().info("✓ All doors meet width requirements")

        if validation_results['corridor_widths']:
            self.get_logger().warn(f"Found {len(validation_results['corridor_widths'])} narrow corridors")
        else:
            self.get_logger().info("✓ All corridors meet width requirements")

        if validation_results['navigation_paths']['unreachable_rooms']:
            self.get_logger().warn(f"Found {len(validation_results['navigation_paths']['unreachable_rooms'])} unreachable rooms")
        else:
            self.get_logger().info("✓ All rooms are connected and reachable")

        if validation_results['obstacle_clearance']:
            self.get_logger().warn(f"Found {len(validation_results['obstacle_clearance'])} obstacles with insufficient clearance")
        else:
            self.get_logger().info("✓ All obstacles maintain safe clearance")

def main(args=None):
    rclpy.init(args=args)
    validator = EnvironmentValidator()

    try:
        rclpy.spin(validator)
    except KeyboardInterrupt:
        pass
    finally:
        validator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Best Practices for Environment Design

### Design Principles

Creating effective multi-room environments for humanoid robots requires following best practices:

1. **Realistic Proportions**: Ensure rooms and doorways match real-world dimensions
2. **Gradual Complexity**: Start with simple environments and increase complexity
3. **Safety Margins**: Include adequate clearance for robot movement
4. **Consistent Layouts**: Use familiar room layouts that reflect real homes or offices
5. **Interactive Elements**: Include objects that robots can interact with
6. **Dynamic Elements**: Add moving obstacles to test navigation in dynamic environments

### Performance Optimization

For large, complex environments, consider performance optimization:

```csharp
using UnityEngine;
using System.Collections.Generic;

public class EnvironmentOptimization : MonoBehaviour
{
    [Header("LOD Configuration")]
    public float lodDistance = 10.0f;
    public int maxActiveObjects = 50;

    [Header("Occlusion Culling")]
    public bool enableOcclusionCulling = true;

    [Header("Object Pooling")]
    public bool enableObjectPooling = true;
    public List<GameObject> pooledObjects = new List<GameObject>();

    private List<GameObject> activeObjects = new List<GameObject>();
    private Queue<GameObject> inactiveObjects = new Queue<GameObject>();

    void Start()
    {
        if (enableObjectPooling)
        {
            InitializeObjectPool();
        }
    }

    void Update()
    {
        if (enableOcclusionCulling)
        {
            PerformOcclusionCulling();
        }

        if (enableObjectPooling)
        {
            ManageObjectPool();
        }
    }

    void InitializeObjectPool()
    {
        // Pre-instantiate objects for reuse
        foreach (GameObject prefab in pooledObjects)
        {
            for (int i = 0; i < 10; i++) // Create 10 instances of each prefab
            {
                GameObject obj = Instantiate(prefab);
                obj.SetActive(false);
                inactiveObjects.Enqueue(obj);
            }
        }
    }

    GameObject GetPooledObject(string objectType)
    {
        if (inactiveObjects.Count > 0)
        {
            GameObject obj = inactiveObjects.Dequeue();
            obj.SetActive(true);
            activeObjects.Add(obj);
            return obj;
        }
        else
        {
            // Create new object if pool is empty
            GameObject prefab = pooledObjects.Find(p => p.name == objectType);
            if (prefab != null)
            {
                GameObject obj = Instantiate(prefab);
                activeObjects.Add(obj);
                return obj;
            }
        }

        return null;
    }

    void ReturnToPool(GameObject obj)
    {
        if (activeObjects.Contains(obj))
        {
            activeObjects.Remove(obj);
            obj.SetActive(false);
            inactiveObjects.Enqueue(obj);
        }
    }

    void PerformOcclusionCulling()
    {
        // Implement occlusion culling logic
        // Only render objects that are visible to the camera
        Camera mainCamera = Camera.main;
        if (mainCamera != null)
        {
            foreach (GameObject obj in activeObjects)
            {
                if (obj != null)
                {
                    Renderer renderer = obj.GetComponent<Renderer>();
                    if (renderer != null)
                    {
                        // Check if object is visible to camera
                        bool isVisible = GeometryUtility.TestPlanesAABB(
                            GeometryUtility.CalculateFrustumPlanes(mainCamera),
                            renderer.bounds
                        );

                        renderer.enabled = isVisible;
                    }
                }
            }
        }
    }

    void ManageObjectPool()
    {
        // Limit the number of active objects
        if (activeObjects.Count > maxActiveObjects)
        {
            // Deactivate excess objects
            int excess = activeObjects.Count - maxActiveObjects;
            for (int i = 0; i < excess; i++)
            {
                if (activeObjects.Count > 0)
                {
                    GameObject obj = activeObjects[0];
                    ReturnToPool(obj);
                }
            }
        }
    }

    void OnDrawGizmos()
    {
        // Visualize LOD distance
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, lodDistance);
    }
}
```

## Looking Ahead

Multi-room navigation and interactive scenario design form the foundation for advanced humanoid robot testing and development. These environments allow for comprehensive testing of navigation algorithms, obstacle avoidance, human-robot interaction, and task-oriented behaviors.

The next chapter in this module will cover simulation tools and best practices for validating and testing humanoid robot behaviors in complex environments. We'll explore advanced techniques for creating realistic sensor data, implementing physics-based interactions, and ensuring that simulation results accurately reflect real-world performance.

## Citations

- Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. IEEE/RSJ International Conference on Intelligent Robots and Systems.
- Unity Technologies. (2023). Unity 3D Documentation: NavMesh and Pathfinding. Unity Technologies.
- ROS Navigation Stack Documentation. (2023). Navigation Tuning Guide. ROS Wiki.
- Stilman, B., & Kuffner, J. (2007). Navigation among movable obstacles: Real-time reasoning in complex environments. IEEE International Conference on Humanoid Robots.

## Summary

This chapter explored the design and implementation of complex multi-room environments for humanoid robot navigation and interaction. We covered architectural planning, implementation in both Gazebo and Unity, dynamic obstacle simulation, interactive scenario creation, and validation techniques. The chapter provided practical code examples for both simulation environments and emphasized best practices for creating realistic and challenging environments that properly test humanoid robot capabilities.

## Review Questions/Exercises

1. What are the minimum doorway width requirements for humanoid robot navigation, and why are they important?
2. How would you implement a dynamic obstacle that follows a predefined patrol route in a multi-room environment?
3. Design a validation system that checks if all rooms in a multi-room environment are accessible to a humanoid robot.
4. What are the key differences between implementing multi-room environments in Gazebo versus Unity, and when would you choose each?
5. Create a scenario complexity grading system that evaluates the difficulty of navigation tasks based on environmental factors.

---

**Chapter Specifications:**
- **Expected Length**: 2,000-3,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using rclpy where applicable for ROS 2 modules, C# for Unity implementations
- **Diagrams/Illustrations**: Text-based ASCII or references to images in `/static/img/book/module-X/`
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides