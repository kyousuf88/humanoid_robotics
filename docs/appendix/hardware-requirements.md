---
sidebar_position: 1
---

# Hardware Requirements

This appendix provides detailed hardware requirements for each module of the Physical AI & Humanoid Robotics book. Verify your system meets these specifications before starting each module.

## Overview

The hardware requirements vary significantly across modules due to the different computational demands of each technology stack:

| Module | CPU | RAM | GPU | Storage |
|--------|-----|-----|-----|---------|
| Module 1: ROS 2 | 4+ cores | 8 GB | Optional | 50 GB |
| Module 2: Digital Twin | 6+ cores | 16 GB | GTX 1060+ | 100 GB |
| Module 3: Isaac | 8+ cores | 32 GB | RTX 2070+ | 200 GB |
| Module 4: VLA | 8+ cores | 32 GB | RTX 3060 12GB+ | 100 GB |

## Module 1: ROS 2 — The Robotic Nervous System

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 4 cores (Intel i5 / AMD Ryzen 5 or equivalent) |
| **RAM** | 8 GB DDR4 |
| **Storage** | 50 GB free space (SSD recommended) |
| **GPU** | Not required (integrated graphics sufficient) |
| **OS** | Ubuntu 22.04 LTS (recommended) |
| **Network** | Internet connection for package installation |

### Recommended Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 8 cores (Intel i7 / AMD Ryzen 7 or equivalent) |
| **RAM** | 16 GB DDR4 |
| **Storage** | 100 GB SSD |
| **GPU** | NVIDIA GPU for RViz2 visualization (optional) |
| **OS** | Ubuntu 22.04 LTS |

### Software Dependencies

- ROS 2 Humble Hawksbill (LTS)
- Python 3.10+
- colcon build tools
- RViz2 (visualization)

---

## Module 2: Digital Twin — Gazebo & Unity

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 6 cores (Intel i5 / AMD Ryzen 5 or equivalent) |
| **RAM** | 16 GB DDR4 |
| **Storage** | 100 GB free space (SSD required) |
| **GPU** | NVIDIA GTX 1060 6GB / AMD RX 580 |
| **OS** | Ubuntu 22.04 LTS |
| **Display** | 1920x1080 resolution |

### Recommended Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 8+ cores (Intel i7 / AMD Ryzen 7 or equivalent) |
| **RAM** | 32 GB DDR4 |
| **Storage** | 200 GB NVMe SSD |
| **GPU** | NVIDIA RTX 3060 or better |
| **OS** | Ubuntu 22.04 LTS |

### Software Dependencies

- Gazebo Harmonic
- Unity 2022 LTS
- Unity Robotics Hub
- ROS 2 Humble Hawksbill

:::warning GPU Requirements
Gazebo and Unity both require dedicated graphics cards for acceptable performance. Integrated graphics are not supported for simulation work.
:::

---

## Module 3: AI-Robot Brain — NVIDIA Isaac

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 8 cores (Intel i7 / AMD Ryzen 7 or equivalent) |
| **RAM** | 32 GB DDR4 |
| **Storage** | 200 GB NVMe SSD |
| **GPU** | NVIDIA RTX 2070 8GB (RTX required) |
| **OS** | Ubuntu 22.04 LTS |
| **CUDA** | CUDA 12.x compatible driver |

### Recommended Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 12+ cores (Intel i9 / AMD Ryzen 9 or equivalent) |
| **RAM** | 64 GB DDR4/DDR5 |
| **Storage** | 500 GB NVMe SSD |
| **GPU** | NVIDIA RTX 3080 10GB or RTX 4080 |
| **OS** | Ubuntu 22.04 LTS |

### Software Dependencies

- NVIDIA Isaac Sim 2023.1.x
- Isaac ROS packages
- NVIDIA Omniverse Launcher
- CUDA Toolkit 12.x
- cuDNN 8.x

:::danger RTX GPU Required
Isaac Sim requires an NVIDIA RTX series GPU (Turing architecture or newer). GTX series and AMD GPUs are NOT supported.
:::

---

## Module 4: Vision-Language-Action (VLA)

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 8 cores (Intel i7 / AMD Ryzen 7 or equivalent) |
| **RAM** | 32 GB DDR4 |
| **Storage** | 100 GB NVMe SSD |
| **GPU** | NVIDIA RTX 3060 12GB (for LLM inference) |
| **OS** | Ubuntu 22.04 LTS |
| **Audio** | Microphone (for Whisper voice input) |

### Recommended Requirements

| Component | Specification |
|-----------|---------------|
| **CPU** | 16 cores (Intel i9 / AMD Ryzen 9 or equivalent) |
| **RAM** | 64 GB DDR4/DDR5 |
| **Storage** | 200 GB NVMe SSD |
| **GPU** | NVIDIA RTX 4080 16GB or RTX 4090 24GB |
| **OS** | Ubuntu 22.04 LTS |

### Software Dependencies

- OpenAI Whisper
- Llama 3 (8B or 70B model)
- PyTorch 2.x
- CUDA Toolkit 12.x
- ROS 2 Humble Hawksbill

:::tip VRAM Considerations
Local LLM inference requires significant GPU VRAM:
- Llama 3 8B: ~16GB VRAM (quantized: ~8GB)
- Llama 3 70B: ~140GB VRAM (quantized: ~40GB)

Consider using quantized models or API-based inference if GPU VRAM is limited.
:::

---

## Cloud Alternatives

If your local hardware doesn't meet the requirements, consider these cloud options:

### For Module 3 (Isaac Sim)

- **NVIDIA Omniverse Cloud**: Official cloud-hosted Isaac Sim
- **AWS EC2 G5 instances**: NVIDIA A10G GPUs
- **Google Cloud GPU VMs**: NVIDIA T4, A100 options

### For Module 4 (LLM Inference)

- **AWS SageMaker**: Managed LLM inference
- **Google Vertex AI**: Hosted Llama models
- **Together.ai**: Cost-effective LLM API
- **Ollama**: Local LLM with optimized inference

---

## Verification Commands

### Check CPU

```bash
lscpu | grep "CPU(s):"
```

### Check RAM

```bash
free -h
```

### Check GPU

```bash
nvidia-smi
```

### Check Storage

```bash
df -h /
```

### Check CUDA Version

```bash
nvcc --version
```

---

## References

- NVIDIA Isaac Sim Requirements: https://docs.omniverse.nvidia.com/isaacsim/latest/installation/requirements.html
- ROS 2 Humble Installation: https://docs.ros.org/en/humble/Installation.html
- Gazebo Harmonic Requirements: https://gazebosim.org/docs/harmonic/install
- Unity System Requirements: https://docs.unity3d.com/2022.3/Documentation/Manual/system-requirements.html
