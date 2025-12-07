
---

# 📁 `docs/ros2/urdf.md`

```md
---
id: urdf
sidebar_position: 3
title: Robot Description with URDF
---

# Robot Description Format (URDF)

**URDF** defines the robot's physical structure:

- Links (rigid bodies)  
- Joints (connections)  
- Sensors  
- Actuators  

Example: A humanoid arm:

```xml
<link name="upper_arm"/>
<joint name="elbow_joint" type="revolute">
  <parent link="upper_arm"/>
  <child link="forearm"/>
</joint>
