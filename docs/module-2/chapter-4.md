---
id: module-2-chapter-4
sidebar_position: 4
title: "Chapter 4 - Unity for High-Fidelity Robot Visualization"
---

# Chapter 4: Unity for High-Fidelity Robot Visualization

## Learning Objectives
- [X] Set up Unity for robotics visualization and integrate with ROS 2
- [X] Create realistic humanoid robot models and animations in Unity
- [X] Implement ROS-Unity communication for real-time data exchange
- [X] Develop visualization techniques for robotic perception and control data

## Key Concepts
- [X] **Unity Robotics**: Integration of Unity 3D engine with robotics frameworks
- [X] **Real-time Rendering**: High-performance visualization of robot data
- [X] **ROS Integration**: Connecting Unity with ROS 2 for bidirectional communication
- [X] **Perception Visualization**: Visualizing sensor data and perception results
- [X] **Control Feedback**: Displaying control states and robot behavior

## Introduction

Unity has emerged as a powerful platform for high-fidelity robot visualization, offering photorealistic rendering capabilities, sophisticated physics simulation, and intuitive development tools. For humanoid robotics, Unity provides an ideal environment for creating compelling visualizations that bridge the gap between simulation and reality.

Unlike physics-focused simulators like Gazebo, Unity excels in visual quality and user experience, making it perfect for:
- High-fidelity robot visualization and presentation
- Virtual reality (VR) interfaces for robot teleoperation
- Public demonstrations and educational materials
- Advanced perception visualization
- Human-robot interaction studies

This chapter explores how to set up Unity for robotics applications, integrate it with ROS 2, create realistic humanoid robot models, and develop effective visualization techniques for robotic perception and control data.

## Setting Up Unity for Robotics

### Unity Installation and Robotics Package

To get started with Unity for robotics, install Unity Hub and the latest LTS (Long Term Support) version:

1. Download Unity Hub from https://unity3d.com/get-unity/download
2. Through Unity Hub, install Unity 2021.3 LTS or later
3. Install the Unity Robotics Package through the Package Manager

### Unity-ROS Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Unity-ROS Integration                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │
│  │   Physical  │    │   Unity     │    │   ROS Bridge    │ │
│  │   Robot     │◄──►│   Visual-   │◄──►│   Connection    │ │
│  │   (Real/    │    │   ization   │    │   (WebSocket)   │ │
│  │   Sim)      │    │             │    │                 │ │
│  └─────────────┘    └─────────────┘    └─────────────────┘ │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┤
│  │   Sensor Data   │ │   Unity Scene   │ │   ROS Topics    │
│  │   (IMU, LiDAR,  │ │   (3D Models,  │ │   (JointState,  │
│  │   Camera)       │ │   Animation)    │ │   Twist, etc.)  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘
│         │                   │                   │          │
└─────────┼───────────────────┼───────────────────┼──────────┘
          │                   │                   │
          ▼                   ▼                   ▼
   Real Robot State    Visual Feedback      ROS Messages
    or Simulation        & Interaction       Communication
```

### Installing ROS# Package

ROS# (ROS Sharp) is a popular Unity package for ROS integration:

1. Open Unity Package Manager (Window → Package Manager)
2. Add package from git URL: `https://github.com/siemens/ros-sharp.git`
3. Install the following packages:
   - ROSBridgeClient
   - ROSConnection
   - URDF Importer

### Unity Robotics Hub

Alternatively, you can use Unity's official Robotics packages:

```bash
# Add the Robotics package through Unity's Package Manager
# Use the scoped registry: https://unityrobotics.pkgs.visualstudio.com
```

## Creating Humanoid Robot Models in Unity

### Unity Scene Structure for Humanoid Robot Visualization

A typical Unity scene for humanoid robot visualization follows this structure:

```
Main Scene
├── Robot Models
│   ├── Humanoid_Robot (Root GameObject)
│   │   ├── Base_Link (Pelvis)
│   │   │   ├── Head
│   │   │   │   ├── Camera_Link
│   │   │   │   └── IMU_Link
│   │   │   ├── Left_Upper_Arm
│   │   │   │   └── Left_Lower_Arm
│   │   │       └── Left_Hand
│   │   │   ├── Right_Upper_Arm
│   │   │   │   └── Right_Lower_Arm
│   │   │       └── Right_Hand
│   │   │   ├── Left_Thigh
│   │   │   │   └── Left_Shin
│   │   │       └── Left_Foot
│   │   │   └── Right_Thigh
│   │   │       └── Right_Shin
│   │           └── Right_Foot
│   │   └── Joint_Visualization (Helper objects for joint angles)
├── Environment
│   ├── Ground_Plane
│   ├── Lighting
│   │   ├── Directional_Light
│   │   ├── Point_Lights (for indoor scenes)
│   │   └── Reflection_Probe
│   └── Navigation_Mesh
├── Sensor_Visualization
│   ├── LiDAR_Rays
│   ├── Camera_Frustum
│   ├── Depth_Point_Cloud
│   └── Perception_Overlay
├── UI_Canvas
│   ├── Robot_State_Panel
│   ├── Sensor_Data_Panel
│   └── Control_Interface
└── Managers
    ├── ROS_Connection_Manager
    ├── Animation_Controller
    ├── Visualization_Manager
    └── Performance_Monitor
```

#### Text-based Scene Description

Here's a text-based description of a Unity scene for humanoid robot visualization:

```
Scene: HumanoidRobotVisualization
  Description: Real-time visualization of a humanoid robot with ROS integration

  Camera:
    - Main Camera (Perspective, 60 FOV)
      Position: (0, 5, 10)
      Rotation: (15, 0, 0)
      Clear Flags: Skybox
    - Robot Camera (Orthographic)
      Position: (0, 1.5, -3)
      Rotation: (0, 0, 0)
      Size: 2

  Lighting:
    - Directional Light
      Rotation: (50, -30, 0)
      Intensity: 1.0
      Color: (1, 1, 1, 1)
    - Reflection Probe (Box, Center: (0, 1, 0), Size: (10, 10, 10))

  Environment:
    - Ground Plane (Checkerboard texture, Physic Material)
      Position: (0, -0.01, 0)
      Scale: (20, 1, 20)
    - Boundary Walls (Invisible colliders)
    - Skybox Material: Default

  Robot Model (Humanoid_Robot):
    - Base Link (Capsule Collider, mass: 10kg)
      Position: (0, 1, 0)
      Scale: (0.3, 0.25, 0.4)
      Material: Metallic Gray
    - Head (Sphere Collider, mass: 2kg)
      Position: (0, 0.3, 0) relative to base
      Radius: 0.12
      Material: Skin Tone
    - Left Upper Arm (Capsule Collider, mass: 1.5kg)
      Position: (0.175, 0.125, 0.1) relative to base
      Material: Blue
    - Right Upper Arm (Capsule Collider, mass: 1.5kg)
      Position: (0.175, -0.125, 0.1) relative to base
      Material: Blue
    - Left Thigh (Capsule Collider, mass: 3kg)
      Position: (-0.05, 0.08, -0.2) relative to base
      Material: Dark Gray
    - Right Thigh (Capsule Collider, mass: 3kg)
      Position: (-0.05, -0.08, -0.2) relative to base
      Material: Dark Gray

  Sensors:
    - LiDAR Visualization
      GameObject: LiDAR_Rays
      Prefab: RayVisualization
      Position: (0.1, 0.4, 0) relative to base
    - Camera Visualization
      GameObject: Camera_Frustum
      Prefab: FrustumVisualizer
      Position: (0.05, 0, 0) relative to head

  UI:
    - Canvas (Screen Space - Overlay)
      - Robot State Panel
        Position: (10, 10)
        Size: (300, 200)
      - Sensor Data Panel
        Position: (10, 220)
        Size: (300, 400)
      - Control Interface
        Position: (Screen Width - 310, 10)
        Size: (300, 600)

  Scripts:
    - ROSUnityBridge.cs (on Main Camera)
    - HumanoidAnimationController.cs (on Humanoid_Robot)
    - SensorVisualization.cs (on LiDAR_Rays)
    - PerceptionVisualization.cs (on Camera_Frustum)
    - PerformanceMonitor.cs (on Managers object)
```

### Importing Robot Models

Unity supports importing robot models in several ways:

#### Method 1: URDF Import
Unity's URDF Importer can directly import URDF files:

```csharp
using Unity.Robotics.URDF;
using UnityEngine;

public class RobotImporter : MonoBehaviour
{
    [Header("URDF Settings")]
    public string urdfPath;  // Path to URDF file
    public ImportSettings importSettings;

    void Start()
    {
        // Import robot model from URDF
        var robot = URDFRobotExtensions.CreateRobot(urdfPath, importSettings);
        robot.transform.SetParent(transform);
    }
}
```

#### Method 2: Manual Model Creation
For more control, create humanoid models manually:

```csharp
using UnityEngine;

public class HumanoidModelCreator : MonoBehaviour
{
    [Header("Model Parameters")]
    public float bodyHeight = 1.0f;
    public float bodyWidth = 0.3f;
    public float bodyDepth = 0.2f;

    [Header("Joint Configuration")]
    public Transform[] joints;  // Array of joint transforms

    void Start()
    {
        CreateHumanoidModel();
        SetupJoints();
    }

    void CreateHumanoidModel()
    {
        // Create body
        GameObject body = GameObject.CreatePrimitive(PrimitiveType.Cube);
        body.transform.SetParent(transform);
        body.transform.localPosition = Vector3.zero;
        body.transform.localScale = new Vector3(bodyWidth, bodyHeight, bodyDepth);
        body.name = "Body";

        // Create head
        GameObject head = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        head.transform.SetParent(transform);
        head.transform.localPosition = new Vector3(0, bodyHeight / 2 + 0.1f, 0);
        head.transform.localScale = Vector3.one * 0.2f;
        head.name = "Head";

        // Create limbs (simplified)
        CreateLimb("LeftArm", new Vector3(bodyWidth/2 + 0.1f, bodyHeight/4, 0), new Vector3(0.05f, 0.3f, 0.05f));
        CreateLimb("RightArm", new Vector3(-(bodyWidth/2 + 0.1f), bodyHeight/4, 0), new Vector3(0.05f, 0.3f, 0.05f));
        CreateLimb("LeftLeg", new Vector3(bodyWidth/4, -bodyHeight/2 - 0.15f, 0), new Vector3(0.08f, 0.4f, 0.08f));
        CreateLimb("RightLeg", new Vector3(-bodyWidth/4, -bodyHeight/2 - 0.15f, 0), new Vector3(0.08f, 0.4f, 0.08f));
    }

    void CreateLimb(string name, Vector3 position, Vector3 size)
    {
        GameObject limb = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        limb.transform.SetParent(transform);
        limb.transform.localPosition = position;
        limb.transform.localScale = size;
        limb.name = name;

        // Adjust capsule orientation
        if (name.Contains("Leg"))
        {
            limb.transform.rotation = Quaternion.Euler(90, 0, 0);
        }
    }

    void SetupJoints()
    {
        // Add joint components for animation/physics
        foreach (Transform joint in joints)
        {
            ConfigurableJoint jointComponent = joint.gameObject.AddComponent<ConfigurableJoint>();
            SetupJointConstraints(jointComponent);
        }
    }

    void SetupJointConstraints(ConfigurableJoint joint)
    {
        // Configure joint limits and properties
        joint.xMotion = ConfigurableJointMotion.Locked;
        joint.yMotion = ConfigurableJointMotion.Locked;
        joint.zMotion = ConfigurableJointMotion.Locked;

        joint.angularXMotion = ConfigurableJointMotion.Limited;
        joint.angularYMotion = ConfigurableJointMotion.Limited;
        joint.angularZMotion = ConfigurableJointMotion.Limited;
    }
}
```

### Robot Animation and Kinematics

For humanoid robots, implement forward and inverse kinematics:

```csharp
using UnityEngine;

public class HumanoidAnimationController : MonoBehaviour
{
    [Header("Joint References")]
    public Transform head;
    public Transform leftShoulder, rightShoulder;
    public Transform leftElbow, rightElbow;
    public Transform leftWrist, rightWrist;
    public Transform leftHip, rightHip;
    public Transform leftKnee, rightKnee;
    public Transform leftAnkle, rightAnkle;

    [Header("Animation Parameters")]
    public float walkSpeed = 1.0f;
    public float balanceThreshold = 0.1f;

    void Update()
    {
        UpdateAnimations();
    }

    void UpdateAnimations()
    {
        // Update based on robot state received from ROS
        UpdateWalkingAnimation();
        UpdateBalanceCorrection();
        UpdateGestureAnimations();
    }

    void UpdateWalkingAnimation()
    {
        // Simple walking animation based on step timing
        float time = Time.time * walkSpeed;
        float stepOffset = 0.2f;

        // Animate legs
        leftHip.transform.position += new Vector3(0, Mathf.Sin(time) * 0.02f, 0);
        rightHip.transform.position += new Vector3(0, Mathf.Sin(time + Mathf.PI) * 0.02f, 0);

        // Animate arms to counter-balance
        leftShoulder.transform.position += new Vector3(0, Mathf.Sin(time + Mathf.PI) * 0.01f, 0);
        rightShoulder.transform.position += new Vector3(0, Mathf.Sin(time) * 0.01f, 0);
    }

    void UpdateBalanceCorrection()
    {
        // Simple balance correction based on center of mass
        Vector3 com = CalculateCenterOfMass();

        if (Mathf.Abs(com.x) > balanceThreshold)
        {
            // Lean in opposite direction to maintain balance
            transform.Rotate(0, 0, -com.x * 10);
        }
    }

    void UpdateGestureAnimations()
    {
        // Placeholder for gesture animations
        // This would be driven by high-level commands from ROS
    }

    Vector3 CalculateCenterOfMass()
    {
        // Calculate approximate center of mass
        float totalMass = 0;
        Vector3 com = Vector3.zero;

        // Simplified calculation
        foreach(Transform child in transform)
        {
            float mass = 1.0f; // Assume equal mass for simplicity
            com += child.position * mass;
            totalMass += mass;
        }

        return com / totalMass;
    }
}
```

## ROS-Unity Integration

### ROS Bridge Communication

Unity communicates with ROS through ROS Bridge, a WebSocket-based interface:

```csharp
using System.Collections;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;
using RosMessageTypes.Sensor;
using UnityEngine;

public class ROSUnityBridge : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosIPAddress = "127.0.0.1";
    public int rosPort = 9090;

    [Header("Topics")]
    public string jointStateTopic = "/humanoid/joint_states";
    public string sensorDataTopic = "/humanoid/sensor_data";
    public string controlCommandTopic = "/humanoid/command";

    private ROSConnection ros;
    private JointStateMsg latestJointState;

    void Start()
    {
        // Initialize ROS connection
        ros = ROSConnection.instance;
        ros.Initialize(rosIPAddress, rosPort);

        // Subscribe to ROS topics
        ros.Subscribe<JointStateMsg>(jointStateTopic, OnJointStateReceived);
        ros.Subscribe<ImuMsg>(sensorDataTopic, OnImuReceived);

        // Start publishing sensor data
        StartCoroutine(PublishSensorData());
    }

    void OnJointStateReceived(JointStateMsg jointState)
    {
        // Update robot model based on joint state
        latestJointState = jointState;
        UpdateRobotModel();
    }

    void OnImuReceived(ImuMsg imuData)
    {
        // Update visualization based on IMU data
        UpdateImuVisualization(imuData);
    }

    void UpdateRobotModel()
    {
        if (latestJointState == null || latestJointState.name == null) return;

        // Update joint positions in Unity
        for (int i = 0; i < latestJointState.name.Length; i++)
        {
            string jointName = latestJointState.name[i];
            float jointPosition = (float)latestJointState.position[i];

            Transform jointTransform = FindJointByName(jointName);
            if (jointTransform != null)
            {
                // Update joint rotation based on received position
                jointTransform.localRotation = Quaternion.Euler(0, jointPosition * Mathf.Rad2Deg, 0);
            }
        }
    }

    Transform FindJointByName(string name)
    {
        Transform[] allChildren = GetComponentsInChildren<Transform>();
        foreach (Transform child in allChildren)
        {
            if (child.name == name)
                return child;
        }
        return null;
    }

    void UpdateImuVisualization(ImuMsg imuData)
    {
        // Visualize IMU data
        // Convert quaternion to Unity rotation
        Quaternion imuRotation = new Quaternion(
            (float)imuData.orientation.x,
            (float)imuData.orientation.y,
            (float)imuData.orientation.z,
            (float)imuData.orientation.w
        );

        // Apply to robot model or visualization elements
        transform.rotation = imuRotation;
    }

    IEnumerator PublishSensorData()
    {
        while (true)
        {
            // Publish sensor data back to ROS
            var sensorMsg = new ImuMsg();
            sensorMsg.header = new StdMsgs.Header();
            sensorMsg.header.stamp = new TimeStamp(Time.time);
            sensorMsg.header.frame_id = "unity_imu";

            // Convert Unity rotation to ROS quaternion
            sensorMsg.orientation.x = transform.rotation.x;
            sensorMsg.orientation.y = transform.rotation.y;
            sensorMsg.orientation.z = transform.rotation.z;
            sensorMsg.orientation.w = transform.rotation.w;

            // Publish to ROS
            ros.Publish(sensorDataTopic, sensorMsg);

            yield return new WaitForSeconds(0.1f); // 10Hz update
        }
    }

    void OnDestroy()
    {
        if (ros != null)
        {
            ros.Close();
        }
    }
}
```

### Advanced ROS Integration

For more sophisticated robotics applications, implement additional message types:

```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Navigation;
using RosMessageTypes.Actionlib;
using UnityEngine;

public class AdvancedROSIntegration : MonoBehaviour
{
    [Header("Navigation Topics")]
    public string moveBaseTopic = "/move_base_simple/goal";
    public string pathTopic = "/humanoid/path";

    [Header("Action Topics")]
    public string followJointTrajectoryTopic = "/humanoid/follow_joint_trajectory";

    private ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.instance;

        // Subscribe to navigation goals
        ros.Subscribe<GeometryMsgs.PoseStampedMsg>(moveBaseTopic, OnNavigationGoalReceived);

        // Subscribe to action feedback
        ros.Subscribe<ControlMsgs.FollowJointTrajectoryFeedbackMsg>(
            followJointTrajectoryTopic + "/feedback",
            OnTrajectoryFeedbackReceived
        );
    }

    void OnNavigationGoalReceived(GeometryMsgs.PoseStampedMsg goal)
    {
        // Handle navigation goal received from ROS
        Vector3 targetPosition = new Vector3(
            (float)goal.pose.position.x,
            (float)goal.pose.position.y,
            (float)goal.pose.position.z
        );

        // Update visualization for navigation target
        ShowNavigationTarget(targetPosition);
    }

    void OnTrajectoryFeedbackReceived(ControlMsgs.FollowJointTrajectoryFeedbackMsg feedback)
    {
        // Update visualization based on trajectory execution
        float progress = CalculateTrajectoryProgress(feedback);

        // Visualize trajectory execution progress
        UpdateTrajectoryVisualization(progress);
    }

    void ShowNavigationTarget(Vector3 position)
    {
        // Create visualization for navigation target
        GameObject targetVisual = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        targetVisual.transform.position = position;
        targetVisual.transform.localScale = Vector3.one * 0.1f;
        targetVisual.GetComponent<Renderer>().material.color = Color.green;

        // Add a temporary marker
        Destroy(targetVisual, 5.0f);
    }

    float CalculateTrajectoryProgress(ControlMsgs.FollowJointTrajectoryFeedbackMsg feedback)
    {
        // Calculate progress based on trajectory execution
        // Implementation depends on your specific trajectory structure
        return 0.5f; // Placeholder
    }

    void UpdateTrajectoryVisualization(float progress)
    {
        // Update trajectory visualization based on progress
        // This could be a progress bar, color change, etc.
    }
}
```

## Visualization Techniques for Robotics

### Sensor Data Visualization

Visualize sensor data from different modalities:

```csharp
using UnityEngine;
using System.Collections.Generic;

public class SensorVisualization : MonoBehaviour
{
    [Header("Visualization Settings")]
    public Color lidarColor = Color.red;
    public Color cameraFrustumColor = Color.blue;
    public Color depthPointCloudColor = Color.green;

    [Header("Visualization Parameters")]
    public float lidarMaxRange = 10.0f;
    public float pointSize = 0.02f;

    private List<Vector3> lidarPoints = new List<Vector3>();
    private List<GameObject> depthPointCloud = new List<GameObject>();

    public void VisualizeLidarData(float[] ranges, float angleMin, float angleMax)
    {
        // Clear previous lidar visualization
        ClearLidarVisualization();

        float angleIncrement = (angleMax - angleMin) / ranges.Length;

        for (int i = 0; i < ranges.Length; i++)
        {
            if (ranges[i] > 0 && ranges[i] < lidarMaxRange)
            {
                float angle = angleMin + i * angleIncrement;
                Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));
                Vector3 point = transform.position + direction * ranges[i];

                // Create visualization point
                GameObject lidarPoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                lidarPoint.transform.position = point;
                lidarPoint.transform.localScale = Vector3.one * pointSize;
                lidarPoint.GetComponent<Renderer>().material.color = lidarColor;
                lidarPoint.GetComponent<Renderer>().enabled = true;

                // Make it a child of this object for easy cleanup
                lidarPoint.transform.SetParent(transform);

                lidarPoints.Add(point);
            }
        }
    }

    public void VisualizeCameraFrustum(float fov, float aspect, float near, float far)
    {
        // Visualize camera frustum for depth cameras
        Vector3[] frustumCorners = CalculateFrustumCorners(fov, aspect, near, far);

        // Draw frustum lines
        DrawFrustumLines(frustumCorners);
    }

    Vector3[] CalculateFrustumCorners(float fov, float aspect, float near, float far)
    {
        // Calculate frustum corners in camera space
        float tanFov = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad);
        float nearHeight = near * tanFov;
        float nearWidth = nearHeight * aspect;
        float farHeight = far * tanFov;
        float farWidth = farHeight * aspect;

        Vector3[] corners = new Vector3[8];

        // Near plane corners
        corners[0] = new Vector3(-nearWidth, -nearHeight, near); // Bottom-left
        corners[1] = new Vector3(nearWidth, -nearHeight, near);  // Bottom-right
        corners[2] = new Vector3(nearWidth, nearHeight, near);   // Top-right
        corners[3] = new Vector3(-nearWidth, nearHeight, near);  // Top-left

        // Far plane corners
        corners[4] = new Vector3(-farWidth, -farHeight, far); // Bottom-left
        corners[5] = new Vector3(farWidth, -farHeight, far);  // Bottom-right
        corners[6] = new Vector3(farWidth, farHeight, far);   // Top-right
        corners[7] = new Vector3(-farWidth, farHeight, far);  // Top-left

        return corners;
    }

    void DrawFrustumLines(Vector3[] corners)
    {
        // Draw lines connecting frustum corners
        DrawLine(corners[0], corners[1], cameraFrustumColor); // Near bottom
        DrawLine(corners[1], corners[2], cameraFrustumColor); // Near right
        DrawLine(corners[2], corners[3], cameraFrustumColor); // Near top
        DrawLine(corners[3], corners[0], cameraFrustumColor); // Near left

        DrawLine(corners[4], corners[5], cameraFrustumColor); // Far bottom
        DrawLine(corners[5], corners[6], cameraFrustumColor); // Far right
        DrawLine(corners[6], corners[7], cameraFrustumColor); // Far top
        DrawLine(corners[7], corners[4], cameraFrustumColor); // Far left

        // Connect near to far
        DrawLine(corners[0], corners[4], cameraFrustumColor); // Bottom
        DrawLine(corners[1], corners[5], cameraFrustumColor); // Bottom-right
        DrawLine(corners[2], corners[6], cameraFrustumColor); // Top-right
        DrawLine(corners[3], corners[7], cameraFrustumColor); // Top-left
    }

    void DrawLine(Vector3 start, Vector3 end, Color color)
    {
        // Create a line using a cylinder
        Vector3 direction = end - start;
        float distance = direction.magnitude;
        Vector3 center = (start + end) / 2;

        GameObject line = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        line.transform.position = center;
        line.transform.LookAt(end);
        line.transform.localScale = new Vector3(0.01f, distance / 2, 0.01f);

        line.GetComponent<Renderer>().material.color = color;
        line.GetComponent<Renderer>().enabled = true;
        line.transform.SetParent(transform);

        // Remove the caps to make it look like a line
        Destroy(line.GetComponent<CapsuleCollider>());
    }

    public void VisualizeDepthPointCloud(float[,] depthData, int width, int height)
    {
        // Clear previous point cloud
        ClearDepthPointCloud();

        // Create point cloud from depth data
        for (int y = 0; y < height; y += 5) // Sample every 5 pixels for performance
        {
            for (int x = 0; x < width; x += 5)
            {
                float depth = depthData[x, y];

                if (depth > 0 && depth < 10.0f) // Valid depth range
                {
                    // Convert pixel coordinates to 3D world coordinates
                    Vector3 point = PixelTo3D(new Vector2(x, y), depth, width, height);

                    // Create visualization point
                    GameObject pointObj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                    pointObj.transform.position = point;
                    pointObj.transform.localScale = Vector3.one * 0.01f;
                    pointObj.GetComponent<Renderer>().material.color = depthPointCloudColor;
                    pointObj.GetComponent<Renderer>().enabled = true;

                    pointObj.transform.SetParent(transform);
                    depthPointCloud.Add(pointObj);
                }
            }
        }
    }

    Vector3 PixelTo3D(Vector2 pixelCoord, float depth, int width, int height)
    {
        // Convert pixel coordinates to normalized device coordinates
        float xNorm = (pixelCoord.x / width - 0.5f) * 2.0f;
        float yNorm = (pixelCoord.y / height - 0.5f) * 2.0f;

        // Convert to world coordinates (simplified)
        // In practice, you'd use camera intrinsic parameters
        float fov = 60.0f; // Camera FOV
        float tanFov = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad);

        float xWorld = xNorm * depth * tanFov;
        float yWorld = yNorm * depth * tanFov;
        float zWorld = depth;

        return new Vector3(xWorld, yWorld, zWorld);
    }

    void ClearLidarVisualization()
    {
        // Remove all lidar visualization objects
        foreach (var point in lidarPoints)
        {
            // In practice, we'd track and destroy the actual GameObjects
        }
        lidarPoints.Clear();
    }

    void ClearDepthPointCloud()
    {
        // Remove all point cloud objects
        foreach (GameObject point in depthPointCloud)
        {
            if (point != null)
                DestroyImmediate(point);
        }
        depthPointCloud.Clear();
    }
}
```

### Perception Visualization

Visualize perception results like object detection and segmentation:

```csharp
using UnityEngine;
using System.Collections.Generic;

[System.Serializable]
public class DetectedObject
{
    public string className;
    public float confidence;
    public Bounds boundingBox;
    public Vector3 center;
}

public class PerceptionVisualization : MonoBehaviour
{
    [Header("Object Detection Settings")]
    public Color detectionBoxColor = Color.yellow;
    public Color segmentationColor = new Color(1, 0, 0, 0.3f); // Red with 30% opacity

    private List<GameObject> detectionBoxes = new List<GameObject>();
    private List<GameObject> segmentationMasks = new List<GameObject>();

    public void VisualizeObjectDetections(List<DetectedObject> objects)
    {
        // Clear previous detections
        ClearObjectDetections();

        foreach (DetectedObject obj in objects)
        {
            // Create bounding box visualization
            GameObject detectionBox = GameObject.CreatePrimitive(PrimitiveType.Cube);
            detectionBox.transform.position = obj.center;
            detectionBox.transform.localScale = obj.boundingBox.size;
            detectionBox.GetComponent<Renderer>().material.color = detectionBoxColor;
            detectionBox.GetComponent<Renderer>().enabled = true;

            // Add label with class name and confidence
            AddDetectionLabel(detectionBox, obj.className, obj.confidence);

            detectionBox.transform.SetParent(transform);
            detectionBoxes.Add(detectionBox);
        }
    }

    void AddDetectionLabel(GameObject detectionBox, string className, float confidence)
    {
        // Create a text object for the label
        GameObject label = new GameObject("DetectionLabel");
        label.transform.SetParent(detectionBox.transform);
        label.transform.localPosition = new Vector3(0, detectionBox.transform.localScale.y / 2 + 0.1f, 0);

        // Add text component (you might want to use TextMeshPro)
        TextMesh textMesh = label.AddComponent<TextMesh>();
        textMesh.text = $"{className}: {confidence:F2}";
        textMesh.fontSize = 24;
        textMesh.color = Color.white;
        textMesh.anchor = TextAnchor.LowerCenter;
    }

    public void VisualizeSegmentationMask(float[,] segmentationMask, int width, int height)
    {
        // Clear previous segmentation
        ClearSegmentation();

        // Create a mesh or use quads to visualize segmentation
        for (int y = 0; y < height; y += 10) // Sample for performance
        {
            for (int x = 0; x < width; x += 10)
            {
                float classId = segmentationMask[x, y];

                if (classId > 0) // Not background
                {
                    // Create a quad to represent this segmentation region
                    GameObject segQuad = CreateQuad();
                    segQuad.transform.position = new Vector3(x / (float)width, y / (float)height, 0);
                    segQuad.transform.localScale = new Vector3(0.02f, 0.02f, 1);

                    // Color based on class ID
                    Color segColor = GetClassColor((int)classId);
                    segQuad.GetComponent<Renderer>().material.color = segColor;

                    segmentationMasks.Add(segQuad);
                }
            }
        }
    }

    GameObject CreateQuad()
    {
        GameObject quad = new GameObject("SegmentationQuad");
        quad.AddComponent<MeshFilter>();
        quad.AddComponent<MeshRenderer>();

        // Create a simple quad mesh
        Mesh mesh = new Mesh();
        Vector3[] vertices = new Vector3[4]
        {
            new Vector3(-0.5f, -0.5f, 0),
            new Vector3(0.5f, -0.5f, 0),
            new Vector3(-0.5f, 0.5f, 0),
            new Vector3(0.5f, 0.5f, 0)
        };

        int[] triangles = new int[6] { 0, 2, 1, 2, 3, 1 };

        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.RecalculateNormals();

        quad.GetComponent<MeshFilter>().mesh = mesh;

        // Create material
        Material mat = new Material(Shader.Find("Sprites/Default"));
        quad.GetComponent<Renderer>().material = mat;

        return quad;
    }

    Color GetClassColor(int classId)
    {
        // Return color based on class ID
        // In practice, you'd have a defined color palette
        switch (classId % 10)
        {
            case 0: return Color.red;
            case 1: return Color.green;
            case 2: return Color.blue;
            case 3: return Color.yellow;
            case 4: return Color.magenta;
            case 5: return Color.cyan;
            case 6: return Color.gray;
            case 7: return Color.white;
            case 8: return Color.black;
            case 9: return Color.orange;
            default: return Color.white;
        }
    }

    void ClearObjectDetections()
    {
        foreach (GameObject box in detectionBoxes)
        {
            if (box != null)
                DestroyImmediate(box);
        }
        detectionBoxes.Clear();
    }

    void ClearSegmentation()
    {
        foreach (GameObject mask in segmentationMasks)
        {
            if (mask != null)
                DestroyImmediate(mask);
        }
        segmentationMasks.Clear();
    }
}
```

## Performance Optimization for Real-time Visualization

### Level of Detail (LOD) Systems

Implement LOD for complex humanoid robots:

```csharp
using UnityEngine;

public class HumanoidLODSystem : MonoBehaviour
{
    [Header("LOD Settings")]
    public Transform[] lodGroups;  // Different detail levels
    public float[] lodDistances;   // Distances for switching LODs

    [Header("Performance Settings")]
    public int maxLODLevel = 3;
    public float lodTransitionSpeed = 2.0f;

    private int currentLODLevel = 0;

    void Start()
    {
        if (lodDistances.Length != lodGroups.Length)
        {
            Debug.LogError("LOD distances and groups must have the same length");
            enabled = false;
            return;
        }
    }

    void Update()
    {
        UpdateLOD();
    }

    void UpdateLOD()
    {
        // Calculate distance to main camera
        float distance = Vector3.Distance(transform.position, Camera.main.transform.position);

        // Determine appropriate LOD level
        int targetLOD = 0;
        for (int i = 0; i < lodDistances.Length; i++)
        {
            if (distance > lodDistances[i])
            {
                targetLOD = Mathf.Min(i + 1, maxLODLevel);
            }
            else
            {
                break;
            }
        }

        // Smooth transition between LODs
        if (targetLOD != currentLODLevel)
        {
            StartCoroutine(SwitchLOD(targetLOD));
        }
    }

    System.Collections.IEnumerator SwitchLOD(int newLOD)
    {
        // Smoothly transition to new LOD
        float transitionProgress = 0;

        while (transitionProgress < 1)
        {
            transitionProgress += Time.deltaTime * lodTransitionSpeed;

            // Fade out old LOD
            SetLODVisibility(currentLODLevel, 1 - transitionProgress);
            // Fade in new LOD
            SetLODVisibility(newLOD, transitionProgress);

            yield return null;
        }

        // Final state
        for (int i = 0; i < lodGroups.Length; i++)
        {
            lodGroups[i].gameObject.SetActive(i == newLOD);
        }

        currentLODLevel = newLOD;
    }

    void SetLODVisibility(int lodIndex, float alpha)
    {
        if (lodIndex < lodGroups.Length)
        {
            Renderer[] renderers = lodGroups[lodIndex].GetComponentsInChildren<Renderer>();
            foreach (Renderer renderer in renderers)
            {
                Color color = renderer.material.color;
                color.a = alpha;
                renderer.material.color = color;
            }
        }
    }
}
```

### Culling and Occlusion

Implement efficient culling for better performance:

```csharp
using UnityEngine;

public class VisualizationCulling : MonoBehaviour
{
    [Header("Culling Settings")]
    public float maxVisualizationDistance = 50.0f;
    public float minVisualizationDistance = 0.5f;

    [Header("Occlusion Settings")]
    public LayerMask occlusionMask = -1;
    public int raycastResolution = 10;

    private Camera mainCamera;
    private bool isVisualized = true;

    void Start()
    {
        mainCamera = Camera.main;
    }

    void Update()
    {
        UpdateVisualizationVisibility();
    }

    void UpdateVisualizationVisibility()
    {
        if (mainCamera == null)
        {
            mainCamera = Camera.main;
            return;
        }

        Vector3 robotPosition = transform.position;
        Vector3 cameraPosition = mainCamera.transform.position;

        // Distance-based culling
        float distance = Vector3.Distance(robotPosition, cameraPosition);
        if (distance > maxVisualizationDistance || distance < minVisualizationDistance)
        {
            SetVisualizationActive(false);
            return;
        }

        // Line-of-sight culling
        if (IsOccluded(robotPosition, cameraPosition))
        {
            SetVisualizationActive(false);
        }
        else
        {
            SetVisualizationActive(true);
        }
    }

    bool IsOccluded(Vector3 robotPos, Vector3 cameraPos)
    {
        // Cast multiple rays to check for occlusion
        for (int i = 0; i < raycastResolution; i++)
        {
            float angle = (i / (float)raycastResolution) * Mathf.PI * 2;
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));

            RaycastHit hit;
            Vector3 rayStart = robotPos + direction * 0.5f; // Start from robot surface
            Vector3 rayDirection = (cameraPos - rayStart).normalized;

            if (Physics.Raycast(rayStart, rayDirection, out hit,
                Vector3.Distance(cameraPos, rayStart), occlusionMask))
            {
                // If any ray is blocked, consider object occluded
                return true;
            }
        }

        return false;
    }

    void SetVisualizationActive(bool active)
    {
        if (isVisualized != active)
        {
            // Enable/disable visualization components
            Renderer[] renderers = GetComponentsInChildren<Renderer>();
            foreach (Renderer renderer in renderers)
            {
                renderer.enabled = active;
            }

            // Handle other visualization components
            LineRenderer[] lineRenderers = GetComponentsInChildren<LineRenderer>();
            foreach (LineRenderer lineRenderer in lineRenderers)
            {
                lineRenderer.enabled = active;
            }

            isVisualized = active;
        }
    }
}
```

## VR and AR Integration

### Virtual Reality Teleoperation Interface

Create VR interfaces for humanoid robot teleoperation:

```csharp
using UnityEngine;
using UnityEngine.XR;

public class VRTeleoperationInterface : MonoBehaviour
{
    [Header("VR Controllers")]
    public Transform leftController;
    public Transform rightController;
    public Transform headController;

    [Header("Robot Control Mapping")]
    public Transform robotLeftHand;
    public Transform robotRightHand;
    public Transform robotHead;

    [Header("Teleoperation Settings")]
    public float positionScale = 1.0f;
    public float rotationScale = 1.0f;

    void Update()
    {
        UpdateRobotFromVR();
        UpdateVRFromRobot(); // For haptic feedback
    }

    void UpdateRobotFromVR()
    {
        // Map VR controller positions to robot positions
        if (robotLeftHand != null && leftController != null)
        {
            robotLeftHand.position = transform.position +
                (leftController.position - transform.position) * positionScale;
            robotLeftHand.rotation = leftController.rotation *
                Quaternion.Euler(0, 180, 0) * rotationScale; // Adjust for robot coordinate system
        }

        if (robotRightHand != null && rightController != null)
        {
            robotRightHand.position = transform.position +
                (rightController.position - transform.position) * positionScale;
            robotRightHand.rotation = rightController.rotation *
                Quaternion.Euler(0, 180, 0) * rotationScale;
        }

        if (robotHead != null && headController != null)
        {
            robotHead.rotation = headController.rotation;
        }
    }

    void UpdateVRFromRobot()
    {
        // Provide haptic feedback based on robot state
        // This would involve sending force feedback to VR controllers
    }
}
```

## Best Practices for Unity Robotics

### Asset Management

1. **Optimize 3D Models**: Reduce polygon count for real-time performance
2. **Use Appropriate Textures**: Balance visual quality with performance
3. **Implement Streaming**: Load assets dynamically as needed
4. **Use Object Pooling**: Reuse visualization objects instead of creating/destroying

### Communication Optimization

1. **Throttle Message Rates**: Don't overwhelm the connection
2. **Use Efficient Data Types**: Send only necessary data
3. **Implement Compression**: Compress large data like point clouds
4. **Handle Connection Loss**: Gracefully manage network interruptions

### Visualization Design

1. **Color Consistency**: Use consistent colors for different data types
2. **Scale Appropriately**: Ensure visualizations are visible but not overwhelming
3. **Interactive Elements**: Allow users to control visualization parameters
4. **Performance Monitoring**: Monitor frame rates and adjust complexity as needed

## Looking Ahead

This chapter covered Unity integration for high-fidelity robot visualization, including model creation, ROS integration, and advanced visualization techniques. The next chapter will focus on environment and scenario building for comprehensive robot testing.

## Citations

- Unity Technologies. (2023). Unity Robotics Package Documentation. https://github.com/Unity-Technologies/Unity-Robotics-Hub
- ROS# Team. (2023). ROS# Unity Integration. https://github.com/siemens/ros-sharp
- Unity Technologies. (2023). Unity XR Documentation. https://docs.unity3d.com/Packages/com.unity.xr.management

## Summary

In this chapter, we've explored how to set up Unity for robotics visualization, create realistic humanoid robot models, integrate with ROS 2, and develop effective visualization techniques for robotic perception and control data. Unity provides high-fidelity visualization capabilities that complement physics simulation, making it ideal for presentation, education, and human-robot interaction applications.

## Review Questions/Exercises

1. How do you set up ROS-Unity communication for real-time robot control?
2. What are the key differences between Gazebo and Unity for robot visualization?
3. Design a visualization system for a humanoid robot that shows joint angles, sensor data, and perception results.
4. How would you optimize Unity performance for real-time robot visualization?
5. Create a VR interface for teleoperating a humanoid robot using Unity and ROS integration.

---
**Chapter Specifications:**
- **Expected Length**: 3,000-4,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using rclpy where applicable for ROS 2 modules
- **Diagrams/Illustrations**: Text-based ASCII or references to images in `/static/img/book/module-X/`
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides