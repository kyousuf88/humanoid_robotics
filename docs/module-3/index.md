---
sidebar_position: 0
title: "Module 3: The AI-Robot Brain (NVIDIA Isaac)"
---

# Module 3: The AI-Robot Brain (NVIDIA Isaac)

Welcome to Module 3, where you'll learn to leverage NVIDIA's Isaac ecosystem for perception, navigation, and AI-powered robotics.

## Module Overview

This module covers NVIDIA Isaac Sim and Isaac ROS for advanced robotics development. You'll learn photorealistic simulation, synthetic data generation, perception pipelines, and reinforcement learning for humanoid robots.

### What You'll Learn

- **Chapter 1**: NVIDIA Isaac Ecosystem Overview (Sim, ROS, Omniverse)
- **Chapter 2**: Photorealistic Simulation & Synthetic Data Generation
- **Chapter 3**: Isaac ROS Perception Pipelines (VSLAM, Depth, Object Detection)
- **Chapter 4**: Navigation & Path Planning (Nav2 for Biped Locomotion)
- **Chapter 5**: Reinforcement Learning & Sim-to-Real Transfer

## Hardware Requirements

:::danger RTX GPU Required
NVIDIA Isaac Sim **requires** an RTX series GPU (Turing architecture or newer). GTX GPUs are NOT supported.
:::

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 8 cores (Intel i7 / AMD Ryzen 7) | 12+ cores (Intel i9 / AMD Ryzen 9) |
| **RAM** | 32 GB | 64 GB |
| **Storage** | 100 GB free space | 200 GB NVMe SSD |
| **GPU** | RTX 2070 8GB | RTX 3080 10GB / RTX 4080 16GB |
| **VRAM** | 8 GB | 12+ GB |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### Why RTX is Required

Isaac Sim relies on:
- **RTX Ray Tracing** for photorealistic rendering
- **CUDA Cores** for physics simulation
- **Tensor Cores** for AI inference
- **OptiX** for ray-traced sensor simulation

### Notes

- **NVIDIA Driver 525.60+** is required
- **CUDA 12.x** installed with Isaac Sim
- Isaac Sim downloads ~50GB on first run
- WSL2 is NOT recommended for Isaac Sim

## Software Prerequisites

Before starting this module, ensure you have:

1. **ROS 2 Humble** (from Module 1)
2. **NVIDIA Isaac Sim 2023.1.x** ([Installation Guide](/docs/appendix/tools-setup#nvidia-isaac-sim-20231-installation))
3. **Isaac ROS packages** ([Installation Guide](/docs/appendix/tools-setup#install-isaac-ros))
4. **NVIDIA Omniverse Launcher**

```bash
# Verify NVIDIA driver (must be 525+)
nvidia-smi

# Verify CUDA
nvcc --version
# Expected: CUDA 12.x
```

## Quick Links

- [Chapter 1: NVIDIA Isaac Ecosystem](/docs/module-3/module-3-chapter-1)
- [Troubleshooting Guide](/docs/module-3/troubleshooting)
- [Hardware Requirements (All Modules)](/docs/appendix/hardware-requirements)
- [Tools Setup Guide](/docs/appendix/tools-setup)
