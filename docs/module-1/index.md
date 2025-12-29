---
sidebar_position: 0
title: "Module 1: The Robotic Nervous System (ROS 2)"
---

# Module 1: The Robotic Nervous System (ROS 2)

Welcome to Module 1, where you'll learn the fundamentals of ROS 2 (Robot Operating System 2) as the control backbone for humanoid robots.

## Module Overview

This module covers ROS 2 Humble Hawksbill, the foundation for building robotic systems. You'll learn how to create nodes, manage communication between components, describe robot structures, and implement real-time control.

### What You'll Learn

- **Chapter 1**: Introduction to Physical AI & Robotics Foundations
- **Chapter 2**: ROS 2 Architecture (Nodes, Topics, Services, Actions, DDS, QoS)
- **Chapter 3**: Building ROS 2 Packages with rclpy
- **Chapter 4**: Robot Description Formats (URDF)
- **Chapter 5**: Real-Time Control Concepts

## Hardware Requirements

:::info Minimum Requirements
This module can run on modest hardware as it focuses on ROS 2 fundamentals without heavy simulation.
:::

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores (Intel i5 / AMD Ryzen 5) | 6+ cores (Intel i7 / AMD Ryzen 7) |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 20 GB free space | 50 GB SSD |
| **GPU** | Not required | Any (for RViz acceleration) |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### Notes

- All examples in this module target **ROS 2 Humble Hawksbill**
- GPU is optional but improves RViz visualization performance
- WSL2 on Windows is supported for development

## Software Prerequisites

Before starting this module, ensure you have:

1. **Ubuntu 22.04 LTS** (native or WSL2)
2. **ROS 2 Humble** installed ([Installation Guide](/docs/appendix/tools-setup#ros-2-humble-hawksbill-installation))
3. **Python 3.10+** with pip

```bash
# Verify ROS 2 installation
source /opt/ros/humble/setup.bash
ros2 --version
```

## Quick Links

- [Chapter 1: Introduction to Physical AI](/docs/module-1/chapter-1)
- [Troubleshooting Guide](/docs/module-1/troubleshooting)
- [Hardware Requirements (All Modules)](/docs/appendix/hardware-requirements)
- [Tools Setup Guide](/docs/appendix/tools-setup)
