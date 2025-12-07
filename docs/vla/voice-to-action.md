---
id: voice-to-action
sidebar_position: 2
title: Voice-to-Action Integration
---

# Voice-to-Action

We integrate **OpenAI Whisper** for speech recognition.

Example pipeline:

```text
Microphone → Whisper → Text → LLM Planner → ROS 2 Action → Robot
