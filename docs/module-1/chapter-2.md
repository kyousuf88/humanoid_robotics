# Chapter 2: ROS 2 Architecture (Nodes, Topics, Services, Actions, DDS, QoS)

## Learning Objectives
- [X] Explain the core concepts of ROS 2 architecture and their roles in robotic systems
- [X] Differentiate between nodes, topics, services, and actions and know when to use each
- [X] Understand Quality of Service (QoS) settings and their impact on communication

## Key Concepts
- [X] **Nodes**: Independent processes that perform computation in ROS 2
- [X] **Topics**: Asynchronous, many-to-many communication mechanism using publish-subscribe pattern
- [X] **Services**: Synchronous, request-response communication mechanism
- [X] **Actions**: Asynchronous communication with feedback, goals, and results
- [X] **DDS**: Data Distribution Service, the underlying communication middleware
- [X] **QoS**: Quality of Service policies that control communication behavior

## Introduction

In this chapter, we'll explore the fundamental architectural components of ROS 2 that enable distributed robotic systems to communicate and coordinate effectively. Understanding these concepts is crucial for developing complex robotic applications, particularly humanoid robots that require multiple specialized components working together in real-time.

ROS 2's architecture is built around a distributed computing model where different functionalities are encapsulated in separate processes called "nodes." These nodes communicate with each other using various communication mechanisms, each designed for specific types of interactions. The underlying Data Distribution Service (DDS) implementation ensures reliable communication with configurable Quality of Service (QoS) policies.

## Nodes: The Building Blocks of ROS 2

Nodes are the fundamental execution units in ROS 2. Each node represents an independent process that performs a specific function within the robotic system. Think of nodes as specialized workers, each with their own expertise, collaborating to achieve the robot's overall objectives.

### Node Characteristics

Nodes in ROS 2 have several important characteristics:

**Independence**: Each node runs in its own process space, which means that if one node crashes, it doesn't necessarily affect other nodes. This isolation improves the overall robustness of the system.

**Specialization**: Nodes typically perform specific functions such as sensor processing, control algorithms, or user interfaces. This specialization allows for better organization and maintainability of complex robotic systems.

**Communication**: Nodes communicate with each other through ROS 2's communication mechanisms: topics, services, and actions.

### Creating a Node

Let's look at a basic ROS 2 node structure using Python and the rclpy library:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Minimal node has been created')

def main(args=None):
    rclpy.init(args=args)
    minimal_node = MinimalNode()

    try:
        rclpy.spin(minimal_node)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This example demonstrates the basic structure of a ROS 2 node. The node is created by inheriting from `rclpy.node.Node`, and the `rclpy.spin()` function keeps the node running and processing callbacks.

## Topics: Publish-Subscribe Communication

Topics are the primary mechanism for asynchronous, many-to-many communication in ROS 2. They use a publish-subscribe pattern where nodes can publish messages to a topic and other nodes can subscribe to that topic to receive the messages.

### How Topics Work

The publish-subscribe pattern works as follows:

1. **Publisher**: A node creates a publisher that sends messages to a specific topic
2. **Subscriber**: Another node creates a subscriber that receives messages from the same topic
3. **Communication**: Messages flow from publishers to subscribers without direct connection between them

### Topic Characteristics

**Asynchronous**: Publishers and subscribers don't need to be synchronized. Publishers can send messages regardless of whether subscribers are ready to receive them.

**Many-to-many**: Multiple publishers can publish to the same topic, and multiple subscribers can listen to the same topic.

**Anonymous**: Publishers and subscribers don't need to know about each other's existence. They only need to agree on the topic name and message type.

### Topic Example

Here's an example of a simple publisher node:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()

    try:
        rclpy.spin(minimal_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

And here's a corresponding subscriber:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()

    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### When to Use Topics

Topics are ideal for:
- Sensor data streams (camera images, LiDAR scans, IMU data)
- Continuous control commands
- Status updates
- Broadcasting information to multiple recipients

## Services: Request-Response Communication

Services provide synchronous, request-response communication between nodes. Unlike topics, services establish a direct connection between a client and a server, where the client sends a request and waits for a response.

### How Services Work

1. **Service Server**: A node creates a service server that listens for requests
2. **Service Client**: Another node creates a service client that sends requests
3. **Synchronous Communication**: The client sends a request and waits for the response before continuing

### Service Example

First, the service server:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request\na: {request.a}, b: {request.b}\n')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()

    try:
        rclpy.spin(minimal_service)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

And the corresponding service client:

```python
import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main():
    rclpy.init()
    minimal_client = MinimalClient()
    response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    minimal_client.get_logger().info(f'Result of add_two_ints: {response.sum}')
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### When to Use Services

Services are appropriate for:
- Configuration requests
- One-time computations
- Synchronous operations where the caller needs to wait for results
- Simple request-response interactions

## Actions: Goal-Oriented Communication

Actions are designed for long-running tasks that provide feedback during execution. They combine the benefits of both topics and services, allowing for goal-oriented communication with continuous feedback.

### Action Components

Actions have three main components:
- **Goal**: The request sent to start the action
- **Feedback**: Continuous updates during action execution
- **Result**: The final outcome of the action

### Action Example

Here's a simple action server:

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])

            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Result: {result.sequence}')

        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()

    try:
        rclpy.spin(fibonacci_action_server)
    except KeyboardInterrupt:
        pass
    finally:
        fibonacci_action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### When to Use Actions

Actions are ideal for:
- Navigation tasks (moving to a specific location)
- Manipulation tasks (grasping an object)
- Long-running processes that need to provide feedback
- Tasks that can be canceled or preempted

## Data Distribution Service (DDS)

DDS (Data Distribution Service) is the underlying middleware that powers ROS 2's communication. It's a vendor-neutral standard that provides a publish-subscribe communication model with rich Quality of Service (QoS) controls.

### DDS Benefits

**Standardization**: DDS is an OMG (Object Management Group) standard, ensuring interoperability between different implementations.

**Performance**: DDS implementations are optimized for real-time performance and can handle high-frequency data streams.

**Scalability**: DDS can scale from small embedded systems to large distributed systems.

**Reliability**: DDS provides built-in mechanisms for data persistence, reliability, and fault tolerance.

### DDS Implementations in ROS 2

ROS 2 supports multiple DDS implementations:
- **Fast DDS**: Default implementation from eProsima
- **Cyclone DDS**: From Eclipse Foundation
- **RTI Connext DDS**: Commercial implementation
- **OpenSplice DDS**: Open-source implementation

## Quality of Service (QoS) Policies

QoS policies allow you to configure how messages are handled in terms of reliability, durability, and other characteristics. This is crucial for real-time robotic applications where timing and reliability requirements vary.

### Key QoS Policies

**Reliability**: Determines whether messages are guaranteed to be delivered.
- `RELIABLE`: All messages are guaranteed to be delivered
- `BEST_EFFORT`: Messages may be lost, but faster delivery

**Durability**: Determines how messages are handled when subscribers join late.
- `TRANSIENT_LOCAL`: Messages are stored and available to late-joining subscribers
- `VOLATILE`: Messages are not stored; late joiners don't receive old messages

**History**: Controls how many messages are stored for delivery.
- `KEEP_LAST`: Stores the most recent N messages
- `KEEP_ALL`: Stores all messages (limited by system resources)

**Deadline**: Specifies the maximum time between consecutive messages.

**Liveliness**: How the system monitors if participants are alive.

### QoS Example

Here's how to specify QoS policies when creating a publisher:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Create a QoS profile
qos_profile = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST
)

# Use the QoS profile when creating a publisher
publisher = self.create_publisher(String, 'topic', qos_profile)
```

### Selecting Appropriate QoS

For different types of data, you should select appropriate QoS policies:

- **Sensor Data**: Often `BEST_EFFORT` reliability (you can miss some frames) with `VOLATILE` durability
- **Control Commands**: Usually `RELIABLE` with `VOLATILE` durability
- **Configuration Data**: `RELIABLE` with `TRANSIENT_LOCAL` durability
- **Critical Safety Messages**: `RELIABLE` with specific deadline policies

## Architecture Patterns in Humanoid Robotics

In humanoid robotics, the ROS 2 architecture enables several important patterns:

### Sensor Integration Pattern
Multiple sensor nodes publish data to topics that can be consumed by perception, control, and monitoring nodes simultaneously.

### Control Hierarchy Pattern
High-level planning nodes send goals to action servers that implement low-level control, with feedback indicating progress.

### Behavior Arbitration Pattern
Multiple behavior nodes can publish to the same command topics, with an arbitration node selecting which commands to execute.

### State Monitoring Pattern
Nodes publish their status to monitoring topics, allowing for system-wide health assessment and logging.

## Best Practices for ROS 2 Architecture

### Naming Conventions
- Use descriptive, consistent names for topics, services, and actions
- Group related interfaces under common namespaces
- Avoid special characters in names

### Error Handling
- Implement proper exception handling in nodes
- Use appropriate QoS policies for different types of data
- Monitor node health and implement recovery strategies

### Resource Management
- Properly clean up resources when nodes are destroyed
- Use appropriate message queue sizes
- Consider memory and CPU usage when designing node structure

## Looking Ahead

Understanding ROS 2 architecture is fundamental to building complex robotic systems. In the next chapter, we'll learn how to create ROS 2 packages, implement nodes with publishers and subscribers, and use launch files for system startup. This will give you hands-on experience with the concepts covered in this chapter.

## Citations

- DDS Council. (2023). *Data Distribution Service for Real-Time Systems*. Object Management Group.
- ROS 2 Documentation Team. (2023). *ROS 2 Concepts: Nodes, Topics, Services, Actions*. https://docs.ros.org/
- Colmenares, J., et al. (2020). *ROS 2 Design: A Metamorphosis from ROS 1*. International Conference on Simulation, Modeling, and Programming for Autonomous Robots.

## Summary

In this chapter, we've explored the core architectural components of ROS 2: nodes, topics, services, and actions. We've examined how DDS provides the underlying communication infrastructure and how QoS policies allow for fine-tuning of communication behavior. These concepts form the foundation for building distributed robotic systems, particularly complex humanoid robots that require multiple specialized components working together.

## Review Questions/Exercises

1. What is the difference between topics and services in ROS 2?
2. When would you use an action instead of a service?
3. What are the main QoS policies and why are they important?
4. How does DDS contribute to ROS 2's architecture?
5. Create a simple publisher and subscriber for sensor data with appropriate QoS settings.

---
**Chapter Specifications:**
- **Expected Length**: 3,000-4,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using rclpy where applicable for ROS 2 modules
- **Diagrams/Illustrations**: Text-based ASCII or references to images in `/static/img/book/module-X/`
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides