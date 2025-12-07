---
id: motion-planning
sidebar_position: 2
title: Motion Planning
---

# Motion Planning

Motion planning calculates paths for safe robot movement:

- A* and RRT algorithms  
- Kinematic and dynamic constraints  
- Collision avoidance with obstacles  

Example:

```python
# Use MoveIt2 for motion planning
ros2 launch moveit2_tutorials move_group.launch.py
