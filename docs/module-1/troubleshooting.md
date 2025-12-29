---
sidebar_position: 99
---

# Troubleshooting: Module 1 — ROS 2

This guide covers common issues encountered when working with ROS 2 Humble Hawksbill.

## Quick Diagnosis

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| `ros2: command not found` | Environment not sourced | [ros2-command-not-found](#ros2-command-not-found) |
| Node can't find other nodes | DDS discovery issues | [discovery-issues](#discovery-issues) |
| `colcon build` fails | Missing dependencies | [build-failures](#colcon-build-failures) |
| URDF parsing errors | Invalid XML syntax | [urdf-errors](#urdf-errors) |
| Topics not publishing | QoS mismatch | [qos-mismatch](#qos-mismatch) |

---

## Common Issues

### ros2: command not found {#ros2-command-not-found}

**Symptoms**:
- `ros2: command not found` when running any ROS 2 command
- Tab completion doesn't work for ROS 2 commands

**Cause**:
The ROS 2 environment has not been sourced in the current terminal session.

**Solution**:

1. Source the ROS 2 setup file:
```bash
source /opt/ros/humble/setup.bash
```

2. Add to `~/.bashrc` for automatic sourcing:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

3. If using a workspace, also source it:
```bash
source ~/ros2_ws/install/setup.bash
```

**Prevention**:
Add both setup files to your `~/.bashrc`:
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash 2>/dev/null || true
```

---

### DDS Discovery Issues {#discovery-issues}

**Symptoms**:
- `ros2 topic list` shows topics but no data
- Nodes can't find each other
- `ros2 node list` is empty

**Cause**:
DDS multicast discovery is blocked by firewall or network configuration.

**Solution**:

1. Check if nodes are on the same ROS_DOMAIN_ID:
```bash
echo $ROS_DOMAIN_ID
# Default is 0, ensure all nodes use the same value
```

2. Set domain ID explicitly:
```bash
export ROS_DOMAIN_ID=42
```

3. For localhost-only communication:
```bash
export ROS_LOCALHOST_ONLY=1
```

4. Check firewall settings:
```bash
sudo ufw allow 7400:7500/udp
sudo ufw allow 7400:7500/tcp
```

5. Try different DDS implementation:
```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
sudo apt install ros-humble-rmw-cyclonedds-cpp
```

---

### colcon build Failures {#colcon-build-failures}

**Symptoms**:
- `colcon build` exits with errors
- Package dependencies not found
- CMake configuration failures

**Cause**:
Missing dependencies, incorrect package.xml, or environment issues.

**Solution**:

1. Install missing dependencies:
```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

2. Clean and rebuild:
```bash
rm -rf build/ install/ log/
colcon build --symlink-install
```

3. Build specific package with verbose output:
```bash
colcon build --packages-select <package_name> --event-handlers console_direct+
```

4. Check for circular dependencies:
```bash
colcon graph --packages-up-to <package_name>
```

---

### URDF Parsing Errors {#urdf-errors}

**Symptoms**:
- `robot_state_publisher` crashes
- "Error parsing URDF" messages
- Joint/link visualization incorrect in RViz

**Cause**:
Invalid URDF XML syntax, missing links, or incorrect joint definitions.

**Solution**:

1. Validate URDF syntax:
```bash
check_urdf model.urdf
```

2. Convert xacro to URDF and validate:
```bash
xacro model.urdf.xacro > model.urdf
check_urdf model.urdf
```

3. Common URDF fixes:

**Missing visual/collision geometry**:
```xml
<link name="base_link">
  <visual>
    <geometry>
      <box size="0.1 0.1 0.1"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.1 0.1 0.1"/>
    </geometry>
  </collision>
</link>
```

**Joint without proper parent/child**:
```xml
<joint name="joint1" type="revolute">
  <parent link="base_link"/>  <!-- Must exist -->
  <child link="link1"/>       <!-- Must exist -->
  <axis xyz="0 0 1"/>
  <limit effort="100" lower="-3.14" upper="3.14" velocity="1.0"/>
</joint>
```

---

### QoS Mismatch {#qos-mismatch}

**Symptoms**:
- Subscriber receives no messages despite publisher running
- Warning: "New subscription discovered... but it requested incompatible QoS"

**Cause**:
Publisher and subscriber have incompatible Quality of Service settings.

**Solution**:

1. Check QoS compatibility:
```bash
ros2 topic info /topic_name --verbose
```

2. Match QoS profiles in code:

**Python publisher**:
```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

qos_profile = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)

self.publisher = self.create_publisher(String, 'topic', qos_profile)
```

**Python subscriber**:
```python
# Use matching QoS profile
self.subscription = self.create_subscription(
    String,
    'topic',
    self.callback,
    qos_profile  # Must match publisher
)
```

3. For sensor data (often uses BEST_EFFORT):
```python
from rclpy.qos import qos_profile_sensor_data

self.subscription = self.create_subscription(
    Image,
    '/camera/image_raw',
    self.image_callback,
    qos_profile_sensor_data
)
```

---

### Package Not Found After Build {#package-not-found}

**Symptoms**:
- `ros2 pkg list` doesn't show your package
- `ros2 run <package> <node>` says package not found

**Cause**:
Workspace install not sourced, or build failed silently.

**Solution**:

1. Source the workspace:
```bash
source ~/ros2_ws/install/setup.bash
```

2. Verify package exists:
```bash
ros2 pkg prefix <package_name>
```

3. Check if package built successfully:
```bash
ls ~/ros2_ws/install/<package_name>
```

4. Rebuild with --symlink-install:
```bash
colcon build --symlink-install --packages-select <package_name>
```

---

## Error Messages Reference

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `SetuptoolsDeprecationWarning` | Old setuptools version | `pip install setuptools==58.2.0` |
| `Could not find a package configuration file provided by "rclpy"` | ROS 2 not sourced | `source /opt/ros/humble/setup.bash` |
| `TF_REPEATED_DATA` | Duplicate TF publishers | Check for multiple robot_state_publishers |
| `transform timeout` | TF tree incomplete | Verify all frames are connected |
| `No executable found` | setup.py entry points incorrect | Check entry_points in setup.py |

---

## Performance Issues

### High CPU Usage

**Symptoms**:
- Node uses 100% CPU
- System becomes unresponsive

**Solution**:

1. Add sleep to spin loops:
```python
import rclpy
from rclpy.executors import MultiThreadedExecutor

# Use executor with rate limiting
executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()
```

2. Use timers instead of while loops:
```python
self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
```

---

## Getting Help

### Official Resources

- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 GitHub Issues](https://github.com/ros2/ros2/issues)
- [ROS Answers](https://answers.ros.org/)

### Community Support

- [ROS Discourse](https://discourse.ros.org/)
- [ROS Discord](https://discord.gg/ros)
- [Stack Overflow - ROS tag](https://stackoverflow.com/questions/tagged/ros)

### Reporting Bugs

When reporting issues, include:

1. Operating system and version
2. ROS 2 distribution (`ros2 --version`)
3. Complete error message
4. Minimal reproducible example
5. Steps to reproduce

---

## FAQ

**Q: Can I use ROS 2 Humble on Ubuntu 20.04?**

A: No, ROS 2 Humble requires Ubuntu 22.04 LTS. Use ROS 2 Foxy for Ubuntu 20.04.

**Q: How do I run ROS 2 nodes in Docker?**

A: Use the official ROS 2 Docker images:
```bash
docker run -it --rm ros:humble
```

**Q: Why does my node stop when I close the terminal?**

A: The node runs in the foreground. Use `nohup` or a process manager:
```bash
nohup ros2 run my_package my_node &
```
