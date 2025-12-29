---
sidebar_position: 99
---

# Troubleshooting: Module 2 — Digital Twin (Gazebo & Unity)

This guide covers common issues encountered when working with Gazebo Harmonic and Unity 2022 LTS for robotics simulation.

## Quick Diagnosis

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| Gazebo crashes on startup | GPU driver issues | [gazebo-crashes](#gazebo-crashes-on-startup) |
| Model doesn't appear | SDF/URDF path errors | [model-not-visible](#model-not-visible) |
| Physics behaves strangely | Incorrect mass/inertia | [physics-issues](#physics-issues) |
| ROS bridge not working | Bridge not launched | [ros-bridge](#ros-bridge) |
| Unity ROS connection fails | TCP endpoint mismatch | [unity-ros](#unity-ros-connection) |

---

## Gazebo Issues

### Gazebo Crashes on Startup {#gazebo-crashes-on-startup}

**Symptoms**:
- Gazebo window opens then immediately closes
- Segmentation fault on launch
- Black screen with no response

**Cause**:
GPU driver incompatibility, insufficient VRAM, or OpenGL issues.

**Solution**:

1. Check GPU driver:
```bash
nvidia-smi
# Ensure driver version 525+ is installed
```

2. Try software rendering:
```bash
export LIBGL_ALWAYS_SOFTWARE=1
gz sim empty.sdf
```

3. Update GPU drivers:
```bash
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot
```

4. Check Gazebo logs:
```bash
cat ~/.gz/sim/log/gazebo.log
```

5. Verify OpenGL support:
```bash
glxinfo | grep "OpenGL version"
# Should show 4.5+ for hardware acceleration
```

---

### Model Not Visible {#model-not-visible}

**Symptoms**:
- World loads but robot model is invisible
- Model listed in GUI but not rendered
- "Model not found" warnings in console

**Cause**:
Incorrect model path, missing meshes, or SDF syntax errors.

**Solution**:

1. Set model paths:
```bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/my_models
```

2. Verify model structure:
```
my_robot/
├── model.config
├── model.sdf
└── meshes/
    ├── base_link.dae
    └── wheel.dae
```

3. Check model.config:
```xml
<?xml version="1.0"?>
<model>
  <name>my_robot</name>
  <version>1.0</version>
  <sdf version="1.8">model.sdf</sdf>
</model>
```

4. Validate SDF:
```bash
gz sdf -k model.sdf
```

5. Check mesh file paths in SDF (use relative paths):
```xml
<visual name="visual">
  <geometry>
    <mesh>
      <uri>meshes/base_link.dae</uri>
    </mesh>
  </geometry>
</visual>
```

---

### Physics Simulation Issues {#physics-issues}

**Symptoms**:
- Robot flies away or explodes
- Robot sinks through ground
- Joints behave erratically
- Unrealistic collisions

**Cause**:
Incorrect mass, inertia, or collision properties.

**Solution**:

1. Check mass values (realistic for robot size):
```xml
<inertial>
  <mass>5.0</mass>  <!-- kg, not grams! -->
  <inertia>
    <ixx>0.1</ixx>
    <iyy>0.1</iyy>
    <izz>0.1</izz>
  </inertia>
</inertial>
```

2. Calculate correct inertia for basic shapes:
```python
# Box: I = (1/12) * m * (h² + d²)
# Cylinder: Ixx = Iyy = (1/12) * m * (3r² + h²), Izz = (1/2) * m * r²
# Sphere: I = (2/5) * m * r²
```

3. Ensure collision geometry matches visual:
```xml
<collision name="collision">
  <geometry>
    <box><size>0.5 0.5 0.5</size></box>
  </geometry>
</collision>
<visual name="visual">
  <geometry>
    <box><size>0.5 0.5 0.5</size></box>
  </geometry>
</visual>
```

4. Adjust physics step size for stability:
```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1</real_time_factor>
</physics>
```

---

### ROS-Gazebo Bridge Issues {#ros-bridge}

**Symptoms**:
- Topics from Gazebo not visible in ROS 2
- Commands to Gazebo not received
- `ros2 topic list` missing expected topics

**Cause**:
Bridge not launched or incorrect topic mapping.

**Solution**:

1. Launch the bridge:
```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

2. Use bridge config file:
```yaml
# bridge.yaml
- ros_topic_name: "/cmd_vel"
  gz_topic_name: "/cmd_vel"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "gz.msgs.Twist"
  direction: ROS_TO_GZ
```

3. Launch with config:
```bash
ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=bridge.yaml
```

4. Verify Gazebo topics:
```bash
gz topic -l
```

5. Verify ROS topics:
```bash
ros2 topic list
```

---

### Sensor Data Not Publishing {#sensor-issues}

**Symptoms**:
- LiDAR/Camera/IMU topics empty
- Sensor visible in Gazebo but no data
- Intermittent sensor data

**Cause**:
Sensor plugin not loaded or incorrect topic configuration.

**Solution**:

1. Verify sensor plugin in SDF:
```xml
<sensor name="lidar" type="gpu_lidar">
  <pose>0 0 0.5 0 0 0</pose>
  <topic>scan</topic>
  <update_rate>10</update_rate>
  <gz:frame_id>lidar_link</gz:frame_id>
  <ray>
    <scan>
      <horizontal>
        <samples>640</samples>
        <resolution>1</resolution>
        <min_angle>-1.5707</min_angle>
        <max_angle>1.5707</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
    </range>
  </ray>
</sensor>
```

2. Check Gazebo topic:
```bash
gz topic -e -t /scan
```

3. Bridge sensor topics:
```bash
ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan
```

---

## Unity Issues

### Unity ROS Connection Issues {#unity-ros-connection}

**Symptoms**:
- "Connection refused" in Unity console
- ROS topics not appearing in Unity
- Unity-published messages not received by ROS

**Cause**:
ROS-TCP-Endpoint not running or IP/port mismatch.

**Solution**:

1. Start ROS TCP Endpoint:
```bash
ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_IP:=0.0.0.0
```

2. Configure Unity ROS Settings:
   - Open **Robotics** → **ROS Settings**
   - Set **ROS IP Address**: `127.0.0.1` (localhost) or your machine's IP
   - Set **ROS Port**: `10000` (default)

3. Test connection:
```bash
# In Unity, check Console for:
# "ROS-TCP-Connector: Connected to ROS"
```

4. Firewall configuration:
```bash
sudo ufw allow 10000/tcp
```

---

### URDF Import Fails in Unity {#urdf-import}

**Symptoms**:
- "Failed to parse URDF" error
- Robot appears broken or missing parts
- Joints not working correctly

**Cause**:
URDF syntax incompatible with Unity URDF Importer.

**Solution**:

1. Validate URDF before import:
```bash
check_urdf robot.urdf
```

2. Convert xacro to plain URDF:
```bash
xacro robot.urdf.xacro > robot.urdf
```

3. Fix common Unity URDF issues:
   - Remove `gazebo` tags (Unity ignores them)
   - Use supported mesh formats (DAE, STL, OBJ)
   - Ensure all mesh paths are relative

4. Import settings in Unity:
   - Select URDF file in Project
   - Click **Import Robot from Selected URDF**
   - Choose axis convention (Z-up for ROS)

---

### Unity Performance Issues {#unity-performance}

**Symptoms**:
- Low FPS in simulation
- Stuttering robot movement
- High CPU/GPU usage

**Cause**:
Too many physics calculations, unoptimized meshes, or excessive sensors.

**Solution**:

1. Reduce physics update rate:
   - **Edit** → **Project Settings** → **Time**
   - Set **Fixed Timestep**: `0.02` (50 Hz)

2. Simplify collision meshes:
   - Use primitive colliders (Box, Sphere, Capsule) instead of Mesh Colliders
   - Reduce mesh polygon count

3. Optimize lighting:
   - Use baked lighting where possible
   - Reduce real-time shadow quality

4. Limit sensor data rates:
   - Camera: 30 FPS max
   - LiDAR: 10 Hz max

---

## Error Messages Reference

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `[Err] [Model.cc:95] Missing SDF` | Invalid SDF syntax | Run `gz sdf -k model.sdf` |
| `[Wrn] [gz-sim] Mesh not found` | Missing mesh file | Check mesh paths in SDF |
| `libGL error: No matching fbConfigs` | GPU driver issue | Update NVIDIA drivers |
| `Unity: Connection timed out` | ROS endpoint not running | Start ros_tcp_endpoint |
| `URDF importer: Joint has no parent` | Incomplete URDF kinematic chain | Add missing parent links |

---

## Getting Help

### Official Resources

- [Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic)
- [Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub)
- [ros_gz Bridge](https://github.com/gazebosim/ros_gz)

### Community Support

- [Gazebo Community](https://community.gazebosim.org/)
- [Unity Forums - Robotics](https://forum.unity.com/forums/robotics.623/)
- [ROS Discourse](https://discourse.ros.org/)

---

## FAQ

**Q: Can I use Gazebo Classic with this book?**

A: No, this book uses Gazebo Harmonic (formerly Ignition Gazebo). Gazebo Classic reached end-of-life in 2025.

**Q: Does Unity require a paid license for robotics?**

A: Unity Personal is free for individuals and small businesses under $100K revenue. Unity Pro provides additional features.

**Q: How do I sync Gazebo and Unity simulations?**

A: They typically run independently. Use ROS 2 as middleware to share data between them.
