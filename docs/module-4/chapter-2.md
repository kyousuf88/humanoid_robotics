---
id: module-4-chapter-2
sidebar_position: 2
title: "Chapter 2 - Voice-to-Action Pipeline (Whisper → Intent → ROS 2 Actions)"
---

# Chapter 2: Voice-to-Action Pipeline (Whisper → Intent → ROS 2 Actions)

## Learning Objectives
- [ ] Understand the architecture of voice-to-action systems using Whisper for speech recognition
- [ ] Implement intent classification and natural language parsing for robotic commands
- [ ] Map voice commands to ROS 2 actions with proper validation and error handling
- [ ] Design robust voice command validation and error recovery mechanisms
- [ ] Integrate voice processing with ROS 2 action servers for robot execution

## Key Concepts
- [ ] **Whisper**: OpenAI's automatic speech recognition (ASR) system for converting speech to text
- [ ] **Intent Classification**: Process of determining the underlying goal of a natural language command
- [ ] **ROS 2 Actions**: Asynchronous communication pattern for long-running robot tasks
- [ ] **Voice Command Validation**: Process of verifying that voice commands are valid and executable
- [ ] **Error Handling**: Strategies for managing failures in voice recognition and action execution
- [ ] **Dialogue Management**: Coordination of multi-turn conversations between humans and robots

## Introduction

The voice-to-action pipeline represents a critical component of Vision-Language-Action (VLA) systems, enabling humanoid robots to understand and respond to natural language commands through speech. This pipeline transforms spoken language into executable robot behaviors, creating an intuitive interface that allows humans to interact with robots using natural communication patterns.

The pipeline consists of several interconnected stages: speech recognition converts audio to text, natural language understanding interprets the meaning and intent of commands, and action mapping translates these interpretations into executable ROS 2 actions. Each stage must operate reliably and efficiently to create a responsive and trustworthy human-robot interaction experience.

This chapter explores the implementation of a complete voice-to-action pipeline using OpenAI's Whisper for speech recognition, followed by intent classification and mapping to ROS 2 actions. We'll examine the architecture of such systems, implementation details, and strategies for ensuring robust operation in real-world environments.

The integration of Whisper with ROS 2 provides a powerful foundation for voice-controlled robotics, combining state-of-the-art speech recognition with the reliable communication and action execution capabilities of ROS 2. This combination enables humanoid robots to respond to complex, natural language commands while maintaining the safety and reliability required for human-robot interaction.

## Whisper Integration for Speech Recognition

### Overview of Whisper in Robotics

OpenAI's Whisper is a state-of-the-art automatic speech recognition (ASR) system that demonstrates remarkable performance across multiple languages and domains. For robotics applications, Whisper offers several advantages: high accuracy, robustness to background noise, support for multiple languages, and the ability to run efficiently on modern hardware.

In robotic applications, Whisper serves as the initial stage of the voice-to-action pipeline, converting spoken commands into text that can be processed by subsequent natural language understanding components. The system's ability to handle various accents, speaking styles, and acoustic conditions makes it well-suited for real-world robot deployment.

### Whisper Implementation for Robotics

```python
# Whisper integration for robotic speech recognition
import whisper
import torch
import numpy as np
import rospy
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData
import pyaudio
import wave
import threading
import queue

class WhisperSpeechRecognizer:
    def __init__(self, model_size="base", device="cuda"):
        """
        Initialize Whisper speech recognizer for robotics applications
        """
        # Load Whisper model
        self.model = whisper.load_model(model_size, device=device)

        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_buffer = []

        # ROS publishers/subscribers
        self.transcript_pub = rospy.Publisher('/voice/transcript', String, queue_size=10)
        self.audio_sub = rospy.Subscriber('/audio/audio', AudioData, self.audio_callback)

        # Processing queue for audio chunks
        self.audio_queue = queue.Queue()

        # Processing thread
        self.processing_thread = threading.Thread(target=self.process_audio_stream, daemon=True)
        self.processing_thread.start()

        # Recognition parameters
        self.recognition_threshold = 0.7  # Confidence threshold
        self.silence_duration = 1.0  # Seconds of silence to trigger recognition
        self.max_recognition_time = 30.0  # Maximum time for recognition

    def audio_callback(self, audio_data):
        """
        Callback for incoming audio data
        """
        # Convert audio data to numpy array
        audio_array = np.frombuffer(audio_data.data, dtype=np.int16).astype(np.float32) / 32768.0

        # Add to processing queue
        self.audio_queue.put(audio_array)

    def process_audio_stream(self):
        """
        Process audio stream in a separate thread
        """
        accumulated_audio = np.array([])

        while not rospy.is_shutdown():
            try:
                # Get audio chunk from queue
                audio_chunk = self.audio_queue.get(timeout=1.0)

                # Accumulate audio
                accumulated_audio = np.concatenate([accumulated_audio, audio_chunk])

                # Check if we have enough audio to process
                if len(accumulated_audio) >= self.sample_rate * 0.5:  # 0.5 seconds minimum
                    # Check for voice activity (simplified approach)
                    if self.detect_voice_activity(accumulated_audio):
                        # Continue accumulating until silence is detected
                        continue
                    else:
                        # Process accumulated audio if it contains speech
                        if len(accumulated_audio) > self.sample_rate * 0.1:  # At least 0.1 seconds
                            transcript = self.recognize_speech(accumulated_audio)
                            if transcript and self.is_command_relevant(transcript):
                                self.transcript_pub.publish(transcript)
                                accumulated_audio = np.array([])  # Reset buffer
                        else:
                            # Remove old audio to prevent buffer overflow
                            if len(accumulated_audio) > self.sample_rate * 5:  # Keep max 5 seconds
                                accumulated_audio = accumulated_audio[-int(self.sample_rate * 2):]

            except queue.Empty:
                continue

    def detect_voice_activity(self, audio_data):
        """
        Simple voice activity detection
        """
        # Calculate energy of audio signal
        energy = np.mean(np.abs(audio_data))

        # Threshold-based VAD (simplified)
        return energy > 0.01  # Adjust threshold as needed

    def recognize_speech(self, audio_data):
        """
        Recognize speech using Whisper
        """
        try:
            # Pad or trim audio to meet Whisper's requirements
            if len(audio_data) < self.sample_rate * 0.1:  # Minimum 0.1 seconds
                return None

            # Transcribe audio
            result = self.model.transcribe(audio_data, fp16=torch.cuda.is_available())

            transcript = result["text"].strip()

            # Check confidence (using compression ratio and other metrics as proxy)
            confidence = self.estimate_confidence(result)

            if confidence >= self.recognition_threshold and transcript:
                return transcript
            else:
                rospy.logwarn(f"Low confidence recognition: '{transcript}' (confidence: {confidence:.2f})")
                return None

        except Exception as e:
            rospy.logerr(f"Whisper recognition error: {e}")
            return None

    def estimate_confidence(self, result):
        """
        Estimate confidence in recognition result
        """
        # Use compression ratio and other heuristics as confidence proxy
        compression_ratio = result.get("compression_ratio", 1.0)
        no_speech_prob = result.get("no_speech_prob", 0.0)

        # Lower compression ratio indicates more repetitive text (lower quality)
        compression_score = max(0, min(1, 2.4 - compression_ratio)) / 2.4

        # Lower no_speech_prob indicates higher confidence in speech
        speech_score = 1.0 - no_speech_prob

        # Combined confidence score
        confidence = (compression_score + speech_score) / 2.0
        return confidence

    def is_command_relevant(self, transcript):
        """
        Check if transcript contains relevant commands for the robot
        """
        # Simple keyword-based filtering (in practice, use more sophisticated NLU)
        robot_keywords = ['robot', 'please', 'can you', 'help', 'move', 'go', 'bring', 'take', 'stop', 'wait']

        transcript_lower = transcript.lower()
        return any(keyword in transcript_lower for keyword in robot_keywords)

class VoiceActivityDetector:
    def __init__(self):
        self.energy_threshold = 0.01
        self.silence_frames = 0
        self.min_silence_frames = 16  # At 16kHz, this is about 0.5 seconds of silence
        self.recording = False
        self.audio_buffer = []

    def detect_activity(self, audio_chunk):
        """
        Detect voice activity in audio chunk
        """
        energy = np.mean(np.abs(audio_chunk))

        if energy > self.energy_threshold:
            # Voice detected
            self.silence_frames = 0
            if not self.recording:
                self.recording = True
                self.audio_buffer = []
            self.audio_buffer.extend(audio_chunk)
        else:
            # Silence detected
            if self.recording:
                self.silence_frames += 1
                self.audio_buffer.extend(audio_chunk)

                if self.silence_frames >= self.min_silence_frames:
                    # End of speech detected
                    recording_data = np.array(self.audio_buffer)
                    self.recording = False
                    self.audio_buffer = []
                    return True, recording_data

        return False, None
```

### Optimizing Whisper for Real-Time Robotics

Real-time operation in robotics requires careful optimization of the Whisper model to balance accuracy with processing speed. Several techniques can be employed to achieve real-time performance:

```python
# Optimized Whisper for real-time robotics
class OptimizedWhisperRecognizer:
    def __init__(self, model_size="base"):
        """
        Optimized Whisper recognizer for real-time operation
        """
        # Load model with optimizations
        self.model = whisper.load_model(model_size)

        # Use smaller models for faster processing if accuracy allows
        self.use_quantization = True

        # Pre-allocate tensors to reduce allocation overhead
        self.mel_filters = whisper.api.audio.log_mel_spectrogram.torch_mel_spectrogram

        # Audio processing parameters
        self.sample_rate = 16000
        self.window_size = 1024
        self.hop_length = 512

        # Buffer management for streaming
        self.audio_buffer = np.zeros(self.sample_rate * 3)  # 3 seconds buffer
        self.buffer_offset = 0

        # Processing flags
        self.is_processing = False
        self.processing_queue = queue.Queue(maxsize=5)  # Limit queue size to prevent delays

    def process_audio_chunk(self, audio_chunk):
        """
        Process audio chunk with optimized pipeline
        """
        if self.is_processing:
            # Skip if already processing to prevent backlog
            if not self.processing_queue.full():
                self.processing_queue.put(audio_chunk)
            return None

        # Add chunk to buffer
        chunk_len = len(audio_chunk)
        if self.buffer_offset + chunk_len > len(self.audio_buffer):
            # Shift buffer if needed
            self.audio_buffer = np.roll(self.audio_buffer, -chunk_len)
            self.buffer_offset = len(self.audio_buffer) - chunk_len

        self.audio_buffer[self.buffer_offset:self.buffer_offset + chunk_len] = audio_chunk
        self.buffer_offset += chunk_len

        # Check if we have enough audio to process
        if self.buffer_offset >= self.sample_rate * 0.5:  # At least 0.5 seconds
            # Process in background to avoid blocking
            self.is_processing = True
            processing_thread = threading.Thread(
                target=self._process_buffer,
                args=(self.audio_buffer[:self.buffer_offset].copy(),)
            )
            processing_thread.start()

    def _process_buffer(self, audio_data):
        """
        Internal method to process audio buffer
        """
        try:
            # Perform recognition
            result = self.model.transcribe(audio_data, fp16=torch.cuda.is_available())
            transcript = result["text"].strip()

            # Publish result
            if transcript:
                self.publish_transcript(transcript)

        except Exception as e:
            rospy.logerr(f"Optimized Whisper error: {e}")
        finally:
            self.is_processing = False
            # Process any queued chunks
            if not self.processing_queue.empty():
                queued_chunk = self.processing_queue.get()
                self.process_audio_chunk(queued_chunk)

    def publish_transcript(self, transcript):
        """
        Publish transcript to ROS topic
        """
        # Implementation for publishing to ROS topic
        pass
```

## Intent Classification and Natural Language Parsing

### Intent Recognition Architecture

Intent classification in voice-to-action systems involves determining the underlying goal or purpose of a natural language command. This process bridges the gap between raw speech recognition and actionable robot commands, requiring sophisticated natural language understanding capabilities.

The intent recognition system must handle the ambiguity and variability inherent in natural language while mapping to the specific actions and capabilities of the robot platform. This involves both classification of high-level intents (e.g., navigation, manipulation, information retrieval) and extraction of relevant parameters (e.g., destination, object, person).

```python
# Intent classification system
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import re

class IntentClassifier:
    def __init__(self):
        """
        Initialize intent classification system
        """
        # Load spaCy model for linguistic processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Please install en_core_web_sm: python -m spacy download en_core_web_sm")
            self.nlp = None

        # Define intent categories for robotic commands
        self.intent_categories = {
            'navigation': ['go to', 'move to', 'walk to', 'navigate to', 'go', 'move', 'walk', 'navigate'],
            'manipulation': ['pick up', 'grasp', 'take', 'bring', 'fetch', 'get', 'lift', 'hold'],
            'interaction': ['greet', 'say hello', 'introduce', 'meet', 'talk to', 'wave to'],
            'information': ['what is', 'where is', 'how many', 'tell me', 'describe', 'show me'],
            'control': ['stop', 'wait', 'pause', 'continue', 'start', 'begin', 'end', 'finish'],
            'social': ['please', 'thank you', 'sorry', 'excuse me', 'hello', 'goodbye']
        }

        # Initialize transformer-based classifier
        self.transformer_classifier = pipeline(
            "text-classification",
            model="microsoft/DialoGPT-medium"  # Or a custom trained model
        )

        # Named entity recognition patterns
        self.entity_patterns = {
            'location': [r'\b(kitchen|living room|bedroom|office|bathroom|dining room|hallway|garage)\b',
                        r'\b(table|chair|sofa|couch|bed|desk|counter|shelf)\b'],
            'object': [r'\b(cup|glass|book|phone|keys|wallet|ball|toy|food|water)\b'],
            'person': [r'\b(person|man|woman|child|someone|anyone|nobody)\b'],
            'time': [r'\b(now|immediately|soon|later|today|tomorrow|yesterday)\b']
        }

    def classify_intent(self, text):
        """
        Classify intent of input text
        """
        if not text:
            return {'intent': 'unknown', 'confidence': 0.0, 'entities': {}}

        # Preprocess text
        processed_text = self.preprocess_text(text.lower())

        # Rule-based classification
        rule_intent = self.rule_based_classification(processed_text)

        # Entity extraction
        entities = self.extract_entities(processed_text)

        # Confidence calculation
        confidence = self.calculate_confidence(rule_intent, processed_text)

        return {
            'intent': rule_intent,
            'confidence': confidence,
            'entities': entities,
            'original_text': text
        }

    def preprocess_text(self, text):
        """
        Preprocess text for intent classification
        """
        # Remove punctuation and normalize
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def rule_based_classification(self, text):
        """
        Rule-based intent classification
        """
        for intent, keywords in self.intent_categories.items():
            for keyword in keywords:
                if keyword in text:
                    return intent

        return 'unknown'

    def extract_entities(self, text):
        """
        Extract named entities from text
        """
        entities = {}

        for entity_type, patterns in self.entity_patterns.items():
            entity_list = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                entity_list.extend(matches)
            if entity_list:
                entities[entity_type] = list(set(entity_list))  # Remove duplicates

        return entities

    def calculate_confidence(self, intent, text):
        """
        Calculate confidence in intent classification
        """
        if intent == 'unknown':
            return 0.0

        # Calculate confidence based on keyword matches
        keyword_matches = 0
        total_keywords = 0

        for keywords in self.intent_categories.values():
            total_keywords += len(keywords)
            for keyword in keywords:
                if keyword in text:
                    keyword_matches += 1

        if total_keywords > 0:
            confidence = keyword_matches / total_keywords
            return min(confidence, 1.0)  # Cap at 1.0
        else:
            return 0.5  # Default confidence

class AdvancedIntentClassifier:
    def __init__(self):
        """
        Advanced intent classifier using transformer models
        """
        # Load pre-trained model for sequence classification
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "distilbert-base-uncased",
            num_labels=6  # navigation, manipulation, interaction, information, control, social
        )

        # Intent label mapping
        self.label_map = {
            0: 'navigation',
            1: 'manipulation',
            2: 'interaction',
            3: 'information',
            4: 'control',
            5: 'social'
        }

    def classify_with_transformer(self, text):
        """
        Classify intent using transformer model
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = predictions[0][predicted_class].item()

        return {
            'intent': self.label_map[predicted_class],
            'confidence': confidence,
            'all_scores': {self.label_map[i]: float(predictions[0][i]) for i in range(len(self.label_map))}
        }

class NaturalLanguageParser:
    def __init__(self):
        """
        Natural language parser for extracting structured information from commands
        """
        self.intent_classifier = IntentClassifier()
        self.action_mapper = ActionMapper()

    def parse_command(self, text):
        """
        Parse natural language command into structured action
        """
        # Classify intent
        classification_result = self.intent_classifier.classify_intent(text)

        # Extract action parameters
        action_params = self.extract_action_parameters(text, classification_result['intent'])

        # Map to robot action
        robot_action = self.action_mapper.map_to_robot_action(
            classification_result['intent'],
            action_params,
            classification_result['entities']
        )

        return {
            'intent': classification_result['intent'],
            'confidence': classification_result['confidence'],
            'entities': classification_result['entities'],
            'action': robot_action,
            'original_command': text
        }

    def extract_action_parameters(self, text, intent):
        """
        Extract specific parameters for different intent types
        """
        params = {}

        if intent == 'navigation':
            # Extract destination from navigation commands
            destination = self.extract_destination(text)
            if destination:
                params['destination'] = destination

        elif intent == 'manipulation':
            # Extract object and location for manipulation
            target_object = self.extract_object(text)
            if target_object:
                params['object'] = target_object

            location = self.extract_location(text)
            if location:
                params['location'] = location

        elif intent == 'interaction':
            # Extract person or object to interact with
            target = self.extract_target(text)
            if target:
                params['target'] = target

        return params

    def extract_destination(self, text):
        """
        Extract destination from navigation commands
        """
        # Look for location indicators
        location_patterns = [
            r'to the (\w+)',
            r'to (\w+)',
            r'go to (\w+)',
            r'walk to (\w+)'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def extract_object(self, text):
        """
        Extract object from manipulation commands
        """
        object_patterns = [
            r'pick up the (\w+)',
            r'pick up (\w+)',
            r'grasp the (\w+)',
            r'take the (\w+)',
            r'bring me the (\w+)',
            r'get the (\w+)'
        ]

        for pattern in object_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def extract_location(self, text):
        """
        Extract location from commands
        """
        location_patterns = [
            r'from the (\w+)',
            r'from (\w+)',
            r'in the (\w+)',
            r'on the (\w+)'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def extract_target(self, text):
        """
        Extract target for interaction commands
        """
        target_patterns = [
            r'talk to (\w+)',
            r'greet (\w+)',
            r'meet (\w+)',
            r'wave to (\w+)'
        ]

        for pattern in target_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None
```

## Mapping Voice Commands to ROS 2 Actions

### ROS 2 Action Architecture

ROS 2 actions provide the communication pattern for long-running robot tasks that may take significant time to complete. Actions are ideal for voice-controlled robotics as they provide feedback during execution and allow for goal preemption if new commands are received.

The action architecture consists of three main components:
- **Goal**: The request sent to the action server specifying what should be done
- **Feedback**: Periodic updates on the progress of the action
- **Result**: The final outcome of the action execution

```python
# ROS 2 action interface for voice-controlled robotics
import rclpy
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String
import threading
import time

class VoiceToActionMapper(Node):
    def __init__(self):
        super().__init__('voice_to_action_mapper')

        # Declare parameters
        self.declare_parameter('action_timeout', 60.0)
        self.declare_parameter('command_queue_size', 10)

        # Subscriptions
        self.command_sub = self.create_subscription(
            String,
            '/voice/commands',
            self.command_callback,
            10
        )

        # Action clients for different robot capabilities
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Command queue for processing voice commands
        self.command_queue = []
        self.command_lock = threading.Lock()

        # Timer for processing commands
        self.command_timer = self.create_timer(0.1, self.process_command_queue)

        # Current action tracking
        self.current_goal_handle = None
        self.action_timeout = self.get_parameter('action_timeout').value

    def command_callback(self, msg):
        """
        Callback for incoming voice commands
        """
        with self.command_lock:
            # Add command to queue for processing
            self.command_queue.append(msg.data)
            self.get_logger().info(f"Received voice command: {msg.data}")

    def process_command_queue(self):
        """
        Process commands from the queue
        """
        with self.command_lock:
            if not self.command_queue:
                return

            command = self.command_queue.pop(0)

        # Parse the command
        parser = NaturalLanguageParser()
        parsed_command = parser.parse_command(command)

        if parsed_command['confidence'] < 0.5:
            self.get_logger().warn(f"Low confidence command: {command}")
            return

        # Execute based on intent
        self.execute_command(parsed_command)

    def execute_command(self, parsed_command):
        """
        Execute parsed command by mapping to appropriate ROS 2 action
        """
        intent = parsed_command['intent']
        entities = parsed_command['entities']
        params = parsed_command.get('action', {}).get('params', {})

        if intent == 'navigation':
            self.execute_navigation_command(entities, params)
        elif intent == 'manipulation':
            self.execute_manipulation_command(entities, params)
        elif intent == 'control':
            self.execute_control_command(entities, params)
        else:
            self.get_logger().warn(f"Unsupported intent: {intent}")

    def execute_navigation_command(self, entities, params):
        """
        Execute navigation command by sending NavigateToPose action
        """
        # Extract destination from entities
        destination = entities.get('location', [None])[0] if 'location' in entities else params.get('destination')

        if not destination:
            self.get_logger().error("No destination specified in navigation command")
            return

        # Convert destination to pose (in a real system, this would use a map)
        target_pose = self.get_pose_for_location(destination)
        if not target_pose:
            self.get_logger().error(f"Unknown destination: {destination}")
            return

        # Create navigation goal
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = target_pose

        # Send goal
        self.nav_client.wait_for_server()
        future = self.nav_client.send_goal_async(goal_msg)
        future.add_done_callback(self.navigation_goal_response_callback)

    def get_pose_for_location(self, location):
        """
        Get pose for a named location (simplified - in real system would use map)
        """
        # Predefined locations in the environment
        location_poses = {
            'kitchen': PoseStamped(),
            'living room': PoseStamped(),
            'bedroom': PoseStamped(),
            'office': PoseStamped()
        }

        # Set default pose values
        if location in location_poses:
            pose_stamped = location_poses[location]
            pose_stamped.header.frame_id = 'map'
            # Set pose values based on location (would come from map in real system)
            return pose_stamped.pose

        return None

    def navigation_goal_response_callback(self, future):
        """
        Callback for navigation goal response
        """
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Navigation goal rejected')
            return

        self.get_logger().info('Navigation goal accepted')
        self.current_goal_handle = goal_handle

        # Get result future
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.navigation_result_callback)

    def navigation_result_callback(self, future):
        """
        Callback for navigation result
        """
        result = future.result().result
        self.get_logger().info(f'Navigation result: {result}')
        self.current_goal_handle = None

class ActionMapper:
    def __init__(self):
        """
        Map parsed intents to ROS 2 actions
        """
        self.action_mappings = {
            'navigation': {
                'action_type': 'NavigateToPose',
                'required_params': ['destination'],
                'optional_params': ['orientation']
            },
            'manipulation': {
                'action_type': 'ManipulateObject',
                'required_params': ['object'],
                'optional_params': ['location', 'gripper_position']
            },
            'interaction': {
                'action_type': 'InteractWith',
                'required_params': ['target'],
                'optional_params': ['greeting_type']
            },
            'control': {
                'action_type': 'RobotControl',
                'required_params': ['command'],
                'optional_params': []
            }
        }

    def map_to_robot_action(self, intent, params, entities):
        """
        Map intent and parameters to robot action
        """
        if intent not in self.action_mappings:
            return None

        action_def = self.action_mappings[intent]

        # Check if required parameters are present
        missing_params = []
        for param in action_def['required_params']:
            if param not in params and param not in entities:
                missing_params.append(param)

        if missing_params:
            rospy.logwarn(f"Missing required parameters for {intent}: {missing_params}")
            return None

        # Create action specification
        action_spec = {
            'action_type': action_def['action_type'],
            'intent': intent,
            'required_params': {param: params.get(param) or entities.get(param) for param in action_def['required_params']},
            'optional_params': {param: params.get(param) or entities.get(param) for param in action_def['optional_params']},
            'all_params': {**params, **entities}
        }

        return action_spec

class VoiceCommandValidator:
    def __init__(self, robot_capabilities):
        """
        Validate voice commands against robot capabilities
        """
        self.robot_capabilities = robot_capabilities
        self.valid_destinations = robot_capabilities.get('navigation', {}).get('destinations', [])
        self.valid_objects = robot_capabilities.get('manipulation', {}).get('objects', [])
        self.valid_actions = list(robot_capabilities.keys())

    def validate_command(self, parsed_command):
        """
        Validate parsed command against robot capabilities
        """
        intent = parsed_command['intent']
        entities = parsed_command['entities']
        params = parsed_command.get('action', {}).get('params', {})

        # Check if intent is supported
        if intent not in self.valid_actions:
            return False, f"Robot does not support {intent} actions"

        # Validate navigation commands
        if intent == 'navigation':
            destination = entities.get('location', [None])[0] if 'location' in entities else params.get('destination')
            if destination and destination not in self.valid_destinations:
                return False, f"Robot cannot navigate to {destination}"

        # Validate manipulation commands
        elif intent == 'manipulation':
            target_object = entities.get('object', [None])[0] if 'object' in entities else params.get('object')
            if target_object and target_object not in self.valid_objects:
                return False, f"Robot cannot manipulate {target_object}"

        return True, "Command is valid"
```

### Voice Command Validation and Error Handling

Robust voice-to-action systems must include comprehensive validation and error handling to ensure safe and reliable operation. This includes validation of speech recognition results, intent classification confidence, and action feasibility.

```python
# Voice command validation and error handling
class VoiceCommandValidator:
    def __init__(self, robot_capabilities):
        """
        Initialize validator with robot capabilities
        """
        self.robot_capabilities = robot_capabilities
        self.min_confidence = 0.6
        self.max_command_length = 100  # Maximum number of words
        self.valid_destinations = robot_capabilities.get('navigation', {}).get('destinations', [])
        self.valid_objects = robot_capabilities.get('manipulation', {}).get('objects', [])
        self.valid_actions = list(robot_capabilities.keys())

    def validate_full_command(self, text, parsed_result):
        """
        Validate complete voice command
        """
        # Check text length
        if len(text.split()) > self.max_command_length:
            return False, "Command too long"

        # Check intent confidence
        if parsed_result['confidence'] < self.min_confidence:
            return False, f"Low confidence in intent recognition: {parsed_result['confidence']:.2f}"

        # Validate based on intent
        intent = parsed_result['intent']
        entities = parsed_result['entities']

        if intent not in self.valid_actions:
            return False, f"Unsupported action type: {intent}"

        # Specific validation based on intent
        if intent == 'navigation':
            destination = entities.get('location', [None])[0] if 'location' in entities else None
            if destination and destination not in self.valid_destinations:
                return False, f"Invalid destination: {destination}"

        elif intent == 'manipulation':
            target_object = entities.get('object', [None])[0] if 'object' in entities else None
            if target_object and target_object not in self.valid_objects:
                return False, f"Invalid object: {target_object}"

        return True, "Command is valid"

class ErrorHandler:
    def __init__(self, node):
        self.node = node
        self.error_history = []
        self.max_history = 10

    def handle_recognition_error(self, error_msg):
        """
        Handle speech recognition errors
        """
        self.node.get_logger().error(f"Speech recognition error: {error_msg}")
        self.log_error("recognition", error_msg)

    def handle_intent_error(self, error_msg):
        """
        Handle intent classification errors
        """
        self.node.get_logger().error(f"Intent classification error: {error_msg}")
        self.log_error("intent", error_msg)

    def handle_action_error(self, error_msg):
        """
        Handle action execution errors
        """
        self.node.get_logger().error(f"Action execution error: {error_msg}")
        self.log_error("action", error_msg)

    def log_error(self, error_type, error_msg):
        """
        Log error with timestamp
        """
        error_entry = {
            'timestamp': time.time(),
            'type': error_type,
            'message': error_msg
        }
        self.error_history.append(error_entry)

        # Keep only recent errors
        if len(self.error_history) > self.max_history:
            self.error_history = self.error_history[-self.max_history:]

    def get_error_summary(self):
        """
        Get summary of recent errors
        """
        if not self.error_history:
            return "No recent errors"

        error_types = {}
        for error in self.error_history:
            error_types[error['type']] = error_types.get(error['type'], 0) + 1

        return f"Recent errors: {error_types}"

class VoiceToActionSystem:
    def __init__(self):
        """
        Complete voice-to-action system with validation and error handling
        """
        # Initialize components
        self.speech_recognizer = WhisperSpeechRecognizer()
        self.intent_classifier = IntentClassifier()
        self.action_mapper = ActionMapper()
        self.validator = VoiceCommandValidator(self.get_robot_capabilities())
        self.error_handler = ErrorHandler(self)

        # Command history for context
        self.command_history = []

    def get_robot_capabilities(self):
        """
        Define robot capabilities for validation
        """
        return {
            'navigation': {
                'destinations': ['kitchen', 'living room', 'bedroom', 'office', 'dining room']
            },
            'manipulation': {
                'objects': ['cup', 'book', 'ball', 'phone', 'keys', 'water bottle']
            },
            'interaction': {
                'capabilities': ['greeting', 'following', 'assistance']
            }
        }

    def process_voice_command(self, audio_input):
        """
        Complete pipeline for processing voice command
        """
        try:
            # Step 1: Speech recognition
            text = self.speech_recognizer.recognize_speech(audio_input)
            if not text:
                self.error_handler.handle_recognition_error("No speech detected or low confidence")
                return None

            # Step 2: Intent classification
            parsed_result = self.intent_classifier.classify_intent(text)
            if parsed_result['confidence'] < 0.5:
                self.error_handler.handle_intent_error(f"Low confidence intent: {parsed_result['intent']}")
                return None

            # Step 3: Validation
            is_valid, validation_msg = self.validator.validate_full_command(text, parsed_result)
            if not is_valid:
                self.error_handler.handle_intent_error(f"Command validation failed: {validation_msg}")
                return None

            # Step 4: Action mapping
            robot_action = self.action_mapper.map_to_robot_action(
                parsed_result['intent'],
                parsed_result.get('action', {}).get('params', {}),
                parsed_result['entities']
            )

            if not robot_action:
                self.error_handler.handle_action_error("Could not map intent to action")
                return None

            # Step 5: Store in history
            command_entry = {
                'timestamp': time.time(),
                'original_text': text,
                'parsed': parsed_result,
                'action': robot_action
            }
            self.command_history.append(command_entry)

            # Keep only recent commands
            if len(self.command_history) > 50:
                self.command_history = self.command_history[-50:]

            return robot_action

        except Exception as e:
            self.error_handler.handle_action_error(f"Unexpected error in voice processing: {str(e)}")
            return None

    def get_system_status(self):
        """
        Get status of the voice-to-action system
        """
        return {
            'error_summary': self.error_handler.get_error_summary(),
            'command_count': len(self.command_history),
            'recent_commands': [cmd['original_text'] for cmd in self.command_history[-5:]]
        }
```

## Integration with ROS 2 Action Servers

### ROS 2 Action Client Implementation

The integration of voice processing with ROS 2 action servers requires careful coordination between the speech recognition, intent classification, and action execution components. This integration ensures that voice commands are properly translated into executable robot actions while maintaining the reliability and feedback mechanisms of ROS 2.

```python
# ROS 2 action client for voice-controlled navigation
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy
import json

class VoiceNavigationActionClient(Node):
    def __init__(self):
        super().__init__('voice_navigation_action_client')

        # Create action client for navigation
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Subscription to voice commands
        self.voice_sub = self.create_subscription(
            String,
            'voice_commands',
            self.voice_command_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        )

        # Current goal tracking
        self._goal_handle = None
        self._current_destination = None

    def voice_command_callback(self, msg):
        """
        Callback for voice commands
        """
        command_text = msg.data
        self.get_logger().info(f"Received voice command: {command_text}")

        # Parse the command to extract destination
        destination = self.extract_destination_from_command(command_text)
        if destination:
            self.send_navigation_goal(destination)
        else:
            self.get_logger().warn(f"Could not extract destination from command: {command_text}")

    def extract_destination_from_command(self, command):
        """
        Extract destination from voice command
        """
        # Simple keyword-based extraction (in practice, use NLU)
        command_lower = command.lower()

        # Define known locations
        locations = {
            'kitchen': (1.0, 2.0, 0.0),  # (x, y, theta)
            'living room': (3.0, 1.0, 0.0),
            'bedroom': (0.0, -2.0, 1.57),
            'office': (-1.0, 1.0, 3.14),
            'dining room': (2.0, -1.0, -1.57)
        }

        for location, coordinates in locations.items():
            if location in command_lower:
                return location, coordinates

        return None, None

    def send_navigation_goal(self, destination_info):
        """
        Send navigation goal to action server
        """
        destination, coordinates = destination_info
        self._current_destination = destination

        # Wait for action server
        self._action_client.wait_for_server()

        # Create goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = coordinates[0]
        goal_msg.pose.pose.position.y = coordinates[1]
        goal_msg.pose.pose.position.z = 0.0

        # Set orientation (simple case: facing forward)
        from math import cos, sin
        theta = coordinates[2]
        goal_msg.pose.pose.orientation.z = sin(theta / 2.0)
        goal_msg.pose.pose.orientation.w = cos(theta / 2.0)

        # Send goal
        self.get_logger().info(f"Sending navigation goal to {destination} at {coordinates}")
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """
        Callback for goal response
        """
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Navigation goal rejected')
            return

        self.get_logger().info('Navigation goal accepted')
        self._goal_handle = goal_handle

        # Get result
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """
        Callback for action feedback
        """
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Navigation feedback: {feedback.current_pose}')

    def get_result_callback(self, future):
        """
        Callback for action result
        """
        result = future.result().result
        self.get_logger().info(f'Navigation result: {result}')
        self._goal_handle = None
        self._current_destination = None

class VoiceManipulationActionClient(Node):
    def __init__(self):
        super().__init__('voice_manipulation_action_client')

        # Action clients for manipulation (these would be custom action types)
        # self._grasp_client = ActionClient(self, GraspObject, 'grasp_object')
        # self._place_client = ActionClient(self, PlaceObject, 'place_object')

        # For this example, we'll use a simplified approach
        self.object_locations = {
            'cup': (0.5, 0.5, 0.75),  # (x, y, z) in robot frame
            'book': (0.6, 0.5, 0.75),
            'ball': (0.4, 0.6, 0.75)
        }

    def parse_manipulation_command(self, command):
        """
        Parse manipulation command to extract object and action
        """
        command_lower = command.lower()

        # Extract object
        target_object = None
        for obj in self.object_locations.keys():
            if obj in command_lower:
                target_object = obj
                break

        # Extract action (grasp, place, etc.)
        if 'grasp' in command_lower or 'pick up' in command_lower or 'take' in command_lower:
            action = 'grasp'
        elif 'place' in command_lower or 'put' in command_lower:
            action = 'place'
        else:
            action = 'unknown'

        return action, target_object

# Example of a custom action for manipulation
# This would typically be defined in a custom .action file and generated with action_msgs
class VoiceActionServer(Node):
    def __init__(self):
        super().__init__('voice_action_server')

        # Create action server for voice commands
        # This would be a custom action that handles the complete voice-to-action pipeline
        # self._action_server = ActionServer(
        #     self,
        #     VoiceCommand,  # Custom action type
        #     'voice_command',
        #     self.execute_callback
        # )

    def execute_callback(self, goal_handle):
        """
        Execute voice command goal
        """
        self.get_logger().info('Executing voice command')

        # Process the voice command
        command = goal_handle.request.command
        result = self.process_voice_command(command)

        # Create result message
        goal_handle.succeed()
        result_msg = VoiceCommand.Result()  # Custom result type
        result_msg.success = result['success']
        result_msg.message = result['message']

        return result_msg
```

## Best Practices and Optimization

### Performance Optimization

Optimizing voice-to-action systems requires balancing recognition accuracy with real-time performance. Several strategies can improve system efficiency:

```python
# Performance optimization techniques
class OptimizedVoiceToAction:
    def __init__(self):
        # Use threading for parallel processing
        self.processing_pool = ThreadPoolExecutor(max_workers=3)

        # Cache for frequently used models
        self.model_cache = {}

        # Audio preprocessing optimizations
        self.audio_preprocessor = self.initialize_audio_preprocessor()

        # Confidence threshold adjustment based on environment
        self.adaptive_threshold = 0.7

    def initialize_audio_preprocessor(self):
        """
        Initialize optimized audio preprocessing pipeline
        """
        # Use efficient audio processing libraries
        import webrtcvad  # For voice activity detection
        import pyrubberband  # For audio time stretching if needed

        vad = webrtcvad.Vad()
        vad.set_mode(1)  # Aggressive mode for robotics

        return {
            'vad': vad,
            'sample_rate': 16000,
            'frame_duration': 30  # ms
        }

    def adaptive_confidence_threshold(self, environment_noise_level):
        """
        Adjust confidence threshold based on environment
        """
        # Lower threshold in quiet environments, higher in noisy ones
        base_threshold = 0.7
        noise_factor = min(environment_noise_level / 0.1, 0.3)  # Max 0.3 adjustment

        self.adaptive_threshold = base_threshold + noise_factor
        return self.adaptive_threshold

class DialogueManager:
    def __init__(self):
        """
        Manage multi-turn conversations with robots
        """
        self.conversation_context = {}
        self.follow_up_expected = False
        self.current_task = None

    def process_command_with_context(self, command, user_id="default"):
        """
        Process command considering conversation context
        """
        context = self.conversation_context.get(user_id, {})

        # Handle follow-up commands that may reference previous context
        if self.follow_up_expected and self.current_task:
            # Resolve references like "it", "there", "the same place"
            resolved_command = self.resolve_references(command, context)
        else:
            resolved_command = command

        # Process the resolved command
        result = self.process_voice_command(resolved_command)

        # Update context
        self.update_context(user_id, command, result)

        return result

    def resolve_references(self, command, context):
        """
        Resolve linguistic references in command
        """
        command_lower = command.lower()

        # Replace references with resolved entities from context
        if 'it' in command_lower and context.get('last_object'):
            command = command.replace('it', context['last_object'])

        if 'there' in command_lower and context.get('last_location'):
            command = command.replace('there', context['last_location'])

        return command

    def update_context(self, user_id, command, result):
        """
        Update conversation context
        """
        if user_id not in self.conversation_context:
            self.conversation_context[user_id] = {}

        context = self.conversation_context[user_id]

        # Store relevant information from the interaction
        if result and result.get('entities'):
            if 'object' in result['entities']:
                context['last_object'] = result['entities']['object'][0]
            if 'location' in result['entities']:
                context['last_location'] = result['entities']['location'][0]

        context['last_command'] = command
        context['last_result'] = result
```

### Safety Considerations

Safety is paramount in voice-controlled robotics, especially when dealing with humanoid robots that operate in close proximity to humans.

```python
# Safety framework for voice-controlled robots
class VoiceControlSafetyFramework:
    def __init__(self, robot_interface):
        self.robot_interface = robot_interface
        self.safety_limits = self.define_safety_limits()
        self.emergency_stop_active = False
        self.safety_violations = 0
        self.max_violations_before_stop = 3

    def define_safety_limits(self):
        """
        Define safety limits for voice-controlled operation
        """
        return {
            'navigation': {
                'max_speed': 0.5,  # m/s
                'min_distance_to_human': 0.5,  # meters
                'restricted_areas': []  # Coordinates of restricted zones
            },
            'manipulation': {
                'max_force': 50.0,  # Newtons
                'max_velocity': 0.2,  # m/s
                'forbidden_objects': []  # Objects not to manipulate
            },
            'control': {
                'timeout': 30.0,  # seconds for action timeout
                'emergency_stop_keywords': ['stop', 'emergency', 'help', 'danger']
            }
        }

    def validate_voice_command_for_safety(self, parsed_command):
        """
        Validate voice command against safety constraints
        """
        intent = parsed_command['intent']
        entities = parsed_command['entities']
        action = parsed_command.get('action', {})

        # Check for emergency stop keywords
        original_text = parsed_command.get('original_text', '').lower()
        for keyword in self.safety_limits['control']['emergency_stop_keywords']:
            if keyword in original_text:
                self.trigger_emergency_stop()
                return False, f"Emergency stop triggered by keyword: {keyword}"

        # Validate navigation safety
        if intent == 'navigation':
            destination = entities.get('location', [None])[0] if 'location' in entities else None
            if destination in self.safety_limits['navigation']['restricted_areas']:
                return False, f"Navigation to restricted area: {destination}"

        # Validate manipulation safety
        elif intent == 'manipulation':
            target_object = entities.get('object', [None])[0] if 'object' in entities else None
            if target_object in self.safety_limits['manipulation']['forbidden_objects']:
                return False, f"Manipulation of forbidden object: {target_object}"

        return True, "Command is safe"

    def trigger_emergency_stop(self):
        """
        Trigger emergency stop for the robot
        """
        self.emergency_stop_active = True
        self.robot_interface.emergency_stop()
        self.get_logger().error("EMERGENCY STOP: Safety system activated")
```

## Looking Ahead

The next chapters will build upon this voice-to-action foundation. Chapter 3 will explore cognitive planning using LLMs to generate complex task sequences from high-level commands. Chapter 4 will address multi-modal perception that combines vision and language understanding. Finally, Chapter 5 will integrate all components in a comprehensive capstone project demonstrating a complete VLA-powered humanoid system.

The voice-to-action pipeline forms the foundation for natural human-robot interaction, enabling robots to understand and respond to complex, natural language commands. As these systems mature, we can expect increasingly sophisticated and intuitive interfaces that make robots more accessible and useful in human environments.

## Citations

- Radford, A., et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision. arXiv preprint arXiv:2212.04356.
- Brockett, C., et al. (2022). DialoGPT: Large-Scale Generative Pre-training for Conversational Response Generation. arXiv preprint arXiv:1911.00536.
- ROS 2 Navigation Working Group. (2023). ROS 2 Navigation System Documentation.
- Shi, C., et al. (2022). Spoken Language to Action: A Cross-Modal Learning Approach. Conference on Robot Learning.

## Summary

This chapter covered the implementation of a voice-to-action pipeline using Whisper for speech recognition, intent classification for understanding natural language commands, and mapping to ROS 2 actions for robot execution. We explored the architecture of such systems, implementation details for real-time operation, validation and error handling mechanisms, and integration with ROS 2 action servers. The voice-to-action pipeline enables natural human-robot interaction by converting spoken language into executable robot behaviors, forming a critical component of VLA systems.

## Review Questions/Exercises

1. How does Whisper's architecture make it suitable for real-time robotics applications?
2. What are the key components of intent classification in voice-to-action systems?
3. Explain the process of mapping natural language commands to ROS 2 actions.
4. Design a safety validation system for voice-controlled robot commands.
5. How would you implement dialogue management for multi-turn conversations with a humanoid robot?

---

**Chapter Specifications:**
- **Expected Length**: 2,000-3,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based implementations showing Whisper integration, intent classification, and ROS 2 action mapping
- **Diagrams/Illustrations**: Text-based architecture diagrams showing voice-to-action pipeline
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides