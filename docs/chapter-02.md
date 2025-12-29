---
id: chapter-02
title: "Chapter 2: ROS 2 & The Robotic Nervous System"
sidebar_label: "Ch 2: ROS 2 Framework"
sidebar_position: 3
description: "Master ROS 2 architecture, distributed robot control, nodes, topics, services, actions, and production robotics patterns"
---

# Chapter 2: ROS 2 & The Robotic Nervous System

## Introduction

[SOURCE NEEDED: Introduction explaining ROS 2 as the "nervous system" of modern robots - communication, coordination, distributed processing]

**What you'll learn in this chapter:**
- ROS 2 architecture and design principles
- Building distributed robot systems with nodes and topics
- Request-response patterns with services
- Long-running tasks with actions
- Production-quality robot control implementation
- Debugging and development tools

**Why this matters:**
[SOURCE NEEDED: ROS 2 as industry standard, used by companies like NASA, BMW, etc.]

---

## Learning Objectives

By the end of this chapter, you will be able to:

1. **Architect** ROS 2 systems using nodes, topics, services, and actions, selecting appropriate communication patterns for different scenarios
2. **Implement** robot control loops in ROS 2, including position control, velocity control, and trajectory following
3. **Integrate** sensors and actuators with ROS 2, creating publishers and subscribers for sensor data and control commands
4. **Debug** ROS 2 systems using command-line tools (ros2 topic, ros2 node, ros2 service) and visualization tools (RViz, rqt)
5. **Apply** ROS 2 best practices including parameter management, launch files, and package organization

**Prerequisites:**
- Chapter 1: Physical AI Foundations
- Python proficiency
- Basic understanding of networking concepts
- Linux/Ubuntu command line familiarity

---

## 2.1 ROS 2 Architecture: The Robot's Nervous System

### What is ROS 2?

[SOURCE NEEDED: Definition, history (ROS 1 vs ROS 2), philosophy]

**Key Improvements in ROS 2:**
- [SOURCE NEEDED: Real-time capable]
- [SOURCE NEEDED: DDS middleware]
- [SOURCE NEEDED: Security features]
- [SOURCE NEEDED: Multi-platform support]

### Graph Architecture

[SOURCE NEEDED: Explanation of the ROS 2 graph - nodes, topics, services, actions as neurons and synapses]

**Diagram: ROS 2 Computation Graph**

```
[DIAGRAM DESCRIPTION]
- Multiple "Node" boxes (representing processes)
- "Topic" arrows between nodes (publish/subscribe)
- "Service" bidirectional arrows (request/reply)
- "Action" arrows with feedback loop
- Parameter server connection
```

### DDS Middleware

[SOURCE NEEDED: Data Distribution Service, QoS (Quality of Service) policies]

**QoS Profiles:**
[SOURCE NEEDED: Reliability, durability, history policies and when to use each]

---

## 2.2 Installation and Workspace Setup

### Installing ROS 2

#### On Ubuntu 22.04

```bash
# [SOURCE NEEDED: Complete installation commands for ROS 2 Humble]
# Set up sources
# Install ROS 2 packages
# Install development tools (colcon, rosdep)
# Set up environment
```

### Creating a Workspace

```bash
# [SOURCE NEEDED: Workspace creation commands]
# Create workspace structure
# Source ROS 2
# Build with colcon
```

**Workspace Structure:**
```
ros2_ws/
├── src/           # Source code for packages
├── build/         # Build artifacts
├── install/       # Installed packages
└── log/           # Build and runtime logs
```

---

## 2.3 Nodes: The Basic Unit of Computation

### What is a Node?

[SOURCE NEEDED: Explanation of nodes as modular, single-purpose processes]

**Design Principles:**
- [SOURCE NEEDED: Single responsibility]
- [SOURCE NEEDED: Loose coupling]
- [SOURCE NEEDED: Language agnostic]

### Creating Your First Node (Python)

#### Code Example 1: Minimal Node

```python
"""
Minimal ROS 2 node in Python
[SOURCE NEEDED: Complete working example]
"""

import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        # [SOURCE NEEDED: Node initialization]
        pass

def main(args=None):
    # [SOURCE NEEDED: ROS 2 initialization and spin]
    pass

if __name__ == '__main__':
    main()
```

**Running the Node:**
```bash
# [SOURCE NEEDED: Commands to run the node]
```

### Creating Nodes in C++

#### Code Example 2: Minimal Node (C++)

```cpp
/*
Minimal ROS 2 node in C++
[SOURCE NEEDED: Complete working example]
*/

#include "rclcpp/rclcpp.hpp"

// [SOURCE NEEDED: Node class definition]
// [SOURCE NEEDED: main function with rclcpp::init and spin]
```

---

## 2.4 Topics: Publish-Subscribe Communication

### The Pub/Sub Pattern

[SOURCE NEEDED: Explanation of publish-subscribe for continuous data streams]

**When to Use Topics:**
[SOURCE NEEDED: Sensor data, continuous state updates, many-to-many communication]

### Message Types

[SOURCE NEEDED: Standard message types (std_msgs, geometry_msgs, sensor_msgs)]

**Common Message Types:**
- `std_msgs/String`: [SOURCE NEEDED]
- `geometry_msgs/Twist`: [SOURCE NEEDED]
- `sensor_msgs/LaserScan`: [SOURCE NEEDED]
- `sensor_msgs/Image`: [SOURCE NEEDED]

### Creating a Publisher

#### Code Example 3: Publisher Node

```python
"""
Publisher node example
[SOURCE NEEDED: Complete implementation publishing to a topic]
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PublisherNode(Node):
    # [SOURCE NEEDED: Publisher setup]
    # [SOURCE NEEDED: Timer callback for publishing]
    pass
```

### Creating a Subscriber

#### Code Example 4: Subscriber Node

```python
"""
Subscriber node example
[SOURCE NEEDED: Complete implementation subscribing to a topic]
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SubscriberNode(Node):
    # [SOURCE NEEDED: Subscriber setup]
    # [SOURCE NEEDED: Callback function to process messages]
    pass
```

### QoS (Quality of Service)

[SOURCE NEEDED: Reliability (reliable vs. best effort), Durability (volatile vs. transient local), History (keep last N messages)]

#### Code Example 5: Custom QoS

```python
"""
Using custom QoS profiles
[SOURCE NEEDED: Example with reliable, durable QoS for critical data]
"""

from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# [SOURCE NEEDED: Create custom QoS profile]
# [SOURCE NEEDED: Apply to publisher/subscriber]
```

---

## 2.5 Services: Request-Response Pattern

### What are Services?

[SOURCE NEEDED: Synchronous request-response for occasional operations]

**When to Use Services:**
[SOURCE NEEDED: Computations, queries, configuration changes]

### Creating a Service Server

#### Code Example 6: Service Server

```python
"""
Service server example
[SOURCE NEEDED: Complete implementation of service server]
"""

import rclpy
from rclpy.node import Node
# [SOURCE NEEDED: Import service type, e.g., AddTwoInts]

class ServiceServer(Node):
    # [SOURCE NEEDED: Service server setup]
    # [SOURCE NEEDED: Callback function to process requests]
    pass
```

### Creating a Service Client

#### Code Example 7: Service Client

```python
"""
Service client example
[SOURCE NEEDED: Complete implementation of service client]
"""

import rclpy
from rclpy.node import Node
# [SOURCE NEEDED: Import service type]

class ServiceClient(Node):
    # [SOURCE NEEDED: Service client setup]
    # [SOURCE NEEDED: Sending request and handling response]
    pass
```

---

## 2.6 Actions: Long-Running Tasks with Feedback

### What are Actions?

[SOURCE NEEDED: Asynchronous goal-based interface with feedback and cancellation]

**Action Components:**
- **Goal**: [SOURCE NEEDED: Target to achieve]
- **Feedback**: [SOURCE NEEDED: Progress updates]
- **Result**: [SOURCE NEEDED: Final outcome]

**When to Use Actions:**
[SOURCE NEEDED: Navigation, manipulation, long computations]

### Creating an Action Server

#### Code Example 8: Action Server

```python
"""
Action server example
[SOURCE NEEDED: Complete implementation with goal handling, feedback, result]
"""

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
# [SOURCE NEEDED: Import action type, e.g., Fibonacci]

class FibonacciActionServer(Node):
    # [SOURCE NEEDED: Action server setup]
    # [SOURCE NEEDED: Execute callback with feedback publishing]
    pass
```

### Creating an Action Client

#### Code Example 9: Action Client

```python
"""
Action client example
[SOURCE NEEDED: Complete implementation sending goal and handling feedback]
"""

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
# [SOURCE NEEDED: Import action type]

class FibonacciActionClient(Node):
    # [SOURCE NEEDED: Action client setup]
    # [SOURCE NEEDED: Send goal, handle feedback and result]
    pass
```

---

## 2.7 Robot Control with ROS 2

### Control Architectures

[SOURCE NEEDED: Position control, velocity control, effort control]

**Diagram: Control Loop in ROS 2**

```
[DIAGRAM DESCRIPTION]
- Sensors publish to /sensor_data topic
- Controller node subscribes to /sensor_data, publishes to /cmd_vel
- Actuator node subscribes to /cmd_vel, controls motors
- Feedback loop from actuators back to sensors
```

### Velocity Control

#### Code Example 10: Velocity Controller Node

```python
"""
Velocity controller for differential drive robot
[SOURCE NEEDED: Complete implementation]
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
# [SOURCE NEEDED: Additional imports]

class VelocityController(Node):
    # [SOURCE NEEDED: Subscribe to target velocity]
    # [SOURCE NEEDED: Publish to motor commands]
    # [SOURCE NEEDED: PID control implementation]
    pass
```

### Trajectory Following

[SOURCE NEEDED: Interpolating waypoints, smooth path execution]

#### Code Example 11: Trajectory Follower

```python
"""
Trajectory follower node
[SOURCE NEEDED: Complete implementation following a sequence of waypoints]
"""

import rclpy
from rclpy.node import Node
# [SOURCE NEEDED: Imports]

class TrajectoryFollower(Node):
    # [SOURCE NEEDED: Receive trajectory (list of poses)]
    # [SOURCE NEEDED: Interpolate between waypoints]
    # [SOURCE NEEDED: Execute smooth motion]
    pass
```

---

## 2.8 Integration: Sensors and Actuators

### Sensor Integration Example

[SOURCE NEEDED: Integrating a camera or LiDAR with ROS 2]

#### Code Example 12: Camera Publisher

```python
"""
Publishing camera frames to ROS 2
[SOURCE NEEDED: Complete implementation using cv_bridge]
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
# [SOURCE NEEDED: cv_bridge import]

class CameraPublisher(Node):
    # [SOURCE NEEDED: OpenCV camera capture]
    # [SOURCE NEEDED: Convert to ROS Image message]
    # [SOURCE NEEDED: Publish to topic]
    pass
```

### Actuator Integration Example

[SOURCE NEEDED: Controlling motors via ROS 2]

---

## 2.9 Launch Files: Starting Complex Systems

### What are Launch Files?

[SOURCE NEEDED: Python-based launch system for starting multiple nodes with configuration]

### Creating a Launch File

#### Code Example 13: Launch File

```python
"""
Launch file starting multiple nodes
[SOURCE NEEDED: Complete launch file example]
"""

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # [SOURCE NEEDED: Define nodes to launch]
    # [SOURCE NEEDED: Set parameters]
    # [SOURCE NEEDED: Return LaunchDescription]
    pass
```

**Running a Launch File:**
```bash
# [SOURCE NEEDED: ros2 launch command]
```

---

## 2.10 Parameters: Runtime Configuration

### Parameter Management

[SOURCE NEEDED: Declaring, setting, getting, and updating parameters]

#### Code Example 14: Using Parameters

```python
"""
Node with parameters
[SOURCE NEEDED: Complete implementation with parameter declaration and update]
"""

import rclpy
from rclpy.node import Node

class ParameterNode(Node):
    # [SOURCE NEEDED: Declare parameters]
    # [SOURCE NEEDED: Get parameter values]
    # [SOURCE NEEDED: Parameter update callback]
    pass
```

**Setting Parameters from Command Line:**
```bash
# [SOURCE NEEDED: ros2 param set commands]
```

---

## 2.11 Debugging and Visualization Tools

### Command-Line Tools

```bash
# [SOURCE NEEDED: ros2 node list/info commands]
# [SOURCE NEEDED: ros2 topic list/echo/hz commands]
# [SOURCE NEEDED: ros2 service list/call commands]
# [SOURCE NEEDED: ros2 param list/get/set commands]
```

### RViz: 3D Visualization

[SOURCE NEEDED: Using RViz to visualize robot state, sensor data, transforms]

**Launching RViz:**
```bash
# [SOURCE NEEDED: rviz2 command]
```

### rqt: GUI Tools

[SOURCE NEEDED: rqt_graph for visualizing node connections, rqt_plot for data plotting]

---

## Practical Examples

### Example: Wall-Following Robot

[SOURCE NEEDED: Complete scenario - robot following wall using LaserScan]

#### Code Example 15: Wall Follower Node

```python
"""
Wall-following behavior using LaserScan
[SOURCE NEEDED: Complete implementation]
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollower(Node):
    # [SOURCE NEEDED: Subscribe to /scan]
    # [SOURCE NEEDED: Implement wall-following logic]
    # [SOURCE NEEDED: Publish velocity commands]
    pass
```

---

## Lab Activities

### Lab 4: Publisher-Subscriber Communication

**Objective:** Create talker and listener nodes exchanging custom messages

**Tasks:**
1. [SOURCE NEEDED: Create ROS 2 package]
2. [SOURCE NEEDED: Write publisher node (talker)]
3. [SOURCE NEEDED: Write subscriber node (listener)]
4. [SOURCE NEEDED: Test with different QoS settings]

**Deliverables:**
- Source code for both nodes
- Report on QoS experiment results

**Starter Code:**
[SOURCE NEEDED: Package setup and node templates]

### Lab 5: Service Implementation

**Objective:** Build service for robot configuration

**Tasks:**
1. [SOURCE NEEDED: Define custom service interface]
2. [SOURCE NEEDED: Implement service server]
3. [SOURCE NEEDED: Implement service client]
4. [SOURCE NEEDED: Test with multiple requests]

**Deliverables:**
- Service definition files
- Server and client code
- Testing documentation

### Lab 6: Action-Based Control

**Objective:** Create action for trajectory execution

**Tasks:**
1. [SOURCE NEEDED: Define action interface with goal, feedback, result]
2. [SOURCE NEEDED: Implement action server]
3. [SOURCE NEEDED: Implement action client]
4. [SOURCE NEEDED: Test goal cancellation]

**Deliverables:**
- Action server and client code
- Demonstration of feedback publishing
- Report on cancellation behavior

### Lab 7: Autonomous Navigation in Simulation

**Objective:** Integrate sensors and control for TurtleBot3 navigation in Gazebo

**Tasks:**
1. [SOURCE NEEDED: Launch TurtleBot3 in Gazebo world]
2. [SOURCE NEEDED: Write obstacle avoidance node using /scan]
3. [SOURCE NEEDED: Test in multiple environments]
4. [SOURCE NEEDED: Tune parameters for smooth navigation]

**Deliverables:**
- Navigation node implementation
- Video demonstration in Gazebo
- Parameter tuning report

---

## Summary

### Key Takeaways

1. **ROS 2 is the Robot Nervous System**: [SOURCE NEEDED: Distributed communication and control]
2. **Nodes are Modular Processes**: [SOURCE NEEDED: Single responsibility principle]
3. **Topics for Continuous Data**: [SOURCE NEEDED: Pub/sub pattern for sensor streams]
4. **Services for Request-Response**: [SOURCE NEEDED: Occasional operations]
5. **Actions for Long-Running Tasks**: [SOURCE NEEDED: With feedback and cancellation]
6. **QoS Matters**: [SOURCE NEEDED: Reliability and durability tradeoffs]
7. **Tools for Development**: [SOURCE NEEDED: CLI, RViz, rqt]

### Concepts Covered

- ROS 2 architecture and DDS middleware
- Nodes in Python and C++
- Pub/sub with topics and QoS profiles
- Request-response with services
- Goal-based actions with feedback
- Robot control: velocity and trajectory
- Sensor integration (camera, LaserScan)
- Launch files for system startup
- Parameter management
- Debugging with command-line tools
- Visualization with RViz and rqt

### Looking Ahead

In the next chapter, we'll explore **Simulation with Gazebo, Unity & Digital Twins**. You'll learn to test your ROS 2 systems in virtual environments before deploying to physical robots, enabling rapid prototyping and safe experimentation.

---

## Review Questions

### Conceptual Understanding

1. **Explain** the ROS 2 graph architecture. How do nodes communicate via topics, services, and actions?

2. **Compare** topics vs. services vs. actions. When would you use each communication pattern?

3. **Describe** QoS policies in ROS 2. Why would you use "reliable" vs. "best effort" reliability?

4. **Explain** the role of the DDS middleware in ROS 2. How does it differ from ROS 1's communication?

### Implementation Questions

5. **Write** a Python snippet to create a subscriber to the `/scan` topic (LaserScan message type) with reliable QoS.

6. **Design** a service interface for a robot battery status query. What should the request and response contain?

7. **Implement** the callback function for an action server that moves a robot to a target position, publishing progress feedback every 0.5 seconds.

### Debugging & Troubleshooting

8. **Diagnose**: A subscriber isn't receiving messages from a publisher. Both nodes are running. What commands would you use to debug? List at least 3 `ros2` CLI commands.

9. **Troubleshoot**: Your robot moves erratically with high-frequency oscillations. The control loop runs at 100Hz. What might be wrong, and how would you fix it?

### Application & Design

10. **Design** a ROS 2 system for a warehouse picking robot with the following requirements:
    - Vision system for object detection
    - Arm control for grasping
    - Base navigation for moving between locations
    - Task coordination

    Specify: nodes, topics, services, actions, and their purposes.

11. **Architecture**: You're building a fleet of delivery robots that need to coordinate. How would you structure the ROS 2 system? Consider: individual robot control, fleet management, task assignment.

12. **Performance**: A sensor publishes at 100Hz but your processing can only handle 30Hz. How would you configure the subscriber's QoS to handle this?

---

## Further Reading

### Official Documentation
- [SOURCE NEEDED: ROS 2 documentation links]
- [SOURCE NEEDED: rclpy (Python) API reference]
- [SOURCE NEEDED: rclcpp (C++) API reference]

### Tutorials
- [SOURCE NEEDED: ROS 2 tutorials for beginners]
- [SOURCE NEEDED: Advanced ROS 2 patterns]

### Books
- [SOURCE NEEDED: ROS 2 textbooks and guides]

### Community
- [SOURCE NEEDED: ROS Discourse, GitHub repos, community projects]

---

## Code Repository

All code examples from this chapter are available at:
[SOURCE NEEDED: GitHub repository link with ROS 2 packages]

---

**Next Chapter:** [Chapter 3: Simulation with Gazebo, Unity & Digital Twins](./chapter-03.md)
