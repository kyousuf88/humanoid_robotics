---
sidebar_position: 0
title: "Module 2: The Digital Twin (Gazebo & Unity)"
---

# Module 2: The Digital Twin (Gazebo & Unity)

Welcome to Module 2, where you'll learn to create digital twins of humanoid robots using Gazebo for physics simulation and Unity for high-fidelity visualization.

## Module Overview

This module covers simulation technologies essential for robotics development. You'll learn to build accurate virtual representations of robots, simulate sensors, and create realistic environments for testing.

### What You'll Learn

- **Chapter 1**: Digital Twins in Physical AI & the Sim-to-Real Gap
- **Chapter 2**: Gazebo Fundamentals (SDF, URDF, Models, Plugins)
- **Chapter 3**: Sensor Simulation (LiDAR, IMUs, Depth Cameras)
- **Chapter 4**: Unity for High-Fidelity Robot Visualization
- **Chapter 5**: Environment & Scenario Building

## Hardware Requirements

:::warning GPU Required
This module requires a dedicated GPU for physics simulation and rendering.
:::

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 6 cores (Intel i5 / AMD Ryzen 5) | 8+ cores (Intel i7 / AMD Ryzen 7) |
| **RAM** | 16 GB | 32 GB |
| **Storage** | 50 GB free space | 100 GB SSD |
| **GPU** | GTX 1060 6GB / RTX 2060 | RTX 3060 12GB or better |
| **VRAM** | 6 GB | 8+ GB |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### Notes

- **Gazebo Harmonic** requires OpenGL 4.5+ support
- **Unity 2022 LTS** benefits from higher VRAM for complex scenes
- Dual monitor setup recommended for development

## Software Prerequisites

Before starting this module, ensure you have:

1. **ROS 2 Humble** (from Module 1)
2. **Gazebo Harmonic** installed ([Installation Guide](/docs/appendix/tools-setup#gazebo-harmonic-installation))
3. **Unity 2022 LTS** with Unity Robotics Hub ([Installation Guide](/docs/appendix/tools-setup#unity-2022-lts-installation))
4. **NVIDIA Drivers** 525+ (for GPU acceleration)

```bash
# Verify Gazebo installation
gz sim --version
# Expected: Gazebo Sim, version 8.x.x

# Verify GPU driver
nvidia-smi
```

## Quick Links

- [Chapter 1: Digital Twins & Sim-to-Real Gap](/docs/module-2/module-2-chapter-1)
- [Troubleshooting Guide](/docs/module-2/troubleshooting)
- [Hardware Requirements (All Modules)](/docs/appendix/hardware-requirements)
- [Tools Setup Guide](/docs/appendix/tools-setup)
