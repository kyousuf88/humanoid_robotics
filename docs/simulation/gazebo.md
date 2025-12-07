---
id: gazebo
sidebar_position: 2
title: Gazebo Simulation
---

# Gazebo Simulation

Gazebo allows you to:

- Load URDF models  
- Simulate physics: gravity, collisions, friction  
- Test sensors: cameras, IMUs, LiDAR  

Basic workflow:

1. Install Gazebo (ROS 2 compatible)  
2. Launch a world:

```bash
ros2 launch my_robot_gazebo my_world.launch.py
