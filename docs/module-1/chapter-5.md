# Chapter 5: Real-Time Control Concepts (Controller Manager, PID, Sensor Fusion)

## Learning Objectives
- [X] Implement real-time control systems for robots using ros2_control
- [X] Understand PID control in the context of robotics and apply it to robot control
- [X] Apply sensor fusion techniques to improve robot state estimation
- [X] Use the controller manager for coordinating multiple robot controllers

## Key Concepts
- [X] **Real-time Control**: Control systems that must respond within strict timing constraints
- [X] **PID Controller**: Proportional-Integral-Derivative controller for feedback control
- [X] **ros2_control**: ROS 2 framework for robot control
- [X] **Controller Manager**: Component that manages multiple controllers
- [X] **Sensor Fusion**: Combining data from multiple sensors to improve state estimation
- [X] **State Estimation**: Determining the robot's state from sensor measurements

## Introduction

Real-time control is fundamental to humanoid robotics, where precise timing and coordination are essential for stable locomotion, dexterous manipulation, and safe human interaction. This chapter explores the core concepts of real-time control in ROS 2, focusing on the ros2_control framework, PID controllers, and sensor fusion techniques that enable humanoid robots to move and interact with their environment effectively.

Humanoid robots present unique challenges for control systems due to their complex kinematic structure, multiple degrees of freedom, and the need for stable, human-like motion. Unlike simpler robots, humanoid robots must maintain balance while moving, coordinate multiple limbs simultaneously, and respond quickly to environmental changes and disturbances.

## Understanding Real-Time Control in Robotics

Real-time control in robotics refers to control systems that must compute and execute control actions within strict timing constraints. For humanoid robots, this is particularly important because:

1. **Balance Maintenance**: Humanoid robots need continuous adjustment of their center of mass to maintain balance
2. **Safety**: Fast response to prevent falls or collisions
3. **Smooth Motion**: Consistent control updates ensure fluid, human-like movement
4. **Sensor Integration**: Real-time processing of sensor data for state estimation

### Real-Time Requirements for Humanoid Robots

Different aspects of humanoid robot control have different real-time requirements:

- **High-Frequency Control (1-10 kHz)**: Joint position/velocity control, balance feedback
- **Medium-Frequency Control (10-100 Hz)**: Walking pattern generation, whole-body control
- **Low-Frequency Control (1-10 Hz)**: High-level planning, behavior selection

### Challenges in Real-Time Robot Control

- **Computational Constraints**: Complex algorithms must execute within timing constraints
- **Communication Latency**: Network delays can affect control performance
- **Sensor Noise**: Noisy sensor data can lead to unstable control
- **Model Uncertainty**: Real robots don't perfectly match their mathematical models

## ros2_control Framework

ros2_control is the standard control framework for ROS 2, designed to provide a unified interface for robot control. It separates the control algorithm from the hardware interface, making controllers portable across different robots and simulation environments.

### Architecture of ros2_control

The ros2_control architecture consists of several key components:

1. **Hardware Interface**: Abstraction layer for physical or simulated hardware
2. **Controller Manager**: Manages multiple controllers and handles resource conflicts
3. **Controllers**: Implement specific control algorithms (position, velocity, effort)
4. **Resource Manager**: Tracks and manages hardware resources

### Hardware Interface

The hardware interface abstracts the physical hardware, providing a standard interface for controllers:

```cpp
// Example hardware interface (C++)
#include "hardware_interface/base_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"

class MyRobotHardware : public hardware_interface::BaseInterface<hardware_interface::SystemInterface>
{
public:
  hardware_interface::return_type configure(const hardware_interface::HardwareInfo & system_info) override
  {
    // Configure the hardware based on the provided information
    return hardware_interface::return_type::OK;
  }

  std::vector<hardware_interface::StateInterface> export_state_interfaces() override
  {
    // Export state interfaces for position, velocity, effort
    std::vector<hardware_interface::StateInterface> state_interfaces;
    for (auto & joint : info_.joints) {
      state_interfaces.emplace_back(hardware_interface::StateInterface(
        joint.name, hardware_interface::HW_IF_POSITION, &joint_position_[0]));
      state_interfaces.emplace_back(hardware_interface::StateInterface(
        joint.name, hardware_interface::HW_IF_VELOCITY, &joint_velocity_[0]));
      state_interfaces.emplace_back(hardware_interface::StateInterface(
        joint.name, hardware_interface::HW_IF_EFFORT, &joint_effort_[0]));
    }
    return state_interfaces;
  }

  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override
  {
    // Export command interfaces
    std::vector<hardware_interface::CommandInterface> command_interfaces;
    for (auto i = 0u; i < info_.joints.size(); i++) {
      command_interfaces.emplace_back(hardware_interface::CommandInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &joint_position_command_[i]));
    }
    return command_interfaces;
  }

  hardware_interface::return_type read() override
  {
    // Read current state from hardware
    return hardware_interface::return_type::OK;
  }

  hardware_interface::return_type write() override
  {
    // Write commands to hardware
    return hardware_interface::return_type::OK;
  }
};
```

For Python-based hardware interfaces, you would typically use ros2_control's Python interfaces or create custom solutions.

### Controller Manager

The controller manager is responsible for loading, starting, stopping, and switching controllers. It ensures that controllers don't conflict with each other when accessing hardware resources.

```yaml
# controller_manager.yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    # Joint state broadcaster
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    # Position controllers
    left_arm_controller:
      type: position_controllers/JointGroupPositionController

    right_arm_controller:
      type: position_controllers/JointGroupPositionController

    # Whole body controller
    whole_body_controller:
      type: effort_controllers/JointGroupEffortController
```

### Controller Types

ros2_control provides several types of controllers:

- **Joint Trajectory Controller**: Follows trajectories for position, velocity, or acceleration
- **Position Controllers**: Control joint positions
- **Velocity Controllers**: Control joint velocities
- **Effort Controllers**: Control joint torques/forces
- **Forward Command Controllers**: Forward commands directly to joints
- **Imu Sensor**: Reads IMU data
- **Force/Torque Sensor**: Reads force/torque sensor data

## PID Control in Robotics

PID (Proportional-Integral-Derivative) control is a fundamental control technique widely used in robotics. It adjusts control outputs based on the error between desired and actual values.

### PID Controller Theory

A PID controller calculates its output using three terms:

- **Proportional (P)**: Proportional to the current error
- **Integral (I)**: Proportional to the accumulated error over time
- **Derivative (D)**: Proportional to the rate of change of error

The control output is: `u(t) = Kp * e(t) + Ki * ∫e(t)dt + Kd * de(t)/dt`

Where:
- `u(t)` is the control output
- `e(t)` is the error (desired - actual)
- `Kp`, `Ki`, `Kd` are the controller gains

### PID Implementation for Joint Control

Here's a Python implementation of a PID controller for robot joint control:

```python
class JointPIDController:
    def __init__(self, kp, ki, kd, dt=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt

        self.previous_error = 0.0
        self.integral = 0.0

    def update(self, desired_position, actual_position):
        # Calculate error
        error = desired_position - actual_position

        # Proportional term
        p_term = self.kp * error

        # Integral term
        self.integral += error * self.dt
        i_term = self.ki * self.integral

        # Derivative term
        derivative = (error - self.previous_error) / self.dt
        d_term = self.kd * derivative

        # Store current error for next iteration
        self.previous_error = error

        # Calculate total output
        output = p_term + i_term + d_term

        return output

    def reset(self):
        self.previous_error = 0.0
        self.integral = 0.0
```

### PID Tuning for Humanoid Robots

Tuning PID parameters for humanoid robots requires special consideration:

```python
class HumanoidJointController:
    def __init__(self, joint_name):
        self.joint_name = joint_name

        # Different PID parameters for different joints
        if 'hip' in joint_name:
            # Hip joints need more aggressive control for balance
            self.pid = JointPIDController(kp=100.0, ki=10.0, kd=15.0)
        elif 'ankle' in joint_name:
            # Ankle joints need precise control for balance
            self.pid = JointPIDController(kp=80.0, ki=8.0, kd=12.0)
        elif 'shoulder' in joint_name:
            # Shoulder joints may need less aggressive control
            self.pid = JointPIDController(kp=50.0, ki=5.0, kd=8.0)
        else:
            # Default parameters
            self.pid = JointPIDController(kp=60.0, ki=6.0, kd=10.0)

        self.last_update_time = None

    def update_control(self, desired_pos, actual_pos, current_time):
        if self.last_update_time is None:
            dt = 0.01  # Default time step
        else:
            dt = (current_time - self.last_update_time).nanoseconds / 1e9

        # Update PID controller with proper time step
        command = self.pid.update(desired_pos, actual_pos)

        self.last_update_time = current_time
        return command
```

### Advanced PID Techniques

For humanoid robots, you may need more sophisticated control approaches:

```python
import numpy as np

class AdvancedJointController:
    def __init__(self, joint_name):
        self.joint_name = joint_name
        self.kp = 100.0
        self.ki = 10.0
        self.kd = 15.0

        # Feedforward terms for gravity compensation
        self.gravity_compensation = 0.0
        self.friction_compensation = 0.0

        # Adaptive parameters
        self.error_history = []
        self.max_history = 100

    def update_with_feedforward(self, desired_pos, actual_pos, desired_vel=0.0, actual_vel=0.0):
        # Standard PID
        error = desired_pos - actual_pos
        error_vel = desired_vel - actual_vel

        p_term = self.kp * error
        d_term = self.kd * error_vel  # Use velocity error instead of position derivative

        # Update integral with anti-windup
        self.integral = getattr(self, 'integral', 0.0)
        self.integral += error * 0.01  # Assuming 100Hz control rate

        # Anti-windup: limit integral term
        integral_limit = 10.0
        self.integral = np.clip(self.integral, -integral_limit, integral_limit)

        i_term = self.ki * self.integral

        # Feedforward terms
        feedforward = self.gravity_compensation + self.friction_compensation

        # Total control output
        output = p_term + i_term + d_term + feedforward

        # Store error for adaptive tuning
        self.error_history.append(abs(error))
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)

        return output

    def adaptive_tuning(self):
        """Adjust parameters based on error history"""
        if len(self.error_history) == self.max_history:
            avg_error = sum(self.error_history) / len(self.error_history)

            # Adjust parameters based on average error
            if avg_error > 0.1:  # High error - be more aggressive
                self.kp *= 1.1
                self.kd *= 1.1
            elif avg_error < 0.01:  # Low error - reduce aggressiveness
                self.kp *= 0.99
                self.kd *= 0.99
```

## Sensor Fusion for Humanoid Robots

Sensor fusion combines data from multiple sensors to improve state estimation. For humanoid robots, this is crucial for balance, navigation, and interaction.

### IMU Integration

IMUs (Inertial Measurement Units) provide acceleration and angular velocity data, which can be fused to estimate orientation:

```python
import numpy as np
from scipy.spatial.transform import Rotation as R

class IMUProcessor:
    def __init__(self):
        self.orientation = R.from_quat([0, 0, 0, 1])  # Identity quaternion
        self.linear_acceleration = np.array([0.0, 0.0, 0.0])
        self.angular_velocity = np.array([0.0, 0.0, 0.0])

        # Gravity vector in world frame
        self.gravity = np.array([0.0, 0.0, -9.81])

    def update_from_imu(self, linear_acc, angular_vel, dt):
        # Update angular velocity
        self.angular_velocity = angular_vel

        # Integrate angular velocity to get orientation change
        # Convert angular velocity to rotation vector
        rotation_vector = angular_vel * dt
        rotation = R.from_rotvec(rotation_vector)

        # Update orientation
        self.orientation = self.orientation * rotation

        # Transform linear acceleration to world frame
        world_acc = self.orientation.apply(linear_acc)

        # Remove gravity to get true acceleration
        self.linear_acceleration = world_acc - self.gravity

        return self.orientation, self.linear_acceleration
```

### Kalman Filter for State Estimation

A Kalman filter can be used to fuse IMU and encoder data for better state estimation:

```python
class KalmanFilter:
    def __init__(self, dim_x, dim_z, dim_u=0):
        """Simple Kalman filter implementation"""
        self.dim_x = dim_x  # State dimension
        self.dim_z = dim_z  # Measurement dimension
        self.dim_u = dim_u  # Control dimension (optional)

        # State vector [position, velocity]
        self.x = np.zeros(dim_x)

        # State covariance matrix
        self.P = np.eye(dim_x) * 1000.0

        # Process noise covariance
        self.Q = np.eye(dim_x) * 0.1

        # Measurement noise covariance
        self.R = np.eye(dim_z) * 1.0

        # Measurement matrix
        self.H = np.zeros((dim_z, dim_x))

        # State transition matrix
        self.F = np.eye(dim_x)

        # Control matrix (if control input is used)
        self.B = np.zeros((dim_x, dim_u)) if dim_u > 0 else None

    def predict(self, u=None):
        """Predict next state"""
        if u is not None:
            self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
        else:
            self.x = np.dot(self.F, self.x)

        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        """Update state with measurement"""
        # Calculate Kalman gain
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # Update state
        y = z - np.dot(self.H, self.x)  # Residual
        self.x = self.x + np.dot(K, y)

        # Update covariance
        I_KH = np.eye(self.dim_x) - np.dot(K, self.H)
        self.P = np.dot(I_KH, self.P)

class JointStateEstimator:
    def __init__(self, joint_name):
        # For each joint, estimate position and velocity
        self.kf = KalmanFilter(dim_x=2, dim_z=1)  # [pos, vel], measurement: pos

        # Initialize matrices for position-velocity estimation
        dt = 0.01  # 100Hz
        self.kf.F = np.array([[1.0, dt],
                             [0.0, 1.0]])  # State transition model

        self.kf.H = np.array([[1.0, 0.0]])  # Measurement model (measure position)

        self.joint_name = joint_name
        self.last_time = None

    def update(self, encoder_pos, imu_vel=None):
        """Update estimate with encoder position and optional IMU velocity"""
        current_time = time.time()

        if self.last_time is not None:
            dt = current_time - self.last_time
            # Update state transition matrix with actual dt
            self.kf.F[0, 1] = dt

        # Measurement update
        z = np.array([encoder_pos])
        self.kf.update(z)

        # Prediction for next cycle
        self.kf.predict()

        self.last_time = current_time

        # Return estimated position and velocity
        return self.kf.x[0], self.kf.x[1]  # pos, vel
```

### Extended Kalman Filter for Nonlinear Systems

For more complex state estimation, an Extended Kalman Filter (EKF) can handle nonlinear dynamics:

```python
class ExtendedKalmanFilter:
    def __init__(self, dim_x, dim_z):
        self.dim_x = dim_x
        self.dim_z = dim_z

        self.x = np.zeros(dim_x)  # State vector
        self.P = np.eye(dim_x) * 1000.0  # Covariance
        self.Q = np.eye(dim_x) * 0.1  # Process noise
        self.R = np.eye(dim_z) * 1.0  # Measurement noise

    def predict(self, f_func, F_func, dt):
        """Nonlinear prediction step"""
        # State prediction using nonlinear function f
        self.x = f_func(self.x, dt)

        # Jacobian of the state transition function
        F = F_func(self.x, dt)

        # Covariance prediction
        self.P = F @ self.P @ F.T + self.Q

    def update(self, h_func, H_func, z):
        """Nonlinear update step"""
        # Measurement prediction
        h_x = h_func(self.x)

        # Jacobian of the measurement function
        H = H_func(self.x)

        # Innovation covariance
        S = H @ self.P @ H.T + self.R

        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)

        # State update
        y = z - h_x  # Innovation
        self.x = self.x + K @ y

        # Covariance update
        I_KH = np.eye(self.dim_x) - K @ H
        self.P = I_KH @ self.P
```

## Whole-Body Control

For humanoid robots, whole-body control coordinates multiple joints simultaneously to achieve complex tasks while maintaining balance:

```python
class WholeBodyController:
    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.joint_controllers = {}

        # Initialize PID controllers for each joint
        for joint_name in robot_model.joint_names:
            self.joint_controllers[joint_name] = HumanoidJointController(joint_name)

        # Center of mass estimator
        self.com_estimator = CenterOfMassEstimator(robot_model)

        # Balance controller
        self.balance_controller = BalanceController()

    def compute_control_commands(self, desired_com_pos, current_sensor_data):
        """Compute joint commands to achieve desired center of mass position"""

        # Estimate current center of mass
        current_com_pos = self.com_estimator.estimate(
            current_sensor_data['joint_positions'],
            current_sensor_data['joint_velocities']
        )

        # Compute balance corrections
        balance_corrections = self.balance_controller.compute_balance(
            desired_com_pos, current_com_pos,
            current_sensor_data['imu_orientation']
        )

        # Generate joint commands
        joint_commands = {}
        for joint_name in self.joint_controllers:
            # Get desired position from whole-body solution
            desired_pos = self.compute_joint_desired_position(
                joint_name, balance_corrections
            )

            # Get current position from sensors
            current_pos = current_sensor_data['joint_positions'][joint_name]

            # Compute control command
            command = self.joint_controllers[joint_name].update_control(
                desired_pos, current_pos, time.time()
            )

            joint_commands[joint_name] = command

        return joint_commands

    def compute_joint_desired_position(self, joint_name, balance_corrections):
        """Compute desired joint position based on balance requirements"""
        # This would involve inverse kinematics and whole-body optimization
        # For simplicity, we'll return a basic implementation
        base_desired = 0.0  # Default position

        # Apply balance corrections based on joint role
        if 'hip' in joint_name or 'ankle' in joint_name:
            # Balance joints get larger corrections
            correction = balance_corrections.get(joint_name, 0.0) * 0.5
        else:
            correction = balance_corrections.get(joint_name, 0.0) * 0.1

        return base_desired + correction
```

## ros2_control Configuration for Humanoid Robots

Here's a complete configuration example for a humanoid robot using ros2_control:

```yaml
# robot_controllers.yaml
controller_manager:
  ros__parameters:
    update_rate: 1000  # Hz - high rate for humanoid stability

    # Available controllers
    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    # Individual joint controllers
    left_leg_controller:
      type: position_controllers/JointGroupPositionController

    right_leg_controller:
      type: position_controllers/JointGroupPositionController

    left_arm_controller:
      type: position_controllers/JointGroupPositionController

    right_arm_controller:
      type: position_controllers/JointGroupPositionController

    # Balance controller
    balance_controller:
      type: effort_controllers/JointGroupEffortController

# Joint trajectory controller configuration
joint_trajectory_controller:
  ros__parameters:
    joints:
      - left_hip_yaw
      - left_hip_roll
      - left_hip_pitch
      - left_knee
      - left_ankle_pitch
      - left_ankle_roll
      - right_hip_yaw
      - right_hip_roll
      - right_hip_pitch
      - right_knee
      - right_ankle_pitch
      - right_ankle_roll
      - left_shoulder_pitch
      - left_shoulder_roll
      - left_elbow
      - right_shoulder_pitch
      - right_shoulder_roll
      - right_elbow

    command_interfaces:
      - position

    state_interfaces:
      - position
      - velocity

# Individual controller configurations
left_leg_controller:
  ros__parameters:
    joints:
      - left_hip_yaw
      - left_hip_roll
      - left_hip_pitch
      - left_knee
      - left_ankle_pitch
      - left_ankle_roll

right_leg_controller:
  ros__parameters:
    joints:
      - right_hip_yaw
      - right_hip_roll
      - right_hip_pitch
      - right_knee
      - right_ankle_pitch
      - right_ankle_roll

left_arm_controller:
  ros__parameters:
    joints:
      - left_shoulder_pitch
      - left_shoulder_roll
      - left_elbow

right_arm_controller:
  ros__parameters:
    joints:
      - right_shoulder_pitch
      - right_shoulder_roll
      - right_elbow
```

## Launch File for Control System

Here's a launch file to start the complete control system:

```python
# launch/humanoid_control.launch.py

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    urdf_model_path = LaunchConfiguration('urdf_model')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Get URDF via xacro
    robot_description_content = Command([
        'xacro ',
        PathJoinSubstitution([FindPackageShare('humanoid_description'), 'urdf', 'humanoid.urdf.xacro'])
    ])
    robot_description = {'robot_description': robot_description_content}

    # Robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description, {'use_sim_time': use_sim_time}],
    )

    # Controller manager
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description,
                   PathJoinSubstitution(
                       [FindPackageShare('humanoid_control'), 'config', 'robot_controllers.yaml']),
                   {'use_sim_time': use_sim_time}],
        output='both',
    )

    # Joint state broadcaster
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )

    # Robot trajectory controller
    robot_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
    )

    # Delay rviz start after joint_state_publisher to avoid race conditions
    delay_rviz_after_joint_state_publisher = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=joint_state_broadcaster_spawner,
            on_start=[
                robot_controller_spawner,
            ],
        )
    )

    nodes = [
        robot_state_publisher_node,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        delay_rviz_after_joint_state_publisher
    ]

    return LaunchDescription(nodes)
```

## Safety Considerations

When implementing real-time control for humanoid robots, safety is paramount:

### Emergency Stop Systems
```python
class SafetyMonitor:
    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.emergency_stop = False
        self.safety_limits = self.define_safety_limits()

    def define_safety_limits(self):
        """Define safety limits for various robot states"""
        return {
            'max_joint_velocity': 5.0,  # rad/s
            'max_joint_torque': 100.0,  # Nm
            'max_com_height': 1.2,      # m (for bipedal robots)
            'min_com_height': 0.3,      # m
            'max_tilt_angle': 0.5,      # rad
        }

    def check_safety(self, current_state):
        """Check if current state is safe, trigger emergency stop if not"""
        # Check joint limits
        for joint_name, pos in current_state['joint_positions'].items():
            if abs(current_state['joint_velocities'][joint_name]) > self.safety_limits['max_joint_velocity']:
                self.emergency_stop = True
                return False

        # Check COM stability
        com_pos = current_state['center_of_mass']
        if com_pos[2] < self.safety_limits['min_com_height'] or com_pos[2] > self.safety_limits['max_com_height']:
            self.emergency_stop = True
            return False

        return True

    def get_emergency_stop_state(self):
        return self.emergency_stop
```

### Control Rate Monitoring
```python
import time

class ControlRateMonitor:
    def __init__(self, expected_rate):
        self.expected_rate = expected_rate
        self.expected_dt = 1.0 / expected_rate
        self.last_update = None
        self.max_jitter = 0.005  # 5ms tolerance

    def check_timing(self):
        current_time = time.time()

        if self.last_update is not None:
            actual_dt = current_time - self.last_update

            # Check if control loop is running too slowly
            if actual_dt > (self.expected_dt + self.max_jitter):
                print(f"Control loop timing violation: expected {self.expected_dt:.3f}s, got {actual_dt:.3f}s")
                return False

        self.last_update = current_time
        return True
```

## Performance Optimization

For real-time performance with humanoid robots:

### Efficient State Updates
```python
class EfficientStateEstimator:
    def __init__(self, num_joints):
        self.num_joints = num_joints
        self.joint_positions = np.zeros(num_joints)
        self.joint_velocities = np.zeros(num_joints)
        self.joint_efforts = np.zeros(num_joints)

        # Pre-allocate arrays to avoid memory allocation during control
        self.temp_array = np.zeros(num_joints)

    def update_batch(self, positions, velocities, efforts):
        """Update all joint states in a single operation"""
        np.copyto(self.joint_positions, positions)
        np.copyto(self.joint_velocities, velocities)
        np.copyto(self.joint_efforts, efforts)

    def get_joint_state(self, joint_idx):
        """Fast access to individual joint state"""
        return (self.joint_positions[joint_idx],
                self.joint_velocities[joint_idx],
                self.joint_efforts[joint_idx])
```

## Looking Ahead

This chapter has covered the essential concepts of real-time control for humanoid robots, including ros2_control, PID controllers, and sensor fusion. These concepts are crucial for creating stable, responsive humanoid robots. The next modules will build upon these control foundations to create more sophisticated behaviors and capabilities.

## Citations

- ROS 2 Control Team. (2023). *ros2_control documentation*. https://control.ros.org/
- Siciliano, B., & Khatib, O. (2016). *Springer Handbook of Robotics*. Springer.
- Slotine, J. J. E., & Li, W. (1991). *Applied Nonlinear Control*. Prentice Hall.

## Summary

In this chapter, we've explored the fundamental concepts of real-time control for humanoid robots. We've learned about the ros2_control framework, PID controllers, sensor fusion techniques, and how to implement safe and effective control systems. These concepts form the foundation for creating stable, responsive humanoid robots capable of complex behaviors.

## Review Questions/Exercises

1. What are the key differences between position, velocity, and effort control?
2. How would you tune PID parameters for a humanoid robot's ankle joint?
3. What is the role of the controller manager in ros2_control?
4. Design a sensor fusion system that combines IMU and encoder data for a humanoid robot.
5. Implement a simple whole-body controller that maintains balance while moving the arms.

---
**Chapter Specifications:**
- **Expected Length**: 3,000-4,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using rclpy where applicable for ROS 2 modules
- **Diagrams/Illustrations**: Text-based ASCII or references to images in `/static/img/book/module-X/`
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides