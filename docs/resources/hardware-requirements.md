---
id: hardware-requirements
title: Hardware Requirements
sidebar_label: Hardware Requirements
sidebar_position: 3
description: "Minimum and recommended hardware specifications"
---

# Hardware Requirements

This page outlines the hardware specifications needed for different parts of the course.

## Minimum Requirements

### For Chapters 1-3 (ROS 2, Gazebo, Unity)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Intel i5 / AMD Ryzen 5 (4 cores) | Intel i7 / AMD Ryzen 7 (8 cores) |
| **RAM** | 8GB | 16GB |
| **Storage** | 50GB free | 100GB+ SSD |
| **GPU** | Integrated graphics | Dedicated GPU (GTX 1650 or better) |
| **OS** | Ubuntu 22.04 LTS or Windows 10+ with WSL2 | Ubuntu 22.04 LTS (native) |

**Can complete**: Chapters 1-3 fully

---

## Recommended Requirements

### For Chapters 1-4 (Including NVIDIA Isaac)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Intel i7 / AMD Ryzen 7 (8 cores) | Intel i9 / AMD Ryzen 9 (16 cores) |
| **RAM** | 16GB | 32GB+ |
| **Storage** | 100GB SSD | 250GB+ NVMe SSD |
| **GPU** | NVIDIA RTX 3060 (6GB VRAM) | NVIDIA RTX 4070 or better (12GB+ VRAM) |
| **OS** | Ubuntu 22.04 LTS (native) | Ubuntu 22.04 LTS (native) |

**Can complete**: All chapters including GPU-accelerated Isaac Sim

---

## GPU Requirements Breakdown

### Why NVIDIA GPU?

- **Isaac Sim**: Requires NVIDIA RTX GPU with ray tracing support
- **CUDA**: GPU-accelerated ML training
- **TensorRT**: Optimized inference on Jetson devices

### GPU Comparison

| GPU Model | VRAM | Isaac Sim | ML Training | Recommended For |
|-----------|------|-----------|-------------|-----------------|
| GTX 1650 | 4GB | ❌ No | Basic | Chapters 1-3 only |
| RTX 3060 | 6GB | ✅ Yes | Moderate | Chapters 1-4 (small scenes) |
| RTX 3070 | 8GB | ✅ Yes | Good | All chapters |
| RTX 4070 | 12GB | ✅ Yes | Excellent | All chapters + complex scenes |
| RTX 4090 | 24GB | ✅ Yes | Outstanding | Professional use |

---

## Cloud Computing Alternatives

If you don't have access to the required hardware, consider:

### Google Colab

**Pros:**
- [SOURCE NEEDED: Colab advantages]

**Cons:**
- [SOURCE NEEDED: Colab limitations]

**Good for:** Chapters 1, 2, and ML portions of Chapters 4-5

### AWS EC2 with GPU

**Pros:**
- [SOURCE NEEDED: AWS advantages]

**Cost:** [SOURCE NEEDED: Pricing estimates]

**Good for:** All chapters

### NVIDIA Omniverse Cloud

**Pros:**
- [SOURCE NEEDED: Omniverse Cloud advantages]

**Good for:** Chapter 4 (Isaac Sim)

---

## Physical Robot Hardware (Optional)

For those wanting to deploy on real hardware:

### Budget Option: TurtleBot3 Burger

**Cost**: ~$500
**Specs**: [SOURCE NEEDED]
**Good for**: Chapters 2-3 sim-to-real

### Mid-Range: TurtleBot3 Waffle Pi

**Cost**: ~$1,800
**Specs**: [SOURCE NEEDED]
**Good for**: Chapters 2-4

### Advanced: NVIDIA Jetson with Custom Robot

**Cost**: $200-$1,000+
**Specs**: [SOURCE NEEDED]
**Good for**: Edge deployment (Chapter 4)

---

## Storage Breakdown

| Component | Disk Space |
|-----------|------------|
| Ubuntu 22.04 LTS | ~10GB |
| ROS 2 Humble | ~5GB |
| Gazebo Classic + Models | ~5GB |
| Unity Editor | ~15GB |
| NVIDIA Isaac Sim | ~30GB |
| ML Libraries (PyTorch, TensorFlow) | ~10GB |
| Project Files and Datasets | ~20GB |
| **Total** | **~95GB** |

Recommendation: **150GB+ of fast SSD storage**

---

## Checking Your System

### CPU Information

```bash
# Linux
lscpu

# Windows
wmic cpu get name
```

### RAM Information

```bash
# Linux
free -h

# Windows
wmic memorychip get capacity
```

### GPU Information

```bash
# Linux (NVIDIA)
nvidia-smi

# Windows (NVIDIA)
nvidia-smi
```

### Disk Space

```bash
# Linux
df -h

# Windows
wmic logicaldisk get size,freespace,caption
```

---

## Upgrade Recommendations

If you're considering upgrading your hardware:

1. **Priority 1: GPU** - If you have integrated graphics, adding any dedicated GPU will significantly improve performance. For Isaac Sim, prioritize NVIDIA RTX series.

2. **Priority 2: RAM** - Upgrading from 8GB to 16GB will allow running multiple tools simultaneously (ROS, Gazebo, Unity, IDE).

3. **Priority 3: Storage** - SSD dramatically improves build times and simulation loading. NVMe is even better.

4. **Priority 4: CPU** - More cores help with parallel compilation and multiple simulations.

---

## Can I Still Take the Course?

**Yes!** Even with below-minimum hardware:

- Use **cloud platforms** for GPU-intensive work (Chapter 4)
- Focus on **conceptual learning** and run lighter examples
- Use **smaller simulation scenes** with reduced complexity
- Team up with classmates who have better hardware

---

**Questions?** Contact [SOURCE NEEDED: Support information]

Return to the [Course Home](../intro.md)
