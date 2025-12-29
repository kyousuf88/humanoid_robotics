---
sidebar_position: 99
---

# Troubleshooting: Module 4 — Vision-Language-Action (VLA)

This guide covers common issues encountered when working with Whisper, LLMs (Llama 3), and VLA systems for robotics.

## Quick Diagnosis

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| Whisper not transcribing | Audio format issues | [whisper-issues](#whisper-issues) |
| LLM runs out of memory | Model too large | [llm-memory](#llm-memory) |
| Slow LLM inference | No GPU acceleration | [slow-inference](#slow-inference) |
| Action parsing fails | Prompt format wrong | [action-parsing](#action-parsing) |
| ROS action not executing | Action server not running | [ros-action](#ros-action) |

---

## Whisper Issues

### Whisper Transcription Issues {#whisper-issues}

**Symptoms**:
- Whisper returns empty transcription
- Audio not recognized
- "Invalid audio format" error

**Cause**:
Incompatible audio format, sample rate mismatch, or microphone configuration.

**Solution**:

1. Check audio format (must be 16kHz mono):
```python
import whisper
import librosa

# Load and resample audio
audio, sr = librosa.load("audio.wav", sr=16000, mono=True)
```

2. Verify microphone input:
```bash
# List audio devices
arecord -l

# Test recording
arecord -d 5 -f cd test.wav
aplay test.wav
```

3. Use correct Whisper model:
```python
import whisper

# Choose model based on accuracy/speed needs
model = whisper.load_model("base")  # Fast
model = whisper.load_model("small")  # Balanced
model = whisper.load_model("medium")  # Accurate
model = whisper.load_model("large")  # Most accurate (needs GPU)
```

4. Handle streaming audio:
```python
import sounddevice as sd
import numpy as np

def record_audio(duration=5, sample_rate=16000):
    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate,
                   channels=1,
                   dtype='float32')
    sd.wait()
    return audio.flatten()
```

5. Debug transcription:
```python
result = model.transcribe("audio.wav", verbose=True)
print(f"Language detected: {result['language']}")
print(f"Transcription: {result['text']}")
```

---

### Whisper Performance Issues {#whisper-performance}

**Symptoms**:
- Transcription takes too long
- High CPU usage
- Real-time transcription impossible

**Cause**:
Using CPU instead of GPU, or model too large.

**Solution**:

1. Enable GPU acceleration:
```python
import whisper
import torch

# Check CUDA availability
print(f"CUDA available: {torch.cuda.is_available()}")

# Load model on GPU
model = whisper.load_model("base", device="cuda")
```

2. Use faster-whisper for better performance:
```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.wav", beam_size=5)
```

3. Use appropriate model size:

| Model | VRAM Required | Speed | Accuracy |
|-------|---------------|-------|----------|
| tiny | ~1 GB | Fastest | Low |
| base | ~1 GB | Fast | Medium |
| small | ~2 GB | Medium | Good |
| medium | ~5 GB | Slow | High |
| large | ~10 GB | Slowest | Highest |

---

## LLM Issues

### LLM Memory Issues {#llm-memory}

**Symptoms**:
- "CUDA out of memory" error
- System hangs when loading model
- Python process killed

**Cause**:
Model size exceeds available GPU VRAM or system RAM.

**Solution**:

1. Check VRAM requirements:

| Model | Full Precision | 8-bit | 4-bit |
|-------|----------------|-------|-------|
| Llama 3 8B | ~16 GB | ~8 GB | ~4 GB |
| Llama 3 70B | ~140 GB | ~70 GB | ~35 GB |

2. Use quantized models:
```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"
)
```

3. Use llama.cpp for efficient inference:
```bash
# Build llama.cpp with CUDA
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make LLAMA_CUDA=1

# Download quantized model (GGUF format)
# Run inference
./main -m models/llama-3-8b-instruct.Q4_K_M.gguf -p "Your prompt here"
```

4. Use Ollama for simplified deployment:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama 3
ollama pull llama3

# Run
ollama run llama3 "Your prompt here"
```

---

### Slow LLM Inference {#slow-inference}

**Symptoms**:
- Response takes 30+ seconds
- Real-time interaction impossible
- GPU utilization low

**Cause**:
Running on CPU, inefficient loading, or suboptimal settings.

**Solution**:

1. Verify GPU is being used:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.current_device()}")
```

2. Use Flash Attention:
```python
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    torch_dtype=torch.float16,
    attn_implementation="flash_attention_2",  # Requires compatible GPU
    device_map="auto"
)
```

3. Use vLLM for high-throughput inference:
```bash
pip install vllm
```

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Meta-Llama-3-8B-Instruct")
sampling_params = SamplingParams(temperature=0.7, max_tokens=256)
outputs = llm.generate(["Your prompt"], sampling_params)
```

4. Limit max tokens for faster responses:
```python
# Shorter responses = faster generation
outputs = model.generate(
    inputs,
    max_new_tokens=128,  # Limit output length
    do_sample=True,
    temperature=0.7
)
```

---

## Action Parsing Issues

### Action Parsing Failures {#action-parsing}

**Symptoms**:
- LLM output can't be parsed into actions
- Robot doesn't understand commands
- Incorrect action sequences generated

**Cause**:
Inconsistent prompt format or LLM not following instructions.

**Solution**:

1. Use structured output format:
```python
SYSTEM_PROMPT = """You are a robot task planner. Given a user command,
output a JSON list of actions. Each action has:
- action_type: one of [move, pick, place, look, speak]
- parameters: dictionary of action parameters

Example output:
[
  {"action_type": "move", "parameters": {"target": "kitchen"}},
  {"action_type": "pick", "parameters": {"object": "cup"}}
]

Only output valid JSON. No explanations."""
```

2. Add output validation:
```python
import json

def parse_actions(llm_output):
    try:
        # Try to extract JSON from response
        json_start = llm_output.find('[')
        json_end = llm_output.rfind(']') + 1
        json_str = llm_output[json_start:json_end]

        actions = json.loads(json_str)
        return validate_actions(actions)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return None

def validate_actions(actions):
    valid_types = ['move', 'pick', 'place', 'look', 'speak']
    for action in actions:
        if action.get('action_type') not in valid_types:
            raise ValueError(f"Invalid action type: {action.get('action_type')}")
    return actions
```

3. Use few-shot prompting:
```python
FEW_SHOT_EXAMPLES = """
User: Go to the kitchen and get a cup
Output: [{"action_type": "move", "parameters": {"target": "kitchen"}},
         {"action_type": "pick", "parameters": {"object": "cup"}}]

User: Look for the red ball
Output: [{"action_type": "look", "parameters": {"object": "red ball"}}]

User: {user_command}
Output:"""
```

---

## ROS Action Issues

### ROS Action Issues {#ros-action}

**Symptoms**:
- `ros2 action send_goal` hangs
- Action server not responding
- Goal rejected or aborted

**Cause**:
Action server not running, type mismatch, or execution errors.

**Solution**:

1. Verify action server is running:
```bash
ros2 action list
ros2 action info /robot_action
```

2. Check action type:
```bash
ros2 action type /robot_action
# Should match your client's action type
```

3. Implement robust action server:
```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from robot_interfaces.action import ExecuteTask

class TaskActionServer(Node):
    def __init__(self):
        super().__init__('task_action_server')
        self._action_server = ActionServer(
            self,
            ExecuteTask,
            'execute_task',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

    def goal_callback(self, goal_request):
        self.get_logger().info(f'Received goal: {goal_request.task}')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Cancel requested')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        try:
            # Execute task
            result = ExecuteTask.Result()
            result.success = True
            goal_handle.succeed()
            return result
        except Exception as e:
            self.get_logger().error(f'Execution failed: {e}')
            goal_handle.abort()
            return ExecuteTask.Result(success=False)
```

4. Debug action client:
```python
import rclpy
from rclpy.action import ActionClient

class TaskActionClient(Node):
    def __init__(self):
        super().__init__('task_action_client')
        self._action_client = ActionClient(self, ExecuteTask, 'execute_task')

    def send_goal(self, task):
        # Wait for server
        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Action server not available')
            return None

        goal_msg = ExecuteTask.Goal()
        goal_msg.task = task

        future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        return future
```

---

## Error Messages Reference

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `Whisper: Invalid audio format` | Sample rate != 16kHz | Resample to 16kHz mono |
| `CUDA out of memory` | Model too large for VRAM | Use quantized model |
| `torch.cuda.OutOfMemoryError` | Insufficient GPU memory | Reduce batch size, use 4-bit |
| `JSONDecodeError` | LLM output not valid JSON | Add output validation, improve prompt |
| `Action server not available` | Server not running | Start action server node |

---

## Getting Help

### Official Resources

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Llama 3 Documentation](https://llama.meta.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [ROS 2 Actions Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)

### Community Support

- [Hugging Face Forums](https://discuss.huggingface.co/)
- [LocalLLaMA Reddit](https://www.reddit.com/r/LocalLLaMA/)
- [ROS Discourse](https://discourse.ros.org/)

---

## FAQ

**Q: Can I use ChatGPT instead of local LLMs?**

A: Yes, but consider latency (~500ms+ API calls vs ~50ms local) and cost for real-time robotics applications.

**Q: What's the minimum GPU for Llama 3 8B?**

A: RTX 3060 12GB can run 4-bit quantized Llama 3 8B. For full precision, RTX 4090 24GB or better is needed.

**Q: How do I handle multi-turn conversations?**

A: Maintain conversation history in your prompt:
```python
history = []
def get_response(user_input):
    history.append({"role": "user", "content": user_input})
    response = llm.chat(messages=history)
    history.append({"role": "assistant", "content": response})
    return response
```
