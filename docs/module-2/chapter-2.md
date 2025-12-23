---
id: module-2-chapter-2
sidebar_position: 2
title: "Chapter 2 - Gazebo Fundamentals (SDF, URDF, Models, Plugins)"
---

# Chapter 2: Gazebo Fundamentals (SDF, URDF, Models, Plugins)

## Learning Objectives
- [X] Understand Gazebo's architecture and core components for robotics simulation
- [X] Create and modify robot models using SDF format with accurate physical properties
- [X] Implement Gazebo plugins for sensors and actuators in humanoid robot simulation
- [X] Integrate Gazebo with ROS 2 for comprehensive simulation workflows

## Key Concepts
- [X] **SDF**: Simulation Description Format, Gazebo's native XML-based robot description language
- [X] **Gazebo Plugins**: Extensions that provide functionality for sensors, actuators, and controllers
- [X] **Physics Engine**: The underlying system that calculates forces, collisions, and motion
- [X] **Model Database**: Repository of pre-built simulation models and environments
- [X] **ROS Integration**: Connecting Gazebo simulation with ROS 2 for control and perception

## Introduction

Gazebo is a powerful, open-source robotics simulator that provides accurate physics simulation, high-quality graphics, and convenient programmatic interfaces. For humanoid robotics, Gazebo serves as a critical tool for testing control algorithms, validating sensor systems, and training AI models before deployment on physical robots.

This chapter explores the fundamentals of Gazebo simulation, focusing on the Simulation Description Format (SDF), the plugin system, and integration with ROS 2. We'll cover how to create accurate humanoid robot models, implement sensor and actuator plugins, and establish robust simulation workflows that bridge the gap between virtual and real-world robotics.

Gazebo's modular architecture makes it particularly suitable for humanoid robotics simulation. The physics engine accurately models complex multi-body dynamics required for balance and locomotion, while the plugin system allows for sophisticated sensor simulation and controller integration.

## Gazebo Architecture and Components

### Core Architecture

Gazebo's architecture consists of several key components working together:

**Server (gzserver)**: The core simulation engine that handles physics calculations, sensor simulation, and plugin execution. It runs the simulation loop and maintains the state of the virtual world.

**Client (gzclient)**: The graphical user interface that provides visualization of the simulation. It connects to the server and displays the 3D environment.

**Transport Layer**: Handles communication between server and client, as well as between plugins and the main simulation engine.

**Physics Engine**: The underlying system that calculates forces, collisions, and motion. Gazebo supports multiple physics engines including ODE, Bullet, and DART.

**Sensor System**: Simulates various sensor types including cameras, LiDAR, IMUs, and force/torque sensors.

### Gazebo Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Gazebo Simulation                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │
│  │   Physics   │    │   Sensor    │    │   Transport     │ │
│  │   Engine    │    │   System    │    │   Layer       │ │
│  │ (ODE/Bullet │◄──►│ (Cameras,   │◄──►│ (Pub/Sub,      │ │
│  │  /DART)     │    │  LiDAR,     │    │  Services)     │ │
│  │             │    │  IMUs)      │    │                │ │
│  └─────────────┘    └─────────────┘    └─────────────────┘ │
│           ▲                   ▲                   ▲        │
│           │                   │                   │        │
│  ┌────────▼───────────────────▼───────────────────▼────────┐│
│  │                    Gazebo Server                       ││
│  │  ┌─────────────────┐    ┌─────────────────────────────┐││
│  │  │ World Manager   │    │ Plugin Manager              │││
│  │  │ (Models,       │    │ (Sensor, Controller,        │││
│  │  │  Environments)  │    │  World plugins)            │││
│  │  └─────────────────┘    └─────────────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                              ▲                             │
├──────────────────────────────┼─────────────────────────────┤
│                              │                             │
│                    ┌─────────▼─────────┐                   │
│                    │  Gazebo Client    │                   │
│                    │   (gzclient)      │                   │
│                    │   Visualization   │                   │
│                    └───────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

### Installation and Setup

To install Gazebo for ROS 2 Humble:

```bash
# Install Gazebo Garden (recommended for ROS 2 Humble)
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins

# Or install the full desktop version
sudo apt install ros-humble-gazebo-dev ros-humble-gazebo-plugins ros-humble-gazebo-ros
```

Verify the installation:

```bash
# Launch Gazebo GUI
gz sim

# Or launch without GUI for faster simulation
gz sim -s
```

## Simulation Description Format (SDF)

### SDF vs URDF

While URDF (Unified Robot Description Format) is the standard for ROS, Gazebo uses SDF (Simulation Description Format) as its native format. However, Gazebo can work with URDF through the liburdf library, making it flexible for different workflows.

**SDF Advantages**:
- Native Gazebo format with full feature support
- More expressive for simulation-specific properties
- Better support for complex environments and multi-robot scenarios

**URDF Advantages**:
- Standard ROS format with extensive tooling
- Seamless integration with ROS ecosystem
- Extensive community models available

### Basic SDF Structure

Here's a minimal SDF file for a simple robot:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_robot">
    <!-- Base link -->
    <link name="chassis">
      <pose>0 0 0.1 0 0 0</pose>
      <inertial>
        <mass>5.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.1</iyy>
          <iyz>0.0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>

      <visual name="chassis_visual">
        <geometry>
          <box>
            <size>0.5 0.3 0.2</size>
          </box>
        </geometry>
        <material>
          <ambient>0.8 0.8 0.8 1</ambient>
          <diffuse>0.8 0.8 0.8 1</diffuse>
        </material>
      </visual>

      <collision name="chassis_collision">
        <geometry>
          <box>
            <size>0.5 0.3 0.2</size>
          </box>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
```

### Advanced SDF Features

For humanoid robots, SDF supports more complex features:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="humanoid_robot">
    <!-- Model properties -->
    <static>false</static>
    <self_collide>false</self_collide>
    <enable_wind>false</enable_wind>

    <!-- Base link - pelvis -->
    <link name="base_link">
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.5</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.6</iyy>
          <iyz>0.0</iyz>
          <izz>0.3</izz>
        </inertia>
      </inertial>

      <visual name="base_visual">
        <geometry>
          <box>
            <size>0.3 0.2 0.4</size>
          </box>
        </geometry>
        <material>
          <ambient>0.7 0.7 0.7 1</ambient>
          <diffuse>0.7 0.7 0.7 1</diffuse>
        </material>
      </visual>

      <collision name="base_collision">
        <geometry>
          <box>
            <size>0.3 0.2 0.4</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Head link -->
    <link name="head">
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.004</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.004</iyy>
          <iyz>0.0</iyz>
          <izz>0.004</izz>
        </inertia>
      </inertial>

      <visual name="head_visual">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
        <material>
          <ambient>0.8 0.6 0.4 1</ambient>
          <diffuse>0.8 0.6 0.4 1</diffuse>
        </material>
      </visual>

      <collision name="head_collision">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
      </collision>
    </link>

    <!-- Joint connecting base to head -->
    <joint name="neck_joint" type="revolute">
      <parent>base_link</parent>
      <child>head</child>
      <pose>0 0 0.3 0 0 0</pose>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
          <effort>10</effort>
          <velocity>2</velocity>
        </limit>
      </axis>
    </joint>

    <!-- Sensor: IMU -->
    <link name="imu_link">
      <inertial>
        <mass>0.01</mass>
        <inertia>
          <ixx>0.000001</ixx>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyy>0.000001</iyy>
          <iyz>0</iyz>
          <izz>0.000001</izz>
        </inertia>
      </inertial>
    </link>

    <joint name="imu_joint" type="fixed">
      <parent>base_link</parent>
      <child>imu_link</child>
      <pose>0.1 0 0.1 0 0 0</pose>
    </joint>

    <!-- IMU sensor plugin -->
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <pose>0.1 0 0.1 0 0 0</pose>
      <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>~/out:=imu/data</remapping>
        </ros>
        <initial_orientation_as_reference>false</initial_orientation_as_reference>
        <topic>~/out</topic>
      </plugin>
    </sensor>
  </model>
</sdf>
```

## Working with URDF in Gazebo

While SDF is native to Gazebo, you can use URDF with Gazebo through the robot_state_publisher and gazebo_ros_pkgs. Here's how to prepare a URDF for Gazebo:

### URDF with Gazebo Extensions

```xml
<?xml version="1.0"?>
<robot name="humanoid_with_gazebo_extensions" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include common properties -->
  <xacro:property name="M_PI" value="3.1415926535897931" />

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.6" iyz="0.0" izz="0.3"/>
    </inertial>
  </link>

  <!-- Gazebo-specific extensions -->
  <gazebo reference="base_link">
    <material>Gazebo/Grey</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
    <self_collide>false</self_collide>
    <gravity>true</gravity>
    <max_contacts>10</max_contacts>
  </gazebo>

  <!-- IMU sensor -->
  <link name="imu_link">
    <inertial>
      <mass value="0.01"/>
      <inertia ixx="0.000001" ixy="0" ixz="0" iyy="0.000001" iyz="0" izz="0.000001"/>
    </inertial>
  </link>

  <joint name="imu_joint" type="fixed">
    <parent link="base_link"/>
    <child link="imu_link"/>
    <origin xyz="0.1 0 0.1"/>
  </joint>

  <!-- Gazebo plugin for IMU -->
  <gazebo reference="imu_link">
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <visualize>false</visualize>
      <plugin name="gazebo_ros_imu" filename="libgazebo_ros_imu.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>imu/data:=/imu/data_raw</remapping>
        </ros>
        <initial_orientation_as_reference>false</initial_orientation_as_reference>
        <topic>~/out</topic>
      </plugin>
    </sensor>
  </gazebo>

  <!-- Camera sensor -->
  <link name="camera_link">
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </collision>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 0.05" rpy="0 0 0"/>
  </joint>

  <!-- Gazebo plugin for camera -->
  <gazebo reference="camera_link">
    <sensor type="camera" name="camera_sensor">
      <update_rate>30</update_rate>
      <camera name="head_camera">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>100</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>~/image_raw:=/camera/image_raw</remapping>
          <remapping>~/camera_info:=/camera/camera_info</remapping>
        </ros>
      </plugin>
    </sensor>
  </gazebo>

  <!-- ROS Control interface -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/humanoid</robotNamespace>
      <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
    </plugin>
  </gazebo>

</robot>
```

## Gazebo Plugins for Humanoid Robotics

### Plugin Architecture

Gazebo plugins extend the simulator's functionality. For humanoid robots, key plugins include:

- **Sensor plugins**: IMU, camera, LiDAR, force/torque sensors
- **Controller plugins**: Joint controllers, ros_control interface
- **Model plugins**: Custom behaviors, AI training environments
- **World plugins**: Custom physics, environment effects

### Common Sensor Plugins

#### IMU Plugin
```xml
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate>
  <plugin name="gazebo_ros_imu" filename="libgazebo_ros_imu.so">
    <ros>
      <namespace>/robot</namespace>
      <remapping>~/out:=imu/data</remapping>
    </ros>
    <initial_orientation_as_reference>false</initial_orientation_as_reference>
    <topic>~/out</topic>
  </plugin>
</sensor>
```

#### Complete Humanoid Robot URDF with SDF Integration
```xml
<?xml version="1.0"?>
<robot name="simple_humanoid" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Constants -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="mass_pelvis" value="10.0" />
  <xacro:property name="mass_head" value="2.0" />
  <xacro:property name="mass_arm" value="1.5" />
  <xacro:property name="mass_leg" value="3.0" />

  <!-- Base/Pelvis Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.25 0.4" />
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.25 0.4" />
      </geometry>
    </collision>
    <inertial>
      <mass value="${mass_pelvis}"/>
      <inertia ixx="0.15" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.18"/>
    </inertial>
  </link>

  <!-- Head Link -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.12" />
      </geometry>
      <material name="skin_color">
        <color rgba="0.8 0.6 0.4 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.12" />
      </geometry>
    </collision>
    <inertial>
      <mass value="${mass_head}"/>
      <inertia ixx="0.006" ixy="0.0" ixz="0.0" iyy="0.006" iyz="0.0" izz="0.006"/>
    </inertial>
  </link>

  <joint name="neck_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0.0 0.0 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/3}" upper="${M_PI/3}" effort="100" velocity="1.0"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <capsule length="0.3" radius="0.05"/>
      </geometry>
      <material name="arm_color">
        <color rgba="0.5 0.5 0.7 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="${mass_arm}"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>

  <joint name="left_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.175 0.125 0.1" rpy="0 0 ${M_PI/2}"/>
    <axis xyz="1 0 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="50" velocity="2.0"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <geometry>
        <capsule length="0.25" radius="0.04"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.25" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.006" ixy="0.0" ixz="0.0" iyy="0.006" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0.0 0.0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="30" velocity="2.0"/>
  </joint>

  <!-- Right Arm (mirror of left) -->
  <link name="right_upper_arm">
    <visual>
      <geometry>
        <capsule length="0.3" radius="0.05"/>
      </geometry>
      <material name="arm_color"/>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="${mass_arm}"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>

  <joint name="right_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_arm"/>
    <origin xyz="0.175 -0.125 0.1" rpy="0 0 ${-M_PI/2}"/>
    <axis xyz="1 0 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="50" velocity="2.0"/>
  </joint>

  <link name="right_lower_arm">
    <visual>
      <geometry>
        <capsule length="0.25" radius="0.04"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.25" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.006" ixy="0.0" ixz="0.0" iyy="0.006" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <joint name="right_elbow_joint" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_lower_arm"/>
    <origin xyz="0.0 0.0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="30" velocity="2.0"/>
  </joint>

  <!-- Left Leg -->
  <link name="left_thigh">
    <visual>
      <geometry>
        <capsule length="0.4" radius="0.06"/>
      </geometry>
      <material name="leg_color">
        <color rgba="0.4 0.4 0.6 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.4" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="${mass_leg}"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.008"/>
    </inertial>
  </link>

  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_thigh"/>
    <origin xyz="-0.05 0.08 -0.2" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="1.5"/>
  </joint>

  <link name="left_shin">
    <visual>
      <geometry>
        <capsule length="0.4" radius="0.05"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.4" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.5"/>
      <inertia ixx="0.015" ixy="0.0" ixz="0.0" iyy="0.015" iyz="0.0" izz="0.006"/>
    </inertial>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_thigh"/>
    <child link="left_shin"/>
    <origin xyz="0.0 0.0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100" velocity="1.5"/>
  </joint>

  <link name="left_foot">
    <visual>
      <geometry>
        <box size="0.18 0.1 0.06"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.18 0.1 0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.003" iyz="0.0" izz="0.003"/>
    </inertial>
  </link>

  <joint name="left_ankle_joint" type="revolute">
    <parent link="left_shin"/>
    <child link="left_foot"/>
    <origin xyz="0.0 0.0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="${-M_PI/6}" upper="${M_PI/6}" effort="50" velocity="1.0"/>
  </joint>

  <!-- Right Leg (mirror of left) -->
  <link name="right_thigh">
    <visual>
      <geometry>
        <capsule length="0.4" radius="0.06"/>
      </geometry>
      <material name="leg_color"/>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.4" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="${mass_leg}"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.008"/>
    </inertial>
  </link>

  <joint name="right_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_thigh"/>
    <origin xyz="-0.05 -0.08 -0.2" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="1.5"/>
  </joint>

  <link name="right_shin">
    <visual>
      <geometry>
        <capsule length="0.4" radius="0.05"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <capsule length="0.4" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.5"/>
      <inertia ixx="0.015" ixy="0.0" ixz="0.0" iyy="0.015" iyz="0.0" izz="0.006"/>
    </inertial>
  </link>

  <joint name="right_knee_joint" type="revolute">
    <parent link="right_thigh"/>
    <child link="right_shin"/>
    <origin xyz="0.0 0.0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100" velocity="1.5"/>
  </joint>

  <link name="right_foot">
    <visual>
      <geometry>
        <box size="0.18 0.1 0.06"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.18 0.1 0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.003" iyz="0.0" izz="0.003"/>
    </inertial>
  </link>

  <joint name="right_ankle_joint" type="revolute">
    <parent link="right_shin"/>
    <child link="right_foot"/>
    <origin xyz="0.0 0.0 -0.4" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="${-M_PI/6}" upper="${M_PI/6}" effort="50" velocity="1.0"/>
  </joint>

  <!-- Gazebo-specific extensions -->
  <gazebo reference="base_link">
    <material>Gazebo/Grey</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
    <self_collide>false</self_collide>
    <gravity>true</gravity>
    <max_contacts>10</max_contacts>
  </gazebo>

  <gazebo reference="head">
    <material>Gazebo/Purple</material>
  </gazebo>

  <gazebo reference="left_upper_arm">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="right_upper_arm">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="left_thigh">
    <material>Gazebo/DarkGrey</material>
  </gazebo>

  <gazebo reference="right_thigh">
    <material>Gazebo/DarkGrey</material>
  </gazebo>

  <!-- IMU sensor on head -->
  <sensor name="imu_sensor" type="imu">
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <parent link="head"/>
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <plugin name="gazebo_ros_imu" filename="libgazebo_ros_imu.so">
      <ros>
        <namespace>/humanoid</namespace>
        <remapping>~/out:=imu/data</remapping>
      </ros>
      <initial_orientation_as_reference>false</initial_orientation_as_reference>
      <topic>~/out</topic>
    </plugin>
  </sensor>

  <!-- Camera sensor on head -->
  <link name="camera_link">
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </collision>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 0" rpy="0 0 0"/>
  </joint>

  <sensor type="camera" name="camera_sensor">
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <parent link="camera_link"/>
    <update_rate>30</update_rate>
    <camera name="head_camera">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>/humanoid</namespace>
        <remapping>~/image_raw:=/camera/image_raw</remapping>
        <remapping>~/camera_info:=/camera/camera_info</remapping>
      </ros>
    </plugin>
  </sensor>

  <!-- ROS Control interface -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/humanoid</robotNamespace>
      <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
    </plugin>
  </gazebo>

</robot>
```

#### Camera Plugin
```xml
<sensor type="camera" name="camera_sensor">
  <update_rate>30</update_rate>
  <camera name="narrow_stereo_camera">
    <horizontal_fov>1.3962634</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>100</far>
    </clip>
  </camera>
  <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
    <ros>
      <namespace>/robot</namespace>
      <remapping>~/image_raw:=/camera/image_raw</remapping>
      <remapping>~/camera_info:=/camera/camera_info</remapping>
    </ros>
  </plugin>
</sensor>
```

#### LiDAR Plugin
```xml
<sensor type="ray" name="laser_scanner">
  <pose>0.1 0 0.1 0 0 0</pose>
  <visualize>false</visualize>
  <update_rate>10</update_rate>
  <ray>
    <scan>
      <horizontal>
        <samples>720</samples>
        <resolution>1</resolution>
        <min_angle>-1.570796</min_angle>
        <max_angle>1.570796</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>30.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <plugin name="laser_controller" filename="libgazebo_ros_ray_sensor.so">
    <ros>
      <namespace>/robot</namespace>
      <remapping>~/out:=scan</remapping>
    </ros>
    <output_type>sensor_msgs/LaserScan</output_type>
    <topic_name>~/out</topic_name>
  </plugin>
</sensor>
```

### Controller Plugins

#### ros_control Integration
```xml
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/humanoid</robotNamespace>
    <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
    <controlPeriod>0.001</controlPeriod> <!-- 1kHz control -->
  </plugin>
</gazebo>
```

#### Custom Controller Plugin (C++)
```cpp
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Pose3.hh>

namespace gazebo
{
  class HumanoidController : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      // Store the model pointer for convenience
      this->model = _parent;

      // Listen to the update event. This event is broadcast every
      // simulation iteration.
      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&HumanoidController::OnUpdate, this));
    }

    // Called by the world update start event
    public: void OnUpdate()
    {
      // Apply forces to maintain balance
      // This is a simplified example - real balance control is more complex
      auto base_link = this->model->GetLink("base_link");
      ignition::math::Vector3d force(0, 0, 98.1); // Compensate for gravity
      base_link->AddForce(force);
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(HumanoidController)
}
```

## Physics Engine Configuration

### Selecting Physics Engines

Gazebo supports multiple physics engines, each with different characteristics:

**ODE (Open Dynamics Engine)**: Default for older Gazebo versions, good general-purpose physics, good for humanoid balance simulation.

**Bullet**: Good for complex contact scenarios, widely used in game engines.

**DART (Dynamic Animation and Robotics Toolkit)**: Advanced contact handling, good for complex humanoid interactions.

To specify the physics engine in a world file:

```xml
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Physics engine configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Or use DART for more advanced physics -->
    <physics type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Models and environments go here -->
  </world>
</sdf>
```

### Physics Parameters for Humanoid Simulation

For humanoid robots, specific physics parameters are crucial:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>  <!-- 1ms time step for stability -->
  <real_time_factor>1.0</real_time_factor>  <!-- Real-time simulation -->
  <real_time_update_rate>1000</real_time_update_rate>  <!-- 1kHz updates -->
  <gravity>0 0 -9.8</gravity>

  <!-- ODE-specific parameters -->
  <ode>
    <solver>
      <type>quick</type>  <!-- Fast solver for real-time simulation -->
      <iters>1000</iters>  <!-- More iterations for stability -->
      <sor>1.3</sor>      <!-- Successive over-relaxation parameter -->
    </solver>
    <constraints>
      <cfm>0.000001</cfm>  <!-- Constraint force mixing -->
      <erp>0.2</erp>      <!-- Error reduction parameter -->
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## Model Database and Asset Management

### Using Gazebo Model Database

Gazebo provides a model database with pre-built robots and environments:

```bash
# Set GAZEBO_MODEL_PATH to include custom models
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/models

# Or add to your .bashrc
echo 'export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/models' >> ~/.bashrc
```

### Creating Custom Models

Organize your humanoid robot models:

```
~/models/
├── humanoid_robot/
│   ├── model.config
│   └── model.sdf
├── simple_humanoid/
│   ├── model.config
│   └── model.sdf
└── environments/
    ├── office/
    │   ├── model.config
    │   └── model.sdf
    └── outdoor/
        ├── model.config
        └── model.sdf
```

Example `model.config`:
```xml
<?xml version="1.0"?>
<model>
  <name>humanoid_robot</name>
  <version>1.0</version>
  <sdf version="1.7">model.sdf</sdf>

  <author>
    <name>Your Name</name>
    <email>your.email@example.com</email>
  </author>

  <description>
    A humanoid robot model for simulation.
  </description>
</model>
```

## ROS 2 Integration

### Launching Gazebo with ROS 2

Create a launch file to start Gazebo with ROS 2 integration:

```python
# launch/gazebo_humanoid.launch.py

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([
                FindPackageShare('humanoid_description'),
                'worlds',
                world
            ]),
            'use_sim_time': use_sim_time,
        }.items()
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': open(PathJoinSubstitution([
                FindPackageShare('humanoid_description'),
                'urdf',
                'humanoid.urdf.xacro'
            ]).perform({})).read()
        }]
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'humanoid_robot',
            '-x', '0', '-y', '0', '-z', '1.0'  # Spawn 1m above ground
        ],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'world',
            default_value='empty.sdf',
            description='Choose one of the world files from `/humanoid_description/worlds`'
        ),
        gazebo,
        robot_state_publisher,
        spawn_entity
    ])
```

### Control Interface

Connect your ROS 2 controllers to Gazebo:

```yaml
# config/humanoid_controllers.yaml
controller_manager:
  ros__parameters:
    update_rate: 1000  # Hz
    use_sim_time: true

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    left_leg_controller:
      type: position_controllers/JointGroupPositionController

    right_leg_controller:
      type: position_controllers/JointGroupPositionController

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
```

## Converting Between URDF and SDF

### URDF to SDF Conversion

While Gazebo natively uses SDF, it can work with URDF files through the liburdf library. However, for more complex scenarios, you may need to explicitly convert URDF to SDF:

```bash
# Convert URDF to SDF using gz sdf tool
gz sdf -p /path/to/robot.urdf > robot.sdf

# Or convert to a specific SDF version
gz sdf -p -v 1.7 /path/to/robot.urdf > robot.sdf
```

### Complete SDF Conversion Example

Here's how the previous URDF example would look when converted to SDF format:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_humanoid">
    <!-- Links -->
    <link name="base_link">
      <pose>0 0 0 0 0 0</pose>
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.15</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.2</iyy>
          <iyz>0.0</iyz>
          <izz>0.18</izz>
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.3 0.25 0.4</size>
          </box>
        </geometry>
        <material>
          <ambient>0.7 0.7 0.7 1</ambient>
          <diffuse>0.7 0.7 0.7 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.3 0.25 0.4</size>
          </box>
        </geometry>
      </collision>
    </link>

    <link name="head">
      <pose>0 0 0.3 0 0 0</pose>
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.006</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.006</iyy>
          <iyz>0.0</iyz>
          <izz>0.006</izz>
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <sphere>
            <radius>0.12</radius>
          </sphere>
        </geometry>
        <material>
          <ambient>0.8 0.6 0.4 1</ambient>
          <diffuse>0.8 0.6 0.4 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <sphere>
            <radius>0.12</radius>
          </sphere>
        </geometry>
      </collision>
    </link>

    <!-- Additional links would continue in the same pattern -->

    <!-- Joints -->
    <joint name="neck_joint" type="revolute">
      <parent>base_link</parent>
      <child>head</child>
      <pose>0 0 0.3 0 0 0</pose>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.0472</lower> <!-- -π/3 -->
          <upper>1.0472</upper>  <!-- π/3 -->
          <effort>100</effort>
          <velocity>1.0</velocity>
        </limit>
      </axis>
    </joint>

    <!-- Additional joints would continue in the same pattern -->

    <!-- Sensors -->
    <sensor name="imu_sensor" type="imu">
      <pose>0 0 0.05 0 0 0</pose>
      <plugin name="gazebo_ros_imu" filename="libgazebo_ros_imu.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>~/out:=imu/data</remapping>
        </ros>
        <initial_orientation_as_reference>false</initial_orientation_as_reference>
        <topic>~/out</topic>
      </plugin>
    </sensor>

    <!-- Camera sensor -->
    <sensor name="camera_sensor" type="camera">
      <pose>0.05 0 0 0 0 0</pose>
      <camera name="head_camera">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>100</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>~/image_raw:=/camera/image_raw</remapping>
          <remapping>~/camera_info:=/camera/camera_info</remapping>
        </ros>
      </plugin>
    </sensor>

    <!-- Gazebo plugins -->
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/humanoid</robotNamespace>
      <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
    </plugin>
  </model>
</sdf>
```

### Conversion Tools and Utilities

Several tools can help with URDF/SDF conversion:

```bash
# Using xacro to preprocess URDF files before conversion
xacro robot.xacro > robot.urdf

# Using check_urdf to validate the URDF before conversion
check_urdf robot.urdf

# Using gazebo to preview the model
gz sim -f robot.sdf
```

## Best Practices for Humanoid Simulation

### Model Accuracy

For effective humanoid simulation:

1. **Accurate Inertial Properties**: Use CAD tools to calculate precise mass, center of mass, and inertia tensors
2. **Realistic Joint Limits**: Set joint limits that match physical hardware
3. **Proper Meshes**: Use appropriate visual and collision meshes
4. **Sensor Placement**: Position sensors as they are on the real robot

### Performance Optimization

1. **Simplified Collision Meshes**: Use simpler meshes for collision detection than for visualization
2. **Appropriate Update Rates**: Balance accuracy with performance
3. **Efficient Controllers**: Optimize control algorithms for real-time performance
4. **Selective Visualization**: Disable visualization when not needed for faster simulation

### Validation Techniques

1. **Parameter Identification**: Measure real robot parameters and update simulation
2. **Behavior Comparison**: Compare real and simulated robot behaviors
3. **Sensor Validation**: Verify that simulated sensors produce realistic data
4. **Control Validation**: Test that controllers work in both simulation and reality

## Troubleshooting Common Issues

### Physics Instability
- **Symptoms**: Robot shaking, exploding joints, unrealistic movements
- **Solutions**: Reduce time step, adjust ERP/CFM parameters, check inertial properties

### Sensor Noise
- **Symptoms**: Clean simulation data that doesn't match real sensors
- **Solutions**: Add realistic noise models, adjust sensor parameters

### Control Issues
- **Symptoms**: Controllers that work in simulation but not on real robot
- **Solutions**: Add actuator dynamics, adjust control rates, implement system identification

## Looking Ahead

This chapter covered the fundamentals of Gazebo simulation for humanoid robots, including SDF format, plugins, and ROS 2 integration. The next chapter will focus on sensor simulation, covering LiDAR, IMUs, cameras, and other sensors essential for humanoid robot perception.

## Citations

- Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. IEEE/RSJ International Conference on Intelligent Robots and Systems.
- Gazebo Team. (2023). Gazebo Documentation. http://gazebosim.org/
- ROS 2 Control Team. (2023). ros2_control integration with Gazebo. https://control.ros.org/

## Summary

In this chapter, we've explored the fundamentals of Gazebo simulation for humanoid robots. We covered SDF format, Gazebo plugins, physics engine configuration, and ROS 2 integration. These concepts are essential for creating accurate and useful simulation environments for humanoid robot development.

## Review Questions/Exercises

1. What are the key differences between SDF and URDF formats?
2. How do you integrate a custom sensor plugin with ROS 2?
3. What physics parameters are most important for humanoid balance simulation?
4. Create a complete SDF model for a simple humanoid robot with at least 6 degrees of freedom.
5. Design a launch file that starts Gazebo with your humanoid robot model and ROS 2 control interface.

---
**Chapter Specifications:**
- **Expected Length**: 3,000-4,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using rclpy where applicable for ROS 2 modules
- **Diagrams/Illustrations**: Text-based ASCII or references to images in `/static/img/book/module-X/`
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides