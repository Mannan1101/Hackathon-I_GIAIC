---
id: software-setup
title: Software Setup Guide
sidebar_label: Software Setup
sidebar_position: 2
description: "Detailed installation instructions for all required software"
---

# Software Setup Guide

This guide will walk you through installing all software needed for the Physical AI & Humanoid Robotics course.

## Overview

You will need:
1. Ubuntu 22.04 LTS (native or VM)
2. ROS 2 Humble Hawksbill
3. Gazebo Classic / Gazebo Sim
4. Unity with ML-Agents Toolkit
5. NVIDIA Isaac Sim (requires NVIDIA GPU)
6. Python 3.10+ with ML libraries

---

## Step 1: Ubuntu 22.04 LTS Setup

### Option A: Native Installation (Recommended)

[SOURCE NEEDED: Ubuntu installation steps]

### Option B: Windows Subsystem for Linux 2 (WSL2)

[SOURCE NEEDED: WSL2 setup instructions]

### Option C: Virtual Machine

[SOURCE NEEDED: VirtualBox or VMware setup]

---

## Step 2: ROS 2 Humble Installation

### Set Locale

```bash
# [SOURCE NEEDED: Locale setup commands]
```

### Add ROS 2 Repository

```bash
# [SOURCE NEEDED: Repository addition commands]
```

### Install ROS 2 Packages

```bash
# [SOURCE NEEDED: Installation commands]
```

### Environment Setup

```bash
# [SOURCE NEEDED: sourcing and environment configuration]
```

### Verify Installation

```bash
# [SOURCE NEEDED: Verification commands]
```

---

## Step 3: Gazebo Installation

### Gazebo Classic

```bash
# [SOURCE NEEDED: Installation commands]
```

### Gazebo Sim (Ignition)

```bash
# [SOURCE NEEDED: Installation commands]
```

---

## Step 4: Python and ML Libraries

### Python 3.10+

```bash
# [SOURCE NEEDED: Python installation]
```

### Create Virtual Environment

```bash
# [SOURCE NEEDED: venv setup]
```

### Install ML Libraries

```bash
# [SOURCE NEEDED: PyTorch, TensorFlow, NumPy, OpenCV installation]
```

---

## Step 5: Unity and ML-Agents

### Download Unity Hub

[SOURCE NEEDED: Unity Hub download and installation]

### Install Unity Editor

[SOURCE NEEDED: Recommended Unity version]

### ML-Agents Toolkit

```bash
# [SOURCE NEEDED: ML-Agents installation]
```

---

## Step 6: NVIDIA Isaac Sim (Optional, GPU Required)

### System Requirements

[SOURCE NEEDED: GPU requirements, CUDA, driver versions]

### Omniverse Installation

[SOURCE NEEDED: Omniverse Launcher download and setup]

### Isaac Sim Installation

[SOURCE NEEDED: Isaac Sim installation from Omniverse]

---

## Step 7: Additional Tools

### VSCode or PyCharm

[SOURCE NEEDED: IDE setup]

### Git

```bash
# [SOURCE NEEDED: Git installation and configuration]
```

### Docker (Optional)

```bash
# [SOURCE NEEDED: Docker installation]
```

---

## Verification Checklist

Run these commands to verify your setup:

- [ ] `ros2 --version` - Should show ROS 2 Humble
- [ ] `gazebo --version` - Should show Gazebo version
- [ ] `python3 --version` - Should show Python 3.10+
- [ ] `import torch; print(torch.__version__)` - PyTorch installed
- [ ] Unity Hub opens successfully
- [ ] Isaac Sim launches (if installed)

---

## Troubleshooting

### Common Issues

**Issue 1**: ROS 2 commands not found
[SOURCE NEEDED: Solution]

**Issue 2**: Gazebo crashes on launch
[SOURCE NEEDED: Solution]

**Issue 3**: CUDA not detected
[SOURCE NEEDED: Solution]

---

## Cloud Alternatives

If you don't have access to the required hardware:

### Google Colab Pro
[SOURCE NEEDED: Using Colab for ML portions]

### AWS RoboMaker
[SOURCE NEEDED: Cloud ROS development]

### NVIDIA Omniverse Cloud
[SOURCE NEEDED: Cloud Isaac Sim access]

---

**Setup complete?** Return to the [Course Home](../intro.md) to begin!
