---
id: module-4-chapter-4
sidebar_position: 4
title: "Chapter 4 - Multi-Modal Perception (Vision + Language + Sensor Fusion)"
---

# Chapter 4: Multi-Modal Perception (Vision + Language + Sensor Fusion)

## Learning Objectives
- [ ] Understand the principles of multi-modal perception in humanoid robotics
- [ ] Implement vision-language models for enhanced environmental understanding
- [ ] Design sensor fusion algorithms that combine multiple modalities
- [ ] Integrate multi-modal perception with language understanding for contextual awareness
- [ ] Evaluate and optimize multi-modal perception systems for real-world deployment

## Key Concepts
- [ ] **Multi-Modal Perception**: Integration of multiple sensory modalities for comprehensive environmental understanding
- [ ] **Vision-Language Models (VLMs)**: AI models that connect visual perception with language understanding
- [ ] **Sensor Fusion**: Combining data from multiple sensors to improve perception accuracy
- [ ] **Cross-Modal Attention**: Attention mechanisms that connect different sensory modalities
- [ ] **Embodied Perception**: Perception systems that understand objects in terms of their affordances and functions
- [ ] **Contextual Scene Understanding**: Understanding scenes in relation to tasks and goals

## Introduction

Multi-modal perception represents a critical advancement in humanoid robotics, enabling robots to understand their environment through the integration of multiple sensory modalities including vision, language, and various sensors. Unlike traditional perception systems that process individual modalities in isolation, multi-modal systems create coherent, contextual understanding by connecting visual information with linguistic concepts and sensor data.

For humanoid robots operating in human environments, multi-modal perception is essential for natural interaction and task execution. These robots must understand not only what objects look like but also what they are called, how they are used, and how they relate to human intentions expressed in language. This requires sophisticated integration of computer vision, natural language processing, and sensor fusion techniques.

The chapter explores the architecture of multi-modal perception systems, focusing on vision-language models that connect visual perception with language understanding. We'll examine how these systems can be enhanced with additional sensor modalities to create comprehensive environmental awareness that supports both cognitive planning and natural human-robot interaction.

Multi-modal perception systems enable humanoid robots to perform complex tasks that require understanding of both visual scenes and linguistic commands. For example, when a human says "Please bring me the red cup from the kitchen counter," the robot must integrate visual perception to identify the cup, spatial reasoning to navigate to the kitchen, and language understanding to connect the linguistic description with visual features.

## Vision-Language Model Integration

### Overview of Vision-Language Models

Vision-Language Models (VLMs) represent a significant breakthrough in AI, enabling machines to connect visual content with linguistic concepts. These models learn joint representations of images and text during training, allowing them to perform tasks like image captioning, visual question answering, and image-text matching with remarkable accuracy.

For humanoid robotics, VLMs provide the foundation for understanding objects in both visual and linguistic contexts. This enables robots to recognize objects based on natural language descriptions, understand scenes in terms of their functional layout, and connect perceptual information with human communication.

The most prominent VLM architectures include:

**CLIP (Contrastive Language-Image Pretraining)**: Learns visual concepts through natural language supervision by training on millions of image-text pairs.

**BLIP (Bootstrapping Language-Image Pretraining)**: Unifies vision-language understanding and generation tasks in a single framework.

**Flamingo**: A multimodal model that can understand images and text in context.

### CLIP Integration for Robotics

CLIP has proven particularly valuable for robotics applications due to its ability to recognize objects in images based on text descriptions without requiring task-specific training. This zero-shot capability allows robots to identify objects they may not have encountered during training, as long as they can be described in natural language.

```python
# CLIP integration for robotic perception
import torch
import clip
from PIL import Image
import numpy as np
import cv2
from typing import List, Dict, Any

class VisionLanguagePerceptor:
    def __init__(self, model_name="ViT-B/32"):
        """
        Initialize CLIP-based vision-language perceptor
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess = clip.load(model_name, device=self.device)

        # Common object categories for robotics
        self.robotic_objects = [
            "a photo of a cup",
            "a photo of a book",
            "a photo of a ball",
            "a photo of a chair",
            "a photo of a table",
            "a photo of a bottle",
            "a photo of a phone",
            "a photo of keys",
            "a photo of a computer",
            "a photo of a remote",
            "a photo of a paper",
            "a photo of a box",
            "a photo of a plant",
            "a photo of a person",
            "a photo of a door",
            "a photo of a window"
        ]

        # Precompute embeddings for common objects
        self.object_embeddings = self.compute_text_embeddings(self.robotic_objects)

    def compute_text_embeddings(self, texts: List[str]) -> torch.Tensor:
        """
        Compute embeddings for text descriptions
        """
        text_tokens = clip.tokenize(texts).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features

    def recognize_objects(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Recognize objects in image using CLIP
        """
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            # Calculate similarity between image and text embeddings
            logits_per_image = (100.0 * image_features @ self.object_embeddings.T).softmax(dim=-1)
            probs = logits_per_image.cpu().numpy()[0]

        # Get top predictions
        top_indices = np.argsort(probs)[::-1][:5]  # Top 5 predictions
        predictions = []

        for idx in top_indices:
            if probs[idx] > 0.01:  # Only include predictions with confidence > 1%
                object_name = self.robotic_objects[idx].replace("a photo of a ", "").replace("a photo of ", "")
                predictions.append({
                    'object': object_name,
                    'confidence': float(probs[idx]),
                    'category_index': int(idx)
                })

        return predictions

    def find_object_by_description(self, image_path: str, description: str) -> float:
        """
        Find how well an image matches a text description
        """
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        text_tokens = clip.tokenize([f"a photo of {description}"]).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(text_tokens)

            # Normalize features
            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)

            # Calculate similarity
            similarity = (image_features @ text_features.T).item()

        return similarity

    def describe_scene(self, image_path: str) -> str:
        """
        Generate a natural language description of a scene
        """
        # For now, we'll use object recognition results to generate a simple description
        # In practice, you'd use more sophisticated models like BLIP for image captioning
        objects = self.recognize_objects(image_path)

        if not objects:
            return "The scene contains no recognizable objects."

        # Filter by confidence
        confident_objects = [obj for obj in objects if obj['confidence'] > 0.05]

        if not confident_objects:
            return "The scene contains objects with low recognition confidence."

        # Create description
        object_names = [obj['object'] for obj in confident_objects]
        if len(object_names) == 1:
            return f"The scene contains a {object_names[0]}."
        elif len(object_names) == 2:
            return f"The scene contains a {object_names[0]} and a {object_names[1]}."
        else:
            return f"The scene contains: {', '.join(object_names[:-1])}, and a {object_names[-1]}."

class ObjectDetectorWithLanguage:
    def __init__(self, vision_language_perceptor: VisionLanguagePerceptor):
        """
        Object detection enhanced with language understanding
        """
        self.vlp = vision_language_perceptor
        self.spatial_reasoner = SpatialReasoner()

    def detect_and_identify_objects(self, image_path: str, environment_context: Dict = None) -> List[Dict[str, Any]]:
        """
        Detect and identify objects with spatial and contextual information
        """
        # Get CLIP-based object recognition
        clip_detections = self.vlp.recognize_objects(image_path)

        # Enhance with spatial information (in a real system, you'd use an actual object detector)
        enhanced_detections = []

        for detection in clip_detections:
            # Add spatial context if available
            spatial_info = self.spatial_reasoner.get_spatial_context(detection['object'], environment_context)

            enhanced_detection = {
                'object': detection['object'],
                'confidence': detection['confidence'],
                'spatial_context': spatial_info,
                'affordances': self.get_object_affordances(detection['object']),
                'action_potential': self.get_action_potential(detection['object'])
            }

            enhanced_detections.append(enhanced_detection)

        return enhanced_detections

    def get_object_affordances(self, object_name: str) -> List[str]:
        """
        Get possible actions (affordances) for an object
        """
        affordance_map = {
            'cup': ['grasp', 'lift', 'move', 'place', 'fill', 'empty'],
            'book': ['grasp', 'lift', 'move', 'place', 'open', 'close', 'read'],
            'ball': ['grasp', 'lift', 'move', 'place', 'throw', 'roll'],
            'chair': ['move', 'sit_on', 'approach'],
            'table': ['approach', 'navigate_around', 'place_objects_on'],
            'bottle': ['grasp', 'lift', 'move', 'place', 'open', 'close', 'pour'],
            'phone': ['grasp', 'lift', 'move', 'place', 'answer', 'call'],
            'keys': ['grasp', 'lift', 'move', 'place', 'unlock', 'lock']
        }

        return affordance_map.get(object_name.lower(), ['grasp', 'move', 'place'])

    def get_action_potential(self, object_name: str) -> str:
        """
        Get the functional potential of an object
        """
        function_map = {
            'cup': 'container for liquids',
            'book': 'information storage and retrieval',
            'ball': 'play and movement',
            'chair': 'seating and support',
            'table': 'surface for placing objects',
            'bottle': 'container for liquids',
            'phone': 'communication device',
            'keys': 'access control'
        }

        return function_map.get(object_name.lower(), 'general object')
```

### BLIP Integration for Scene Understanding

While CLIP excels at object recognition based on text descriptions, BLIP (Bootstrapping Language-Image Pretraining) provides more sophisticated image understanding capabilities including image captioning and visual question answering. For humanoid robots, these capabilities enable more detailed scene understanding and contextual awareness.

```python
# BLIP integration for advanced scene understanding
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

class BLIPSceneUnderstanding:
    def __init__(self):
        """
        Initialize BLIP for scene understanding
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(self.device)

    def generate_caption(self, image_path: str) -> str:
        """
        Generate a caption for an image
        """
        raw_image = Image.open(image_path).convert('RGB')

        # Generate caption
        inputs = self.processor(raw_image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            out = self.model.generate(**inputs, max_length=50)

        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption

    def answer_visual_question(self, image_path: str, question: str) -> str:
        """
        Answer a question about an image
        """
        raw_image = Image.open(image_path).convert('RGB')

        # Prepare inputs for VQA
        inputs = self.processor(raw_image, question, return_tensors="pt").to(self.device)

        with torch.no_grad():
            out = self.model.generate(**inputs)

        answer = self.processor.decode(out[0], skip_special_tokens=True)
        return answer

class IntegratedVisionLanguageSystem:
    def __init__(self):
        """
        Integrated system combining CLIP and BLIP capabilities
        """
        self.clip_perceptor = VisionLanguagePerceptor()
        self.blip_understanding = BLIPSceneUnderstanding()
        self.scene_memory = {}  # Store scene understanding for context

    def understand_scene(self, image_path: str, context: Dict = None) -> Dict[str, Any]:
        """
        Comprehensive scene understanding using both CLIP and BLIP
        """
        # Get object recognition from CLIP
        objects = self.clip_perceptor.recognize_objects(image_path)

        # Get scene description from BLIP
        caption = self.blip_understanding.generate_caption(image_path)

        # Combine information
        scene_understanding = {
            'objects': objects,
            'scene_caption': caption,
            'spatial_relationships': self.extract_spatial_relationships(objects, image_path),
            'contextual_awareness': self.enhance_with_context(objects, caption, context)
        }

        # Store in memory for future reference
        self.scene_memory[image_path] = scene_understanding

        return scene_understanding

    def extract_spatial_relationships(self, objects: List[Dict], image_path: str) -> List[Dict[str, Any]]:
        """
        Extract spatial relationships between objects (simplified implementation)
        """
        # In a real implementation, this would use object detection bounding boxes
        # to determine spatial relationships
        relationships = []

        if len(objects) > 1:
            # Example relationships (in practice, you'd use actual position data)
            relationships.append({
                'subject': objects[0]['object'],
                'relation': 'near',
                'object': objects[1]['object'],
                'confidence': min(objects[0]['confidence'], objects[1]['confidence'])
            })

        return relationships

    def enhance_with_context(self, objects: List[Dict], caption: str, context: Dict) -> Dict[str, Any]:
        """
        Enhance scene understanding with contextual information
        """
        enhanced_context = {
            'location_hints': self.extract_location_hints(caption),
            'activity_inference': self.infer_activity(caption),
            'object_relevance': self.rank_object_relevance(objects, context)
        }

        return enhanced_context

    def extract_location_hints(self, caption: str) -> List[str]:
        """
        Extract location information from caption
        """
        location_keywords = ['kitchen', 'living room', 'bedroom', 'office', 'dining', 'bathroom', 'hallway']
        found_locations = []

        for keyword in location_keywords:
            if keyword in caption.lower():
                found_locations.append(keyword)

        return found_locations

    def infer_activity(self, caption: str) -> str:
        """
        Infer likely activities from scene caption
        """
        activity_keywords = {
            'cooking': ['kitchen', 'food', 'cooking', 'stove', 'oven'],
            'reading': ['book', 'library', 'desk', 'reading'],
            'relaxing': ['sofa', 'couch', 'tv', 'relaxing'],
            'working': ['computer', 'desk', 'office', 'working'],
            'dining': ['table', 'food', 'dining', 'eating']
        }

        for activity, keywords in activity_keywords.items():
            if any(keyword in caption.lower() for keyword in keywords):
                return activity

        return 'unknown'

    def rank_object_relevance(self, objects: List[Dict], context: Dict) -> Dict[str, float]:
        """
        Rank objects by relevance to current context
        """
        if not context:
            return {obj['object']: obj['confidence'] for obj in objects}

        relevance_scores = {}
        task_context = context.get('current_task', '').lower()

        for obj in objects:
            relevance = obj['confidence']

            # Boost relevance if object is mentioned in task
            if obj['object'].lower() in task_context:
                relevance *= 2.0

            # Boost relevance based on affordances matching task needs
            affordances = self.get_object_affordances(obj['object'])
            if any(affordance in task_context for affordance in affordances):
                relevance *= 1.5

            relevance_scores[obj['object']] = min(relevance, 1.0)  # Cap at 1.0

        return relevance_scores

    def get_object_affordances(self, object_name: str) -> List[str]:
        """
        Get possible actions (affordances) for an object
        """
        affordance_map = {
            'cup': ['grasp', 'lift', 'move', 'place', 'fill', 'empty'],
            'book': ['grasp', 'lift', 'move', 'place', 'open', 'close', 'read'],
            'ball': ['grasp', 'lift', 'move', 'place', 'throw', 'roll'],
            'chair': ['move', 'sit_on', 'approach'],
            'table': ['approach', 'navigate_around', 'place_objects_on'],
            'bottle': ['grasp', 'lift', 'move', 'place', 'open', 'close', 'pour'],
            'phone': ['grasp', 'lift', 'move', 'place', 'answer', 'call'],
            'keys': ['grasp', 'lift', 'move', 'place', 'unlock', 'lock']
        }

        return affordance_map.get(object_name.lower(), ['grasp', 'move', 'place'])
```

## Sensor Fusion Techniques

### Multi-Sensor Integration Architecture

Sensor fusion in multi-modal perception systems combines data from various sensors including cameras, LiDAR, IMU, force/torque sensors, and more. The goal is to create a more robust and accurate understanding of the environment than any single sensor could provide.

The fusion process typically occurs at different levels:

**Data Level Fusion**: Combining raw sensor measurements before processing.

**Feature Level Fusion**: Combining extracted features from different sensors.

**Decision Level Fusion**: Combining decisions or interpretations from different sensors.

For humanoid robots, sensor fusion must account for the robot's mobility, changing viewpoints, and the need to maintain consistent spatial understanding across time.

```python
# Multi-sensor fusion system
import numpy as np
from scipy.spatial.transform import Rotation as R
from typing import Dict, List, Any, Tuple
import threading
import time

class SensorFusionSystem:
    def __init__(self):
        """
        Initialize multi-sensor fusion system
        """
        self.sensors = {
            'camera': {'type': 'camera', 'timestamp': 0, 'data': None},
            'lidar': {'type': 'lidar', 'timestamp': 0, 'data': None},
            'imu': {'type': 'imu', 'timestamp': 0, 'data': None},
            'force_torque': {'type': 'force_torque', 'timestamp': 0, 'data': None}
        }

        self.fusion_results = {}
        self.spatial_transformer = SpatialTransformer()
        self.uncertainty_estimator = UncertaintyEstimator()

        # Thread for continuous fusion
        self.fusion_thread = None
        self.running = False

    def start_fusion_loop(self):
        """
        Start continuous sensor fusion in a separate thread
        """
        self.running = True
        self.fusion_thread = threading.Thread(target=self.fusion_loop)
        self.fusion_thread.start()

    def stop_fusion_loop(self):
        """
        Stop the fusion loop
        """
        self.running = False
        if self.fusion_thread:
            self.fusion_thread.join()

    def fusion_loop(self):
        """
        Continuous fusion loop
        """
        while self.running:
            # Check if we have new sensor data
            if self.have_new_sensor_data():
                self.perform_fusion()

            time.sleep(0.01)  # 100Hz fusion rate

    def have_new_sensor_data(self) -> bool:
        """
        Check if any sensor has new data
        """
        current_time = time.time()
        for sensor_name, sensor_info in self.sensors.items():
            if sensor_info['data'] is not None and sensor_info['timestamp'] > current_time - 0.1:
                return True
        return False

    def update_sensor_data(self, sensor_name: str, data: Any, timestamp: float = None):
        """
        Update sensor data
        """
        if sensor_name in self.sensors:
            self.sensors[sensor_name]['data'] = data
            self.sensors[sensor_name]['timestamp'] = timestamp or time.time()
        else:
            print(f"Unknown sensor: {sensor_name}")

    def perform_fusion(self):
        """
        Perform sensor fusion
        """
        # Get current sensor data
        camera_data = self.sensors['camera']['data']
        lidar_data = self.sensors['lidar']['data']
        imu_data = self.sensors['imu']['data']

        # Perform fusion based on available sensors
        fusion_result = {}

        if camera_data is not None and lidar_data is not None:
            # Camera-LiDAR fusion
            fusion_result.update(self.fuse_camera_lidar(camera_data, lidar_data))

        if camera_data is not None and imu_data is not None:
            # Camera-IMU fusion for pose estimation
            fusion_result.update(self.fuse_camera_imu(camera_data, imu_data))

        # Update fusion results
        self.fusion_results = fusion_result

    def fuse_camera_lidar(self, camera_data: Any, lidar_data: Any) -> Dict[str, Any]:
        """
        Fuse camera and LiDAR data
        """
        # Project LiDAR points to camera image
        projected_points = self.project_lidar_to_camera(lidar_data, camera_data)

        # Associate 3D points with 2D image features
        associations = self.associate_points_features(projected_points, camera_data)

        # Create fused object detections
        fused_detections = self.create_fused_detections(associations, lidar_data, camera_data)

        return {
            'fused_detections': fused_detections,
            'spatial_map': self.create_spatial_map(lidar_data, camera_data),
            'confidence_map': self.estimate_fusion_confidence(associations)
        }

    def project_lidar_to_camera(self, lidar_data: Any, camera_data: Any) -> List[Tuple[float, float, float]]:
        """
        Project LiDAR points to camera image coordinates
        """
        # This would involve the camera intrinsic and extrinsic parameters
        # For this example, we'll return a simplified projection
        if hasattr(lidar_data, 'points'):
            points_3d = lidar_data.points
        else:
            # Simulated LiDAR data
            points_3d = np.random.rand(100, 3) * 10  # 100 random points in 10m cube

        # Simulated camera projection (simplified)
        # In reality, you'd use camera calibration parameters
        projected_points = []
        for point in points_3d:
            # Simple pinhole camera model (simplified)
            x, y, z = point
            if z > 0:  # Only points in front of camera
                u = (x * 500) / z + 320  # fx = 500, cx = 320
                v = (y * 500) / z + 240  # fy = 500, cy = 240
                projected_points.append((u, v, z))  # (image_x, image_y, depth)

        return projected_points

    def associate_points_features(self, projected_points: List, camera_data: Any) -> List[Dict]:
        """
        Associate LiDAR points with camera image features
        """
        associations = []

        # In a real system, this would match LiDAR points with image features
        # For this example, we'll create simple associations
        for i, (u, v, depth) in enumerate(projected_points):
            if 0 <= u < 640 and 0 <= v < 480:  # Within image bounds (assuming 640x480 image)
                associations.append({
                    'lidar_idx': i,
                    'image_coords': (u, v),
                    'depth': depth,
                    'confidence': 0.8  # Simulated confidence
                })

        return associations

    def create_fused_detections(self, associations: List[Dict], lidar_data: Any, camera_data: Any) -> List[Dict]:
        """
        Create fused object detections from associations
        """
        # This would combine object detections from camera with 3D information from LiDAR
        # For this example, we'll simulate fused detections
        fused_detections = []

        # Group associated points by proximity to form objects
        if associations:
            # Simple clustering of points (in reality, use more sophisticated clustering)
            clusters = self.cluster_associations(associations)

            for i, cluster in enumerate(clusters):
                if len(cluster) > 3:  # At least 3 points to form an object
                    # Calculate object properties from cluster
                    avg_depth = np.mean([assoc['depth'] for assoc in cluster])
                    avg_coords = np.mean([assoc['image_coords'] for assoc in cluster], axis=0)

                    fused_detections.append({
                        'id': i,
                        'type': 'object',  # Would be classified in real system
                        'position_3d': [avg_coords[0], avg_coords[1], avg_depth],
                        'position_2d': avg_coords.tolist(),
                        'size': len(cluster),
                        'confidence': 0.8,
                        'sensor_sources': ['camera', 'lidar']
                    })

        return fused_detections

    def cluster_associations(self, associations: List[Dict]) -> List[List[Dict]]:
        """
        Simple clustering of associations
        """
        clusters = []
        used_indices = set()

        for i, assoc1 in enumerate(associations):
            if i in used_indices:
                continue

            cluster = [assoc1]
            used_indices.add(i)

            for j, assoc2 in enumerate(associations[i+1:], i+1):
                if j in used_indices:
                    continue

                # Simple distance check in image coordinates
                dist = np.sqrt((assoc1['image_coords'][0] - assoc2['image_coords'][0])**2 +
                              (assoc1['image_coords'][1] - assoc2['image_coords'][1])**2)

                if dist < 50:  # Within 50 pixels
                    cluster.append(assoc2)
                    used_indices.add(j)

            clusters.append(cluster)

        return clusters

    def fuse_camera_imu(self, camera_data: Any, imu_data: Any) -> Dict[str, Any]:
        """
        Fuse camera and IMU data for improved pose estimation
        """
        # Get pose from IMU (orientation)
        imu_orientation = self.extract_orientation_from_imu(imu_data)

        # Use camera for position (if using visual odometry)
        camera_position = self.extract_position_from_camera(camera_data)

        # Combine for full 6DOF pose
        combined_pose = {
            'position': camera_position,
            'orientation': imu_orientation,
            'timestamp': time.time()
        }

        return {
            'refined_pose': combined_pose,
            'pose_uncertainty': self.estimate_pose_uncertainty(imu_data, camera_data)
        }

    def extract_orientation_from_imu(self, imu_data: Any) -> List[float]:
        """
        Extract orientation from IMU data
        """
        # Simulated IMU data processing
        if hasattr(imu_data, 'orientation'):
            return [imu_data.orientation.x, imu_data.orientation.y, imu_data.orientation.z, imu_data.orientation.w]
        else:
            # Return identity quaternion if no orientation data
            return [0, 0, 0, 1]

    def extract_position_from_camera(self, camera_data: Any) -> List[float]:
        """
        Extract position from camera data (using visual odometry)
        """
        # This would use visual odometry techniques
        # For simulation, return origin
        return [0, 0, 0]

    def estimate_pose_uncertainty(self, imu_data: Any, camera_data: Any) -> Dict[str, float]:
        """
        Estimate uncertainty in pose estimation
        """
        # Simulated uncertainty estimation
        return {
            'position_uncertainty': 0.05,  # 5cm
            'orientation_uncertainty': 0.1  # 0.1 radians
        }

    def create_spatial_map(self, lidar_data: Any, camera_data: Any) -> Dict[str, Any]:
        """
        Create spatial map from fused sensor data
        """
        # This would create an occupancy grid or point cloud map
        # For this example, we'll return a simplified representation
        return {
            'occupied_cells': [],  # List of occupied grid cells
            'free_space': [],      # List of free space cells
            'unknown_space': [],   # List of unknown space cells
            'resolution': 0.1      # 10cm resolution
        }

    def estimate_fusion_confidence(self, associations: List[Dict]) -> np.ndarray:
        """
        Estimate confidence for each pixel/region based on sensor fusion
        """
        # Create a confidence map (simulated)
        confidence_map = np.ones((480, 640)) * 0.5  # Default confidence

        for assoc in associations:
            u, v = int(assoc['image_coords'][0]), int(assoc['image_coords'][1])
            if 0 <= u < 640 and 0 <= v < 480:
                confidence_map[v, u] = assoc['confidence']

        return confidence_map

class SpatialTransformer:
    def __init__(self):
        """
        Handle spatial transformations between different sensor frames
        """
        self.transforms = {}  # Store transformation matrices

    def set_transform(self, from_frame: str, to_frame: str, transform_matrix: np.ndarray):
        """
        Set transformation between two frames
        """
        key = f"{from_frame}_to_{to_frame}"
        self.transforms[key] = transform_matrix

    def transform_point(self, point: np.ndarray, from_frame: str, to_frame: str) -> np.ndarray:
        """
        Transform a point from one frame to another
        """
        key = f"{from_frame}_to_{to_frame}"
        if key in self.transforms:
            transform = self.transforms[key]
            # Apply transformation: [R|t] where R is 3x3 rotation, t is 3x1 translation
            point_h = np.append(point, 1)  # Homogeneous coordinates
            transformed = transform @ point_h
            return transformed[:3]  # Return 3D coordinates
        else:
            # No transform found, return original point
            return point

class UncertaintyEstimator:
    def __init__(self):
        """
        Estimate uncertainty in sensor measurements and fusion results
        """
        pass

    def estimate_sensor_uncertainty(self, sensor_type: str, measurement: Any) -> float:
        """
        Estimate uncertainty for a sensor measurement
        """
        # Different sensors have different uncertainty characteristics
        uncertainty_map = {
            'camera': 0.05,    # 5cm for depth from stereo
            'lidar': 0.02,     # 2cm for distance measurement
            'imu': 0.01,       # 0.01 rad for orientation
            'force_torque': 0.1 # 0.1 N for force
        }

        return uncertainty_map.get(sensor_type, 0.1)

    def combine_uncertainties(self, uncertainties: List[float]) -> float:
        """
        Combine multiple uncertainties (using root-sum-square method)
        """
        return np.sqrt(sum(u**2 for u in uncertainties))
```

### Kalman Filtering for Sensor Fusion

Kalman filtering provides an optimal way to combine measurements from multiple sensors with different noise characteristics. For humanoid robots, this is particularly important for maintaining accurate state estimates while walking and manipulating objects.

```python
# Kalman filter implementation for sensor fusion
import numpy as np
from typing import Tuple

class KalmanFilter:
    def __init__(self, state_dim: int, measurement_dim: int):
        """
        Initialize Kalman filter
        """
        self.state_dim = state_dim
        self.measurement_dim = measurement_dim

        # State vector [x, y, z, vx, vy, vz] for position and velocity
        self.x = np.zeros(state_dim)  # State estimate

        # Error covariance matrix
        self.P = np.eye(state_dim) * 1000  # Initial uncertainty

        # Process noise covariance
        self.Q = np.eye(state_dim) * 0.1

        # Measurement noise covariance
        self.R = np.eye(measurement_dim) * 1.0

        # State transition model (for constant velocity model)
        self.F = self.create_state_transition_matrix()

        # Measurement model
        self.H = self.create_measurement_matrix()

    def create_state_transition_matrix(self) -> np.ndarray:
        """
        Create state transition matrix for constant velocity model
        """
        dt = 0.01  # Time step (100Hz)
        F = np.eye(self.state_dim)

        # For a 6D state [x, y, z, vx, vy, vz]
        if self.state_dim >= 6:
            # Update positions based on velocities
            F[0, 3] = dt  # x += vx * dt
            F[1, 4] = dt  # y += vy * dt
            F[2, 5] = dt  # z += vz * dt

        return F

    def create_measurement_matrix(self) -> np.ndarray:
        """
        Create measurement matrix
        """
        # For measuring position only (not velocity)
        H = np.zeros((self.measurement_dim, self.state_dim))
        for i in range(min(self.measurement_dim, self.state_dim//2)):
            H[i, i] = 1  # Measure position components

        return H

    def predict(self):
        """
        Prediction step of Kalman filter
        """
        # Predict state: x = F * x
        self.x = self.F @ self.x

        # Predict error covariance: P = F * P * F^T + Q
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, measurement: np.ndarray):
        """
        Update step of Kalman filter
        """
        # Innovation: y = z - H * x
        innovation = measurement - self.H @ self.x

        # Innovation covariance: S = H * P * H^T + R
        S = self.H @ self.P @ self.H.T + self.R

        # Kalman gain: K = P * H^T * S^(-1)
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # Update state: x = x + K * y
        self.x = self.x + K @ innovation

        # Update error covariance: P = (I - K * H) * P
        I = np.eye(self.state_dim)
        self.P = (I - K @ self.H) @ self.P

    def get_state(self) -> np.ndarray:
        """
        Get current state estimate
        """
        return self.x.copy()

class MultiModalKalmanFilter:
    def __init__(self):
        """
        Multi-modal Kalman filter that handles different sensor types
        """
        # Separate filters for different modalities
        self.position_filter = KalmanFilter(state_dim=6, measurement_dim=3)  # x, y, z + velocities
        self.orientation_filter = KalmanFilter(state_dim=4, measurement_dim=4)  # quaternion
        self.confidence_scores = {}

    def process_camera_measurement(self, position: np.ndarray, timestamp: float):
        """
        Process position measurement from camera
        """
        # Update position filter
        self.position_filter.predict()
        self.position_filter.update(position)

        # Update confidence based on measurement quality
        self.confidence_scores['camera'] = self.estimate_measurement_confidence(position, 'camera')

    def process_lidar_measurement(self, position: np.ndarray, timestamp: float):
        """
        Process position measurement from LiDAR
        """
        # Update position filter
        self.position_filter.predict()
        self.position_filter.update(position)

        # LiDAR typically has higher accuracy for position
        self.confidence_scores['lidar'] = self.estimate_measurement_confidence(position, 'lidar')

    def process_imu_measurement(self, orientation: np.ndarray, timestamp: float):
        """
        Process orientation measurement from IMU
        """
        # Update orientation filter
        self.orientation_filter.predict()
        self.orientation_filter.update(orientation)

        self.confidence_scores['imu'] = self.estimate_measurement_confidence(orientation, 'imu')

    def estimate_measurement_confidence(self, measurement: np.ndarray, sensor_type: str) -> float:
        """
        Estimate confidence in a measurement
        """
        # Different sensors have different reliability characteristics
        if sensor_type == 'lidar':
            # LiDAR is very reliable for distance measurements
            return 0.9
        elif sensor_type == 'camera':
            # Camera reliability depends on lighting, texture, etc.
            return 0.7
        elif sensor_type == 'imu':
            # IMU is reliable for orientation but can drift
            return 0.8
        else:
            return 0.5  # Default confidence

    def get_fused_state(self) -> Dict[str, np.ndarray]:
        """
        Get fused state from all filters
        """
        return {
            'position': self.position_filter.get_state()[:3],
            'velocity': self.position_filter.get_state()[3:],
            'orientation': self.orientation_filter.get_state(),
            'position_uncertainty': np.diag(self.position_filter.P[:3, :3]),
            'orientation_uncertainty': np.diag(self.orientation_filter.P)
        }

class AdaptiveSensorFusion:
    def __init__(self):
        """
        Adaptive sensor fusion that adjusts based on sensor reliability
        """
        self.kalman_filter = MultiModalKalmanFilter()
        self.sensor_reliability = {
            'camera': 0.7,
            'lidar': 0.9,
            'imu': 0.8
        }
        self.adaptation_history = []

    def adapt_to_environment(self, environment_conditions: Dict[str, float]):
        """
        Adapt fusion parameters based on environment conditions
        """
        # Adjust reliability based on conditions
        if environment_conditions.get('lighting', 1.0) < 0.3:  # Poor lighting
            self.sensor_reliability['camera'] *= 0.5

        if environment_conditions.get('texture', 1.0) < 0.2:  # Low texture
            self.sensor_reliability['camera'] *= 0.7

        if environment_conditions.get('dynamic_objects', 0) > 5:  # Many moving objects
            self.sensor_reliability['lidar'] *= 0.8  # Moving objects may affect LiDAR

        # Record adaptation
        self.adaptation_history.append({
            'timestamp': time.time(),
            'conditions': environment_conditions,
            'reliability': self.sensor_reliability.copy()
        })

        # Keep only recent history
        if len(self.adaptation_history) > 100:
            self.adaptation_history = self.adaptation_history[-100:]
```

## Integration with Language Understanding

### Language-Grounded Perception

Language-grounded perception connects visual perception with linguistic concepts, enabling robots to understand their environment in terms of human language. This connection is crucial for humanoid robots that need to respond to natural language commands and interact naturally with humans.

The integration involves several key components:

**Visual Grounding**: Connecting linguistic references to visual entities in the environment.

**Semantic Understanding**: Understanding the meaning and function of objects and scenes.

**Contextual Reasoning**: Using language context to disambiguate perceptual information.

```python
# Language-grounded perception system
class LanguageGroundedPerceptor:
    def __init__(self, vision_language_system: IntegratedVisionLanguageSystem):
        """
        Initialize language-grounded perception system
        """
        self.vls = vision_language_system
        self.language_parser = LanguageParser()
        self.semantic_memory = SemanticMemory()
        self.grounding_cache = {}

    def perceive_with_language_context(self, image_path: str, language_context: str) -> Dict[str, Any]:
        """
        Perceive scene with language context for grounding
        """
        # Get visual understanding
        visual_understanding = self.vls.understand_scene(image_path)

        # Parse language context
        language_semantics = self.language_parser.parse(language_context)

        # Ground language to visual elements
        grounded_perception = self.ground_language_to_visual(
            visual_understanding,
            language_semantics,
            language_context
        )

        return grounded_perception

    def ground_language_to_visual(self, visual_data: Dict, language_semantics: Dict, language_context: str) -> Dict[str, Any]:
        """
        Ground language concepts to visual elements
        """
        # Extract relevant objects based on language context
        relevant_objects = self.identify_relevant_objects(
            visual_data['objects'],
            language_semantics,
            language_context
        )

        # Find spatial relationships relevant to language
        relevant_relationships = self.identify_relevant_relationships(
            visual_data['spatial_relationships'],
            language_context
        )

        # Create grounded perception result
        grounded_result = {
            'relevant_objects': relevant_objects,
            'relevant_relationships': relevant_relationships,
            'scene_interpretation': self.interpret_scene_with_language(visual_data, language_context),
            'action_affordances': self.extract_action_affordances(relevant_objects, language_context),
            'confidence': self.calculate_grounding_confidence(relevant_objects, language_context)
        }

        return grounded_result

    def identify_relevant_objects(self, objects: List[Dict], language_semantics: Dict, language_context: str) -> List[Dict]:
        """
        Identify objects relevant to the language context
        """
        relevant_objects = []

        # Check each object for relevance to language context
        for obj in objects:
            relevance_score = self.calculate_object_language_relevance(obj, language_context)

            # Include object if relevance is above threshold
            if relevance_score > 0.3:  # Threshold can be adjusted
                obj_with_relevance = obj.copy()
                obj_with_relevance['relevance_score'] = relevance_score
                relevant_objects.append(obj_with_relevance)

        return relevant_objects

    def calculate_object_language_relevance(self, obj: Dict, language_context: str) -> float:
        """
        Calculate relevance of an object to language context
        """
        obj_name = obj['object'].lower()
        context_lower = language_context.lower()

        # Direct match score
        direct_match = 1.0 if obj_name in context_lower else 0.0

        # Semantic similarity (simplified)
        semantic_score = 0.0
        if any(affordance in context_lower for affordance in obj.get('affordances', [])):
            semantic_score = 0.5

        # Context keywords that might relate to object
        context_keywords = ['get', 'bring', 'take', 'find', 'locate', 'move', 'grasp']
        action_score = 0.3 if any(keyword in context_lower for keyword in context_keywords) else 0.0

        # Combine scores
        total_relevance = (direct_match * 0.5) + (semantic_score * 0.3) + (action_score * 0.2)

        return total_relevance

    def identify_relevant_relationships(self, relationships: List[Dict], language_context: str) -> List[Dict]:
        """
        Identify spatial relationships relevant to language context
        """
        relevant_relationships = []
        context_lower = language_context.lower()

        for rel in relationships:
            # Check if relationship is relevant to context
            if self.is_relationship_relevant(rel, context_lower):
                rel_with_relevance = rel.copy()
                relevant_relationships.append(rel_with_relevance)

        return relevant_relationships

    def is_relationship_relevant(self, relationship: Dict, context: str) -> bool:
        """
        Check if a spatial relationship is relevant to the language context
        """
        # Check for spatial language in context
        spatial_indicators = ['on', 'in', 'next to', 'near', 'by', 'at', 'from', 'to']
        return any(indicator in context for indicator in spatial_indicators)

    def interpret_scene_with_language(self, visual_data: Dict, language_context: str) -> str:
        """
        Interpret the scene in the context of language
        """
        # Use visual and language information to create a contextual interpretation
        caption = visual_data['scene_caption']
        objects = [obj['object'] for obj in visual_data['objects'][:3]]  # Top 3 objects

        # Create interpretation based on language context
        if 'kitchen' in language_context.lower():
            return f"Kitchen scene with {', '.join(objects)}. Suitable for food-related tasks."
        elif 'living room' in language_context.lower():
            return f"Living room scene with {', '.join(objects)}. Suitable for social interaction tasks."
        elif any(action in language_context.lower() for action in ['get', 'bring', 'take']):
            return f"Scene with {', '.join(objects)}. Objects are potentially actionable."
        else:
            return f"Scene with {', '.join(objects)}. {caption}"

    def extract_action_affordances(self, relevant_objects: List[Dict], language_context: str) -> List[Dict]:
        """
        Extract action affordances based on relevant objects and language context
        """
        affordances = []

        for obj in relevant_objects:
            obj_affordances = obj.get('affordances', [])

            # Filter affordances based on language context
            relevant_affordances = []
            for affordance in obj_affordances:
                if self.is_affordance_relevant(affordance, language_context):
                    relevant_affordances.append(affordance)

            if relevant_affordances:
                affordances.append({
                    'object': obj['object'],
                    'affordances': relevant_affordances,
                    'relevance': obj['relevance_score']
                })

        return affordances

    def is_affordance_relevant(self, affordance: str, language_context: str) -> bool:
        """
        Check if an affordance is relevant to the language context
        """
        # Map language actions to affordances
        action_affordance_map = {
            'get': ['grasp', 'lift', 'take'],
            'bring': ['grasp', 'lift', 'move', 'carry'],
            'take': ['grasp', 'lift', 'move'],
            'move': ['move', 'reposition'],
            'place': ['place', 'set_down'],
            'open': ['open'],
            'close': ['close'],
            'fill': ['fill'],
            'empty': ['empty']
        }

        for action, aff_list in action_affordance_map.items():
            if action in language_context.lower() and affordance in aff_list:
                return True

        return False

    def calculate_grounding_confidence(self, relevant_objects: List[Dict], language_context: str) -> float:
        """
        Calculate confidence in language-grounded perception
        """
        if not relevant_objects:
            return 0.1  # Low confidence if no relevant objects found

        # Calculate average relevance score
        avg_relevance = np.mean([obj['relevance_score'] for obj in relevant_objects])

        # Boost confidence if there are multiple highly relevant objects
        high_relevance_count = sum(1 for obj in relevant_objects if obj['relevance_score'] > 0.7)

        confidence = avg_relevance
        if high_relevance_count > 1:
            confidence = min(confidence * 1.2, 1.0)  # Boost for multiple relevant objects

        return confidence

class LanguageParser:
    def __init__(self):
        """
        Parse natural language for semantic content relevant to perception
        """
        # Define semantic categories
        self.semantic_categories = {
            'actions': ['get', 'bring', 'take', 'move', 'place', 'grasp', 'lift', 'find', 'locate'],
            'spatial': ['on', 'in', 'next to', 'near', 'by', 'at', 'from', 'to', 'above', 'below'],
            'objects': ['cup', 'book', 'ball', 'chair', 'table', 'bottle', 'phone', 'keys'],
            'locations': ['kitchen', 'living room', 'bedroom', 'office', 'dining room', 'bathroom']
        }

    def parse(self, text: str) -> Dict[str, List[str]]:
        """
        Parse text for semantic content
        """
        text_lower = text.lower()
        semantics = {}

        for category, keywords in self.semantic_categories.items():
            found_keywords = [kw for kw in keywords if kw in text_lower]
            semantics[category] = found_keywords

        return semantics

class SemanticMemory:
    def __init__(self):
        """
        Store and retrieve semantic information about objects and scenes
        """
        self.object_semantics = {
            'cup': {
                'category': 'container',
                'function': 'holding liquids',
                'typical_locations': ['kitchen', 'dining room', 'office'],
                'affordances': ['grasp', 'lift', 'move', 'fill', 'empty', 'place']
            },
            'book': {
                'category': 'information',
                'function': 'storing and retrieving information',
                'typical_locations': ['living room', 'office', 'bedroom'],
                'affordances': ['grasp', 'lift', 'move', 'open', 'close', 'read']
            },
            'chair': {
                'category': 'furniture',
                'function': 'seating',
                'typical_locations': ['dining room', 'office', 'living room'],
                'affordances': ['move', 'sit_on', 'approach']
            }
        }

    def get_object_semantics(self, object_name: str) -> Dict[str, Any]:
        """
        Get semantic information about an object
        """
        return self.object_semantics.get(object_name.lower(), {
            'category': 'unknown',
            'function': 'unknown',
            'typical_locations': ['unknown'],
            'affordances': ['grasp', 'move', 'place']
        })

    def get_location_context(self, location: str) -> Dict[str, Any]:
        """
        Get context information about a location
        """
        location_contexts = {
            'kitchen': {
                'typical_objects': ['cup', 'bottle', 'food', 'utensils'],
                'typical_actions': ['cooking', 'eating', 'drinking'],
                'spatial_layout': 'contains counter, sink, appliances'
            },
            'living_room': {
                'typical_objects': ['chair', 'table', 'tv', 'books'],
                'typical_actions': ['relaxing', 'watching', 'talking'],
                'spatial_layout': 'contains seating, entertainment center'
            }
        }

        return location_contexts.get(location.lower(), {
            'typical_objects': [],
            'typical_actions': [],
            'spatial_layout': 'unknown'
        })
```

### Contextual Scene Understanding

Contextual scene understanding goes beyond object recognition to understand scenes in terms of their functional layout, activity patterns, and relationship to tasks. This level of understanding is crucial for humanoid robots to navigate and interact effectively in human environments.

```python
# Contextual scene understanding system
class ContextualSceneUnderstanding:
    def __init__(self, language_grounding_system: LanguageGroundedPerceptor):
        """
        Initialize contextual scene understanding system
        """
        self.language_grounding = language_grounding_system
        self.scene_classifier = SceneClassifier()
        self.activity_recognizer = ActivityRecognizer()
        self.functional_analyzer = FunctionalSceneAnalyzer()

    def understand_scene_contextually(self, image_path: str, task_context: str = None) -> Dict[str, Any]:
        """
        Understand scene with contextual awareness
        """
        # Get basic visual understanding
        visual_data = self.language_grounding.vls.understand_scene(image_path)

        # Classify scene type
        scene_type = self.scene_classifier.classify_scene(visual_data)

        # Recognize potential activities
        potential_activities = self.activity_recognizer.recognize_activities(visual_data)

        # Analyze functional layout
        functional_layout = self.functional_analyzer.analyze_layout(visual_data, scene_type)

        # If task context is provided, refine understanding
        if task_context:
            contextual_adjustment = self.adjust_for_task_context(
                visual_data,
                scene_type,
                functional_layout,
                task_context
            )
        else:
            contextual_adjustment = {}

        # Combine all information
        contextual_understanding = {
            'scene_type': scene_type,
            'potential_activities': potential_activities,
            'functional_layout': functional_layout,
            'key_objects': self.identify_key_objects(visual_data, task_context),
            'navigable_areas': self.identify_navigable_areas(visual_data),
            'interaction_zones': self.identify_interaction_zones(visual_data),
            'safety_considerations': self.assess_safety(visual_data),
            'task_relevance': contextual_adjustment.get('task_relevance', {}),
            'action_recommendations': self.generate_action_recommendations(
                scene_type, functional_layout, task_context
            )
        }

        return contextual_understanding

    def adjust_for_task_context(self, visual_data: Dict, scene_type: str,
                              functional_layout: Dict, task_context: str) -> Dict[str, Any]:
        """
        Adjust scene understanding based on task context
        """
        task_keywords = task_context.lower().split()

        # Identify objects relevant to task
        relevant_objects = []
        for obj in visual_data['objects']:
            obj_lower = obj['object'].lower()
            if any(keyword in obj_lower for keyword in task_keywords):
                relevant_objects.append(obj)

        # Identify areas relevant to task
        relevant_areas = self.identify_task_relevant_areas(functional_layout, task_context)

        # Assess task feasibility
        task_feasible = self.assess_task_feasibility(scene_type, relevant_objects, task_context)

        return {
            'relevant_objects': relevant_objects,
            'relevant_areas': relevant_areas,
            'task_feasibility': task_feasible,
            'task_relevance': self.calculate_task_relevance(visual_data, task_context)
        }

    def identify_task_relevant_areas(self, functional_layout: Dict, task_context: str) -> List[Dict]:
        """
        Identify areas in the scene relevant to the task
        """
        relevant_areas = []
        context_lower = task_context.lower()

        for area in functional_layout.get('areas', []):
            area_relevance = 0

            # Check if area function matches task
            if 'kitchen' in context_lower and area.get('function', '').lower() == 'food preparation':
                area_relevance = 1.0
            elif 'work' in context_lower and 'desk' in area.get('objects', []):
                area_relevance = 1.0
            elif 'sit' in context_lower and 'seating' in area.get('function', '').lower():
                area_relevance = 1.0

            if area_relevance > 0.5:
                area_with_relevance = area.copy()
                area_with_relevance['relevance'] = area_relevance
                relevant_areas.append(area_with_relevance)

        return relevant_areas

    def assess_task_feasibility(self, scene_type: str, relevant_objects: List[Dict], task_context: str) -> bool:
        """
        Assess whether the task is feasible in this scene
        """
        # Simple feasibility check
        if 'kitchen' in task_context.lower() and scene_type != 'kitchen':
            # Task requires kitchen but we're not in kitchen
            return False

        if 'grasp' in task_context.lower() and not relevant_objects:
            # Task requires grasping but no objects detected
            return False

        # More sophisticated feasibility analysis would go here
        return True

    def calculate_task_relevance(self, visual_data: Dict, task_context: str) -> Dict[str, float]:
        """
        Calculate relevance of scene elements to task
        """
        relevance_scores = {}

        # Calculate object relevance
        for obj in visual_data['objects']:
            obj_relevance = self.calculate_object_task_relevance(obj['object'], task_context)
            relevance_scores[f"object_{obj['object']}"] = obj_relevance

        # Calculate scene type relevance
        scene_relevance = self.calculate_scene_task_relevance(visual_data['scene_caption'], task_context)
        relevance_scores['scene'] = scene_relevance

        return relevance_scores

    def calculate_object_task_relevance(self, object_name: str, task_context: str) -> float:
        """
        Calculate relevance of an object to the task
        """
        # Map task keywords to relevant objects
        task_object_map = {
            'drink': ['cup', 'bottle', 'glass'],
            'read': ['book', 'paper', 'magazine'],
            'sit': ['chair', 'sofa', 'stool'],
            'eat': ['table', 'chair', 'food'],
            'work': ['desk', 'computer', 'chair']
        }

        object_lower = object_name.lower()
        task_lower = task_context.lower()

        relevance = 0.1  # Base relevance

        # Check direct task-object mappings
        for task, objects in task_object_map.items():
            if task in task_lower and object_lower in objects:
                relevance = 0.9
                break

        # Check if object affordances match task actions
        affordances = self.language_grounding.semantic_memory.get_object_semantics(object_name).get('affordances', [])
        task_actions = ['grasp', 'lift', 'move', 'place', 'take', 'get', 'bring']
        if any(action in task_lower for action in task_actions) and any(affordance in affordances for affordance in ['grasp', 'lift', 'move']):
            relevance = max(relevance, 0.7)

        return min(relevance, 1.0)

    def calculate_scene_task_relevance(self, scene_caption: str, task_context: str) -> float:
        """
        Calculate relevance of scene to task
        """
        scene_lower = scene_caption.lower()
        task_lower = task_context.lower()

        # Check for location-task matches
        location_task_matches = [
            ('kitchen', 'cook'),
            ('kitchen', 'drink'),
            ('office', 'work'),
            ('living room', 'relax'),
            ('dining', 'eat'),
            ('bedroom', 'sleep')
        ]

        relevance = 0.5  # Base relevance

        for scene_loc, task_act in location_task_matches:
            if scene_loc in scene_lower and task_act in task_lower:
                relevance = 0.9
                break

        return min(relevance, 1.0)

    def identify_key_objects(self, visual_data: Dict, task_context: str = None) -> List[Dict]:
        """
        Identify key objects in the scene
        """
        objects = visual_data['objects']

        if task_context:
            # Rank objects by relevance to task
            ranked_objects = sorted(objects,
                                  key=lambda obj: self.calculate_object_task_relevance(obj['object'], task_context),
                                  reverse=True)
            return ranked_objects[:5]  # Return top 5 objects
        else:
            # Rank by general importance
            return objects[:5]  # Return top 5 objects by detection confidence

    def identify_navigable_areas(self, visual_data: Dict) -> List[Dict]:
        """
        Identify navigable areas in the scene
        """
        # In a real system, this would use spatial analysis of the scene
        # For this example, we'll return a simplified result
        return [
            {
                'name': 'center_area',
                'coordinates': [0.5, 0.5],  # Normalized coordinates
                'traversable': True,
                'size': 'large',
                'obstacles': []
            }
        ]

    def identify_interaction_zones(self, visual_data: Dict) -> List[Dict]:
        """
        Identify areas suitable for human-robot interaction
        """
        # In a real system, this would analyze scene layout for interaction
        # For this example, we'll return a simplified result
        interaction_zones = []

        for obj in visual_data['objects'][:3]:  # Consider top 3 objects
            if obj['object'] in ['table', 'counter', 'desk']:
                interaction_zones.append({
                    'type': 'surface_interaction',
                    'object': obj['object'],
                    'position': 'in front of object',
                    'size': 'medium',
                    'accessibility': 'high'
                })

        return interaction_zones

    def assess_safety(self, visual_data: Dict) -> List[Dict]:
        """
        Assess safety considerations in the scene
        """
        safety_issues = []

        # Check for fragile objects
        for obj in visual_data['objects']:
            if obj['object'] in ['glass', 'vase', 'fragile_item']:
                safety_issues.append({
                    'type': 'fragile_object',
                    'object': obj['object'],
                    'location': 'unknown',
                    'risk_level': 'medium'
                })

        # More sophisticated safety analysis would go here
        return safety_issues

    def generate_action_recommendations(self, scene_type: str, functional_layout: Dict, task_context: str) -> List[str]:
        """
        Generate action recommendations based on scene understanding
        """
        recommendations = []

        if task_context:
            if 'kitchen' in task_context.lower() and scene_type == 'kitchen':
                recommendations.append("Navigate to the counter area for food preparation")

            if 'work' in task_context.lower():
                recommendations.append("Locate a clear surface for workspace")

            if 'sit' in task_context.lower():
                recommendations.append("Find an available seating area")

        return recommendations

class SceneClassifier:
    def classify_scene(self, visual_data: Dict) -> str:
        """
        Classify the scene type based on visual content
        """
        caption = visual_data['scene_caption'].lower()
        objects = [obj['object'].lower() for obj in visual_data['objects']]

        # Simple classification based on keywords
        if any(keyword in caption for keyword in ['kitchen', 'cooking', 'food', 'stove', 'refrigerator']):
            return 'kitchen'
        elif any(keyword in caption for keyword in ['bed', 'bedroom', 'sleep', 'bedroom']):
            return 'bedroom'
        elif any(keyword in caption for keyword in ['sofa', 'couch', 'tv', 'living', 'relax']):
            return 'living_room'
        elif any(keyword in caption for keyword in ['desk', 'computer', 'office', 'work']):
            return 'office'
        elif any(keyword in objects for keyword in ['table', 'chair', 'food']):
            return 'dining_room'
        else:
            return 'unknown'

class ActivityRecognizer:
    def recognize_activities(self, visual_data: Dict) -> List[str]:
        """
        Recognize potential activities in the scene
        """
        caption = visual_data['scene_caption'].lower()
        objects = [obj['object'].lower() for obj in visual_data['objects']]

        potential_activities = []

        # Identify activities based on objects and scene context
        if any(obj in objects for obj in ['cup', 'bottle', 'glass']):
            potential_activities.append('drinking')

        if any(obj in objects for obj in ['book', 'paper', 'magazine']):
            potential_activities.append('reading')

        if any(obj in objects for obj in ['chair', 'sofa']):
            potential_activities.append('sitting')

        if 'food' in caption or any(obj in ['plate', 'food'] for obj in objects):
            potential_activities.append('eating')

        if 'work' in caption or any(obj in ['computer', 'desk'] for obj in objects):
            potential_activities.append('working')

        return potential_activities

class FunctionalSceneAnalyzer:
    def analyze_layout(self, visual_data: Dict, scene_type: str) -> Dict[str, Any]:
        """
        Analyze the functional layout of the scene
        """
        objects = visual_data['objects']

        # Identify functional areas based on object groupings
        areas = []

        # Kitchen-specific analysis
        if scene_type == 'kitchen':
            areas.append({
                'name': 'cooking_area',
                'function': 'food preparation',
                'objects': [obj['object'] for obj in objects if obj['object'] in ['stove', 'oven', 'microwave']],
                'center': [0, 0]  # Would be actual coordinates
            })

            areas.append({
                'name': 'storage_area',
                'function': 'food storage',
                'objects': [obj['object'] for obj in objects if obj['object'] in ['refrigerator', 'cabinet', 'pantry']],
                'center': [0, 0]
            })

        # General analysis
        areas.append({
            'name': 'activity_area',
            'function': 'general activity',
            'objects': [obj['object'] for obj in objects],
            'center': [0, 0]
        })

        return {
            'areas': areas,
            'layout_type': scene_type,
            'object_distributions': self.analyze_object_distribution(objects)
        }

    def analyze_object_distribution(self, objects: List[Dict]) -> Dict[str, int]:
        """
        Analyze how objects are distributed in the scene
        """
        distribution = {}

        for obj in objects:
            obj_type = obj['object']
            distribution[obj_type] = distribution.get(obj_type, 0) + 1

        return distribution
```

## Best Practices and Optimization

### Performance Optimization for Multi-Modal Systems

Multi-modal perception systems can be computationally intensive due to the need to process multiple data streams simultaneously. Several optimization strategies can improve performance while maintaining accuracy:

```python
# Performance optimization for multi-modal systems
class OptimizedMultiModalSystem:
    def __init__(self):
        """
        Initialize optimized multi-modal system
        """
        self.model_cache = {}
        self.computation_scheduler = ComputationScheduler()
        self.data_pipeline = DataPipelineOptimizer()
        self.fusion_optimizer = FusionOptimizer()

        # Performance metrics
        self.metrics = {
            'processing_times': [],
            'memory_usage': [],
            'accuracy_degradation': []
        }

    def process_with_optimization(self, sensor_inputs: Dict, language_context: str = None) -> Dict:
        """
        Process multi-modal inputs with performance optimization
        """
        start_time = time.time()

        # Schedule computations based on priority and resource availability
        scheduled_tasks = self.computation_scheduler.schedule_tasks(sensor_inputs)

        # Process inputs through optimized pipeline
        processed_results = self.data_pipeline.process_optimized(scheduled_tasks)

        # Perform optimized fusion
        fusion_result = self.fusion_optimizer.fuse_optimized(processed_results, language_context)

        # Record performance metrics
        processing_time = time.time() - start_time
        self.metrics['processing_times'].append(processing_time)

        return fusion_result

class ComputationScheduler:
    def __init__(self):
        """
        Schedule computations based on priority and resource constraints
        """
        self.task_queue = []
        self.resource_monitor = ResourceMonitor()

    def schedule_tasks(self, inputs: Dict) -> List[Dict]:
        """
        Schedule processing tasks based on priority and resources
        """
        tasks = []

        # Assign priorities based on task criticality
        for sensor_type, data in inputs.items():
            task = {
                'sensor_type': sensor_type,
                'data': data,
                'priority': self.calculate_priority(sensor_type),
                'estimated_time': self.estimate_processing_time(sensor_type),
                'resource_requirements': self.get_resource_requirements(sensor_type)
            }
            tasks.append(task)

        # Sort by priority (higher priority first)
        tasks.sort(key=lambda x: x['priority'], reverse=True)

        # Consider resource availability
        available_resources = self.resource_monitor.get_available_resources()

        # Adjust schedule based on resources
        scheduled_tasks = self.allocate_resources(tasks, available_resources)

        return scheduled_tasks

    def calculate_priority(self, sensor_type: str) -> int:
        """
        Calculate priority for sensor processing
        """
        # Higher priority for safety-critical sensors
        priority_map = {
            'imu': 10,  # Critical for balance
            'force_torque': 9,  # Critical for manipulation safety
            'lidar': 7,  # Important for navigation
            'camera': 6,  # Important for recognition
            'microphone': 5  # Important for interaction
        }

        return priority_map.get(sensor_type, 3)

    def estimate_processing_time(self, sensor_type: str) -> float:
        """
        Estimate processing time for sensor data
        """
        time_map = {
            'camera': 0.05,  # 50ms for image processing
            'lidar': 0.03,   # 30ms for point cloud processing
            'imu': 0.001,    # 1ms for IMU processing
            'force_torque': 0.001,  # 1ms for force sensing
            'microphone': 0.02  # 20ms for audio processing
        }

        return time_map.get(sensor_type, 0.05)

    def get_resource_requirements(self, sensor_type: str) -> Dict[str, float]:
        """
        Get resource requirements for sensor processing
        """
        return {
            'cpu': 0.1,  # Fraction of CPU core needed
            'gpu': 0.2 if sensor_type in ['camera', 'lidar'] else 0.0,  # GPU for vision
            'memory': 100 * 1024 * 1024  # 100MB memory
        }

    def allocate_resources(self, tasks: List[Dict], available_resources: Dict) -> List[Dict]:
        """
        Allocate resources to tasks considering availability
        """
        # Simple allocation - in practice, use more sophisticated scheduling
        allocated_tasks = []

        for task in tasks:
            # Check if resources are available
            if (task['resource_requirements']['cpu'] <= available_resources.get('cpu', 1.0) and
                task['resource_requirements']['gpu'] <= available_resources.get('gpu', 1.0)):

                # Allocate resources
                available_resources['cpu'] -= task['resource_requirements']['cpu']
                available_resources['gpu'] -= task['resource_requirements']['gpu']

                allocated_tasks.append(task)

        return allocated_tasks

class DataPipelineOptimizer:
    def __init__(self):
        """
        Optimize data processing pipeline
        """
        self.pipeline_cache = {}
        self.preprocessing_cache = {}

    def process_optimized(self, tasks: List[Dict]) -> Dict:
        """
        Process tasks through optimized pipeline
        """
        results = {}

        for task in tasks:
            sensor_type = task['sensor_type']
            data = task['data']

            # Preprocess data
            preprocessed_data = self.preprocess_optimized(sensor_type, data)

            # Process with appropriate model
            result = self.process_with_cached_model(sensor_type, preprocessed_data)

            results[sensor_type] = result

        return results

    def preprocess_optimized(self, sensor_type: str, data: Any) -> Any:
        """
        Optimized preprocessing for sensor data
        """
        cache_key = f"{sensor_type}_{hash(str(data)[:100])}"  # Simplified hash

        if cache_key in self.preprocessing_cache:
            return self.preprocessing_cache[cache_key]

        # Apply optimized preprocessing
        if sensor_type == 'camera':
            # Resize image to optimal size for model
            processed = self.resize_image_optimally(data)
        elif sensor_type == 'lidar':
            # Downsample point cloud if too dense
            processed = self.downsample_pointcloud(data)
        else:
            processed = data  # No special preprocessing needed

        # Cache result
        self.preprocessing_cache[cache_key] = processed

        # Limit cache size
        if len(self.preprocessing_cache) > 1000:
            # Remove oldest entries
            oldest_key = next(iter(self.preprocessing_cache))
            del self.preprocessing_cache[oldest_key]

        return processed

    def resize_image_optimally(self, image_data: Any) -> Any:
        """
        Resize image to optimal dimensions for processing
        """
        # In practice, this would use actual image processing
        # For simulation, return the same data
        return image_data

    def downsample_pointcloud(self, pointcloud_data: Any) -> Any:
        """
        Downsample point cloud to reduce computational load
        """
        # In practice, this would perform actual downsampling
        # For simulation, return the same data
        return pointcloud_data

    def process_with_cached_model(self, sensor_type: str, data: Any) -> Any:
        """
        Process data with cached model to avoid loading overhead
        """
        if sensor_type not in self.pipeline_cache:
            # Load model if not already cached
            model = self.load_sensor_model(sensor_type)
            self.pipeline_cache[sensor_type] = model

        model = self.pipeline_cache[sensor_type]

        # Process data with model
        result = self.apply_model(model, data, sensor_type)

        return result

    def load_sensor_model(self, sensor_type: str):
        """
        Load appropriate model for sensor type
        """
        # In practice, this would load actual models
        # For simulation, return placeholder
        return f"model_for_{sensor_type}"

    def apply_model(self, model, data: Any, sensor_type: str) -> Any:
        """
        Apply model to data
        """
        # Simulate model application
        return f"processed_by_{model}"

class FusionOptimizer:
    def __init__(self):
        """
        Optimize sensor fusion process
        """
        self.fusion_cache = {}
        self.uncertainty_aware = True

    def fuse_optimized(self, processed_results: Dict, language_context: str = None) -> Dict:
        """
        Perform optimized sensor fusion
        """
        # Create cache key
        cache_key = self.create_fusion_cache_key(processed_results, language_context)

        if cache_key in self.fusion_cache:
            return self.fusion_cache[cache_key]

        # Perform fusion
        fusion_result = self.perform_optimized_fusion(processed_results, language_context)

        # Cache result if appropriate
        if len(self.fusion_cache) < 100:  # Limit cache size
            self.fusion_cache[cache_key] = fusion_result

        return fusion_result

    def create_fusion_cache_key(self, results: Dict, context: str = None) -> str:
        """
        Create cache key for fusion results
        """
        import hashlib
        cache_input = f"{str(sorted(results.keys()))}_{context or 'none'}"
        return hashlib.md5(cache_input.encode()).hexdigest()

    def perform_optimized_fusion(self, results: Dict, language_context: str = None) -> Dict:
        """
        Perform optimized sensor fusion
        """
        # Use uncertainty-aware fusion if enabled
        if self.uncertainty_aware:
            return self.uncertainty_aware_fusion(results, language_context)
        else:
            return self.simple_fusion(results, language_context)

    def uncertainty_aware_fusion(self, results: Dict, language_context: str = None) -> Dict:
        """
        Perform fusion considering uncertainty of different sensors
        """
        # Assign weights based on sensor uncertainty
        weighted_results = {}

        for sensor_type, data in results.items():
            uncertainty = self.estimate_sensor_uncertainty(sensor_type)
            weight = 1.0 / (uncertainty + 0.01)  # Add small value to avoid division by zero

            weighted_results[sensor_type] = {
                'data': data,
                'weight': weight,
                'uncertainty': uncertainty
            }

        # Combine weighted results
        combined_result = self.combine_weighted_results(weighted_results)

        return combined_result

    def estimate_sensor_uncertainty(self, sensor_type: str) -> float:
        """
        Estimate uncertainty for sensor type
        """
        uncertainty_map = {
            'camera': 0.05,
            'lidar': 0.02,
            'imu': 0.01,
            'force_torque': 0.1,
            'microphone': 0.05
        }

        return uncertainty_map.get(sensor_type, 0.05)

    def combine_weighted_results(self, weighted_results: Dict) -> Dict:
        """
        Combine weighted results from different sensors
        """
        # For this example, return a simplified combination
        combined = {
            'fused_data': {},
            'confidence': 0.0,
            'source_contributions': {s: w['weight'] for s, w in weighted_results.items()}
        }

        return combined

    def simple_fusion(self, results: Dict, language_context: str = None) -> Dict:
        """
        Simple fusion without uncertainty considerations
        """
        return {
            'fused_data': results,
            'confidence': 0.8,  # Default confidence
            'source_contributions': {s: 1.0 for s in results.keys()}
        }

class ResourceMonitor:
    def __init__(self):
        """
        Monitor system resources for optimization
        """
        self.resource_history = []

    def get_available_resources(self) -> Dict[str, float]:
        """
        Get current available resources
        """
        # Simulate resource monitoring
        # In practice, this would check actual system resources
        return {
            'cpu': 0.7,  # 70% CPU available
            'gpu': 0.5,  # 50% GPU available
            'memory': 0.8 * 1024 * 1024 * 1024  # 0.8GB available
        }

    def monitor_resources(self):
        """
        Continuously monitor resources
        """
        # Implementation would run in background thread
        pass
```

### Safety and Validation in Multi-Modal Perception

Safety validation is crucial for multi-modal perception systems, especially in humanoid robotics where incorrect perception can lead to dangerous situations. The validation process must ensure that fused information is reliable and that the system can handle edge cases safely.

```python
# Safety and validation for multi-modal perception
class SafetyValidator:
    def __init__(self):
        """
        Initialize safety validation system
        """
        self.safety_rules = self.define_safety_rules()
        self.anomaly_detector = AnomalyDetector()
        self.confidence_validator = ConfidenceValidator()

    def define_safety_rules(self) -> Dict[str, List[Dict]]:
        """
        Define safety rules for multi-modal perception
        """
        return {
            'spatial': [
                {'rule': 'maintain_safe_distance_from_humans', 'threshold': 0.8},  # meters
                {'rule': 'avoid_collisions_with_obstacles', 'threshold': 0.3},    # meters
                {'rule': 'respects_navigation_boundaries', 'areas': ['restricted_zones']}
            ],
            'temporal': [
                {'rule': 'consistent_object_tracking', 'max_velocity': 5.0},  # m/s
                {'rule': 'stable_pose_estimation', 'max_drift': 0.5}          # meters per second
            ],
            'semantic': [
                {'rule': 'validate_object_classifications', 'confidence_threshold': 0.7},
                {'rule': 'check_action_feasibility', 'required_affordances': ['grasp', 'move']}
            ]
        }

    def validate_perception(self, fusion_result: Dict, environment_context: Dict) -> Dict:
        """
        Validate multi-modal perception results for safety
        """
        validation_results = {
            'is_safe': True,
            'violations': [],
            'warnings': [],
            'confidence_score': 0.0,
            'actionable': True
        }

        # Check spatial safety
        spatial_violations = self.check_spatial_safety(fusion_result, environment_context)
        validation_results['violations'].extend(spatial_violations)

        # Check temporal consistency
        temporal_violations = self.check_temporal_consistency(fusion_result)
        validation_results['violations'].extend(temporal_violations)

        # Check semantic validity
        semantic_violations = self.check_semantic_validity(fusion_result)
        validation_results['violations'].extend(semantic_violations)

        # Detect anomalies
        anomalies = self.anomaly_detector.detect_anomalies(fusion_result)
        validation_results['warnings'].extend(anomalies)

        # Validate confidence
        confidence_score = self.confidence_validator.validate_confidence(fusion_result)
        validation_results['confidence_score'] = confidence_score

        # Update safety status
        validation_results['is_safe'] = len(validation_results['violations']) == 0
        validation_results['actionable'] = confidence_score > 0.5 and validation_results['is_safe']

        return validation_results

    def check_spatial_safety(self, fusion_result: Dict, environment_context: Dict) -> List[Dict]:
        """
        Check spatial safety of perception results
        """
        violations = []

        # Check for humans in proximity
        humans = fusion_result.get('humans', [])
        for human in humans:
            distance_to_robot = self.calculate_distance_to_robot(human)
            if distance_to_robot < 0.8:  # Too close
                violations.append({
                    'type': 'unsafe_proximity',
                    'severity': 'high',
                    'description': f'Human detected at {distance_to_robot:.2f}m, below safe distance of 0.8m',
                    'location': human.get('position', 'unknown')
                })

        # Check for obstacles in navigation path
        obstacles = fusion_result.get('obstacles', [])
        navigation_path = environment_context.get('navigation_path', [])

        for obstacle in obstacles:
            if self.obstacle_in_navigation_path(obstacle, navigation_path):
                violations.append({
                    'type': 'navigation_hazard',
                    'severity': 'high',
                    'description': 'Obstacle detected in planned navigation path',
                    'obstacle': obstacle
                })

        return violations

    def check_temporal_consistency(self, fusion_result: Dict) -> List[Dict]:
        """
        Check temporal consistency of perception
        """
        violations = []

        # Check for object velocity consistency
        tracked_objects = fusion_result.get('tracked_objects', {})
        for obj_id, obj_data in tracked_objects.items():
            velocity = obj_data.get('velocity', [0, 0, 0])
            speed = np.linalg.norm(velocity)

            if speed > 5.0:  # Unusually fast for indoor environment
                violations.append({
                    'type': 'inconsistent_velocity',
                    'severity': 'medium',
                    'description': f'Object {obj_id} moving at {speed:.2f} m/s, exceeding threshold of 5.0 m/s',
                    'velocity': velocity
                })

        # Check for pose drift
        pose_history = fusion_result.get('pose_history', [])
        if len(pose_history) >= 2:
            # Calculate average pose change rate
            time_diff = pose_history[-1]['timestamp'] - pose_history[-2]['timestamp']
            if time_diff > 0:
                position_change = np.array(pose_history[-1]['position']) - np.array(pose_history[-2]['position'])
                drift_rate = np.linalg.norm(position_change) / time_diff

                if drift_rate > 0.5:  # More than 0.5 m/s drift
                    violations.append({
                        'type': 'pose_drift',
                        'severity': 'medium',
                        'description': f'Pose drifting at {drift_rate:.2f} m/s, exceeding threshold of 0.5 m/s',
                        'drift_rate': float(drift_rate)
                    })

        return violations

    def check_semantic_validity(self, fusion_result: Dict) -> List[Dict]:
        """
        Check semantic validity of perception results
        """
        violations = []

        # Check object classification confidence
        objects = fusion_result.get('objects', [])
        for obj in objects:
            confidence = obj.get('confidence', 0)
            if confidence < 0.7:
                violations.append({
                    'type': 'low_classification_confidence',
                    'severity': 'medium',
                    'description': f'Object {obj.get("name", "unknown")} classified with low confidence {confidence:.2f}',
                    'confidence': confidence,
                    'object_type': obj.get('type', 'unknown')
                })

        # Check action feasibility
        actionable_objects = fusion_result.get('actionable_objects', [])
        for obj in actionable_objects:
            affordances = obj.get('affordances', [])
            if not affordances:
                violations.append({
                    'type': 'no_affordances',
                    'severity': 'medium',
                    'description': f'Object {obj.get("name", "unknown")} has no identified affordances for action',
                    'object': obj
                })

        return violations

    def calculate_distance_to_robot(self, human_location: Dict) -> float:
        """
        Calculate distance from human to robot
        """
        # Simplified calculation
        robot_pos = [0, 0, 0]  # Robot at origin for this example
        human_pos = human_location.get('position', [0, 0, 0])

        diff = np.array(robot_pos) - np.array(human_pos)
        return float(np.linalg.norm(diff))

    def obstacle_in_navigation_path(self, obstacle: Dict, path: List[Dict]) -> bool:
        """
        Check if obstacle is in navigation path
        """
        # Simplified check - in practice, this would be more sophisticated
        if not path:
            return False

        # Check if obstacle is close to any point in path
        obstacle_pos = obstacle.get('position', [0, 0, 0])

        for path_point in path[:5]:  # Check first 5 points of path
            path_pos = path_point.get('position', [0, 0, 0])
            distance = np.linalg.norm(np.array(obstacle_pos) - np.array(path_pos))

            if distance < 0.5:  # Within 50cm of path
                return True

        return False

class AnomalyDetector:
    def __init__(self):
        """
        Detect anomalies in multi-modal perception
        """
        self.anomaly_thresholds = {
            'object_size': [0.01, 2.0],  # min and max size in meters
            'object_height': [0.0, 2.5],  # min and max height in meters
            'detection_frequency': [0.1, 100.0],  # min and max Hz
            'sensor_variance': [0.0, 1.0]  # max variance threshold
        }

    def detect_anomalies(self, fusion_result: Dict) -> List[Dict]:
        """
        Detect anomalies in fusion results
        """
        anomalies = []

        # Check object properties
        objects = fusion_result.get('objects', [])
        for obj in objects:
            # Check object size
            size = obj.get('size', {}).get('volume', 0)
            if size < self.anomaly_thresholds['object_size'][0] or size > self.anomaly_thresholds['object_size'][1]:
                anomalies.append({
                    'type': 'anomalous_size',
                    'severity': 'warning',
                    'description': f'Object {obj.get("name", "unknown")} has anomalous size {size:.3f}m³',
                    'value': size,
                    'thresholds': self.anomaly_thresholds['object_size']
                })

            # Check object height
            height = obj.get('position', [0, 0, 0])[2]  # z-coordinate
            if height < self.anomaly_thresholds['object_height'][0] or height > self.anomaly_thresholds['object_height'][1]:
                anomalies.append({
                    'type': 'anomalous_height',
                    'severity': 'warning',
                    'description': f'Object {obj.get("name", "unknown")} has anomalous height {height:.2f}m',
                    'value': height,
                    'thresholds': self.anomaly_thresholds['object_height']
                })

        # Check sensor data quality
        sensor_data = fusion_result.get('sensor_data', {})
        for sensor_type, data in sensor_data.items():
            variance = self.calculate_variance(data)
            if variance > self.anomaly_thresholds['sensor_variance'][1]:
                anomalies.append({
                    'type': 'high_sensor_variance',
                    'severity': 'warning',
                    'description': f'{sensor_type} sensor showing high variance {variance:.3f}',
                    'value': variance,
                    'threshold': self.anomaly_thresholds['sensor_variance'][1]
                })

        return anomalies

    def calculate_variance(self, data: Any) -> float:
        """
        Calculate variance of sensor data
        """
        # Simplified variance calculation
        if isinstance(data, (list, tuple, np.ndarray)):
            if len(data) > 1:
                return float(np.var(data))
        return 0.0

class ConfidenceValidator:
    def __init__(self):
        """
        Validate confidence in perception results
        """
        self.confidence_weights = {
            'camera': 0.3,
            'lidar': 0.3,
            'imu': 0.2,
            'fusion_agreement': 0.2
        }

    def validate_confidence(self, fusion_result: Dict) -> float:
        """
        Validate overall confidence in fusion result
        """
        # Calculate confidence from different sources
        camera_conf = fusion_result.get('camera_confidence', 0.5)
        lidar_conf = fusion_result.get('lidar_confidence', 0.5)
        imu_conf = fusion_result.get('imu_confidence', 0.5)

        # Check agreement between sensors
        agreement_score = self.calculate_sensor_agreement(fusion_result)

        # Calculate weighted confidence
        total_confidence = (
            camera_conf * self.confidence_weights['camera'] +
            lidar_conf * self.confidence_weights['lidar'] +
            imu_conf * self.confidence_weights['imu'] +
            agreement_score * self.confidence_weights['fusion_agreement']
        )

        return min(total_confidence, 1.0)  # Cap at 1.0

    def calculate_sensor_agreement(self, fusion_result: Dict) -> float:
        """
        Calculate agreement between different sensors
        """
        # Simplified agreement calculation
        # In practice, this would compare estimates from different sensors
        return 0.8  # Assume good agreement for this example
```

## Looking Ahead

The next chapter will integrate all the components discussed in this module into a comprehensive capstone project. We'll demonstrate a complete VLA-powered humanoid system that combines vision-language models, sensor fusion, cognitive planning, and natural language understanding into a unified system capable of complex task execution in human environments.

Multi-modal perception systems represent a significant advancement in robotic capabilities, enabling robots to understand and interact with their environment in more human-like ways. As these systems continue to evolve, we can expect increasingly sophisticated and intuitive human-robot interaction that makes robots more useful and accessible in everyday environments.

## Citations

- Radford, A., et al. (2021). Learning Transferable Visual Models From Natural Language Supervision. Proceedings of the International Conference on Machine Learning.
- Li, J., et al. (2022). BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation. International Conference on Machine Learning.
- Requeima, J., et al. (2019). Fast and Flexible Multivariate Gaussian Process Regression. arXiv preprint arXiv:1910.01568.
- Hermann, K. M., et al. (2022). Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents. International Conference on Machine Learning.

## Summary

This chapter covered multi-modal perception systems that integrate vision, language, and sensor fusion for humanoid robotics. We explored vision-language model integration using CLIP and BLIP, implemented sensor fusion techniques with Kalman filtering, and discussed the integration of multi-modal perception with language understanding for contextual awareness. The chapter emphasized the importance of performance optimization and safety validation in creating robust multi-modal perception systems that enable humanoid robots to understand and interact with their environment effectively.

## Review Questions/Exercises

1. How do vision-language models like CLIP enable more flexible object recognition in robotics?
2. What are the key challenges in fusing data from different sensor modalities?
3. Explain the role of Kalman filtering in multi-modal perception systems.
4. Design a safety validation system for multi-modal perception outputs.
5. How would you implement contextual scene understanding that adapts to different environments?

---

**Chapter Specifications:**
- **Expected Length**: 2,000-3,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based implementations showing vision-language integration, sensor fusion, and language grounding
- **Diagrams/Illustrations**: Text-based architecture diagrams showing multi-modal system components
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides