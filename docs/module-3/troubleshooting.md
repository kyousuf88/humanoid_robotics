---
sidebar_position: 99
---

# Troubleshooting: Module 3 — AI-Robot Brain (NVIDIA Isaac)

This guide covers common issues encountered when working with NVIDIA Isaac Sim 2023.1 and Isaac ROS.

## Quick Diagnosis

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| Isaac Sim won't launch | GPU not supported | [launch-failures](#launch-failures) |
| "CUDA out of memory" | Insufficient VRAM | [cuda-memory](#cuda-memory) |
| Isaac ROS nodes crash | Version mismatch | [isaac-ros-crashes](#isaac-ros-crashes) |
| Synthetic data incorrect | Replicator config error | [synthetic-data](#synthetic-data) |
| Nav2 not navigating | Costmap issues | [nav2-issues](#nav2-issues) |

---

## Isaac Sim Issues

### Isaac Sim Launch Failures {#launch-failures}

**Symptoms**:
- Isaac Sim window doesn't appear
- Omniverse Launcher shows "Launch Failed"
- Crash immediately after loading

**Cause**:
Unsupported GPU, outdated drivers, or missing dependencies.

**Solution**:

1. Verify GPU compatibility:
```bash
nvidia-smi
# Must show RTX 2070 or newer (Turing/Ampere/Ada architecture)
```

:::danger GTX GPUs Not Supported
Isaac Sim requires RTX series GPUs. GTX 1080 Ti and older are NOT supported due to missing ray-tracing hardware.
:::

2. Check NVIDIA driver version:
```bash
nvidia-smi --query-gpu=driver_version --format=csv
# Requires 525.60 or newer
```

3. Update NVIDIA drivers:
```bash
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot
```

4. Check Omniverse logs:
```bash
cat ~/.nvidia-omniverse/logs/kit/Isaac-Sim-*/kit_*.log
```

5. Clear Omniverse cache:
```bash
rm -rf ~/.nvidia-omniverse/cache/*
rm -rf ~/.cache/ov/*
```

---

### CUDA Out of Memory {#cuda-memory}

**Symptoms**:
- "CUDA error: out of memory"
- Simulation freezes when loading complex scenes
- Sudden crashes during rendering

**Cause**:
GPU VRAM insufficient for scene complexity.

**Solution**:

1. Check current VRAM usage:
```bash
nvidia-smi
# Watch VRAM usage during simulation
watch -n 1 nvidia-smi
```

2. Reduce rendering quality:
   - In Isaac Sim: **Rendering** → **Render Settings**
   - Set **RTX Mode**: Real-Time (not Path Traced)
   - Reduce **Samples Per Pixel**: 1-4

3. Simplify scene:
   - Reduce mesh polygon counts
   - Lower texture resolutions
   - Disable unnecessary sensors

4. Increase swap space:
```bash
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

5. Use GPU memory optimization in Python:
```python
import torch
torch.cuda.empty_cache()
```

---

### Slow Simulation Performance {#slow-performance}

**Symptoms**:
- Simulation runs slower than real-time
- High GPU utilization but low FPS
- Physics stuttering

**Cause**:
Scene too complex, suboptimal settings, or physics step size too small.

**Solution**:

1. Adjust physics settings:
   - **Physics** → **Physics Scene**
   - Set **Time Steps Per Second**: 60 (not 120)
   - Enable **GPU Dynamics** if using RTX 3000+

2. Reduce rendering load:
   - Disable ray-traced shadows
   - Lower viewport resolution
   - Use Level of Detail (LOD) for distant objects

3. Profile performance:
   - **Window** → **Profiler**
   - Identify bottleneck (CPU/GPU/Physics)

4. Use headless mode for data generation:
```bash
./python.sh scripts/my_script.py --headless
```

---

## Isaac ROS Issues

### Isaac ROS Node Crashes {#isaac-ros-crashes}

**Symptoms**:
- Isaac ROS nodes exit immediately
- "Segmentation fault" in terminal
- Missing GPU acceleration

**Cause**:
Version mismatch between Isaac Sim and Isaac ROS, or missing CUDA dependencies.

**Solution**:

1. Verify Isaac ROS version matches Isaac Sim:
```bash
# Isaac Sim 2023.1.x requires Isaac ROS 2.1.x
cd ~/isaac_ros_ws/src/isaac_ros_common
git log --oneline -1
```

2. Rebuild Isaac ROS workspace:
```bash
cd ~/isaac_ros_ws
rm -rf build/ install/ log/
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

3. Source environment correctly:
```bash
source /opt/ros/humble/setup.bash
source ~/isaac_ros_ws/install/setup.bash
```

4. Check CUDA availability:
```bash
python3 -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

5. Use Isaac ROS Docker container:
```bash
cd ~/isaac_ros_ws/src/isaac_ros_common
./scripts/run_dev.sh
```

---

### VSLAM Not Tracking {#vslam-issues}

**Symptoms**:
- Visual SLAM loses tracking frequently
- Odometry jumps or drifts
- "Tracking lost" warnings

**Cause**:
Poor image quality, insufficient features, or incorrect camera calibration.

**Solution**:

1. Verify camera calibration:
```bash
ros2 topic echo /camera/camera_info --once
# Check distortion coefficients and camera matrix
```

2. Improve lighting in simulation:
   - Add ambient lighting
   - Avoid pure white/black textures
   - Add texture to featureless surfaces

3. Adjust VSLAM parameters:
```yaml
# vslam_params.yaml
visual_slam:
  enable_imu_fusion: true
  gyro_noise_density: 0.001
  gyro_random_walk: 0.0001
  accel_noise_density: 0.01
  accel_random_walk: 0.001
```

4. Check image rate:
```bash
ros2 topic hz /camera/image_raw
# Should be 30+ Hz for stable tracking
```

---

### Synthetic Data Issues {#synthetic-data}

**Symptoms**:
- Generated images are black or corrupted
- Annotations missing or incorrect
- Domain randomization not working

**Cause**:
Replicator configuration errors or rendering issues.

**Solution**:

1. Verify Replicator setup:
```python
import omni.replicator.core as rep

# Check camera is rendering
camera = rep.create.camera(position=(0, 0, 5))
render_product = rep.create.render_product(camera, (1280, 720))

# Verify output
rep.orchestrator.run()
```

2. Enable correct annotators:
```python
# Add required annotators
rep.AnnotatorRegistry.get_annotator("rgb")
rep.AnnotatorRegistry.get_annotator("bounding_box_2d_tight")
rep.AnnotatorRegistry.get_annotator("instance_segmentation")
```

3. Check output directory permissions:
```bash
ls -la ~/synthetic_data/
# Ensure write permissions
```

4. Debug domain randomization:
```python
# Add debug visualization
with rep.new_layer():
    rep.randomizer.color(
        materials=rep.get.material("/World/Robot/Body"),
        colors=rep.distribution.uniform((0, 0, 0), (1, 1, 1))
    )
```

---

## Nav2 Issues

### Nav2 Navigation Issues {#nav2-issues}

**Symptoms**:
- Robot doesn't move to goal
- Path planning fails repeatedly
- Costmap shows obstacles incorrectly

**Cause**:
Incorrect costmap configuration, TF tree issues, or sensor data problems.

**Solution**:

1. Verify TF tree:
```bash
ros2 run tf2_tools view_frames
# Check for complete transform chain: map → odom → base_link → sensors
```

2. Check costmap is receiving data:
```bash
ros2 topic echo /local_costmap/costmap --once
```

3. Adjust costmap parameters for humanoid:
```yaml
# nav2_params.yaml
local_costmap:
  robot_radius: 0.3  # Adjust for humanoid footprint
  inflation_layer:
    inflation_radius: 0.5
  obstacle_layer:
    observation_sources: scan
    scan:
      topic: /scan
      max_obstacle_height: 2.0
      clearing: True
      marking: True
```

4. Configure for bipedal locomotion:
```yaml
controller_server:
  ros__parameters:
    FollowPath:
      plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
      desired_linear_vel: 0.3  # Slower for bipedal
      max_angular_accel: 1.5   # Limited for balance
```

---

## Error Messages Reference

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `CUDA error: no kernel image is available` | GPU architecture mismatch | Rebuild with correct CUDA arch |
| `Failed to create render delegate` | GPU not supported | Verify RTX GPU, update drivers |
| `Isaac ROS: TensorRT engine build failed` | Incompatible TensorRT version | Use Isaac ROS Docker container |
| `Nav2: Plan not found` | Start/goal outside costmap | Check map bounds, clear costmap |
| `Replicator: No valid render products` | Camera not configured | Add render_product to camera |

---

## Getting Help

### Official Resources

- [Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/)
- [Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/)
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/c/agx-autonomous-machines/isaac/)

### Community Support

- [Isaac Sim GitHub Issues](https://github.com/NVIDIA-Omniverse/IsaacSim/issues)
- [Isaac ROS GitHub](https://github.com/NVIDIA-ISAAC-ROS)
- [NVIDIA Discord](https://discord.gg/nvidia)

---

## FAQ

**Q: Can I run Isaac Sim on a laptop?**

A: Yes, if it has an RTX GPU (RTX 2060 Laptop or better). Expect reduced performance compared to desktop GPUs.

**Q: How much VRAM do I need?**

A: Minimum 8GB for simple scenes. 16GB+ recommended for complex environments with multiple robots.

**Q: Can I use AMD GPUs with Isaac Sim?**

A: No, Isaac Sim requires NVIDIA RTX GPUs due to its reliance on CUDA, OptiX, and RTX ray-tracing features.
