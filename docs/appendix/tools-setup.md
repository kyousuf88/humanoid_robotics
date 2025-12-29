---
sidebar_position: 2
---

# Tools Setup Guide

This guide provides installation instructions for all tools used in this book with **pinned versions** to ensure reproducibility (FR-023).

## Pinned Tool Versions

:::warning Version Compatibility
All examples in this book are tested with the specific versions listed below. Using different versions may result in compatibility issues or unexpected behavior.
:::

| Tool | Version | Support End Date |
|------|---------|------------------|
| **ROS 2** | Humble Hawksbill (LTS) | May 2027 |
| **Gazebo** | Harmonic | TBD |
| **Unity** | 2022 LTS (2022.3.x) | 2025 |
| **NVIDIA Isaac Sim** | 2023.1.x | Ongoing |
| **Python** | 3.10+ | October 2026 |
| **Ubuntu** | 22.04 LTS | April 2027 |

---

## Operating System Setup

### Ubuntu 22.04 LTS Installation

All tools in this book are designed for **Ubuntu 22.04 LTS**. This is the recommended operating system.

```bash
# Verify your Ubuntu version
lsb_release -a
```

Expected output:
```
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.x LTS
Release:        22.04
Codename:       jammy
```

### WSL2 (Windows Users)

Windows users can use WSL2 with Ubuntu 22.04:

```powershell
# Install WSL2 with Ubuntu 22.04
wsl --install -d Ubuntu-22.04
```

---

## ROS 2 Humble Hawksbill Installation

### Set Locale

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Setup Sources

```bash
# Enable Ubuntu Universe repository
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Install ROS 2 Humble

```bash
sudo apt update
sudo apt upgrade

# Desktop install (recommended - includes RViz, demos, tutorials)
sudo apt install ros-humble-desktop

# Development tools
sudo apt install ros-dev-tools
```

### Environment Setup

```bash
# Add to ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify Installation

```bash
# Check ROS 2 version
ros2 --version
# Expected: ros2 0.9.x (Humble)

# Test with talker/listener
ros2 run demo_nodes_cpp talker
# In another terminal:
ros2 run demo_nodes_cpp listener
```

---

## Gazebo Harmonic Installation

:::note Gazebo vs Gazebo Classic
This book uses **Gazebo Harmonic** (formerly Ignition Gazebo), NOT Gazebo Classic. Gazebo Classic reached end-of-life in 2025.
:::

### Install Gazebo Harmonic

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install lsb-release wget gnupg

# Add Gazebo repository
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install Gazebo Harmonic
sudo apt-get update
sudo apt-get install gz-harmonic
```

### Install ROS-Gazebo Integration

```bash
# Install ros_gz for ROS 2 Humble + Gazebo Harmonic
sudo apt install ros-humble-ros-gz
```

### Verify Installation

```bash
# Check Gazebo version
gz sim --version
# Expected: Gazebo Sim, version 8.x.x

# Launch empty world
gz sim empty.sdf
```

---

## Unity 2022 LTS Installation

### Download Unity Hub

1. Visit: https://unity.com/download
2. Download Unity Hub for Linux
3. Install the AppImage:

```bash
chmod +x UnityHub.AppImage
./UnityHub.AppImage
```

### Install Unity 2022 LTS

1. Open Unity Hub
2. Go to **Installs** → **Install Editor**
3. Select **Unity 2022.3.x LTS** (latest patch version)
4. Include modules:
   - Linux Build Support (IL2CPP)
   - Documentation

### Install Unity Robotics Hub

```bash
# Clone Unity Robotics Hub
git clone https://github.com/Unity-Technologies/Unity-Robotics-Hub.git
cd Unity-Robotics-Hub

# The package can be added to your Unity project via Package Manager
# Add from git URL: https://github.com/Unity-Technologies/ROS-TCP-Connector.git?path=/com.unity.robotics.ros-tcp-connector
```

### Verify Installation

1. Create a new Unity project
2. Open Package Manager (Window → Package Manager)
3. Add package from git URL:
   - `https://github.com/Unity-Technologies/ROS-TCP-Connector.git?path=/com.unity.robotics.ros-tcp-connector`

---

## NVIDIA Isaac Sim 2023.1 Installation

:::danger Prerequisites
- NVIDIA RTX GPU (Turing or newer)
- NVIDIA Driver 525.60 or newer
- Ubuntu 22.04 LTS
:::

### Install NVIDIA Drivers

```bash
# Add NVIDIA PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install recommended driver (usually 535+)
ubuntu-drivers devices
sudo apt install nvidia-driver-535
sudo reboot
```

### Install NVIDIA Omniverse Launcher

1. Visit: https://www.nvidia.com/en-us/omniverse/
2. Download Omniverse Launcher for Linux
3. Install:

```bash
chmod +x omniverse-launcher-linux.AppImage
./omniverse-launcher-linux.AppImage
```

### Install Isaac Sim 2023.1

1. Open Omniverse Launcher
2. Go to **Exchange** tab
3. Search for "Isaac Sim"
4. Select version **2023.1.x** and click Install

### Install Isaac ROS

```bash
# Create Isaac ROS workspace
mkdir -p ~/isaac_ros_ws/src
cd ~/isaac_ros_ws/src

# Clone Isaac ROS Common
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git

# Build
cd ~/isaac_ros_ws
colcon build --symlink-install
source install/setup.bash
```

### Verify Installation

```bash
# Launch Isaac Sim
# From Omniverse Launcher, click "Launch" on Isaac Sim

# In Isaac Sim, load a sample:
# File → Open → omniverse://localhost/NVIDIA/Assets/Isaac/2023.1/Samples/
```

---

## Python Environment Setup

### Install Python 3.10

```bash
# Python 3.10 is default on Ubuntu 22.04
python3 --version
# Expected: Python 3.10.x

# Install pip and venv
sudo apt install python3-pip python3-venv
```

### Create Virtual Environment

```bash
# Create project virtual environment
python3 -m venv ~/robotics_venv
source ~/robotics_venv/bin/activate

# Install common dependencies
pip install numpy scipy matplotlib pytorch transformers
```

### Install Whisper (for Module 4)

```bash
pip install openai-whisper
```

### Install Llama.cpp (for local LLM inference)

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Build with CUDA support
make LLAMA_CUDA=1

# Download Llama 3 model (requires Meta approval)
# Place model files in models/ directory
```

---

## Verification Checklist

Run these commands to verify your complete setup:

```bash
# ROS 2
ros2 --version

# Gazebo
gz sim --version

# Python
python3 --version

# NVIDIA Driver
nvidia-smi

# CUDA
nvcc --version
```

### Expected Versions

| Tool | Command | Expected Output |
|------|---------|-----------------|
| ROS 2 | `ros2 --version` | `ros2 0.9.x` |
| Gazebo | `gz sim --version` | `Gazebo Sim, version 8.x.x` |
| Python | `python3 --version` | `Python 3.10.x` |
| NVIDIA Driver | `nvidia-smi` | Driver 525+ |
| CUDA | `nvcc --version` | CUDA 12.x |

---

## Troubleshooting

### ROS 2 Not Found

```bash
# Ensure setup.bash is sourced
source /opt/ros/humble/setup.bash
```

### Gazebo Crashes on Launch

```bash
# Check GPU driver
nvidia-smi

# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
gz sim empty.sdf
```

### Isaac Sim Won't Start

1. Verify RTX GPU is detected
2. Check NVIDIA driver version (525+)
3. Review Omniverse logs: `~/.nvidia-omniverse/logs/`

---

## References

- ROS 2 Humble Installation: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
- Gazebo Harmonic Installation: https://gazebosim.org/docs/harmonic/install_ubuntu
- Unity 2022 LTS: https://unity.com/releases/lts
- NVIDIA Isaac Sim: https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html
