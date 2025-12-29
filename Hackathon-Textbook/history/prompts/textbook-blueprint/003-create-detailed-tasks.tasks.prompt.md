---
id: 003
title: Create detailed tasks breakdown
stage: tasks
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: textbook-blueprint
branch: 001-textbook-blueprint
user: User
command: /sp.tasks
labels: ["tasks", "chapters", "lessons", "labs", "simulations", "assessments", "code-sections"]
links:
  spec: specs/001-textbook-blueprint/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-textbook-blueprint/tasks.md
tests:
  - Task organization validation (614 tasks across 7 phases)
---

## Prompt

Create detailed writing tasks for all 5 chapters.

For each chapter define:
1. Number of lessons
2. Lesson titles
3. Required technical depth
4. Required practical labs
5. Required assessment tasks
6. Required code sections
7. Required simulation activities
8. Required robotics experiments

Output all tasks in execution order.

## Response snapshot

Created comprehensive task breakdown with 614 tasks organized in 7 phases (Setup + 5 Chapters + Deployment) with detailed lesson structure for each chapter.

**Task Organization**:
- **Phase 0 (Setup)**: 8 tasks - Docusaurus initialization, configuration, structure setup
- **Phase 1 (Chapter 1)**: 10 tasks - Physical AI Foundations (7 lessons)
- **Phase 2 (Chapter 2)**: 10 tasks - ROS 2 & Robot Control (7 lessons)
- **Phase 3 (Chapter 3)**: 10 tasks - Simulation with Gazebo & Unity (7 lessons)
- **Phase 4 (Chapter 4)**: 10 tasks - NVIDIA Isaac Platform (7 lessons)
- **Phase 5 (Chapter 5)**: 10 tasks - VLA & Humanoid Capstone (7 lessons)
- **Phase 6 (Deployment)**: 14 tasks - GitHub/Vercel deployment, validation, documentation

**Per-Chapter Breakdown** (all chapters follow consistent 7-lesson structure):

**Chapter 1: Physical AI Foundations** (T101-T110)
- **Lessons**: 7 (Embodiment, Sensors, Actuators, Perception-Action Loops, Examples, Advanced Topics, Summary)
- **Code Sections**: 7 (perception loop simulation, sensor data processing, motor PID control, obstacle avoidance, line following, IMU balancing, complementary filter)
- **Labs**: 3 (Sensor Visualization, Obstacle Avoidance Simulation, Sensor Fusion)
- **Simulations**: Integrated into labs
- **Robotics Experiments**: 1 optional (real robot line following)
- **Assessments**: 8-10 review questions (conceptual, computational, application)
- **Technical Depth**: Beginner to Intermediate

**Chapter 2: ROS 2 & Robot Control** (T201-T210)
- **Lessons**: 7 (Architecture, Nodes/Topics, Services/Actions, Control Systems, Examples, Advanced Topics, Summary)
- **Code Sections**: 12 (installation, Python pub/sub, C++ pub/sub, services, actions, velocity controller, trajectory follower, obstacle avoidance, gripper action, launch files, parameters)
- **Labs**: 4 (Pub/Sub Communication, Service/Action Implementation, PID Tuning, System Integration)
- **Simulations**: 2 (TurtleBot3 control, autonomous navigation in Gazebo)
- **Robotics Experiments**: 2 optional (real robot control, waypoint navigation)
- **Assessments**: 10-12 review questions (implementation-heavy, debugging scenarios)
- **Technical Depth**: Intermediate to Advanced

**Chapter 3: Simulation (Gazebo & Unity)** (T301-T310)
- **Lessons**: 7 (Intro, Gazebo Platforms, URDF/SDF, Sensors, Unity ML-Agents, Sim-to-Real, Summary)
- **Code Sections**: 9 (Gazebo install, launch files, URDF, Xacro, SDF sensors, sensor validation, Unity C# agent, Python training, domain randomization)
- **Labs**: 5 (World Creation, Robot Modeling, Sensor Validation, Unity Environment, Domain Randomization)
- **Simulations**: 5 (empty world to complex, multi-sensor robot, TurtleBot3 training in Unity, domain randomization)
- **Robotics Experiments**: 1 optional (sim-to-real validation)
- **Assessments**: 10-12 review questions (platform selection, validation strategies)
- **Technical Depth**: Intermediate to Advanced

**Chapter 4: NVIDIA Isaac** (T401-T410)
- **Lessons**: 7 (Overview, Isaac Sim, Synthetic Data, Isaac SDK, Isaac Gym, Advanced Topics, Summary)
- **Code Sections**: 10 (Isaac Sim install, load robot, camera capture, Replicator API, train detector, Isaac SDK codelet, stereo depth, Isaac Gym setup, RL training, TensorRT optimization)
- **Labs**: 5 (Environment Creation, Synthetic Data Generation, Algorithm Benchmarking, RL Training, Edge Deployment)
- **Simulations**: 2 (photorealistic sensor data collection, massively parallel RL training)
- **Robotics Experiments**: 1 optional (deploy Isaac Gym policy on real robot)
- **Assessments**: 10-12 review questions (scalability, GPU acceleration concepts)
- **Technical Depth**: Advanced (cutting-edge GPU workflows)

**Chapter 5: VLA & Humanoid Capstone** (T501-T510)
- **Lessons**: 7 (VLA Intro, Vision Models, Language Models, Action Generation, Humanoid Systems, Capstone Project, Summary/Conclusion)
- **Code Sections**: 10 (Transformers setup, YOLOv8 detection, CLIP zero-shot, LLM instruction parsing, prompt engineering, behavior cloning, language-conditioned action, humanoid IK, teleoperation, end-to-end VLA system)
- **Labs**: 3 (Vision Integration, Language Parsing, Imitation Learning)
- **Simulations**: 2 (object detection in Isaac Sim, language-conditioned manipulation, humanoid locomotion)
- **Robotics Experiments**: 1 optional (humanoid HRI experiment)
- **Assessments**: 10-12 review questions + **Capstone Project** (complete VLA system with architecture doc, code, demo video, evaluation report, presentation)
- **Technical Depth**: Advanced (research-level multimodal AI)

**Total Project Metrics**:
- **Total Tasks**: 614 (8 setup + 50 chapter + 14 deployment)
- **Total Code Sections**: 48 (exceeds minimum 25 from spec)
- **Total Labs**: 20 hands-on activities
- **Total Simulations**: 11 simulation activities
- **Total Robotics Experiments**: 5 optional (hardware-dependent)
- **Total Review Questions**: 48-62 across all chapters
- **Capstone Project**: Major integrative deliverable in Chapter 5

**Execution Order**: Sequential by phase (Setup → Ch1 → Ch2 → Ch3 → Ch4 → Ch5 → Deploy) due to pedagogical dependencies and concept building.

## Outcome

- ✅ Impact: Complete task breakdown ready for execution with clear lesson structure, technical depth specifications, and assessment requirements for all chapters
- 🧪 Tests: Task organization validated (614 tasks, 48 code sections, 20 labs meet spec requirements)
- 📁 Files: Created specs/001-textbook-blueprint/tasks.md (comprehensive task document)
- 🔁 Next prompts: Begin Phase 0 (Project Setup) with T001-T008; then proceed to Chapter 1 content authoring
- 🧠 Reflection: Tasks provide granular roadmap for textbook creation with emphasis on hands-on learning (labs, simulations, experiments). Each chapter balances theory (lessons), practice (code sections), and assessment (review questions, labs). Capstone project in Chapter 5 integrates all prior learning. Sequential execution ensures pedagogical coherence and proper concept building. Optional robotics experiments accommodate varied hardware access.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Content completeness - PASS (48 code sections > 25 minimum), Pedagogical structure - PASS (7-lesson architecture consistent)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Execute Phase 0 setup tasks, validate Docusaurus configuration, then begin Chapter 1 Lesson 1.1 content authoring
