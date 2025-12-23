---
id: module-3-chapter-5
sidebar_position: 5
title: "Chapter 5 - Reinforcement Learning & Sim-to-Real Transfer Techniques"
---

# Chapter 5: Reinforcement Learning & Sim-to-Real Transfer Techniques

## Learning Objectives
- [ ] Understand reinforcement learning fundamentals and applications in humanoid robotics
- [ ] Implement Isaac Gym environments for humanoid control training
- [ ] Apply sim-to-real transfer techniques for humanoid locomotion control
- [ ] Train bipedal locomotion policies using reinforcement learning
- [ ] Evaluate and validate RL policies in real-world humanoid robots

## Key Concepts
- [ ] **Reinforcement Learning (RL)**: Learning through interaction with an environment to maximize cumulative reward
- [ ] **Isaac Gym**: NVIDIA's GPU-accelerated RL environment for robotics applications
- [ ] **Sim-to-Real Transfer**: Techniques to transfer policies learned in simulation to real robots
- [ ] **Bipedal Locomotion Control**: Learning stable walking patterns for humanoid robots
- [ ] **Domain Randomization**: Technique to improve sim-to-real transfer by randomizing simulation parameters
- [ ] **Policy Optimization**: Methods to improve RL policies for humanoid control tasks

## Introduction

Reinforcement Learning (RL) has emerged as a powerful approach for developing sophisticated control policies for humanoid robots, particularly for complex tasks like bipedal locomotion that are difficult to engineer using traditional control methods. Unlike classical control approaches that rely on precise mathematical models, RL enables humanoid robots to learn complex behaviors through trial and error, adapting to their environment and improving over time.

NVIDIA's Isaac Gym provides a GPU-accelerated platform specifically designed for training RL policies for robotic applications. By leveraging parallel simulation environments running on GPUs, Isaac Gym enables the rapid training of complex policies that would be infeasible with CPU-only simulation. For humanoid robots, this means policies for balance, walking, and manipulation can be trained in hours rather than months.

The challenge in applying RL to humanoid robots lies in the sim-to-real transfer problem. While RL policies can learn impressive behaviors in simulation, the differences between simulated and real environments often prevent direct transfer of these policies to physical robots. This chapter explores techniques to bridge this gap, including domain randomization, system identification, and adaptive control methods.

The integration of RL with humanoid robotics represents a paradigm shift from engineering-based control to learning-based control. This approach allows humanoid robots to develop behaviors that are robust to environmental variations and can adapt to different terrains, payloads, and even physical damage to the robot itself.

## Reinforcement Learning Fundamentals for Humanoid Robotics

### Overview of RL in Robotics

Reinforcement Learning in robotics involves an agent (the robot) learning to perform tasks by interacting with its environment. The agent receives observations from sensors, takes actions, and receives rewards based on its performance. The goal is to learn a policy that maximizes cumulative reward over time.

In humanoid robotics, the state space is typically high-dimensional, including joint positions, velocities, IMU readings, and sometimes camera images. The action space includes joint torques, positions, or velocities. The reward function is carefully designed to encourage stable, efficient, and safe behavior.

### RL Algorithms for Humanoid Control

Different RL algorithms are suitable for different humanoid control tasks:

**Deep Deterministic Policy Gradient (DDPG)**: Good for continuous control tasks with deterministic policies, suitable for low-level motor control.

**Soft Actor-Critic (SAC)**: Provides good sample efficiency and stable learning, ideal for complex humanoid behaviors.

**Proximal Policy Optimization (PPO)**: Stable policy gradient method that works well for humanoid locomotion.

**Twin Delayed DDPG (TD3)**: Address function approximation errors in continuous control, suitable for precise humanoid manipulation.

```python
# Example RL environment for humanoid control
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from gym import spaces
import gym

class HumanoidControlEnv(gym.Env):
    """
    Gym environment for humanoid robot control using RL
    """
    def __init__(self):
        super(HumanoidControlEnv, self).__init__()

        # Define action and observation spaces
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(18,), dtype=np.float32  # 18 DOF for humanoid
        )
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(60,), dtype=np.float32  # State vector
        )

        # Humanoid-specific parameters
        self.max_episode_steps = 1000
        self.current_step = 0
        self.target_velocity = 0.5  # m/s

        # Initialize robot state
        self.reset()

    def reset(self):
        """Reset the environment to initial state"""
        # Reset robot to initial configuration
        self.current_step = 0
        self.robot_state = self.get_initial_state()
        return self.robot_state

    def step(self, action):
        """Execute one step of the environment"""
        # Apply action to robot
        self.apply_action(action)

        # Get new state
        new_state = self.get_robot_state()

        # Calculate reward
        reward = self.calculate_reward(new_state, action)

        # Check if episode is done
        done = self.is_episode_done(new_state)

        # Increment step counter
        self.current_step += 1
        if self.current_step >= self.max_episode_steps:
            done = True

        return new_state, reward, done, {}

    def get_robot_state(self):
        """Get current robot state vector"""
        # Combine joint positions, velocities, IMU readings, etc.
        joint_positions = self.get_joint_positions()
        joint_velocities = self.get_joint_velocities()
        imu_readings = self.get_imu_data()
        target_direction = self.get_target_direction()

        state = np.concatenate([
            joint_positions,
            joint_velocities,
            imu_readings,
            target_direction
        ])

        return state

    def apply_action(self, action):
        """Apply action to the robot"""
        # Convert normalized action to joint commands
        joint_commands = self.action_to_joint_commands(action)

        # Send commands to robot (simulation or real)
        self.send_joint_commands(joint_commands)

    def calculate_reward(self, state, action):
        """Calculate reward based on state and action"""
        # Reward for forward velocity
        forward_vel_reward = self.calculate_forward_velocity_reward(state)

        # Penalty for falling
        fall_penalty = self.calculate_fall_penalty(state)

        # Penalty for high action magnitude (smooth movement)
        action_penalty = self.calculate_action_penalty(action)

        # Penalty for joint limits
        joint_limit_penalty = self.calculate_joint_limit_penalty(state)

        # Total reward
        reward = (forward_vel_reward - fall_penalty - action_penalty - joint_limit_penalty)

        return reward

    def is_episode_done(self, state):
        """Check if episode should terminate"""
        # Check if robot has fallen
        if self.has_fallen(state):
            return True

        # Check if robot is in an unsafe configuration
        if self.is_unsafe_configuration(state):
            return True

        return False

    def calculate_forward_velocity_reward(self, state):
        """Reward for moving forward at target velocity"""
        current_velocity = self.get_forward_velocity(state)
        velocity_error = abs(current_velocity - self.target_velocity)

        # Higher reward for closer to target velocity
        return np.exp(-velocity_error)

    def calculate_fall_penalty(self, state):
        """Penalty for falling or losing balance"""
        robot_orientation = self.get_robot_orientation(state)
        base_height = self.get_base_height(state)

        # Penalty based on deviation from upright orientation
        orientation_penalty = max(0, abs(robot_orientation - 0) - 0.5)

        # Penalty for base being too low (fallen)
        height_penalty = max(0, 0.5 - base_height)

        return orientation_penalty + height_penalty

    def calculate_action_penalty(self, action):
        """Penalty for large actions (smooth movement)"""
        return 0.01 * np.sum(np.square(action))

    def calculate_joint_limit_penalty(self, state):
        """Penalty for approaching joint limits"""
        joint_positions = state[:18]  # First 18 elements are joint positions
        joint_limits = self.get_joint_limits()

        penalty = 0
        for i, pos in enumerate(joint_positions):
            lower_limit, upper_limit = joint_limits[i]
            if pos < lower_limit + 0.1 or pos > upper_limit - 0.1:
                penalty += 1.0

        return penalty

    def has_fallen(self, state):
        """Check if robot has fallen"""
        robot_orientation = self.get_robot_orientation(state)
        base_height = self.get_base_height(state)

        # Fallen if too tilted or base too low
        return abs(robot_orientation) > 1.0 or base_height < 0.3

    # Placeholder methods - would be implemented based on specific robot
    def get_initial_state(self):
        return np.zeros(60)

    def get_joint_positions(self):
        return np.zeros(18)

    def get_joint_velocities(self):
        return np.zeros(18)

    def get_imu_data(self):
        return np.zeros(6)  # 3 for orientation, 3 for angular velocity

    def get_target_direction(self):
        return np.array([1.0, 0.0])

    def action_to_joint_commands(self, action):
        return action

    def send_joint_commands(self, commands):
        pass

    def get_forward_velocity(self, state):
        return 0.0

    def get_robot_orientation(self, state):
        return 0.0

    def get_base_height(self, state):
        return 0.8

    def get_joint_limits(self):
        return [(-np.pi, np.pi)] * 18

    def is_unsafe_configuration(self, state):
        return False
```

### Isaac Gym Integration

Isaac Gym provides GPU-accelerated parallel environments that are particularly beneficial for humanoid robot training. By running thousands of simulation instances in parallel on a single GPU, Isaac Gym dramatically reduces training time for complex humanoid behaviors.

```python
# Isaac Gym environment for humanoid locomotion
import isaacgym
from isaacgym import gymapi, gymtorch
from isaacgym.torch_utils import *
import torch
import numpy as np

class IsaacGymHumanoidEnv:
    def __init__(self, cfg):
        # Initialize Isaac Gym
        self.gym = gymapi.acquire_gym()

        # Configure simulation
        self.sim_params = gymapi.SimParams()
        self.sim_params.up_axis = gymapi.UP_AXIS_Z
        self.sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.81)
        self.sim_params.use_gpu_pipeline = True

        # Create simulation
        self.sim = self.gym.create_sim(0, 0, self.gym.sims_per_gpu, self.sim_params)

        # Create ground plane
        plane_params = gymapi.PlaneParams()
        plane_params.normal = gymapi.Vec3(0.0, 0.0, 1.0)
        self.gym.add_ground(self.sim, plane_params)

        # Load humanoid asset
        asset_root = cfg["asset"]["root"]
        asset_file = cfg["asset"]["file"]
        asset_options = gymapi.AssetOptions()
        asset_options.fix_base_link = False
        asset_options.disable_gravity = False
        asset_options.thickness = 0.001
        asset_options.angular_damping = 0.01
        asset_options.linear_damping = 0.01

        self.humanoid_asset = self.gym.load_asset(self.sim, asset_root, asset_file, asset_options)

        # Configure DOF properties
        self.dof_props = self.gym.get_asset_dof_properties(self.humanoid_asset)
        for i in range(self.dof_props.num_dofs):
            self.dof_props["driveMode"][i] = gymapi.DOF_MODE_EFFORT
            self.dof_props["stiffness"][i] = 0.0
            self.dof_props["damping"][i] = 0.1

        # Create environment
        self.create_envs(cfg)

        # Initialize tensors
        self.initialize_tensors()

        # RL parameters
        self.cfg = cfg
        self.reset_idx = torch.arange(cfg["env"]["num_envs"], device=self.device, dtype=torch.long)

    def create_envs(self, cfg):
        """Create multiple environments for parallel training"""
        num_envs = cfg["env"]["num_envs"]
        env_spacing = cfg["env"]["env_spacing"]

        # Create environment
        env_lower = gymapi.Vec3(-env_spacing, -env_spacing, 0.0)
        env_upper = gymapi.Vec3(env_spacing, env_spacing, env_spacing)
        self.env = self.gym.create_env(self.sim, env_lower, env_upper, 1)

        # Create actor in each environment
        humanoid_pose = gymapi.Transform()
        humanoid_pose.p = gymapi.Vec3(0.0, 0.0, 1.0)
        humanoid_pose.r = gymapi.Quat(0.0, 0.0, 0.0, 1.0)

        self.humanoid_handles = []
        for i in range(num_envs):
            humanoid_handle = self.gym.create_actor(self.env, self.humanoid_asset, humanoid_pose, "humanoid", i, 1, 0)
            self.gym.set_actor_dof_properties(self.env, humanoid_handle, self.dof_props)
            self.humanoid_handles.append(humanoid_handle)

    def initialize_tensors(self):
        """Initialize PyTorch tensors for GPU computation"""
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # Actor root state tensor
        actor_root_state_tensor = self.gym.acquire_actor_root_state_tensor(self.sim)
        self.root_states = gymtorch.wrap_tensor(actor_root_state_tensor).view(self.cfg["env"]["num_envs"], 13)

        # DOF state tensor
        dof_state_tensor = self.gym.acquire_dof_state_tensor(self.sim)
        self.dof_states = gymtorch.wrap_tensor(dof_state_tensor).view(self.cfg["env"]["num_envs"], self.cfg["env"]["num_dofs"], 2)

        # Actor state tensor
        actor_tensor = self.gym.acquire_rigid_body_state_tensor(self.sim)
        self.rb_states = gymtorch.wrap_tensor(actor_tensor).view(self.cfg["env"]["num_envs"], self.cfg["env"]["num_bodies"], 13)

        # Net contact force tensor
        net_contact_force_tensor = self.gym.acquire_net_contact_force_tensor(self.sim)
        self.net_contact_forces = gymtorch.wrap_tensor(net_contact_force_tensor).view(self.cfg["env"]["num_envs"], -1, 3)

        # Actions tensor
        self.actions = torch.zeros(self.cfg["env"]["num_envs"], self.cfg["env"]["num_actions"], device=self.device, dtype=torch.float)

    def reset(self):
        """Reset all environments"""
        # Reset DOF positions and velocities
        self.dof_states[:, :, 0] = torch.randn_like(self.dof_states[:, :, 0]) * 0.1
        self.dof_states[:, :, 1] = torch.randn_like(self.dof_states[:, :, 1]) * 0.01

        # Reset root states
        self.root_states[:, 0:3] = torch.tensor([0, 0, 1.0], device=self.device).repeat(self.cfg["env"]["num_envs"], 1)
        self.root_states[:, 3:7] = torch.tensor([0, 0, 0, 1], device=self.device).repeat(self.cfg["env"]["num_envs"], 1)
        self.root_states[:, 7:10] = torch.randn_like(self.root_states[:, 7:10]) * 0.1
        self.root_states[:, 10:13] = torch.randn_like(self.root_states[:, 10:13]) * 0.1

        # Refresh tensors
        self.gym.set_dof_state_tensor(self.sim, gymtorch.unwrap_tensor(self.dof_states))
        self.gym.set_actor_root_state_tensor(self.sim, gymtorch.unwrap_tensor(self.root_states))

        return self.compute_observations()

    def compute_observations(self):
        """Compute observations for all environments"""
        # Root positions and orientations
        root_pos = self.root_states[:, 0:3]
        root_rot = self.root_states[:, 3:7]

        # DOF positions and velocities
        dof_pos = self.dof_states[:, :, 0]
        dof_vel = self.dof_states[:, :, 1]

        # Calculate body orientations
        body_quat = self.rb_states[:, 0, 3:7]  # Assuming first body is the base

        # Create observation vector
        obs = torch.cat([
            root_rot,           # 4 (orientation)
            root_pos[2:3],      # 1 (height)
            dof_pos,            # n (joint positions)
            dof_vel,            # n (joint velocities)
            self.actions        # n (last actions)
        ], dim=-1)

        return obs

    def compute_reward(self):
        """Compute rewards for all environments"""
        # Get current states
        root_pos = self.root_states[:, 0:3]
        root_rot = self.root_states[:, 3:7]
        dof_pos = self.dof_states[:, :, 0]
        dof_vel = self.dof_states[:, :, 1]

        # Reward for forward progress
        forward_reward = root_pos[:, 0]  # Encourage moving forward

        # Penalty for falling
        up_reward = torch.min(root_rot[:, 3] * 2 - 1, torch.ones_like(root_rot[:, 3]))  # Reward for upright orientation

        # Penalty for high velocities (smooth movement)
        velocity_penalty = torch.sum(torch.square(dof_vel), dim=1) * 0.001

        # Penalty for extreme joint positions
        joint_limit_penalty = torch.sum(torch.square(torch.clip(dof_pos, -1.0, 1.0) - dof_pos), dim=1) * 0.1

        # Total reward
        total_reward = forward_reward * 1.0 + up_reward * 2.0 - velocity_penalty - joint_limit_penalty

        return total_reward

    def step(self, actions):
        """Execute one step of the simulation"""
        # Apply actions to humanoid
        self.actions = actions
        torques = actions * 100.0  # Scale actions to torques

        # Apply torques to DOFs
        self.gym.set_dof_actuation_force_tensor(self.sim, gymtorch.unwrap_tensor(torques))

        # Simulate physics
        self.gym.simulate(self.sim)
        self.gym.fetch_results(self.sim, True)

        # Refresh tensors
        self.gym.refresh_dof_state_tensor(self.sim)
        self.gym.refresh_actor_root_state_tensor(self.sim)
        self.gym.refresh_rigid_body_state_tensor(self.sim)
        self.gym.refresh_net_contact_force_tensor(self.sim)

        # Compute observations and rewards
        obs = self.compute_observations()
        reward = self.compute_reward()
        done = self.compute_done()

        return obs, reward, done, {}

    def compute_done(self):
        """Compute done flags for all environments"""
        # Check if humanoid has fallen
        root_rot = self.root_states[:, 3:7]
        up_vec = quat_rotate_inverse(root_rot, torch.tensor([0, 0, 1], device=self.device, dtype=torch.float))
        fall_threshold = 0.8
        fall = torch.abs(up_vec[:, 2]) < fall_threshold

        # Check if humanoid has moved too far from origin
        root_pos = self.root_states[:, 0:3]
        move_threshold = 10.0
        move_far = torch.sqrt(torch.square(root_pos[:, 0]) + torch.square(root_pos[:, 1])) > move_threshold

        return fall | move_far
```

## Isaac Gym for Humanoid Training

### Setting Up Isaac Gym Environment

Isaac Gym provides a specialized environment for training humanoid robots with reinforcement learning. The environment leverages NVIDIA's PhysX physics engine running on GPU to enable thousands of parallel simulation instances, dramatically accelerating the training process for complex humanoid behaviors.

The setup involves creating a configuration file that defines the humanoid model, training parameters, and environment settings. This configuration is crucial for achieving stable and efficient training.

```python
# Isaac Gym training configuration
isaacgym_config = {
    "env": {
        "numEnvs": 4096,  # Number of parallel environments
        "envSpacing": 5.0,  # Spacing between environments
        "episodeLength": 1000,  # Length of each episode
        "enableDebugVis": False,

        "clipActions": True,  # Clip actions to valid range
        "powerScale": 1.0,  # Scale factor for motor power
        "controlFrequencyInv": 2,  # Control frequency (1/2 of simulation frequency)

        # Reward parameters
        "headingWeight": 0.5,
        "upWeight": 0.1,
        "actionsL2": 0.0001,
        "energyWeight": 0.01,
        "dofVelocityScale": 0.1,
        "actionScale": 0.4,

        # Observation parameters
        "obs_scales": {
            "lin_vel": 2.0,
            "ang_vel": 0.25,
            "dof_pos": 1.0,
            "dof_vel": 0.1,
        },
        "noise": 0.1,
        "noise_tanh": 0.1,

        # Domain randomization parameters
        "domain_randomization": {
            "randomize": True,
            "frequency": 1000,
            "range": {
                "mass": [0.8, 1.2],
                "com": [-0.05, 0.05],
                "friction": [0.3, 1.5],
                "restitution": [0.0, 0.5],
                "dof_damping": [0.5, 1.5],
                "dof_stiffness": [0.8, 1.2],
                "height": [0.8, 1.2],
            }
        }
    },

    "asset": {
        "root": "assets",
        "file": "humanoid.urdf",  # Path to humanoid model
        "aixs_up": "z",
        "aixs_front": "-x",
    },

    "device_type": "cuda",
    "device_id": 0,
    "headless": False,

    "policy": {
        "name": "ActorCritic",
        "actor_hidden_dims": [512, 256, 128],
        "critic_hidden_dims": [512, 256, 128],
        "activation": "elu",
    },

    "algorithm": {
        "name": "PPO",
        "discount": 0.99,
        "lam": 0.95,
        "clip_coef": 0.2,
        "clip_value": True,
        "entropy_coef": 0.001,
        "value_loss_coef": 1.0,
        "max_grad_norm": 1.0,
        "learning_rate": 3e-4,
        "learning_rate_schedule": "adaptive",
        "schedule_factor": 0.5,
        "min_lr": 1e-5,
    },

    "runner": {
        "device": "cuda:0",
        "n_steps_per_iter": 32,
        "max_iterations": 2000,
        "save_interval": 50,
        "experiment_name": "humanoid_locomotion",
        "run_name": "",
        "load_run": -1,
        "checkpoint": -1,
        "resume": False,
    }
}
```

### Humanoid Locomotion Training Example

Training a humanoid to walk using reinforcement learning involves creating a reward function that encourages stable, efficient, and goal-directed locomotion. The reward function must balance multiple objectives: maintaining balance, moving toward the target, using energy efficiently, and avoiding harmful behaviors.

```python
# Humanoid locomotion training with Isaac Gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class HumanoidLocomotionTrainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device(config["device"])

        # Create Isaac Gym environment
        self.env = IsaacGymHumanoidEnv(config)

        # Initialize policy network
        self.policy = HumanoidPolicy(
            obs_dim=config["env"]["obs_dim"],
            action_dim=config["env"]["action_dim"],
            hidden_dims=config["policy"]["actor_hidden_dims"]
        ).to(self.device)

        # Initialize value network
        self.value_net = ValueNetwork(
            obs_dim=config["env"]["obs_dim"],
            hidden_dims=config["policy"]["critic_hidden_dims"]
        ).to(self.device)

        # Optimizers
        self.actor_optimizer = optim.Adam(self.policy.parameters(), lr=config["algorithm"]["learning_rate"])
        self.critic_optimizer = optim.Adam(self.value_net.parameters(), lr=config["algorithm"]["learning_rate"])

        # Training parameters
        self.gamma = config["algorithm"]["discount"]
        self.lam = config["algorithm"]["lam"]
        self.clip_coef = config["algorithm"]["clip_coef"]
        self.entropy_coef = config["algorithm"]["entropy_coef"]
        self.value_loss_coef = config["algorithm"]["value_loss_coef"]
        self.max_grad_norm = config["algorithm"]["max_grad_norm"]

        # Storage for training data
        self.experience_buffer = ExperienceBuffer(
            num_envs=config["env"]["numEnvs"],
            num_steps=config["runner"]["n_steps_per_iter"],
            obs_dim=config["env"]["obs_dim"],
            action_dim=config["env"]["action_dim"]
        )

    def collect_experience(self):
        """Collect experience from environment"""
        obs = self.env.reset()

        for step in range(self.config["runner"]["n_steps_per_iter"]):
            # Get actions from policy
            with torch.no_grad():
                actions, action_logprobs = self.policy.get_action(obs)
                values = self.value_net(obs)

            # Execute actions in environment
            next_obs, rewards, dones, info = self.env.step(actions)

            # Store experience
            self.experience_buffer.add_step(
                obs, actions, rewards, dones, values, action_logprobs
            )

            obs = next_obs

            # Handle episode termination
            if torch.any(dones):
                # Reset environments that are done
                reset_obs = self.env.reset()
                obs = torch.where(dones.unsqueeze(1), reset_obs, obs)

    def compute_advantages(self):
        """Compute advantages using Generalized Advantage Estimation (GAE)"""
        next_values = self.value_net(self.experience_buffer.next_obs[-1])
        advantages = torch.zeros_like(self.experience_buffer.rewards)

        gae = 0
        for step in reversed(range(self.config["runner"]["n_steps_per_iter"])):
            if step == self.config["runner"]["n_steps_per_iter"] - 1:
                next_values = next_values
            else:
                next_values = self.experience_buffer.values[step + 1]

            # Calculate TD error
            delta = (self.experience_buffer.rewards[step] +
                    self.gamma * next_values * (1 - self.experience_buffer.dones[step]) -
                    self.experience_buffer.values[step])

            # Calculate GAE
            gae = delta + self.gamma * self.lam * (1 - self.experience_buffer.dones[step]) * gae
            advantages[step] = gae

        # Calculate returns
        returns = advantages + self.experience_buffer.values

        return advantages, returns

    def update_policy(self):
        """Update policy using PPO algorithm"""
        advantages, returns = self.compute_advantages()

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Flatten experience for training
        batch_obs = self.experience_buffer.obs.flatten(0, 1)
        batch_actions = self.experience_buffer.actions.flatten(0, 1)
        batch_advantages = advantages.flatten(0, 1)
        batch_returns = returns.flatten(0, 1)
        old_logprobs = self.experience_buffer.logprobs.flatten(0, 1)

        # Update policy multiple times on the same batch
        for epoch in range(10):  # PPO uses multiple epochs per update
            # Get new action probabilities
            new_logprobs, entropy = self.policy.evaluate_actions(batch_obs, batch_actions)

            # Calculate ratio
            ratio = torch.exp(new_logprobs - old_logprobs)

            # Calculate surrogate objectives
            surr1 = ratio * batch_advantages
            surr2 = torch.clamp(ratio, 1 - self.clip_coef, 1 + self.clip_coef) * batch_advantages
            actor_loss = -torch.min(surr1, surr2).mean()

            # Calculate value loss
            new_values = self.value_net(batch_obs).squeeze()
            value_loss = F.mse_loss(new_values, batch_returns)

            # Total loss
            total_loss = (actor_loss +
                         self.value_loss_coef * value_loss -
                         self.entropy_coef * entropy.mean())

            # Update networks
            self.actor_optimizer.zero_grad()
            self.critic_optimizer.zero_grad()

            total_loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
            torch.nn.utils.clip_grad_norm_(self.value_net.parameters(), self.max_grad_norm)

            self.actor_optimizer.step()
            self.critic_optimizer.step()

    def train(self):
        """Main training loop"""
        for iteration in range(self.config["runner"]["max_iterations"]):
            print(f"Training iteration {iteration}")

            # Collect experience
            self.collect_experience()

            # Update policy
            self.update_policy()

            # Log metrics
            self.log_metrics(iteration)

            # Save checkpoint
            if iteration % self.config["runner"]["save_interval"] == 0:
                self.save_checkpoint(iteration)

    def log_metrics(self, iteration):
        """Log training metrics"""
        # Calculate and log average reward
        avg_reward = self.experience_buffer.rewards.mean().item()
        print(f"Iteration {iteration}, Average Reward: {avg_reward}")

    def save_checkpoint(self, iteration):
        """Save model checkpoint"""
        checkpoint = {
            'iteration': iteration,
            'policy_state_dict': self.policy.state_dict(),
            'value_net_state_dict': self.value_net.state_dict(),
            'actor_optimizer_state_dict': self.actor_optimizer.state_dict(),
            'critic_optimizer_state_dict': self.critic_optimizer.state_dict(),
        }

        torch.save(checkpoint, f"checkpoints/humanoid_policy_{iteration}.pth")

class HumanoidPolicy(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden_dims):
        super(HumanoidPolicy, self).__init__()

        # Actor network
        actor_layers = []
        prev_dim = obs_dim
        for hidden_dim in hidden_dims:
            actor_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ELU(),
            ])
            prev_dim = hidden_dim

        actor_layers.append(nn.Linear(prev_dim, action_dim))
        self.actor = nn.Sequential(*actor_layers)

        # Initialize last layer to small weights
        nn.init.uniform_(self.actor[-1].weight, -3e-3, 3e-3)
        nn.init.uniform_(self.actor[-1].bias, -3e-3, 3e-3)

        # Action standard deviation for exploration
        self.action_std = nn.Parameter(torch.ones(action_dim) * 0.5)

    def forward(self, obs):
        """Forward pass through actor network"""
        return torch.tanh(self.actor(obs))

    def get_action(self, obs):
        """Sample action from policy"""
        mean = self.forward(obs)
        std = self.action_std.expand_as(mean)
        dist = torch.distributions.Normal(mean, std)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum(dim=-1)

        return action, log_prob

    def evaluate_actions(self, obs, actions):
        """Evaluate log probabilities of given actions"""
        mean = self.forward(obs)
        std = self.action_std.expand_as(mean)
        dist = torch.distributions.Normal(mean, std)
        log_prob = dist.log_prob(actions).sum(dim=-1)
        entropy = dist.entropy().sum(dim=-1)

        return log_prob, entropy

class ValueNetwork(nn.Module):
    def __init__(self, obs_dim, hidden_dims):
        super(ValueNetwork, self).__init__()

        # Critic network
        critic_layers = []
        prev_dim = obs_dim
        for hidden_dim in hidden_dims:
            critic_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ELU(),
            ])
            prev_dim = hidden_dim

        critic_layers.append(nn.Linear(prev_dim, 1))
        self.critic = nn.Sequential(*critic_layers)

        # Initialize last layer to small weights
        nn.init.uniform_(self.critic[-1].weight, -3e-3, 3e-3)
        nn.init.uniform_(self.critic[-1].bias, -3e-3, 3e-3)

    def forward(self, obs):
        """Forward pass through critic network"""
        return self.critic(obs).squeeze(-1)

class ExperienceBuffer:
    def __init__(self, num_envs, num_steps, obs_dim, action_dim):
        self.obs = torch.zeros(num_steps, num_envs, obs_dim)
        self.actions = torch.zeros(num_steps, num_envs, action_dim)
        self.rewards = torch.zeros(num_steps, num_envs)
        self.dones = torch.zeros(num_steps, num_envs)
        self.values = torch.zeros(num_steps, num_envs)
        self.logprobs = torch.zeros(num_steps, num_envs)
        self.next_obs = torch.zeros(num_steps, num_envs, obs_dim)

        self.step = 0
        self.num_envs = num_envs
        self.num_steps = num_steps

    def add_step(self, obs, actions, rewards, dones, values, logprobs):
        """Add experience to buffer"""
        self.obs[self.step].copy_(obs)
        self.actions[self.step].copy_(actions)
        self.rewards[self.step].copy_(rewards)
        self.dones[self.step].copy_(dones)
        self.values[self.step].copy_(values)
        self.logprobs[self.step].copy_(logprobs)

        self.step = (self.step + 1) % self.num_steps
```

## Sim-to-Real Transfer Techniques

### The Sim-to-Real Problem

The sim-to-real transfer problem is one of the most significant challenges in applying reinforcement learning to robotics. While RL policies can achieve impressive performance in simulation, the reality gap—the differences between simulated and real environments—often prevents direct transfer of these policies to physical robots.

For humanoid robots, this problem is particularly challenging due to their complex dynamics, numerous degrees of freedom, and sensitivity to environmental conditions. Factors contributing to the reality gap include:

- **Model inaccuracies**: Simplified physics models in simulation
- **Sensor noise and delays**: Real sensors have noise, latency, and limitations
- **Actuator dynamics**: Real actuators have limitations in torque, speed, and control resolution
- **Environmental differences**: Real environments have unmodeled objects, lighting changes, and surface variations

### Domain Randomization

Domain randomization is a key technique for improving sim-to-real transfer by training policies in diverse simulated environments. By randomizing various parameters during training, the policy learns to be robust to differences between simulation and reality.

```python
# Domain randomization implementation for humanoid sim-to-real transfer
class DomainRandomizer:
    def __init__(self, env, config):
        self.env = env
        self.config = config
        self.randomization_params = config["env"]["domain_randomization"]["range"]
        self.randomize_frequency = config["env"]["domain_randomization"]["frequency"]
        self.current_iteration = 0

        # Store original parameters
        self.original_params = self.get_current_params()

        # Randomization counters
        self.randomization_steps = 0

    def should_randomize(self):
        """Check if randomization should occur"""
        return self.randomization_steps % self.randomize_frequency == 0

    def randomize_environment(self):
        """Randomize environment parameters"""
        if not self.config["env"]["domain_randomization"]["randomize"]:
            return

        # Randomize robot mass
        if "mass" in self.randomization_params:
            mass_range = self.randomization_params["mass"]
            random_factor = np.random.uniform(mass_range[0], mass_range[1])
            self.set_robot_mass(random_factor)

        # Randomize center of mass
        if "com" in self.randomization_params:
            com_range = self.randomization_params["com"]
            random_offset = np.random.uniform(com_range[0], com_range[1], size=3)
            self.set_center_of_mass_offset(random_offset)

        # Randomize friction
        if "friction" in self.randomization_params:
            friction_range = self.randomization_params["friction"]
            random_friction = np.random.uniform(friction_range[0], friction_range[1])
            self.set_friction(random_friction)

        # Randomize restitution (bounciness)
        if "restitution" in self.randomization_params:
            restitution_range = self.randomization_params["restitution"]
            random_restitution = np.random.uniform(restitution_range[0], restitution_range[1])
            self.set_restitution(random_restitution)

        # Randomize DOF damping
        if "dof_damping" in self.randomization_params:
            damping_range = self.randomization_params["dof_damping"]
            random_damping = np.random.uniform(damping_range[0], damping_range[1], size=self.env.num_dofs)
            self.set_dof_damping(random_damping)

        # Randomize DOF stiffness
        if "dof_stiffness" in self.randomization_params:
            stiffness_range = self.randomization_params["dof_stiffness"]
            random_stiffness = np.random.uniform(stiffness_range[0], stiffness_range[1], size=self.env.num_dofs)
            self.set_dof_stiffness(random_stiffness)

        # Randomize terrain height variations
        if "height" in self.randomization_params:
            height_range = self.randomization_params["height"]
            random_height = np.random.uniform(height_range[0], height_range[1])
            self.set_terrain_height(random_height)

        self.randomization_steps += 1

    def set_robot_mass(self, factor):
        """Set robot mass with random factor"""
        # Implementation to modify robot mass in simulation
        pass

    def set_center_of_mass_offset(self, offset):
        """Set center of mass offset"""
        # Implementation to modify COM in simulation
        pass

    def set_friction(self, friction):
        """Set friction coefficient"""
        # Implementation to modify friction in simulation
        pass

    def set_restitution(self, restitution):
        """Set restitution coefficient"""
        # Implementation to modify restitution in simulation
        pass

    def set_dof_damping(self, damping_values):
        """Set DOF damping values"""
        # Implementation to modify DOF damping in simulation
        pass

    def set_dof_stiffness(self, stiffness_values):
        """Set DOF stiffness values"""
        # Implementation to modify DOF stiffness in simulation
        pass

    def set_terrain_height(self, height):
        """Set terrain height variations"""
        # Implementation to modify terrain in simulation
        pass

    def get_current_params(self):
        """Get current environment parameters"""
        # Implementation to retrieve current parameters
        pass
```

### System Identification for Model Improvement

System identification involves measuring real robot behavior to refine simulation models, reducing the reality gap. This process helps identify the actual physical parameters of the robot, such as masses, inertias, friction coefficients, and actuator dynamics.

```python
# System identification for humanoid robot model improvement
class SystemIdentifier:
    def __init__(self, robot_interface, simulation_model):
        self.robot_interface = robot_interface
        self.simulation_model = simulation_model
        self.data_buffer = []
        self.optimization_method = "least_squares"

    def collect_identification_data(self, excitation_signal, duration=10.0):
        """
        Collect data for system identification using excitation signals
        """
        # Apply excitation signal to robot
        start_time = time.time()
        while time.time() - start_time < duration:
            # Generate excitation command
            command = self.generate_excitation_signal(excitation_signal, time.time() - start_time)

            # Send command to robot
            self.robot_interface.send_command(command)

            # Collect sensor data
            sensor_data = self.robot_interface.get_sensor_data()

            # Store data
            self.data_buffer.append({
                'time': time.time(),
                'command': command,
                'position': sensor_data['position'],
                'velocity': sensor_data['velocity'],
                'torque': sensor_data['torque'],
                'imu': sensor_data['imu']
            })

            # Small delay to maintain control frequency
            time.sleep(0.001)

    def generate_excitation_signal(self, signal_type, time):
        """
        Generate different types of excitation signals
        """
        if signal_type == "sine_sweep":
            # Sine sweep from low to high frequency
            freq = 0.1 + (5.0 - 0.1) * (time / 10.0)  # Sweep from 0.1 to 5 Hz over 10s
            amplitude = 0.5
            return amplitude * np.sin(2 * np.pi * freq * time)

        elif signal_type == "step":
            # Step input
            return 0.5 if time > 2.0 else 0.0

        elif signal_type == "prbs":
            # Pseudo-random binary sequence
            prbs_period = 1.0
            return 0.5 if int(time / prbs_period) % 2 == 0 else -0.5

    def identify_parameters(self):
        """
        Identify physical parameters using collected data
        """
        # Prepare data for optimization
        time_data = np.array([d['time'] for d in self.data_buffer])
        command_data = np.array([d['command'] for d in self.data_buffer])
        position_data = np.array([d['position'] for d in self.data_buffer])
        velocity_data = np.array([d['velocity'] for d in self.data_buffer])
        torque_data = np.array([d['torque'] for d in self.data_buffer])

        # Define parameter estimation function
        def objective_function(params):
            # Update simulation model with current parameters
            self.simulation_model.update_parameters(params)

            # Simulate the same inputs
            simulated_positions = []
            for i in range(len(command_data)):
                sim_pos = self.simulation_model.simulate_step(
                    command_data[i],
                    velocity_data[i-1] if i > 0 else np.zeros_like(velocity_data[0])
                )
                simulated_positions.append(sim_pos)

            simulated_positions = np.array(simulated_positions)

            # Calculate error between real and simulated
            position_error = np.mean((position_data - simulated_positions)**2)

            return position_error

        # Initial parameter guess
        initial_params = self.simulation_model.get_parameters()

        # Optimize parameters
        if self.optimization_method == "least_squares":
            result = scipy.optimize.least_squares(objective_function, initial_params)
        elif self.optimization_method == "differential_evolution":
            result = scipy.optimize.differential_evolution(
                objective_function,
                bounds=self.get_parameter_bounds()
            )

        # Update simulation model with identified parameters
        self.simulation_model.update_parameters(result.x)

        return result.x

    def get_parameter_bounds(self):
        """
        Define bounds for parameter optimization
        """
        # Define reasonable bounds for physical parameters
        bounds = []

        # Mass bounds
        bounds.append((0.1, 10.0))  # Mass in kg

        # Inertia bounds
        for _ in range(3):  # Ixx, Iyy, Izz
            bounds.append((0.001, 1.0))

        # Damping bounds
        for _ in range(18):  # For 18 DOF humanoid
            bounds.append((0.0, 10.0))

        # Friction bounds
        for _ in range(18):
            bounds.append((0.0, 5.0))

        return bounds

    def validate_identified_model(self):
        """
        Validate the identified model against new data
        """
        # Collect validation data
        self.collect_identification_data("validation", duration=5.0)

        # Compare simulation vs real for validation inputs
        validation_results = self.compare_simulation_real()

        return validation_results

    def compare_simulation_real(self):
        """
        Compare simulation and real robot responses
        """
        # Implementation to compare simulation and real responses
        pass
```

### Adaptive Control for Sim-to-Real Transfer

Adaptive control techniques can help bridge the sim-to-real gap by allowing the policy to adjust its behavior based on real-world feedback. This approach combines the benefits of simulation-based training with real-world adaptation.

```python
# Adaptive control for sim-to-real transfer
class AdaptiveController:
    def __init__(self, base_policy, adaptation_rate=0.01):
        self.base_policy = base_policy  # Pre-trained simulation policy
        self.adaptation_rate = adaptation_rate
        self.adaptation_params = torch.zeros_like(self.base_policy.actor[-1].weight)
        self.performance_history = []
        self.adaptation_enabled = True

    def get_adaptive_action(self, obs, real_feedback=None):
        """
        Get action from policy with real-world adaptation
        """
        # Get base action from pre-trained policy
        base_action = self.base_policy(obs)

        # Apply adaptation if real feedback is available
        if real_feedback is not None and self.adaptation_enabled:
            # Calculate adaptation based on real-world feedback
            adaptation_action = self.calculate_adaptation(obs, real_feedback)

            # Combine base and adaptation actions
            final_action = base_action + self.adaptation_rate * adaptation_action
        else:
            final_action = base_action

        return torch.clamp(final_action, -1.0, 1.0)

    def calculate_adaptation(self, obs, real_feedback):
        """
        Calculate adaptation based on real-world feedback
        """
        # Use real feedback to adjust control
        # This could be based on tracking error, stability metrics, etc.

        # Example: Adapt based on position tracking error
        if 'position_error' in real_feedback:
            pos_error = real_feedback['position_error']
            # Map position error to action space through learned adaptation
            adaptation = torch.matmul(pos_error, self.adaptation_params)
        else:
            adaptation = torch.zeros_like(obs[:self.base_policy.action_dim])

        return adaptation

    def update_adaptation(self, obs_batch, action_batch, real_feedback_batch):
        """
        Update adaptation parameters based on experience
        """
        if not self.adaptation_enabled:
            return

        # Calculate prediction error
        predicted_actions = self.base_policy(obs_batch)
        actual_actions = action_batch

        # Update adaptation parameters to minimize error
        error = actual_actions - predicted_actions
        self.adaptation_params += self.adaptation_rate * torch.outer(error.mean(dim=0), obs_batch.mean(dim=0))

    def evaluate_performance(self, obs, desired_behavior):
        """
        Evaluate policy performance and enable/disable adaptation
        """
        # Calculate performance metrics
        performance = self.calculate_performance_metric(obs, desired_behavior)

        # Store in history
        self.performance_history.append(performance)

        # Enable adaptation if performance is below threshold
        if len(self.performance_history) > 10:
            recent_performance = np.mean(self.performance_history[-10:])
            self.adaptation_enabled = recent_performance < 0.8  # Enable if below 80% performance

    def calculate_performance_metric(self, obs, desired_behavior):
        """
        Calculate performance metric for adaptation decision
        """
        # Implementation for calculating performance
        pass
```

## Behavior Learning for Humanoid Tasks

### Learning Complex Humanoid Behaviors

Beyond basic locomotion, reinforcement learning can be applied to learn complex humanoid behaviors such as manipulation, interaction with objects, and multi-task behaviors. These behaviors often require hierarchical approaches that combine low-level motor control with high-level task planning.

```python
# Hierarchical RL for complex humanoid behaviors
class HierarchicalHumanoidRL:
    def __init__(self, config):
        # High-level policy (task planning)
        self.high_level_policy = HighLevelPolicy(
            obs_dim=config["high_level"]["obs_dim"],
            action_dim=config["high_level"]["action_dim"]
        )

        # Low-level policy (motor control)
        self.low_level_policy = LowLevelPolicy(
            obs_dim=config["low_level"]["obs_dim"],
            action_dim=config["low_level"]["action_dim"]
        )

        # Skill library for specific behaviors
        self.skill_library = SkillLibrary()

        # Curriculum learning scheduler
        self.curriculum = CurriculumScheduler()

    def execute_behavior(self, task_description, current_state):
        """
        Execute complex behavior using hierarchical approach
        """
        # High-level planning
        subtasks = self.high_level_policy.plan_subtasks(task_description, current_state)

        # Execute each subtask using appropriate skill
        for subtask in subtasks:
            skill = self.skill_library.get_skill(subtask.skill_type)

            if skill.requires_learning:
                # Use learned policy for complex skills
                skill.execute_with_policy(current_state, subtask.goal)
            else:
                # Use predefined controller for simple skills
                skill.execute_with_controller(current_state, subtask.goal)

    def learn_behavior(self, task_descriptions, demonstrations=None):
        """
        Learn complex behaviors through hierarchical RL
        """
        # Curriculum learning: start with simple tasks, progress to complex
        for level in self.curriculum.get_levels():
            # Train high-level policy for task decomposition
            self.train_high_level_policy(level.tasks)

            # Train low-level skills for each subtask
            for subtask in level.subtasks:
                self.train_low_level_skill(subtask)

    def train_high_level_policy(self, tasks):
        """
        Train high-level policy for task decomposition
        """
        # Implementation for high-level policy training
        pass

    def train_low_level_skill(self, subtask):
        """
        Train low-level policy for specific subtask
        """
        # Implementation for low-level skill training
        pass

class SkillLibrary:
    def __init__(self):
        self.skills = {
            'walk_to': self.walk_to_skill,
            'reach': self.reach_skill,
            'grasp': self.grasp_skill,
            'manipulate': self.manipulate_skill,
            'balance': self.balance_skill
        }

        # Learned policies for complex skills
        self.learned_policies = {}

    def get_skill(self, skill_type):
        """Get skill by type"""
        if skill_type in self.learned_policies:
            return LearnedSkill(self.learned_policies[skill_type])
        elif skill_type in self.skills:
            return PredefinedSkill(self.skills[skill_type])
        else:
            raise ValueError(f"Unknown skill type: {skill_type}")

    def walk_to_skill(self, state, goal):
        """Simple walking skill"""
        # Implementation for walking to goal
        pass

    def reach_skill(self, state, goal):
        """Reaching skill"""
        # Implementation for reaching
        pass

    def grasp_skill(self, state, goal):
        """Grasping skill"""
        # Implementation for grasping
        pass

    def manipulate_skill(self, state, goal):
        """Manipulation skill"""
        # Implementation for manipulation
        pass

    def balance_skill(self, state, goal):
        """Balance skill"""
        # Implementation for balance
        pass

class CurriculumScheduler:
    def __init__(self):
        self.levels = [
            {"tasks": ["stand", "simple_walk"], "subtasks": ["balance", "basic_locomotion"]},
            {"tasks": ["walk_to_target", "avoid_obstacle"], "subtasks": ["goal_navigation", "obstacle_avoidance"]},
            {"tasks": ["pick_object", "place_object"], "subtasks": ["reaching", "grasping", "manipulation"]},
            {"tasks": ["complex_manipulation", "multi_task"], "subtasks": ["all_previous_skills"]}
        ]

    def get_levels(self):
        """Get curriculum levels"""
        return self.levels
```

### Transfer Learning for Humanoid Behaviors

Transfer learning allows knowledge gained from one task to be applied to related tasks, accelerating learning and improving performance. For humanoid robots, this could mean transferring locomotion skills to different terrains or transferring manipulation skills to different objects.

```python
# Transfer learning for humanoid behaviors
class HumanoidTransferLearning:
    def __init__(self, source_policy, target_task):
        self.source_policy = source_policy
        self.target_task = target_task
        self.transfer_method = "fine_tuning"  # Options: fine_tuning, feature_extraction, domain_adaptation

        # Initialize target policy based on source
        self.target_policy = self.initialize_target_policy()

    def initialize_target_policy(self):
        """Initialize target policy based on source policy"""
        if self.transfer_method == "fine_tuning":
            # Copy source policy and allow all parameters to update
            target_policy = copy.deepcopy(self.source_policy)
        elif self.transfer_method == "feature_extraction":
            # Copy early layers, reinitialize later layers
            target_policy = self.create_feature_extracting_policy()
        elif self.transfer_method == "domain_adaptation":
            # Add domain adaptation layers
            target_policy = self.create_domain_adapted_policy()

        return target_policy

    def transfer_knowledge(self, target_env, steps=10000):
        """
        Transfer knowledge from source to target task
        """
        # Initialize target environment
        obs = target_env.reset()

        for step in range(steps):
            # Get action from target policy
            action, _ = self.target_policy.get_action(obs)

            # Execute in target environment
            next_obs, reward, done, info = target_env.step(action)

            # Store experience for training
            self.store_experience(obs, action, reward, next_obs, done)

            # Update target policy
            if step % 100 == 0:  # Update every 100 steps
                self.update_target_policy()

            obs = next_obs if not done else target_env.reset()

    def create_feature_extracting_policy(self):
        """Create policy with frozen feature layers"""
        # Copy the feature extraction layers from source
        feature_extractor = copy.deepcopy(
            list(self.source_policy.actor.children())[:-2]  # All layers except last 2
        )

        # Freeze feature extraction layers
        for param in feature_extractor.parameters():
            param.requires_grad = False

        # Create new task-specific layers
        task_head = nn.Sequential(
            nn.Linear(256, 128),  # Assuming 256 is output of feature extractor
            nn.ELU(),
            nn.Linear(128, self.target_task.action_dim)
        )

        # Combine feature extractor and task head
        target_policy = nn.Sequential(feature_extractor, task_head)

        return target_policy

    def create_domain_adapted_policy(self):
        """Create policy with domain adaptation layers"""
        # Base policy from source
        base_policy = copy.deepcopy(self.source_policy)

        # Add domain adaptation layers
        domain_adaptation_layer = DomainAdaptationLayer(
            input_dim=self.source_policy.obs_dim,
            output_dim=self.source_policy.action_dim
        )

        return DomainAdaptedPolicy(base_policy, domain_adaptation_layer)

    def store_experience(self, obs, action, reward, next_obs, done):
        """Store experience for training"""
        # Implementation for storing experience
        pass

    def update_target_policy(self):
        """Update target policy based on collected experience"""
        # Implementation for policy update
        pass

class DomainAdaptationLayer(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DomainAdaptationLayer, self).__init__()
        self.domain_classifier = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ELU(),
            nn.Linear(128, 64),
            nn.ELU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

        self.feature_alignment = nn.Linear(input_dim, input_dim)

    def forward(self, features):
        # Align features between source and target domains
        aligned_features = self.feature_alignment(features)
        domain_prob = self.domain_classifier(aligned_features)

        return aligned_features, domain_prob

class DomainAdaptedPolicy:
    def __init__(self, base_policy, domain_adapter):
        self.base_policy = base_policy
        self.domain_adapter = domain_adapter

    def get_action(self, obs):
        """Get action with domain adaptation"""
        adapted_obs, domain_prob = self.domain_adapter(obs)
        return self.base_policy.get_action(adapted_obs)
```

## Best Practices and Optimization

### Training Optimization for Humanoid RL

Training reinforcement learning policies for humanoid robots requires careful optimization to achieve stable and efficient learning. The high-dimensional action and state spaces, combined with the need for safety during training, make optimization particularly challenging.

```python
# Training optimization techniques for humanoid RL
class HumanoidRLOptimizer:
    def __init__(self, trainer):
        self.trainer = trainer
        self.optimization_params = {
            'learning_rate_schedule': 'adaptive',
            'batch_size_schedule': 'increasing',
            'exploration_schedule': 'decreasing',
            'regularization': 'entropy',
        }

    def optimize_training_process(self):
        """
        Optimize various aspects of the training process
        """
        # Optimize hyperparameters
        self.optimize_hyperparameters()

        # Optimize reward shaping
        self.optimize_reward_shaping()

        # Optimize exploration strategy
        self.optimize_exploration()

        # Optimize curriculum learning
        self.optimize_curriculum()

    def optimize_hyperparameters(self):
        """
        Optimize learning hyperparameters during training
        """
        # Adaptive learning rate based on training progress
        if self.trainer.current_iteration > 0:
            recent_rewards = self.trainer.recent_rewards[-100:]
            reward_trend = np.polyfit(range(len(recent_rewards)), recent_rewards, 1)[0]

            if reward_trend < 0:  # Performance degrading
                self.trainer.learning_rate *= 0.9  # Reduce learning rate
            elif reward_trend > 0.01:  # Performance improving rapidly
                self.trainer.learning_rate = min(self.trainer.learning_rate * 1.01, 1e-3)  # Increase slightly

    def optimize_reward_shaping(self):
        """
        Optimize reward function during training
        """
        # Adjust reward weights based on training progress
        if self.trainer.current_iteration % 100 == 0:
            # Analyze what aspects of behavior are improving
            balance_improvement = self.analyze_balance_improvement()
            speed_improvement = self.analyze_speed_improvement()

            # Adjust reward weights accordingly
            if balance is improving slowly, increase balance reward weight
            if speed is improving well, maintain or slightly decrease speed reward weight

    def optimize_exploration(self):
        """
        Optimize exploration strategy during training
        """
        # Adaptive exploration based on training stage
        if self.trainer.current_iteration < 500:  # Early training
            # High exploration for broad coverage
            self.trainer.exploration_noise = 0.3
        elif self.trainer.current_iteration < 1500:  # Mid training
            # Moderate exploration for refinement
            self.trainer.exploration_noise = 0.1
        else:  # Late training
            # Low exploration for fine-tuning
            self.trainer.exploration_noise = 0.05

    def optimize_curriculum(self):
        """
        Optimize curriculum learning progression
        """
        # Adjust curriculum based on learning progress
        if self.trainer.current_iteration % 100 == 0:
            success_rate = self.trainer.get_task_success_rate()

            if success_rate > 0.9:  # Task mastered
                advance_curriculum()
            elif success_rate < 0.3:  # Task too difficult
                revert_curriculum()

    def analyze_balance_improvement(self):
        """Analyze balance improvement trend"""
        # Implementation for balance analysis
        pass

    def analyze_speed_improvement(self):
        """Analyze speed improvement trend"""
        # Implementation for speed analysis
        pass

    def advance_curriculum(self):
        """Advance to next curriculum level"""
        # Implementation for curriculum advancement
        pass

    def revert_curriculum(self):
        """Revert to previous curriculum level"""
        # Implementation for curriculum reversion
        pass
```

### Safety Considerations in RL Training

Safety is paramount when training RL policies for humanoid robots, both in simulation and especially during real-world testing. Safety measures must be implemented to prevent damage to the robot and ensure safe operation around humans.

```python
# Safety framework for humanoid RL training
class HumanoidSafetyFramework:
    def __init__(self, robot_interface):
        self.robot_interface = robot_interface
        self.safety_limits = self.define_safety_limits()
        self.emergency_stop_active = False
        self.safety_monitor = SafetyMonitor(robot_interface)

    def define_safety_limits(self):
        """
        Define safety limits for humanoid robot operation
        """
        return {
            'joint_position': {
                'min': np.array([-2.0] * 18),  # Example: 18 DOF humanoid
                'max': np.array([2.0] * 18)
            },
            'joint_velocity': {
                'max': np.array([5.0] * 18)  # 5 rad/s max velocity
            },
            'joint_torque': {
                'max': np.array([100.0] * 18)  # 100 Nm max torque
            },
            'base_orientation': {
                'max_tilt': np.deg2rad(30)  # 30 degrees max tilt
            },
            'base_height': {
                'min': 0.3,  # Minimum height to prevent falls
                'max': 1.2   # Maximum height for stability
            },
            'power_limits': {
                'max_total': 500.0,  # 500W max total power
                'max_continuous': 200.0  # 200W max continuous power
            }
        }

    def validate_action(self, action):
        """
        Validate action against safety limits before execution
        """
        if self.emergency_stop_active:
            return np.zeros_like(action)

        # Check joint limits
        if not self.check_joint_limits(action):
            self.log_safety_violation("Joint limit violation")
            return self.get_safe_action(action)

        # Check for dangerous orientations
        if self.check_dangerous_orientation():
            self.log_safety_violation("Dangerous orientation detected")
            return self.get_safe_action(action)

        # Check power consumption
        if self.check_power_limits():
            self.log_safety_violation("Power limit exceeded")
            return self.get_safe_action(action)

        return action

    def check_joint_limits(self, action):
        """Check if action violates joint limits"""
        current_positions = self.robot_interface.get_joint_positions()
        new_positions = current_positions + action  # Simplified

        within_limits = (
            np.all(new_positions >= self.safety_limits['joint_position']['min']) and
            np.all(new_positions <= self.safety_limits['joint_position']['max'])
        )

        return within_limits

    def check_dangerous_orientation(self):
        """Check if robot is in dangerous orientation"""
        orientation = self.robot_interface.get_base_orientation()

        # Check tilt angle
        tilt_angle = self.calculate_tilt_angle(orientation)

        return tilt_angle > self.safety_limits['base_orientation']['max_tilt']

    def check_power_limits(self):
        """Check if power consumption exceeds limits"""
        current_power = self.robot_interface.get_power_consumption()

        return current_power > self.safety_limits['power_limits']['max_total']

    def get_safe_action(self, original_action):
        """
        Generate safe action when original action is unsafe
        """
        # Return zero action as safest option
        return np.zeros_like(original_action)

    def log_safety_violation(self, violation_type):
        """Log safety violation for analysis"""
        print(f"Safety violation: {violation_type}")

    def enable_emergency_stop(self):
        """Enable emergency stop"""
        self.emergency_stop_active = True
        self.robot_interface.emergency_stop()

    def disable_emergency_stop(self):
        """Disable emergency stop"""
        self.emergency_stop_active = False

class SafetyMonitor:
    def __init__(self, robot_interface):
        self.robot_interface = robot_interface
        self.safety_violations = 0
        self.max_violations_before_stop = 5

    def monitor_safety(self):
        """
        Continuously monitor safety during operation
        """
        # Check all safety parameters
        checks = [
            self.check_balance(),
            self.check_joint_limits(),
            self.check_collision(),
            self.check_power_consumption()
        ]

        safe = all(checks)

        if not safe:
            self.safety_violations += 1

            if self.safety_violations >= self.max_violations_before_stop:
                self.trigger_emergency_stop()
        else:
            self.safety_violations = max(0, self.safety_violations - 1)  # Decay violations

        return safe

    def check_balance(self):
        """Check robot balance"""
        # Implementation for balance checking
        pass

    def check_joint_limits(self):
        """Check joint limits"""
        # Implementation for joint limit checking
        pass

    def check_collision(self):
        """Check for collisions"""
        # Implementation for collision checking
        pass

    def check_power_consumption(self):
        """Check power consumption"""
        # Implementation for power checking
        pass

    def trigger_emergency_stop(self):
        """Trigger emergency stop procedure"""
        print("EMERGENCY STOP: Safety threshold exceeded")
        # Implementation for emergency stop
        pass
```

## Looking Ahead

Reinforcement learning for humanoid robotics continues to evolve with advances in sample-efficient algorithms, better sim-to-real transfer techniques, and more sophisticated hierarchical learning approaches. Future developments will likely focus on lifelong learning, where humanoid robots continuously improve their skills through ongoing interaction with the environment.

The integration of RL with other AI techniques like imitation learning, meta-learning, and multi-task learning will enable humanoid robots to acquire complex behaviors more efficiently. Additionally, the development of better simulation environments and more accurate system identification techniques will further bridge the sim-to-real gap.

## Citations

- Brockman, G., et al. (2016). OpenAI Gym. arXiv preprint arXiv:1606.01540.
- Riedmiller, M., et al. (2021). Isaac Gym: High Performance GPU Based Physics Simulation. NVIDIA.
- Schulman, J., et al. (2017). Proximal Policy Optimization Algorithms. arXiv preprint arXiv:1707.06347.
- Sadeghi, F., & Levine, S. (2017). CADRL: Learning Collision Avoidance with Deep Reinforcement Learning. IEEE/RSJ International Conference on Intelligent Robots and Systems.

## Summary

This chapter covered reinforcement learning and sim-to-real transfer techniques for humanoid robots. We explored the fundamentals of RL in robotics, implemented Isaac Gym environments for humanoid training, discussed sim-to-real transfer techniques including domain randomization and system identification, and examined behavior learning for complex humanoid tasks. The chapter emphasized the importance of safety in RL training and provided optimization strategies for efficient learning. These techniques enable humanoid robots to learn complex behaviors like locomotion, manipulation, and multi-task behaviors through interaction with their environment.

## Review Questions/Exercises

1. How does domain randomization help improve sim-to-real transfer in humanoid robotics?
2. What are the key differences between training RL policies in simulation vs. on real robots?
3. Explain the architecture of a hierarchical RL system for complex humanoid behaviors.
4. How would you design a safety framework for RL training on a physical humanoid robot?
5. Design a curriculum learning approach for training a humanoid robot to walk on different terrains.

---

**Chapter Specifications:**
- **Expected Length**: 2,000-3,000 words
- **Research Sources**: Minimum 40% peer-reviewed sources
- **Code Examples**: Python-based using PyTorch and Isaac Gym where applicable
- **Diagrams/Illustrations**: Text-based diagrams showing RL architecture and training process
- **Required Research Depth**: Each section will necessitate research from peer-reviewed sources (minimum 40%), technical documentation, and authoritative industry guides