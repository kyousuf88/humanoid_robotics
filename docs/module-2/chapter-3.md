---
id: module-2-chapter-3
sidebar_position: 3
title: "Chapter 3 - Sensor Simulation (LiDAR, IMUs, Depth Cameras, noise models)"
---

# Chapter 3: Sensor Simulation (LiDAR, IMUs, Depth Cameras, noise models)

## Learning Objectives
- [X] Simulate various sensor types in Gazebo with realistic characteristics
- [X] Understand noise models and their impact on robotic perception systems
- [X] Validate sensor simulation against real sensors for accuracy
- [X] Implement sensor fusion techniques using simulated data

## Key Concepts
- [X] **Sensor Simulation**: Replication of real sensor behavior in virtual environments
- [X] **Noise Models**: Mathematical representations of sensor imperfections and uncertainties
- [X] **Sensor Fusion**: Combining data from multiple sensors to improve perception
- [X] **Calibration**: Adjusting sensor models to match real-world behavior
- [X] **Validation**: Ensuring simulated sensors produce realistic data

## Introduction

Sensors are the eyes, ears, and sensory organs of humanoid robots, providing the critical data needed for navigation, manipulation, and interaction with the environment. In simulation, accurately modeling these sensors is crucial for developing robust perception and control systems that can transfer effectively to real robots.

This chapter explores the simulation of various sensor types commonly used in humanoid robotics: LiDAR for 3D mapping and navigation, IMUs for orientation and motion sensing, depth cameras for 3D perception, and other sensors essential for robot perception. We'll examine how to model sensor characteristics, implement realistic noise models, and validate simulation results against real-world data.

The fidelity of sensor simulation directly impacts the sim-to-real transfer of robotic systems. Poorly modeled sensors can lead to control strategies that work in simulation but fail on real robots, while accurate sensor models enable more effective development and testing of perception and control algorithms.

## LiDAR Simulation

### Understanding LiDAR in Robotics

LiDAR (Light Detection and Ranging) sensors provide accurate 3D measurements of the environment by timing the round-trip of laser pulses. For humanoid robots, LiDAR is essential for:

- Environment mapping and localization
- Obstacle detection and avoidance
- Navigation planning
- Human detection and tracking

### LiDAR Simulation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   LiDAR Simulation                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │
│  │   Physical  │    │   Sensor    │    │   Processing    │ │
│  │   World     │───►│   Model     │───►│   Pipeline      │ │
│  │   (Gazebo)  │    │   (Ray)     │    │   (ROS 2)       │ │
│  └─────────────┘    └─────────────┘    └─────────────────┘ │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌─────────────────────────────────────────────────────────┤
│  │  Environment:         │  Ray Casting:      │  Data:    │
│  │  - Objects            │  - 720 rays        │  - Scan   │
│  │  - Surfaces           │  - Distance calc   │  - Noise  │
│  │  - Materials          │  - Reflection      │  - Filter │
│  └─────────────────────────────────────────────────────────┘
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┤
│  │   Ray-Surface   │ │   Range Check   │ │   Message       │
│  │   Intersections │ │   & Validation  │ │   Generation    │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘
│         │                   │                   │          │
└─────────┼───────────────────┼───────────────────┼──────────┘
          │                   │                   │
          ▼                   ▼                   ▼
   Realistic Point      Validated Range    ROS 2 LaserScan
      Cloud Data            Measurements       Messages
```

### LiDAR Simulation in Gazebo

Gazebo provides realistic LiDAR simulation through ray sensor plugins. Here's a detailed configuration for a 2D LiDAR similar to the Hokuyo URG-04LX:

```xml
<!-- 2D LiDAR Sensor -->
<sensor name="laser_2d" type="ray">
  <pose>0.15 0 0.3 0 0 0</pose> <!-- Positioned at head level -->
  <visualize>false</visualize>
  <update_rate>10</update_rate>

  <ray>
    <scan>
      <horizontal>
        <samples>720</samples> <!-- 0.5 degree resolution over 360 degrees -->
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle> <!-- -π radians -->
        <max_angle>3.14159</max_angle>  <!-- π radians -->
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>    <!-- 0.1m minimum range -->
      <max>5.6</max>    <!-- 5.6m maximum range -->
      <resolution>0.01</resolution> <!-- 1cm resolution -->
    </range>
  </ray>

  <!-- Add noise to make it more realistic -->
  <noise>
    <type>gaussian</type>
    <mean>0.0</mean>
    <stddev>0.01</stddev> <!-- 1cm standard deviation -->
  </noise>

  <!-- ROS 2 plugin for the sensor -->
  <plugin name="laser_2d_controller" filename="libgazebo_ros_ray_sensor.so">
    <ros>
      <namespace>/humanoid</namespace>
      <remapping>~/out:=scan</remapping>
    </ros>
    <output_type>sensor_msgs/LaserScan</output_type>
    <topic_name>~/out</topic_name>
    <frame_name>laser_2d_frame</frame_name>
  </plugin>
</sensor>
```

### 3D LiDAR Simulation

For more sophisticated humanoid robots, 3D LiDAR provides volumetric perception:

```xml
<!-- 3D LiDAR Sensor (Velodyne VLP-16 equivalent) -->
<sensor name="velodyne_3d" type="ray">
  <pose>0.2 0 0.5 0 0 0</pose> <!-- Higher position for better view -->
  <visualize>false</visualize>
  <update_rate>10</update_rate>

  <ray>
    <scan>
      <horizontal>
        <samples>1800</samples> <!-- High resolution for accuracy -->
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
      <vertical>
        <samples>16</samples> <!-- 16 laser beams vertically -->
        <resolution>1</resolution>
        <min_angle>-0.2618</min_angle> <!-- -15 degrees -->
        <max_angle>0.2618</max_angle>   <!-- 15 degrees -->
      </vertical>
    </scan>
    <range>
      <min>0.3</min>    <!-- 0.3m minimum range -->
      <max>100.0</max>  <!-- 100m maximum range -->
      <resolution>0.001</resolution> <!-- 1mm resolution -->
    </range>
  </ray>

  <!-- More complex noise model for 3D LiDAR -->
  <noise>
    <type>gaussian</type>
    <mean>0.0</mean>
    <stddev>0.02</stddev> <!-- 2cm standard deviation -->
  </noise>

  <plugin name="velodyne_3d_controller" filename="libgazebo_ros_ray_sensor.so">
    <ros>
      <namespace>/humanoid</namespace>
      <remapping>~/out:=points</remapping>
    </ros>
    <output_type>sensor_msgs/PointCloud2</output_type>
    <topic_name>~/out</topic_name>
    <frame_name>velodyne_3d_frame</frame_name>
  </plugin>
</sensor>
```

### LiDAR Processing Pipeline

Here's how to process simulated LiDAR data in ROS 2:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
from std_msgs.msg import Header
import numpy as np
from scipy.spatial.transform import Rotation as R

class LIDARProcessor(Node):
    def __init__(self):
        super().__init__('lidar_processor')

        # Subscribe to LiDAR data
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/humanoid/scan',
            self.scan_callback,
            10
        )

        # Publisher for processed data
        self.obstacle_publisher = self.create_publisher(
            PointCloud2,
            '/humanoid/obstacles',
            10
        )

        # Parameters
        self.min_obstacle_distance = 1.0  # meters
        self.obstacle_threshold = 0.1     # meters difference from expected

        self.get_logger().info('LiDAR Processor initialized')

    def scan_callback(self, msg):
        """Process incoming LiDAR scan data"""
        try:
            # Convert scan to Cartesian coordinates
            angles = np.linspace(msg.angle_min, msg.angle_max, len(msg.ranges))
            ranges = np.array(msg.ranges)

            # Filter out invalid ranges
            valid_indices = (ranges >= msg.range_min) & (ranges <= msg.range_max)
            valid_angles = angles[valid_indices]
            valid_ranges = ranges[valid_indices]

            # Convert to Cartesian coordinates
            x_coords = valid_ranges * np.cos(valid_angles)
            y_coords = valid_ranges * np.sin(valid_angles)

            # Detect obstacles
            obstacles = self.detect_obstacles(x_coords, y_coords, msg.header)

            # Publish obstacles
            if obstacles is not None:
                self.obstacle_publisher.publish(obstacles)

        except Exception as e:
            self.get_logger().error(f'Error processing LiDAR data: {e}')

    def detect_obstacles(self, x_coords, y_coords, header):
        """Detect obstacles from LiDAR data"""
        # Simple obstacle detection: points within min_obstacle_distance
        distances = np.sqrt(x_coords**2 + y_coords**2)
        obstacle_indices = distances < self.min_obstacle_distance

        if np.any(obstacle_indices):
            obstacle_points = np.column_stack([
                x_coords[obstacle_indices],
                y_coords[obstacle_indices],
                np.zeros(np.sum(obstacle_indices))  # z=0 for ground-level obstacles
            ])

            # Convert to PointCloud2 message
            return self.create_pointcloud2(obstacle_points, header)

        return None

    def create_pointcloud2(self, points, header):
        """Create PointCloud2 message from numpy array"""
        # This is a simplified implementation
        # In practice, you'd use sensor_msgs_py.point_cloud2
        pc2_msg = PointCloud2()
        pc2_msg.header = header
        pc2_msg.height = 1
        pc2_msg.width = len(points)
        pc2_msg.is_dense = False
        pc2_msg.is_bigendian = False

        # Define fields (x, y, z)
        # This would require more complex implementation in practice
        return pc2_msg

def main(args=None):
    rclpy.init(args=args)
    processor = LIDARProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## IMU Simulation

### Understanding IMU Sensors

Inertial Measurement Units (IMUs) provide crucial information about a robot's orientation, angular velocity, and linear acceleration. For humanoid robots, IMUs are essential for:

- Balance control and stabilization
- Motion detection and classification
- Orientation estimation
- Fall detection

### IMU Configuration in Gazebo

Here's a realistic IMU configuration for a humanoid robot:

```xml
<!-- IMU Sensor -->
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate> <!-- 100Hz update rate -->
  <pose>0.0 0.0 0.0 0 0 0</pose> <!-- Position at center of mass -->
  <visualize>false</visualize>

  <!-- Noise parameters based on real IMU specifications -->
  <imu>
    <!-- Linear acceleration noise -->
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01759259</stddev> <!-- ~0.018 m/s² -->
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.001759259</bias_stddev> <!-- ~0.0018 m/s² -->
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01759259</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.001759259</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01759259</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.001759259</bias_stddev>
        </noise>
      </z>
    </linear_acceleration>

    <!-- Angular velocity noise -->
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.001466049</stddev> <!-- ~0.0015 rad/s -->
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0001466049</bias_stddev> <!-- ~0.00015 rad/s -->
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.001466049</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0001466049</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.001466049</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0001466049</bias_stddev>
        </noise>
      </z>
    </angular_velocity>

    <!-- Orientation noise (usually minimal) -->
    <orientation>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0001</stddev> <!-- Very small noise for orientation -->
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0001</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0001</stddev>
        </noise>
      </z>
    </orientation>
  </imu>

  <!-- ROS 2 plugin for IMU -->
  <plugin name="imu_controller" filename="libgazebo_ros_imu.so">
    <ros>
      <namespace>/humanoid</namespace>
      <remapping>~/out:=imu/data</remapping>
    </ros>
    <initial_orientation_as_reference>false</initial_orientation_as_reference>
    <topic>~/out</topic>
    <frame_name>imu_link</frame_name>
  </plugin>
</sensor>
```

### IMU Data Processing

Processing IMU data for humanoid robots requires filtering and fusion techniques:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
import numpy as np
from scipy.spatial.transform import Rotation as R
import math

class IMUProcessor(Node):
    def __init__(self):
        super().__init__('imu_processor')

        # Subscribe to IMU data
        self.imu_subscription = self.create_subscription(
            Imu,
            '/humanoid/imu/data',
            self.imu_callback,
            10
        )

        # Publisher for processed orientation
        self.orientation_publisher = self.create_publisher(
            Vector3,
            '/humanoid/orientation_rpy',
            10
        )

        # Complementary filter parameters
        self.complementary_filter_gain = 0.98
        self.dt = 0.01  # 100Hz update rate

        # Initialize orientation estimate
        self.orientation_estimate = R.from_quat([0, 0, 0, 1])  # Identity quaternion
        self.last_time = None

        # Gravity vector in world frame
        self.gravity_world = np.array([0, 0, 9.81])

        self.get_logger().info('IMU Processor initialized')

    def imu_callback(self, msg):
        """Process incoming IMU data using complementary filter"""
        current_time = self.get_clock().now().nanoseconds / 1e9

        if self.last_time is not None:
            dt = current_time - self.last_time
        else:
            dt = self.dt  # Use default if first reading

        # Extract measurements
        angular_velocity = np.array([
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z
        ])

        linear_acceleration = np.array([
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z
        ])

        # Get orientation from quaternion in message
        quat = np.array([
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w
        ])

        # Use complementary filter to combine gyroscope and accelerometer data
        orientation_from_gyro = self.integrate_gyro(angular_velocity, dt)
        orientation_from_accel = self.estimate_from_accelerometer(linear_acceleration)

        # Complementary filter: blend gyro integration with accelerometer correction
        # Higher gain means trust gyroscope more (less drift), lower gain means trust accelerometer more (less noise)
        self.orientation_estimate = self.complementary_filter(
            self.orientation_estimate,
            orientation_from_gyro,
            orientation_from_accel,
            self.complementary_filter_gain
        )

        # Publish orientation in RPY format
        rpy = self.orientation_estimate.as_euler('xyz')
        rpy_msg = Vector3()
        rpy_msg.x = rpy[0]  # Roll
        rpy_msg.y = rpy[1]  # Pitch
        rpy_msg.z = rpy[2]  # Yaw

        self.orientation_publisher.publish(rpy_msg)

        # Update time for next iteration
        self.last_time = current_time

        # Log balance information for humanoid robot
        self.check_balance(rpy)

    def integrate_gyro(self, angular_velocity, dt):
        """Integrate gyroscope data to estimate orientation change"""
        # Convert angular velocity to rotation vector
        rotation_vector = angular_velocity * dt

        # Create rotation from rotation vector
        rotation = R.from_rotvec(rotation_vector)

        # Apply rotation to current estimate
        return self.orientation_estimate * rotation

    def estimate_from_accelerometer(self, linear_acceleration):
        """Estimate orientation from accelerometer data"""
        # Normalize accelerometer reading (remove magnitude, keep direction)
        accel_norm = linear_acceleration / np.linalg.norm(linear_acceleration)

        # The accelerometer measures gravity in the body frame
        # So we want to find the rotation that transforms the world gravity vector
        # to the measured acceleration vector
        gravity_body = -accel_norm  # Accelerometer measures opposite of gravity

        # Create a rotation that aligns the z-axis with the measured gravity direction
        # This is a simplified approach - in practice, you'd use more sophisticated methods
        z_axis = gravity_body / np.linalg.norm(gravity_body)

        # Create an arbitrary x-axis perpendicular to z-axis
        if abs(z_axis[2]) < 0.9:
            x_axis = np.cross([0, 0, 1], z_axis)
        else:
            x_axis = np.cross([1, 0, 0], z_axis)
        x_axis = x_axis / np.linalg.norm(x_axis)

        # Create y-axis as cross product
        y_axis = np.cross(z_axis, x_axis)

        # Create rotation matrix
        rotation_matrix = np.column_stack([x_axis, y_axis, z_axis])

        return R.from_matrix(rotation_matrix)

    def complementary_filter(self, current_orientation, gyro_orientation, accel_orientation, gain):
        """Apply complementary filter to combine gyroscope and accelerometer data"""
        # Convert to rotation vectors for interpolation
        current_rotvec = current_orientation.as_rotvec()
        gyro_rotvec = gyro_orientation.as_rotvec()
        accel_rotvec = accel_orientation.as_rotvec()

        # Apply complementary filter in rotation vector space
        filtered_rotvec = gain * gyro_rotvec + (1 - gain) * accel_rotvec

        # Create new rotation from filtered vector
        filtered_rotation = R.from_rotvec(filtered_rotvec)

        return filtered_rotation

    def check_balance(self, rpy):
        """Check if humanoid robot is maintaining balance based on IMU data"""
        roll, pitch, yaw = rpy

        # Define balance thresholds (in radians)
        max_roll = 0.3  # ~17 degrees
        max_pitch = 0.3  # ~17 degrees

        if abs(roll) > max_roll or abs(pitch) > max_pitch:
            self.get_logger().warn(
                f'Balance warning: Roll={roll:.2f}, Pitch={pitch:.2f} '
                f'exceeds safe limits ({max_roll:.2f}, {max_pitch:.2f})'
            )
        else:
            # Balance is within acceptable range
            pass

def main(args=None):
    rclpy.init(args=args)
    processor = IMUProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Depth Camera Simulation

### Understanding Depth Cameras

Depth cameras provide 3D information about the environment by measuring the distance to objects in the scene. For humanoid robots, depth cameras are essential for:

- 3D mapping and reconstruction
- Object recognition and manipulation
- Human detection and gesture recognition
- Safe navigation around obstacles

### Depth Camera Configuration in Gazebo

Here's a configuration for a realistic depth camera simulation:

```xml
<!-- Depth Camera Sensor -->
<sensor name="depth_camera" type="depth">
  <always_on>true</always_on>
  <update_rate>30</update_rate> <!-- 30Hz update rate -->
  <visualize>true</visualize>
  <pose>0.1 0 0.4 0 0 0</pose> <!-- Positioned at head level -->

  <camera name="depth_cam">
    <horizontal_fov>1.047</horizontal_fov> <!-- 60 degrees -->
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>  <!-- 0.1m minimum range -->
      <far>10.0</far>   <!-- 10m maximum range -->
    </clip>

    <!-- Noise parameters -->
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev> <!-- 7mm depth noise -->
    </noise>
  </camera>

  <plugin name="depth_camera_controller" filename="libgazebo_ros_openni_kinect.so">
    <ros>
      <namespace>/humanoid</namespace>
      <remapping>rgb/image_raw:=/camera/rgb/image_raw</remapping>
      <remapping>depth/image_raw:=/camera/depth/image_raw</remapping>
      <remapping>depth/camera_info:=/camera/depth/camera_info</remapping>
      <remapping>rgb/camera_info:=/camera/rgb/camera_info</remapping>
    </ros>

    <!-- Camera parameters -->
    <frame_name>depth_camera_frame</frame_name>
    <baseline>0.2</baseline>
    <distortion_k1>0.0</distortion_k1>
    <distortion_k2>0.0</distortion_k2>
    <distortion_k3>0.0</distortion_k3>
    <distortion_t1>0.0</distortion_t1>
    <distortion_t2>0.0</distortion_t2>

    <!-- Point cloud parameters -->
    <point_cloud_cutoff>0.3</point_cloud_cutoff>
    <point_cloud_cutoff_max>5.0</point_cloud_cutoff_max>
  </plugin>
</sensor>
```

### Processing Depth Camera Data

Here's how to process depth camera data in ROS 2:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import numpy as np
import cv2
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point

class DepthCameraProcessor(Node):
    def __init__(self):
        super().__init__('depth_camera_processor')

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Subscribe to depth camera data
        self.depth_subscription = self.create_subscription(
            Image,
            '/humanoid/camera/depth/image_raw',
            self.depth_callback,
            10
        )

        # Subscribe to RGB camera data
        self.rgb_subscription = self.create_subscription(
            Image,
            '/humanoid/camera/rgb/image_raw',
            self.rgb_callback,
            10
        )

        # Publisher for point cloud markers
        self.marker_publisher = self.create_publisher(
            Marker,
            '/humanoid/depth_objects',
            10
        )

        # Store latest images
        self.latest_depth_image = None
        self.latest_rgb_image = None

        self.get_logger().info('Depth Camera Processor initialized')

    def depth_callback(self, msg):
        """Process incoming depth image"""
        try:
            # Convert ROS Image message to OpenCV image
            cv_depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')

            # Store for processing
            self.latest_depth_image = cv_depth_image

            # Process depth data to find objects
            self.process_depth_data(cv_depth_image, msg.header)

        except Exception as e:
            self.get_logger().error(f'Error processing depth image: {e}')

    def rgb_callback(self, msg):
        """Process incoming RGB image"""
        try:
            # Convert ROS Image message to OpenCV image
            cv_rgb_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Store for processing
            self.latest_rgb_image = cv_rgb_image

        except Exception as e:
            self.get_logger().error(f'Error processing RGB image: {e}')

    def process_depth_data(self, depth_image, header):
        """Process depth image to extract 3D information"""
        # Find regions of interest (e.g., objects at specific distances)
        # This is a simplified example looking for objects within 1-2 meters

        # Define distance range of interest
        min_distance = 1.0  # meters
        max_distance = 2.0  # meters

        # Create mask for objects in the distance range
        mask = (depth_image >= min_distance) & (depth_image <= max_distance) & (depth_image > 0)

        if np.any(mask):
            # Find contours of detected objects
            mask_uint8 = (mask * 255).astype(np.uint8)
            contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process each contour
            for contour in contours:
                # Filter by size to avoid noise
                if cv2.contourArea(contour) > 100:  # At least 100 pixels
                    # Calculate bounding box
                    x, y, w, h = cv2.boundingRect(contour)

                    # Calculate center point in 3D space
                    center_x = x + w // 2
                    center_y = y + h // 2

                    # Get depth at center point
                    depth_at_center = depth_image[center_y, center_x]

                    if depth_at_center > 0:
                        # Publish marker for visualization
                        self.publish_object_marker(center_x, center_y, depth_at_center, header)

    def publish_object_marker(self, x, y, depth, header):
        """Publish a marker for detected object"""
        marker = Marker()
        marker.header = header
        marker.ns = "depth_objects"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        # Convert pixel coordinates to 3D world coordinates (simplified)
        # This requires camera intrinsics for accurate conversion
        marker.pose.position.x = depth  # Forward direction
        marker.pose.position.y = (x - 320) * depth * 0.001  # Lateral offset (approximate)
        marker.pose.position.z = (240 - y) * depth * 0.001  # Height offset (approximate)

        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        self.marker_publisher.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    processor = DepthCameraProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Noise Models and Sensor Imperfections

### Understanding Sensor Noise

Real sensors are imperfect and introduce various types of noise and errors. Modeling these imperfections is crucial for realistic simulation:

1. **Gaussian Noise**: Random variations following a normal distribution
2. **Bias**: Systematic offset from true values
3. **Drift**: Slow changes in bias over time
4. **Quantization**: Discrete representation of continuous values
5. **Latency**: Delay between measurement and reporting

### Advanced Noise Models

For more realistic sensor simulation, implement complex noise models:

```python
import numpy as np
from scipy import ndimage
import math

class SensorNoiseModel:
    def __init__(self):
        # IMU noise parameters based on real sensor specifications
        self.imu_params = {
            'accel': {
                'noise_density': 0.002,  # m/s²/√Hz
                'random_walk': 0.0004,   # m/s²/√Hz
                'bias_instability': 0.001  # m/s²
            },
            'gyro': {
                'noise_density': 0.0002,  # rad/s/√Hz
                'random_walk': 0.00004,   # rad/s/√Hz
                'bias_instability': 0.0001  # rad/s
            }
        }

        # Initialize bias random walk states
        self.accel_bias_rw = np.zeros(3)
        self.gyro_bias_rw = np.zeros(3)

        # Initialize bias instability states
        self.accel_bias_instability = np.zeros(3)
        self.gyro_bias_instability = np.zeros(3)

    def add_imu_noise(self, true_accel, true_gyro, dt):
        """Add realistic IMU noise to measurements"""
        # Sample random walk components
        self.accel_bias_rw += np.random.normal(0, self.imu_params['accel']['random_walk'] * np.sqrt(dt), 3)
        self.gyro_bias_rw += np.random.normal(0, self.imu_params['gyro']['random_walk'] * np.sqrt(dt), 3)

        # Update bias instability (first-order Gauss-Markov process)
        beta = 1 / 3600  # Correlation time constant (1 hour)
        self.accel_bias_instability = (
            self.accel_bias_instability * math.exp(-beta * dt) +
            np.random.normal(0, self.imu_params['accel']['bias_instability'] * np.sqrt(2 * beta), 3)
        )
        self.gyro_bias_instability = (
            self.gyro_bias_instability * math.exp(-beta * dt) +
            np.random.normal(0, self.imu_params['gyro']['bias_instability'] * np.sqrt(2 * beta), 3)
        )

        # Calculate noise components
        accel_noise = np.random.normal(0, self.imu_params['accel']['noise_density'] / np.sqrt(dt), 3)
        gyro_noise = np.random.normal(0, self.imu_params['gyro']['noise_density'] / np.sqrt(dt), 3)

        # Apply all noise components
        noisy_accel = (
            true_accel +
            accel_noise +
            self.accel_bias_rw +
            self.accel_bias_instability
        )

        noisy_gyro = (
            true_gyro +
            gyro_noise +
            self.gyro_bias_rw +
            self.gyro_bias_instability
        )

        return noisy_accel, noisy_gyro

    def add_camera_noise(self, image, noise_level=0.01):
        """Add realistic noise to camera images"""
        # Add Gaussian noise
        gaussian_noise = np.random.normal(0, noise_level, image.shape).astype(image.dtype)
        noisy_image = np.clip(image.astype(np.float32) + gaussian_noise * 255, 0, 255).astype(np.uint8)

        # Add some salt and pepper noise
        salt_pepper_prob = 0.001
        random_matrix = np.random.rand(*image.shape[:2])

        noisy_image[random_matrix < salt_pepper_prob/2] = 0  # Salt
        noisy_image[random_matrix > 1 - salt_pepper_prob/2] = 255  # Pepper

        return noisy_image

    def add_lidar_noise(self, ranges, intensity=None):
        """Add realistic noise to LiDAR measurements"""
        # Add distance-dependent noise (noise increases with distance)
        distance_dependent_noise = 0.01 + 0.001 * np.array(ranges)  # 1cm + 0.1% of range
        noise = np.random.normal(0, distance_dependent_noise, len(ranges))

        # Apply noise and ensure positive ranges
        noisy_ranges = np.maximum(0.01, np.array(ranges) + noise)  # Minimum 1cm

        if intensity is not None:
            # Add noise to intensity measurements
            intensity_noise = np.random.normal(0, 0.1, len(intensity))
            noisy_intensity = np.clip(np.array(intensity) + intensity_noise, 0, 1)
            return noisy_ranges, noisy_intensity

        return noisy_ranges
```

## Sensor Fusion Techniques

### Kalman Filter for Multi-Sensor Fusion

For humanoid robots, sensor fusion combines data from multiple sensors to improve perception accuracy:

```python
import numpy as np
from scipy.linalg import block_diag

class SensorFusionKF:
    def __init__(self):
        # State: [x, y, z, vx, vy, vz, roll, pitch, yaw, p_dot, q_dot, r_dot]
        # Position, velocity, orientation, angular velocity
        self.state_dim = 12
        self.state = np.zeros(self.state_dim)

        # Covariance matrix
        self.P = np.eye(self.state_dim) * 1000.0  # Initial uncertainty

        # Process noise
        self.Q = np.eye(self.state_dim) * 0.1

        # Measurement noise for different sensors
        self.R_imu = np.eye(6) * 0.01      # [angular_vel, linear_acc]
        self.R_camera = np.eye(3) * 0.1    # [x, y, z position]
        self.R_lidar = np.eye(3) * 0.05    # [x, y, z position]

        # Time step
        self.dt = 0.01  # 100Hz

    def predict(self, control_input=None):
        """Prediction step of the Kalman filter"""
        # State transition model (simplified)
        F = np.eye(self.state_dim)

        # Position updates based on velocity
        F[0:3, 3:6] = np.eye(3) * self.dt  # position = position + velocity * dt

        # Velocity updates (simplified - no acceleration control input)
        # In a real implementation, you'd include control inputs

        # Orientation updates based on angular velocity
        # This is a simplified model - real implementation would use quaternion math
        F[6:9, 9:12] = np.eye(3) * self.dt  # orientation = orientation + angular_vel * dt

        # Predict state
        self.state = F @ self.state

        # Predict covariance
        self.P = F @ self.P @ F.T + self.Q

    def update_imu(self, measurement):
        """Update with IMU measurement [wx, wy, wz, ax, ay, az]"""
        # Measurement matrix (which state variables are measured by IMU)
        H = np.zeros((6, self.state_dim))
        H[0:3, 9:12] = np.eye(3)  # Angular velocities
        H[3:6, 3:6] = np.eye(3)   # We'll use this for linear acceleration

        # Innovation
        y = measurement - H @ self.state
        S = H @ self.P @ H.T + self.R_imu

        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)

        # Update state and covariance
        self.state = self.state + K @ y
        self.P = (np.eye(self.state_dim) - K @ H) @ self.P

    def update_camera(self, measurement):
        """Update with camera measurement [x, y, z]"""
        # Measurement matrix for position
        H = np.zeros((3, self.state_dim))
        H[0:3, 0:3] = np.eye(3)  # Position measurements

        # Innovation
        y = measurement - H @ self.state
        S = H @ self.P @ H.T + self.R_camera

        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)

        # Update state and covariance
        self.state = self.state + K @ y
        self.P = (np.eye(self.state_dim) - K @ H) @ self.P

    def get_state_estimate(self):
        """Get current state estimate"""
        return self.state.copy(), self.P.copy()

class MultiSensorFusionNode(Node):
    def __init__(self):
        super().__init__('multi_sensor_fusion')

        # Initialize sensor fusion
        self.fusion_filter = SensorFusionKF()

        # Subscribe to different sensors
        self.imu_subscription = self.create_subscription(
            Imu, '/humanoid/imu/data', self.imu_callback, 10
        )

        self.camera_subscription = self.create_subscription(
            Point, '/humanoid/camera/position', self.camera_callback, 10
        )

        # Publisher for fused state
        self.state_publisher = self.create_publisher(
            Point, '/humanoid/fused_state', 10
        )

        # Timer for prediction step
        self.timer = self.create_timer(0.01, self.prediction_step)  # 100Hz

    def imu_callback(self, msg):
        """Process IMU measurement"""
        measurement = np.array([
            msg.angular_velocity.x,  # wx
            msg.angular_velocity.y,  # wy
            msg.angular_velocity.z,  # wz
            msg.linear_acceleration.x,  # ax
            msg.linear_acceleration.y,  # ay
            msg.linear_acceleration.z   # az
        ])

        self.fusion_filter.update_imu(measurement)

    def camera_callback(self, msg):
        """Process camera measurement"""
        measurement = np.array([msg.x, msg.y, msg.z])
        self.fusion_filter.update_camera(measurement)

    def prediction_step(self):
        """Prediction step of the filter"""
        self.fusion_filter.predict()

        # Publish current state estimate
        state, _ = self.fusion_filter.get_state_estimate()
        pos_msg = Point()
        pos_msg.x = state[0]  # x position
        pos_msg.y = state[1]  # y position
        pos_msg.z = state[2]  # z position

        self.state_publisher.publish(pos_msg)
```

## Sensor Validation and Calibration

### Comparing Simulation to Reality

Validating sensor simulation against real hardware is crucial:

```python
class SensorValidator:
    def __init__(self):
        self.simulation_data = []
        self.real_robot_data = []

    def collect_validation_data(self, sim_data, real_data):
        """Collect paired simulation and real robot data"""
        self.simulation_data.append(sim_data)
        self.real_robot_data.append(real_data)

    def calculate_validation_metrics(self):
        """Calculate metrics comparing simulation to real data"""
        if len(self.simulation_data) < 2:
            return None

        sim_array = np.array(self.simulation_data)
        real_array = np.array(self.real_robot_data)

        # Calculate various validation metrics
        metrics = {
            'rmse': np.sqrt(np.mean((sim_array - real_array)**2)),
            'mean_error': np.mean(sim_array - real_array),
            'std_error': np.std(sim_array - real_array),
            'correlation': np.corrcoef(sim_array.flatten(), real_array.flatten())[0, 1]
        }

        return metrics

    def adjust_simulation_parameters(self, metrics):
        """Adjust simulation parameters based on validation results"""
        if metrics['rmse'] > 0.1:  # If error is too high
            # Adjust noise parameters
            pass
        if abs(metrics['mean_error']) > 0.05:  # If bias is too high
            # Adjust bias parameters
            pass

def validate_sensor_models():
    """Example validation process"""
    validator = SensorValidator()

    # This would run in a loop collecting data from both simulation and real robot
    # for sim_data, real_data in zip(simulation_readings, real_readings):
    #     validator.collect_validation_data(sim_data, real_data)

    # metrics = validator.calculate_validation_metrics()
    # if metrics:
    #     validator.adjust_simulation_parameters(metrics)

    print("Sensor validation framework initialized")
```

## Best Practices for Sensor Simulation

### Realistic Parameter Selection

1. **Use Real Sensor Specifications**: Base noise models on actual sensor datasheets
2. **Consider Environmental Factors**: Temperature, humidity, and lighting affect sensors
3. **Validate with Real Data**: Compare simulation output to real sensor readings
4. **Update Models Regularly**: Refine models as more validation data becomes available

### Performance Considerations

1. **Balance Fidelity and Performance**: More realistic models may slow down simulation
2. **Use Appropriate Update Rates**: Match simulation update rates to real sensor rates
3. **Optimize Noise Generation**: Pre-compute noise where possible
4. **Selective Validation**: Focus on critical sensors for the task at hand

### Integration with Control Systems

1. **Maintain Timing Consistency**: Ensure sensor simulation aligns with control loop timing
2. **Implement Sensor Delays**: Add realistic communication and processing delays
3. **Handle Sensor Failures**: Include models for sensor malfunction and recovery
4. **Cross-Validate with Control**: Ensure sensor data supports the intended control strategies

## Looking Ahead

This chapter covered the simulation of various sensor types for humanoid robots, including LiDAR, IMUs, and depth cameras, with realistic noise models and fusion techniques. The next chapter will explore Unity integration for high-fidelity visualization, complementing the physics-based simulation in Gazebo.

## Citations

- Hordur K. Leósson, et al. (2019). "Realistic Sensor Simulation for Robotics using Gazebo." Journal of Field Robotics.
- Siciliano, B., & Khatib, O. (2016). "Springer Handbook of Robotics." Springer.
- Gazebo Team. (2023). "Gazebo Sensor Documentation." http://gazebosim.org/

## Summary

In this chapter, we've explored the simulation of various sensor types crucial for humanoid robotics. We covered LiDAR, IMU, and depth camera simulation with realistic noise models, and discussed sensor fusion techniques that combine multiple sensor inputs. These simulation techniques are essential for developing robust perception and control systems that can transfer effectively from simulation to reality.

## Review Questions/Exercises

1. What are the main sources of noise in IMU sensors and how do you model them?
2. How would you validate that your simulated LiDAR produces realistic data?
3. Design a sensor fusion system that combines IMU, camera, and LiDAR data for humanoid robot localization.
4. What are the computational trade-offs in implementing realistic sensor noise models?
5. Create a complete sensor simulation configuration for a humanoid robot with at least 3 different sensor types.

---
**Chapter Specifications:**
- **Expected Length**: 3,000-4,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using rclpy where applicable for ROS 2 modules
- **Diagrams/Illustrations**: Text-based ASCII or references to images in `/static/img/book/module-X/`
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides