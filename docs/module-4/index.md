---
sidebar_position: 0
title: "Module 4: Vision-Language-Action (VLA)"
---

# Module 4: Vision-Language-Action (VLA)

Welcome to Module 4, where you'll learn to build AI systems that enable natural human-robot interaction through voice commands, language understanding, and intelligent task planning.

## Module Overview

This module covers Vision-Language-Action (VLA) systems that combine speech recognition (Whisper), large language models (Llama 3), and robotic action execution. You'll build systems that can understand natural language commands and execute complex tasks.

### What You'll Learn

- **Chapter 1**: Introduction to VLA Robotics
- **Chapter 2**: Voice-to-Action Pipeline (Whisper → Intent → ROS 2 Actions)
- **Chapter 3**: Cognitive Planning Using LLMs
- **Chapter 4**: Multi-Modal Perception (Vision + Language + Sensor Fusion)
- **Chapter 5**: Capstone Project: The Autonomous Humanoid

## Hardware Requirements

:::danger High-End GPU Required
Running local LLMs (Llama 3 8B) requires significant GPU VRAM. Cloud APIs are an alternative for systems with limited hardware.
:::

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 8 cores (Intel i7 / AMD Ryzen 7) | 12+ cores (Intel i9 / AMD Ryzen 9) |
| **RAM** | 32 GB | 64 GB |
| **Storage** | 100 GB free space | 200 GB NVMe SSD |
| **GPU** | RTX 3060 12GB | RTX 4080 16GB / RTX 4090 24GB |
| **VRAM** | 12 GB (for 4-bit quantized models) | 16+ GB (for better performance) |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### VRAM Requirements by Model

| Model | Full Precision | 8-bit Quantized | 4-bit Quantized |
|-------|----------------|-----------------|-----------------|
| Whisper Base | ~1 GB | ~1 GB | N/A |
| Whisper Medium | ~5 GB | ~3 GB | N/A |
| Llama 3 8B | ~16 GB | ~8 GB | ~4 GB |
| Llama 3 70B | ~140 GB | ~70 GB | ~35 GB |

### Notes

- **4-bit quantization** (via llama.cpp or bitsandbytes) reduces VRAM usage significantly
- **Whisper** can run on CPU but is much slower without GPU acceleration
- **Cloud APIs** (OpenAI, Anthropic) are alternatives if local GPU is insufficient
- Audio input requires a working microphone

## Software Prerequisites

Before starting this module, ensure you have:

1. **ROS 2 Humble** (from Module 1)
2. **Python 3.10+** with PyTorch and CUDA support
3. **OpenAI Whisper** ([Installation Guide](/docs/appendix/tools-setup#install-whisper-for-module-4))
4. **Llama.cpp or Ollama** for local LLM inference ([Installation Guide](/docs/appendix/tools-setup#install-llamacpp-for-local-llm-inference))

```bash
# Verify PyTorch CUDA support
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Verify Whisper installation
python3 -c "import whisper; print('Whisper installed')"

# Test Ollama (if using)
ollama run llama3 "Hello, world"
```

## Cloud Alternatives

If your hardware doesn't meet the minimum requirements, consider:

| Service | Use Case | Cost |
|---------|----------|------|
| **OpenAI API** | GPT-4 for task planning | Pay per token |
| **Anthropic API** | Claude for reasoning | Pay per token |
| **Google Cloud** | Whisper API | Pay per minute |
| **RunPod/Lambda** | GPU rental for local models | $0.50-2/hour |

## Quick Links

- [Chapter 1: Introduction to VLA Robotics](/docs/module-4/chapter-1)
- [Troubleshooting Guide](/docs/module-4/troubleshooting)
- [Hardware Requirements (All Modules)](/docs/appendix/hardware-requirements)
- [Tools Setup Guide](/docs/appendix/tools-setup)
