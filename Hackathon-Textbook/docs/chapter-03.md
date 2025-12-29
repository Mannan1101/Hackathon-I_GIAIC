---
id: chapter-03
title: "Chapter 3: Simulation with Gazebo, Unity & Digital Twins"
sidebar_label: "Ch 3: Simulation & Digital Twins"
sidebar_position: 4
description: "Master robot simulation in Gazebo and Unity, URDF/SDF modeling, sensor simulation, and sim-to-real transfer"
---

# Chapter 3: Simulation with Gazebo, Unity & Digital Twins

## Introduction

[SOURCE NEEDED: Introduction to simulation as essential tool for robotics development - safe testing, rapid iteration, scalability]

**What you'll learn in this chapter:**
- Building simulation environments in Gazebo and Unity
- Creating robot models with URDF/SDF
- Simulating sensors (cameras, LiDAR, IMU)
- Training AI agents in Unity ML-Agents
- Bridging the sim-to-real gap

---

## Learning Objectives

1. **Create** robot simulation environments in Gazebo and Unity, including world design, lighting, and obstacle placement
2. **Integrate** robot models (URDF/SDF) into simulation environments with accurate physics properties and sensor configurations
3. **Implement** simulated sensors (cameras, LiDAR, depth sensors, IMUs) and validate their output against expected behavior
4. **Compare** Gazebo and Unity simulation platforms, selecting the appropriate tool based on use case requirements
5. **Identify** and mitigate sim-to-real gaps, understanding limitations of simulation and validation strategies for physical deployment

**Prerequisites:**
- Chapters 1-2
- 3D geometry basics
- ROS 2 proficiency

---

## 3.1 Why Simulate?

[SOURCE NEEDED: Benefits - cost, safety, scalability, repeatability; Limitations - reality gap, physics approximations]

**Simulation Workflow:**
[SOURCE NEEDED: Design → Simulate → Validate → Deploy cycle]

**Platform Comparison:**

| Platform | Best For | Pros | Cons |
|----------|----------|------|------|
| Gazebo | [SOURCE] | [SOURCE] | [SOURCE] |
| Unity | [SOURCE] | [SOURCE] | [SOURCE] |
| Isaac Sim | [SOURCE] | [SOURCE] | [SOURCE] |

---

## 3.2 Gazebo: Physics-Accurate Simulation

### Gazebo Classic vs. Gazebo Sim

[SOURCE NEEDED: Differences, migration path, when to use each]

### Installation

```bash
# [SOURCE NEEDED: Installation commands for Gazebo Classic and Gazebo Sim on Ubuntu 22.04]
```

### World Creation

[SOURCE NEEDED: Creating environments with models, lighting, physics engines (ODE, Bullet, DART)]

#### Code Example 1: Launch Gazebo with ROS 2

```python
"""
Launch file for Gazebo with ROS 2 integration
[SOURCE NEEDED: Complete launch file]
"""
# [SOURCE NEEDED: gazebo_ros imports]
# [SOURCE NEEDED: World loading]
# [SOURCE NEEDED: Robot spawning]
```

### GUI Overview

[SOURCE NEEDED: Scene editor, model insertion, camera controls, physics tuning]

---

## 3.3 URDF/SDF Robot Modeling

### URDF (Unified Robot Description Format)

[SOURCE NEEDED: Links, joints, visual/collision geometry, inertial properties]

#### Code Example 2: Simple Two-Wheeled Robot URDF

```xml
<!-- [SOURCE NEEDED: Complete URDF with base_link, wheels, joints] -->
<robot name="simple_robot">
  <!-- [SOURCE NEEDED: Links definitions] -->
  <!-- [SOURCE NEEDED: Joints definitions] -->
  <!-- [SOURCE NEEDED: Visual and collision geometry] -->
  <!-- [SOURCE NEEDED: Inertial properties] -->
</robot>
```

### Xacro: Macros for URDF

[SOURCE NEEDED: Parameterized components, reusable macros]

#### Code Example 3: Xacro Wheel Macro

```xml
<!-- [SOURCE NEEDED: Xacro macro for robot wheel] -->
```

### SDF (Simulation Description Format)

[SOURCE NEEDED: Enhanced features for Gazebo, differences from URDF]

---

## 3.4 Sensor Simulation

### Camera Sensors

[SOURCE NEEDED: RGB, depth, stereo cameras in Gazebo]

#### Code Example 4: Camera Plugin in SDF

```xml
<!-- [SOURCE NEEDED: Camera sensor configuration with Gazebo plugin] -->
```

### LiDAR/Laser Scanners

[SOURCE NEEDED: Ray casting, point cloud generation, configuration]

#### Code Example 5: LiDAR Configuration

```xml
<!-- [SOURCE NEEDED: 2D or 3D LiDAR sensor in SDF] -->
```

### IMU Sensors

[SOURCE NEEDED: Acceleration, angular velocity, noise models]

### Sensor Validation

#### Code Example 6: Sensor Data Validator Node

```python
"""
Validate simulated sensor data
[SOURCE NEEDED: Subscribe to sensor topics, check data quality]
"""
```

---

## 3.5 Unity ML-Agents for AI Training

### Unity for Robotics

[SOURCE NEEDED: Unity game engine advantages - rendering quality, ML-Agents toolkit]

### ML-Agents Overview

[SOURCE NEEDED: Reinforcement learning training, agent-environment interaction]

### Creating a Training Environment

[SOURCE NEEDED: Scene setup, agent observations, actions, rewards]

#### Code Example 7: Unity Agent Script (C#)

```csharp
/*
Unity ML-Agents agent implementation
[SOURCE NEEDED: Complete C# agent class]
*/
using Unity.MLAgents;
// [SOURCE NEEDED: Agent observations]
// [SOURCE NEEDED: Actions]
// [SOURCE NEEDED: Reward function]
```

### Training with PPO

#### Code Example 8: Training Configuration

```python
"""
Training script for ML-Agents
[SOURCE NEEDED: PPO configuration and training command]
"""
```

---

## 3.6 Sim-to-Real Transfer

### The Reality Gap

[SOURCE NEEDED: Why simulated robots behave differently than physical robots]

### Domain Randomization

[SOURCE NEEDED: Randomizing textures, lighting, physics to improve robustness]

#### Code Example 9: Domain Randomization Script

```python
"""
Randomize simulation parameters
[SOURCE NEEDED: Lighting, friction, object positions]
"""
```

### System Identification

[SOURCE NEEDED: Measuring real robot parameters to improve simulation accuracy]

### Validation Strategies

[SOURCE NEEDED: Offline metrics, online testing, performance comparison]

---

## Lab Activities

### Lab 9: Gazebo World Creation

**Objective:** Create custom simulation environment

**Tasks:**
1. [SOURCE NEEDED: Design world with obstacles and textures]
2. [SOURCE NEEDED: Add lighting and physics settings]
3. [SOURCE NEEDED: Test robot navigation]

### Lab 10: URDF Robot Modeling

**Objective:** Create URDF for 3-DOF robot arm

**Tasks:**
1. [SOURCE NEEDED: Define links and joints]
2. [SOURCE NEEDED: Add visual and collision geometry]
3. [SOURCE NEEDED: Visualize in RViz]

### Lab 11: Sensor Validation Lab

**Objective:** Compare simulated vs. theoretical sensor characteristics

**Tasks:**
1. [SOURCE NEEDED: Configure camera and LiDAR in Gazebo]
2. [SOURCE NEEDED: Collect sensor data]
3. [SOURCE NEEDED: Analyze and validate]

### Lab 12: Unity Environment Creation

**Objective:** Build simple navigation environment in Unity

**Tasks:**
1. [SOURCE NEEDED: Create Unity scene with obstacles]
2. [SOURCE NEEDED: Add agent with ray cast sensors]
3. [SOURCE NEEDED: Define reward function]

### Lab 13: Domain Randomization Experiment

**Objective:** Train policy with and without randomization, compare performance

**Tasks:**
1. [SOURCE NEEDED: Baseline training without randomization]
2. [SOURCE NEEDED: Training with domain randomization]
3. [SOURCE NEEDED: Evaluate on test scenarios]

---

## Summary

### Key Takeaways

1. **Simulation Enables Safe Development**: [SOURCE NEEDED]
2. **Gazebo for Physics Accuracy**: [SOURCE NEEDED]
3. **Unity for AI Training**: [SOURCE NEEDED]
4. **URDF/SDF for Robot Modeling**: [SOURCE NEEDED]
5. **Sensor Simulation Requires Noise Modeling**: [SOURCE NEEDED]
6. **Domain Randomization Helps Sim-to-Real**: [SOURCE NEEDED]

### Looking Ahead

Next chapter: **NVIDIA Isaac** for GPU-accelerated, photorealistic simulation and synthetic data generation.

---

## Review Questions

1. **Compare** Gazebo vs. Unity. When would you choose each?
2. **Explain** the structure of a URDF file. What are links, joints, and inertial properties?
3. **Describe** three strategies to reduce the sim-to-real gap.
4. **Design** a sensor suite for a simulated autonomous car. Specify types and configurations.
5. **Implement**: Write URDF joint definition for a revolute joint with limits [-π/2, π/2].
6. **Troubleshoot**: Robot falls through floor in Gazebo. What might be wrong?
7. **Architecture**: Design domain randomization strategy for pick-and-place task.
8. **Evaluation**: How would you validate that your simulated camera matches a real camera?

---

## Further Reading

- [SOURCE NEEDED: Gazebo documentation]
- [SOURCE NEEDED: Unity ML-Agents docs]
- [SOURCE NEEDED: URDF/SDF specifications]
- [SOURCE NEEDED: Sim-to-real research papers]

---

**Next Chapter:** [Chapter 4: NVIDIA Isaac, Perception, SLAM & Navigation](./chapter-04.md)
