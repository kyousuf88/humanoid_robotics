---
id: module-1-chapter-3
sidebar_position: 3
title: "Chapter 3 - Building ROS 2 Packages with rclpy (workspaces, nodes, launch files)"
---

# Chapter 3: Building ROS 2 Packages with rclpy (workspaces, nodes, launch files)

## Learning Objectives
- [X] Create ROS 2 packages using Python and the rclpy library
- [X] Implement nodes with publishers, subscribers, services, and actions
- [X] Use launch files to start multiple nodes simultaneously
- [X] Understand the structure of ROS 2 workspaces and packages

## Key Concepts
- [X] **ROS 2 Package**: A container for ROS 2 code, including nodes, libraries, and configuration files
- [X] **Workspace**: A directory that contains multiple ROS 2 packages and build artifacts
- [X] **rclpy**: Python client library for ROS 2 that provides the Python API
- [X] **Launch Files**: XML or Python files that define how to start multiple ROS 2 nodes
- [X] **Package.xml**: Manifest file that describes the package and its dependencies
- [X] **setup.py**: Python setup file that defines how the package is built and installed

## Introduction

In this chapter, we'll learn how to create ROS 2 packages using Python and the rclpy library. We'll explore the structure of ROS 2 workspaces, create nodes with different communication patterns, and use launch files to orchestrate complex robotic systems. This knowledge is essential for developing humanoid robots, which typically consist of many specialized nodes working together.

ROS 2 packages are the fundamental building blocks of ROS 2 applications. They encapsulate functionality into manageable units that can be developed, tested, and maintained independently. The rclpy library provides the Python interface to ROS 2's core functionality, making it accessible to Python developers and well-suited for rapid prototyping and complex algorithm development.

## ROS 2 Workspace Structure

A ROS 2 workspace is a directory that contains multiple packages and their build artifacts. The typical structure of a ROS 2 workspace is:

```
workspace_name/
├── src/
│   ├── package1/
│   │   ├── CMakeLists.txt
│   │   ├── package.xml
│   │   ├── setup.py
│   │   ├── setup.cfg
│   │   └── package_name/
│   │       └── nodes/
│   │           └── node_name.py
│   └── package2/
│       ├── ...
├── build/
├── install/
└── log/
```

### The src Directory
The `src` directory contains all source code for packages in the workspace. Each package is a subdirectory within `src`.

### Build, Install, and Log Directories
- `build/`: Contains temporary build files created during compilation
- `install/`: Contains the installed packages that can be sourced and used
- `log/`: Contains build and runtime logs

## Creating a ROS 2 Package

Let's create a simple ROS 2 package step by step. We'll create a package called `robot_controller` that will contain nodes for controlling a simple robot.

### Step 1: Create the Package Structure

First, navigate to your workspace's `src` directory and create the package:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python robot_controller
```

This command creates the basic structure for a Python-based ROS 2 package:

```
robot_controller/
├── package.xml
├── setup.py
├── setup.cfg
├── test/
│   └── test_copyright.py
│   └── test_flake8.py
│   └── test_pep257.py
└── robot_controller/
    └── __init__.py
```

### Step 2: Understanding Package Files

Let's examine the key files in the package:

**package.xml**: This file describes the package and its dependencies:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>robot_controller</name>
  <version>0.0.0</version>
  <description>Package for controlling robots</description>
  <maintainer email="user@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>geometry_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

**setup.py**: This Python file defines how the package is built and installed:

```python
from setuptools import setup
import os
from glob import glob

package_name = 'robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='Package for controlling robots',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_controller_node = robot_controller.robot_controller_node:main',
            'sensor_publisher = robot_controller.sensor_publisher:main',
        ],
    },
)
```

### Step 3: Creating a Simple Node

Now let's create a simple node. First, create the node file:

```python
# robot_controller/robot_controller/simple_controller.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class SimpleController(Node):
    def __init__(self):
        super().__init__('simple_controller')

        # Create publisher for velocity commands
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Create subscriber for sensor data
        self.sensor_subscriber = self.create_subscription(
            String,
            'sensor_data',
            self.sensor_callback,
            10
        )

        # Create a timer to send commands periodically
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.i = 0

    def sensor_callback(self, msg):
        self.get_logger().info(f'Received sensor data: {msg.data}')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.5  # Move forward at 0.5 m/s
        msg.angular.z = 0.0  # No rotation
        self.cmd_vel_publisher.publish(msg)
        self.get_logger().info(f'Publishing velocity command: {msg.linear.x}, {msg.angular.z}')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    simple_controller = SimpleController()

    try:
        rclpy.spin(simple_controller)
    except KeyboardInterrupt:
        pass
    finally:
        simple_controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Step 4: Adding the Entry Point

Update the `setup.py` file to include our new node in the console scripts:

```python
entry_points={
    'console_scripts': [
        'simple_controller = robot_controller.simple_controller:main',
    ],
},
```

### Step 5: Building the Package

To build the package, go back to the workspace root and run:

```bash
cd ~/ros2_ws
colcon build --packages-select robot_controller
```

### Step 6: Sourcing the Workspace

After building, source the workspace to make the new package available:

```bash
source install/setup.bash
```

## Advanced Node Implementation

Let's create a more sophisticated node that demonstrates multiple communication patterns:

```python
# robot_controller/robot_controller/advanced_controller.py

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from std_msgs.msg import String
from geometry_msgs.msg import Twist, Pose
from example_interfaces.srv import SetBool
from example_interfaces.action import Fibonacci


class AdvancedController(Node):
    def __init__(self):
        super().__init__('advanced_controller')

        # Create callback group for handling multiple callbacks
        callback_group = ReentrantCallbackGroup()

        # Publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.status_publisher = self.create_publisher(String, 'controller_status', 10)

        # Subscribers
        self.pose_subscriber = self.create_subscription(
            Pose,
            'robot_pose',
            self.pose_callback,
            10
        )

        # Services
        self.enable_service = self.create_service(
            SetBool,
            'enable_controller',
            self.enable_callback
        )

        # Actions
        self.fibonacci_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )

        # Timer
        self.timer = self.create_timer(0.1, self.control_loop)

        # Internal state
        self.enabled = True
        self.current_pose = None

    def pose_callback(self, msg):
        self.current_pose = msg
        if self.enabled:
            self.get_logger().info(f'Current pose: ({msg.position.x}, {msg.position.y})')

    def enable_callback(self, request, response):
        self.enabled = request.data
        response.success = True
        response.message = f'Controller {"enabled" if self.enabled else "disabled"}'
        self.get_logger().info(response.message)
        return response

    def control_loop(self):
        if not self.enabled or self.current_pose is None:
            return

        # Simple control logic
        msg = Twist()
        # Move toward origin
        msg.linear.x = -0.1 * self.current_pose.position.x
        msg.linear.y = -0.1 * self.current_pose.position.y
        msg.angular.z = 0.0  # No rotation for now

        self.cmd_vel_publisher.publish(msg)

        # Publish status
        status_msg = String()
        status_msg.data = f'Controller running, position: ({self.current_pose.position.x:.2f}, {self.current_pose.position.y:.2f})'
        self.status_publisher.publish(status_msg)

    def send_fibonacci_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.fibonacci_client.wait_for_server()
        future = self.fibonacci_client.send_goal_async(goal_msg)
        return future


def main(args=None):
    rclpy.init(args=args)
    advanced_controller = AdvancedController()

    # Use a multi-threaded executor to handle multiple callbacks
    executor = MultiThreadedExecutor()
    executor.add_node(advanced_controller)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        advanced_controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Launch Files

Launch files allow you to start multiple nodes with a single command, making it easy to run complex systems. ROS 2 supports both XML and Python launch files.

### XML Launch File

Create a launch directory in your package:

```bash
mkdir robot_controller/launch
```

Now create an XML launch file:

```xml
<!-- robot_controller/launch/robot_system.launch.xml -->
<launch>
  <!-- Arguments -->
  <arg name="use_sim_time" default="false"/>

  <!-- Robot Controller Node -->
  <node pkg="robot_controller" exec="simple_controller" name="simple_controller" output="screen">
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <!-- Sensor Simulator Node -->
  <node pkg="robot_controller" exec="sensor_publisher" name="sensor_publisher" output="screen">
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <!-- Optional: Advanced Controller -->
  <node pkg="robot_controller" exec="advanced_controller" name="advanced_controller" output="screen" if="$(var advanced_enabled)">
    <param name="use_sim_time" value="$(var use_sim_time)"/>
  </node>

  <!-- Arguments that can be passed to the launch file -->
  <arg name="advanced_enabled" default="false"/>
</launch>
```

### Python Launch File

Python launch files offer more flexibility and programmability:

```python
# robot_controller/launch/robot_system.launch.py

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'
        ),

        # Robot Controller Node
        Node(
            package='robot_controller',
            executable='simple_controller',
            name='simple_controller',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        ),

        # Sensor Publisher Node
        Node(
            package='robot_controller',
            executable='sensor_publisher',
            name='sensor_publisher',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        ),

        # Advanced Controller Node
        Node(
            package='robot_controller',
            executable='advanced_controller',
            name='advanced_controller',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time}
            ]
        )
    ])
```

## Parameter Management

Parameters allow you to configure nodes without recompiling. ROS 2 provides several ways to handle parameters:

### YAML Parameter Files

Create a parameter file for your nodes:

```yaml
# robot_controller/config/robot_params.yaml
simple_controller:
  ros__parameters:
    robot_name: "my_robot"
    max_velocity: 1.0
    acceleration_limit: 0.5
    use_sim_time: false

advanced_controller:
  ros__parameters:
    control_frequency: 50.0
    position_tolerance: 0.01
    angular_tolerance: 0.01
    use_sim_time: false
```

### Using Parameters in Nodes

```python
# robot_controller/robot_controller/parameterized_controller.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class ParameterizedController(Node):
    def __init__(self):
        super().__init__('parameterized_controller')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('control_frequency', 10.0)

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.control_frequency = self.get_parameter('control_frequency').value

        # Create publisher
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Create timer based on parameter
        self.timer = self.create_timer(1.0/self.control_frequency, self.control_callback)

        self.get_logger().info(
            f'Initialized {self.robot_name} controller with max velocity {self.max_velocity} '
            f'and frequency {self.control_frequency} Hz'
        )

    def control_callback(self):
        msg = Twist()
        msg.linear.x = min(0.5, self.max_velocity)  # Respect velocity limit
        self.cmd_vel_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    controller = ParameterizedController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Best Practices for Package Development

### Code Organization
- Group related functionality in separate modules
- Use meaningful names for packages, nodes, and topics
- Follow Python naming conventions (PEP 8)

### Error Handling
- Implement proper exception handling
- Use logging for debugging and monitoring
- Gracefully handle node shutdown

### Testing
- Write unit tests for your nodes
- Use ROS 2 testing tools like `ament_copyright`, `ament_flake8`, etc.
- Test communication patterns thoroughly

### Documentation
- Document your code with docstrings
- Provide usage examples in README files
- Document all parameters and their expected values

## Launch File Best Practices

### Modular Design
- Create separate launch files for different configurations
- Use launch arguments to make launch files flexible
- Include other launch files when appropriate

### Parameter Management
- Use YAML files for complex parameter sets
- Set reasonable defaults for all parameters
- Document parameter meanings and valid ranges

### Node Management
- Set appropriate output options for debugging
- Use node namespaces to avoid naming conflicts
- Consider resource usage when launching multiple nodes

## Example: Complete Robot Control Package

Let's put everything together in a complete example that demonstrates a humanoid robot controller:

```python
# robot_controller/robot_controller/humanoid_controller.py

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class HumanoidController(Node):
    def __init__(self):
        super().__init__('humanoid_controller')

        # Declare parameters
        self.declare_parameter('robot_name', 'humanoid_robot')
        self.declare_parameter('control_frequency', 100.0)  # Hz
        self.declare_parameter('max_joint_velocity', 2.0)  # rad/s

        self.robot_name = self.get_parameter('robot_name').value
        self.control_frequency = self.get_parameter('control_frequency').value
        self.max_joint_velocity = self.get_parameter('max_joint_velocity').value

        # Create QoS profile for joint states
        qos_profile = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE
        )

        # Publishers
        self.joint_cmd_publisher = self.create_publisher(
            JointState, 'joint_commands', qos_profile
        )
        self.status_publisher = self.create_publisher(
            String, 'robot_status', 10
        )

        # Subscribers
        self.joint_state_subscriber = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            qos_profile
        )

        self.cmd_vel_subscriber = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Timer for control loop
        self.timer = self.create_timer(
            1.0/self.control_frequency,
            self.control_loop
        )

        # Internal state
        self.current_joint_states = JointState()
        self.desired_velocity = Twist()

        self.get_logger().info(
            f'Humanoid Controller initialized for {self.robot_name} '
            f'with control frequency {self.control_frequency} Hz'
        )

    def joint_state_callback(self, msg):
        self.current_joint_states = msg

    def cmd_vel_callback(self, msg):
        self.desired_velocity = msg

    def control_loop(self):
        # This is where the actual control logic would go
        # For now, we'll just echo the desired velocity as joint commands

        joint_cmd = JointState()
        joint_cmd.header.stamp = self.get_clock().now().to_msg()
        joint_cmd.name = ['left_leg_joint', 'right_leg_joint', 'left_arm_joint', 'right_arm_joint']

        # Simple mapping of velocity to joint commands
        joint_positions = [
            self.desired_velocity.linear.x * 0.1,  # Map linear velocity to leg joints
            self.desired_velocity.linear.x * 0.1,
            self.desired_velocity.angular.z * 0.05,  # Map angular velocity to arm joints
            -self.desired_velocity.angular.z * 0.05
        ]

        joint_cmd.position = joint_positions
        joint_cmd.velocity = [0.0] * len(joint_positions)  # Zero velocity for now
        joint_cmd.effort = [0.0] * len(joint_positions)   # Zero effort for now

        self.joint_cmd_publisher.publish(joint_cmd)

        # Publish status
        status_msg = String()
        status_msg.data = f'{self.robot_name} running, joints: {len(self.current_joint_states.name)}'
        self.status_publisher.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    humanoid_controller = HumanoidController()

    try:
        rclpy.spin(humanoid_controller)
    except KeyboardInterrupt:
        pass
    finally:
        humanoid_controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Running and Debugging

### Starting Nodes
To run a specific node:
```bash
ros2 run robot_controller simple_controller
```

### Using Launch Files
To run a launch file:
```bash
ros2 launch robot_controller robot_system.launch.py
```

### Monitoring the System
Use ROS 2 tools to monitor your system:
```bash
# List all nodes
ros2 node list

# List all topics
ros2 topic list

# Echo a topic
ros2 topic echo /cmd_vel geometry_msgs/msg/Twist

# Check node info
ros2 node info /simple_controller
```

## Quality Assurance for Humanoid Robotics

When developing for humanoid robots, special attention must be paid to:

### Safety
- Implement safety limits for joint positions and velocities
- Include emergency stop mechanisms
- Validate all commands before execution

### Real-time Performance
- Ensure control loops run at consistent frequencies
- Minimize computational overhead in critical paths
- Consider using real-time capable systems

### Fault Tolerance
- Implement graceful degradation when sensors fail
- Include redundancy where possible
- Log errors for post-mortem analysis

## Looking Ahead

In this chapter, we've learned how to create ROS 2 packages, implement nodes with various communication patterns, and use launch files to orchestrate complex systems. In the next chapter, we'll explore Robot Description Format (URDF), which is essential for describing the physical structure of humanoid robots.

## Citations

- ROS 2 Documentation Team. (2023). *Creating Your First ROS 2 Package*. https://docs.ros.org/
- Quigley, M., et al. (2009). *ROS: an open-source Robot Operating System*. ICRA.
- Macenski, S. (2021). *Professional Robotics: Development and Deployment*. Apress.

## Summary

This chapter covered the fundamentals of creating ROS 2 packages with Python and rclpy. We learned how to structure packages, create nodes with different communication patterns, use launch files for system orchestration, and manage parameters. These skills are essential for developing complex robotic systems like humanoid robots.

## Review Questions/Exercises

1. What is the difference between a ROS 2 package and a workspace?
2. How do you create a publisher and subscriber in the same node?
3. What are the advantages of using launch files over running nodes individually?
4. Create a package with a node that publishes joint commands based on sensor input.
5. Implement a launch file that starts multiple nodes with different parameters.

---
**Chapter Specifications:**
- **Expected Length**: 3,000-4,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using rclpy where applicable for ROS 2 modules
- **Diagrams/Illustrations**: Text-based ASCII or references to images in `/static/img/book/module-X/`
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides