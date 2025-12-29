# Implementation Plan: Physical AI & Humanoid Robotics Textbook Website

**Branch**: `001-textbook-blueprint` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-textbook-blueprint/spec.md`

## Summary

Create a complete 5-chapter university textbook on Physical AI & Humanoid Robotics, delivered as a Docusaurus-based static website. The textbook progresses from foundational concepts (embodiment, sensing, action) through practical implementation (ROS 2, simulation platforms) to advanced topics (NVIDIA Isaac, VLA models, humanoid capstone). Each chapter includes learning objectives, prerequisites, core content, code examples, advanced topics, summary, and review questions. The website will be deployed on GitHub Pages with version control workflow and CI/CD automation.

**Technical Approach**: Source-driven content generation → Markdown authoring → Docusaurus site build → Git-based deployment

---

## Technical Context

**Platform**: Docusaurus v3.x (Static Site Generator)
**Primary Language**: Markdown (MDX support for enhanced features)
**Content Format**: Markdown files with YAML frontmatter
**Code Examples**: Python, C++, YAML, Bash (with syntax highlighting)
**Mathematical Notation**: KaTeX for LaTeX rendering
**Version Control**: Git with GitHub remote
**Deployment Targets**: GitHub Pages (primary), Vercel (alternative)
**Build System**: Node.js 18+, npm/yarn for dependencies
**Testing**: Docusaurus build validation, broken link checking, frontmatter validation
**Performance Goals**: <2s page load, <500ms navigation transitions
**Constraints**: Zero hallucination (all content from source docs), Docusaurus standard features only
**Scale/Scope**: 5 chapters, ~50-100 pages total content, 25+ code examples minimum

---

## Constitution Check

*GATE: Must pass before content creation begins*

### Constitutional Compliance

| Principle | Status | Implementation |
|-----------|--------|----------------|
| **I. Content Fidelity** | ✅ PASS | All content extracted from provided source docs; gaps flagged |
| **II. Academic Rigor** | ✅ PASS | University-level standards; beginner→advanced progression |
| **III. Structural Completeness** | ✅ PASS | Exactly 5 chapters, each complete and independent |
| **IV. Docusaurus Compatibility** | ✅ PASS | Standard Docusaurus markdown, proper frontmatter, no custom plugins |
| **V. Pedagogical Structure** | ✅ PASS | 10-part chapter architecture consistently applied |
| **VI. Engineering Focus** | ✅ PASS | Zero marketing; production-quality code examples |
| **VII. Multi-Modal Learning** | ✅ PASS | Code blocks, tables, diagram descriptions, math notation, admonitions |

### Content Standards Compliance

- ✅ **Completeness**: All source concepts included; no forward references without introduction
- ✅ **Code Quality**: Syntactically correct, commented (WHY not WHAT), versioned
- ✅ **Accuracy**: Technical specs verified against source; formulas validated

**Constitution Status**: ✅ **ALL CHECKS PASSED** - Ready for content creation

---

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-blueprint/
├── spec.md                    # Feature specification (✅ complete)
├── plan.md                    # This implementation plan
├── tasks.md                   # Task breakdown (created via /sp.tasks)
├── checklists/
│   └── requirements.md        # Spec quality checklist (✅ complete)
└── research/
    └── source-analysis.md     # Analysis of source documentation (Phase 0)
```

### Docusaurus Project Structure (repository root)

```text
my-project/                    # Repository root
├── docs/                      # Textbook content (Docusaurus docs dir)
│   ├── intro.md              # Homepage/Introduction
│   ├── chapter-01/           # Chapter 1: Physical AI Foundations
│   │   ├── index.md         # Chapter overview page
│   │   ├── 01-embodiment.md
│   │   ├── 02-sensors.md
│   │   ├── 03-actuators.md
│   │   ├── 04-perception-action.md
│   │   ├── 05-examples.md
│   │   ├── 06-advanced.md
│   │   ├── 07-summary.md
│   │   └── assets/          # Chapter-specific images/diagrams
│   ├── chapter-02/           # Chapter 2: ROS 2 & Robot Control
│   │   ├── index.md
│   │   ├── 01-architecture.md
│   │   ├── 02-nodes-topics.md
│   │   ├── 03-services-actions.md
│   │   ├── 04-control-systems.md
│   │   ├── 05-examples.md
│   │   ├── 06-advanced.md
│   │   ├── 07-summary.md
│   │   └── assets/
│   ├── chapter-03/           # Chapter 3: Simulation (Gazebo & Unity)
│   │   ├── index.md
│   │   ├── 01-gazebo-intro.md
│   │   ├── 02-gazebo-worlds.md
│   │   ├── 03-unity-ml-agents.md
│   │   ├── 04-urdf-sdf.md
│   │   ├── 05-sim-to-real.md
│   │   ├── 06-advanced.md
│   │   ├── 07-summary.md
│   │   └── assets/
│   ├── chapter-04/           # Chapter 4: NVIDIA Isaac
│   │   ├── index.md
│   │   ├── 01-isaac-sim.md
│   │   ├── 02-isaac-sdk.md
│   │   ├── 03-synthetic-data.md
│   │   ├── 04-isaac-gym.md
│   │   ├── 05-examples.md
│   │   ├── 06-advanced.md
│   │   ├── 07-summary.md
│   │   └── assets/
│   ├── chapter-05/           # Chapter 5: VLA & Humanoid Capstone
│   │   ├── index.md
│   │   ├── 01-vision-models.md
│   │   ├── 02-language-models.md
│   │   ├── 03-action-generation.md
│   │   ├── 04-vla-integration.md
│   │   ├── 05-humanoid-systems.md
│   │   ├── 06-capstone-project.md
│   │   ├── 07-summary.md
│   │   └── assets/
│   └── resources/            # Course-wide resources
│       ├── prerequisites.md
│       ├── software-setup.md
│       ├── hardware-requirements.md
│       └── glossary.md
│
├── static/                    # Static assets (global images, PDFs, etc.)
│   ├── img/                  # Course branding, logos
│   └── files/                # Downloadable resources
│
├── src/                       # Docusaurus customizations
│   ├── css/
│   │   └── custom.css        # Custom styling
│   └── components/           # Custom React components (if needed)
│
├── docusaurus.config.js       # Docusaurus configuration
├── sidebars.js               # Sidebar navigation structure
├── package.json              # Node.js dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # Repository documentation
│
└── .github/                  # GitHub Actions workflows
    └── workflows/
        └── deploy.yml        # CI/CD for GitHub Pages deployment
```

**Structure Decision**: Standard Docusaurus documentation site with chapter-based organization. Each chapter is a subdirectory under `/docs` with multiple markdown files for sections, allowing granular navigation and maintainability. Assets (images/diagrams) stored per-chapter for modularity.

---

## Complexity Tracking

**No Constitution Violations** - Standard Docusaurus structure with zero custom complexity.

---

## Phase 0: Research & Source Analysis

### Objectives
1. Receive and analyze source documentation covering all 5 chapters
2. Map source content to chapter structure
3. Identify content gaps requiring clarification
4. Extract key concepts, code examples, and technical specifications
5. Validate source completeness against spec requirements

### Inputs
- Source documentation (provided by user) covering:
  - Physical AI fundamentals
  - ROS 2 architecture and control
  - Gazebo and Unity simulation
  - NVIDIA Isaac platform
  - VLA models and humanoid robotics

### Research Tasks
1. **Source Document Inventory**: Catalog all provided source files/documents
2. **Content Coverage Analysis**: Map source content to spec requirements (FR-001 to FR-030)
3. **Technical Extraction**: Extract version numbers, tool specifications, code examples from sources
4. **Gap Identification**: Flag any missing content per chapter (must not hallucinate)
5. **Example Collection**: Identify and validate all code examples for syntax correctness

### Outputs
- `specs/001-textbook-blueprint/research/source-analysis.md`: Document mapping source content to chapters, listing gaps
- `specs/001-textbook-blueprint/research/code-inventory.md`: Catalog of all code examples extracted from sources with language/version info

### Success Criteria
- Source content mapped to all 5 chapters
- All gaps explicitly documented (no assumptions)
- Minimum 25 code examples identified across sources (5 per chapter minimum per FR-006)
- Version numbers extracted for all tools (ROS 2, Gazebo, Unity, Isaac, Python, C++)

---

## Phase 1: Design & Architecture

### Objectives
1. Design detailed chapter outlines with section breakdown
2. Define Docusaurus configuration (sidebar, navigation, frontmatter)
3. Establish markdown formatting standards
4. Create content templates for consistency
5. Design version control workflow

### Design Tasks

#### 1.1 Chapter Outline Design

Create detailed outlines for each chapter following the 10-part architecture:

**Chapter 1: Physical AI Foundations**
- Index page: Chapter overview, learning objectives, prerequisites
- Section 1: What is Physical AI? (embodiment vs. disembodied AI)
- Section 2: Sensor Modalities (cameras, LiDAR, IMUs, tactile)
- Section 3: Actuators and Control Basics
- Section 4: Perception-Action Loops
- Section 5: Practical Examples (code demonstrations)
- Section 6: Advanced Topics (sensor fusion, real-time constraints)
- Section 7: Summary and Review Questions

**Chapter 2: ROS 2 & Robot Control**
- Index page: Chapter overview, learning objectives, prerequisites
- Section 1: ROS 2 Architecture Overview
- Section 2: Nodes and Topics (pub/sub pattern)
- Section 3: Services and Actions (request/response, long-running tasks)
- Section 4: Robot Control Implementation (position, velocity, trajectory)
- Section 5: Practical Examples (ROS 2 code with launch files)
- Section 6: Advanced Topics (parameter management, debugging with ros2 CLI)
- Section 7: Summary and Review Questions

**Chapter 3: Simulation (Gazebo & Unity)**
- Index page: Chapter overview, learning objectives, prerequisites
- Section 1: Introduction to Robot Simulation
- Section 2: Gazebo Classic and Gazebo Sim
- Section 3: Unity with ML-Agents
- Section 4: URDF/SDF Robot Models
- Section 5: Sensor Simulation and Validation
- Section 6: Advanced Topics (sim-to-real transfer, physics tuning)
- Section 7: Summary and Review Questions

**Chapter 4: NVIDIA Isaac Platform**
- Index page: Chapter overview, learning objectives, prerequisites
- Section 1: Isaac Sim Setup and Overview
- Section 2: Isaac SDK for Robot Algorithms
- Section 3: Synthetic Data Generation (domain randomization)
- Section 4: Isaac Gym for RL Training
- Section 5: Practical Examples (GPU-accelerated simulation)
- Section 6: Advanced Topics (photorealistic rendering, parallel environments)
- Section 7: Summary and Review Questions

**Chapter 5: VLA & Humanoid Capstone**
- Index page: Chapter overview, learning objectives, prerequisites
- Section 1: Vision Models for Robotics (object detection, scene understanding)
- Section 2: Language Models and Instruction Following
- Section 3: Action Generation from Language Commands
- Section 4: VLA Pipeline Integration
- Section 5: Humanoid Robot Systems
- Section 6: Capstone Project (end-to-end integration)
- Section 7: Summary and Review Questions

#### 1.2 Docusaurus Configuration Design

**docusaurus.config.js** key settings:
- Site title: "Physical AI & Humanoid Robotics: From Foundations to Deployment"
- Tagline: "A Comprehensive University Course on Building Intelligent Physical Systems"
- URL: `https://[username].github.io` (GitHub Pages) or custom domain
- Base URL: `/[repo-name]/` for GitHub Pages
- Theme: Classic (default Docusaurus theme)
- Syntax highlighting: Prism with Python, C++, YAML, Bash support
- Math support: KaTeX plugin for LaTeX rendering
- Navbar: Home, Chapters (dropdown), Resources, GitHub link
- Footer: Copyright, course metadata, license info

**sidebars.js** structure:
```javascript
module.exports = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 1: Physical AI Foundations',
      collapsible: true,
      collapsed: false,
      items: [
        'chapter-01/index',
        'chapter-01/01-embodiment',
        'chapter-01/02-sensors',
        'chapter-01/03-actuators',
        'chapter-01/04-perception-action',
        'chapter-01/05-examples',
        'chapter-01/06-advanced',
        'chapter-01/07-summary',
      ],
    },
    // ... repeat for chapters 2-5
    {
      type: 'category',
      label: 'Resources',
      items: [
        'resources/prerequisites',
        'resources/software-setup',
        'resources/hardware-requirements',
        'resources/glossary',
      ],
    },
  ],
};
```

#### 1.3 Markdown Formatting Standards

**Frontmatter Template** (every markdown file):
```yaml
---
id: unique-identifier
title: Page Title
sidebar_label: Short Label
sidebar_position: N
description: Brief description for SEO
---
```

**Content Structure Template**:
```markdown
# Page Title

## Learning Objectives (index pages only)
- Objective 1
- Objective 2
- ...

## Prerequisites (index pages only)
- Prerequisite 1
- Prerequisite 2

## Section Content
[Narrative text with proper headings]

### Subsection
[Detailed content]

## Code Examples
\`\`\`python
# Python code with comments explaining WHY
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Create publisher on /topic with QoS
        self.publisher_ = self.create_publisher(String, 'topic', 10)
\`\`\`

## Diagrams
**Figure 1: System Architecture**

[Detailed textual description of architecture diagram]
- Component A: Handles sensing (cameras, LiDAR)
- Component B: Processes perception pipeline
- Component C: Generates control commands
- Data flows from A → B → C with feedback loop

## Tables
| Sensor Type | Range | Accuracy | Use Cases |
|-------------|-------|----------|-----------|
| Camera      | Visual field | High (lighting dependent) | Object detection, scene understanding |
| LiDAR       | 1-100m | ±2cm | Distance measurement, 3D mapping |

## Admonitions
:::tip Best Practice
Always validate sensor data before feeding to control algorithms.
:::

:::warning Safety Consideration
Ensure emergency stop functionality before deploying on physical robots.
:::

:::note Version Info
This example uses ROS 2 Humble (Python 3.10+).
:::

## Summary (summary pages only)
Key takeaways:
- Takeaway 1
- Takeaway 2

## Review Questions (summary pages only)
1. Question testing conceptual understanding
2. Question testing application ability
3. ...
```

**Mathematical Notation**:
- Inline math: `$E = mc^2$`
- Block math:
```
$$
\mathbf{x}_{t+1} = \mathbf{A}\mathbf{x}_t + \mathbf{B}\mathbf{u}_t
$$
```

**Code Block Standards**:
- Always specify language: \`\`\`python, \`\`\`cpp, \`\`\`yaml, \`\`\`bash
- Include comments explaining WHY (not WHAT)
- Show imports and dependencies explicitly
- Provide context before code (what it demonstrates)
- Provide expected output after code (when relevant)

**Image/Diagram Rules**:
- Store in chapter-specific `assets/` directories
- Use relative paths: `./assets/diagram-name.png`
- Always provide alt text for accessibility
- Preferred: Detailed textual descriptions in addition to images (per constitution)
- Syntax: `![Alt text](./assets/image.png)`

#### 1.4 Content Template Creation

Create reusable templates:
- `specs/001-textbook-blueprint/templates/chapter-index.md`: Template for chapter overview pages
- `specs/001-textbook-blueprint/templates/section-content.md`: Template for section pages
- `specs/001-textbook-blueprint/templates/summary-page.md`: Template for chapter summary pages

### Outputs
- `specs/001-textbook-blueprint/design/chapter-outlines.md`: Detailed outlines for all 5 chapters
- `specs/001-textbook-blueprint/design/docusaurus-config.md`: Complete Docusaurus configuration specification
- `specs/001-textbook-blueprint/design/content-standards.md`: Markdown formatting rules, frontmatter spec, code standards
- `specs/001-textbook-blueprint/templates/`: Content templates

### Success Criteria
- All 5 chapters have detailed section-by-section outlines
- Docusaurus configuration fully specified (no ambiguity)
- Markdown standards documented with examples
- Content templates ready for reuse

---

## Phase 2: Chapter Writing Workflow

### Chapter Writing Order

**Sequential Order (recommended for pedagogical coherence)**:
1. Chapter 1: Physical AI Foundations (foundational concepts)
2. Chapter 2: ROS 2 & Robot Control (builds on Ch1 sensing/control concepts)
3. Chapter 3: Simulation (applies Ch1-2 to virtual environments)
4. Chapter 4: NVIDIA Isaac (advanced simulation building on Ch3)
5. Chapter 5: VLA & Humanoid Capstone (integrates all prior chapters)

**Rationale**: Sequential writing ensures concept dependencies are respected and allows for forward references to be planned intentionally.

**Alternative Parallel Order** (if multiple authors available):
- Track 1: Chapter 1 → Chapter 2
- Track 2: Chapter 3 → Chapter 4
- Track 3: Chapter 5 (requires Ch1-4 completion before starting)

### Content Creation Process (per chapter)

#### Step 1: Scaffold Chapter Structure
- Create chapter directory: `docs/chapter-0X/`
- Create all section markdown files from outline
- Add frontmatter to each file (id, title, sidebar_position)
- Create `assets/` subdirectory

#### Step 2: Extract Content from Sources
- Review source analysis from Phase 0
- Extract relevant content for this chapter
- Identify code examples to include
- Flag any gaps requiring clarification

#### Step 3: Write Chapter Index Page
- Learning objectives (3-5 items from spec)
- Prerequisites (reference earlier chapters if needed)
- Chapter overview (motivation and context)
- Section navigation links

#### Step 4: Write Core Content Sections
- Follow markdown formatting standards from Phase 1
- Include technical definitions on first use
- Add code examples with proper formatting
- Insert textual diagram descriptions
- Use tables for comparisons
- Add admonitions for tips/warnings/notes

#### Step 5: Write Practical Examples Section
- Minimum 5 substantial code examples per chapter (per FR-006)
- Include setup/installation instructions
- Show expected output
- Provide troubleshooting tips

#### Step 6: Write Advanced Topics Section
- Clearly labeled as "Advanced"
- Builds on core content
- References further reading

#### Step 7: Write Summary Page
- Key takeaways (5-7 bullet points)
- Review questions (5-10 items, beginner to advanced)
- References to related chapters

#### Step 8: Chapter Quality Check
- Validate all code syntax
- Check frontmatter consistency
- Verify all cross-references
- Ensure no hallucinated content (all traceable to sources)
- Test markdown rendering in Docusaurus

#### Step 9: User Review & Iteration
- Request user review of completed chapter
- Address feedback
- Make revisions

#### Step 10: Finalize Chapter
- Mark chapter as complete
- Commit to version control
- Update sidebar.js if needed
- Build and preview locally

### Parallel Activities (throughout writing)

**Code Validation**: Continuously test code examples for syntax correctness
**Link Management**: Track all cross-references between chapters
**Asset Organization**: Ensure all images/diagrams properly organized
**Glossary Updates**: Add new terms to `resources/glossary.md` as encountered

### Outputs (per chapter)
- Complete chapter directory under `docs/chapter-0X/`
- All section markdown files with content
- Code examples validated
- Chapter added to `sidebars.js`

### Success Criteria (per chapter)
- All mandatory sections present (FR-002)
- Minimum 5 code examples included (FR-006)
- Content traceable to source documentation (FR-021)
- Beginner to advanced progression clear (FR-003)
- All cross-references functional (FR-014)
- Learning objectives and review questions aligned (FR-026, FR-027)

---

## Phase 3: Docusaurus Setup & Configuration

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git repository initialized

### Setup Tasks

#### 3.1 Initialize Docusaurus Project
```bash
# Navigate to repository root
cd my-project

# Initialize Docusaurus (if not already done)
npx create-docusaurus@latest . classic --typescript=false

# Install dependencies
npm install

# Install additional plugins
npm install --save @docusaurus/plugin-ideal-image
npm install --save remark-math@3 rehype-katex@5
```

#### 3.2 Configure Docusaurus

**Edit `docusaurus.config.js`**:
```javascript
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'From Foundations to Deployment',
  url: 'https://[username].github.io',
  baseUrl: '/[repo-name]/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  organizationName: '[username]',
  projectName: '[repo-name]',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/[username]/[repo-name]/edit/main/',
          remarkPlugins: [require('remark-math')],
          rehypePlugins: [require('rehype-katex')],
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
      crossorigin: 'anonymous',
    },
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Course Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Textbook',
        },
        {
          href: 'https://github.com/[username]/[repo-name]',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Course.`,
    },
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
      additionalLanguages: ['python', 'cpp', 'bash', 'yaml'],
    },
  },
};

module.exports = config;
```

**Create/Edit `sidebars.js`**: (see Phase 1 design)

**Edit `src/css/custom.css`**: (optional custom styling)

#### 3.3 Create Introduction Page

**Create `docs/intro.md`**:
```markdown
---
id: intro
title: Welcome
sidebar_label: Introduction
sidebar_position: 1
slug: /
---

# Physical AI & Humanoid Robotics: From Foundations to Deployment

## A Comprehensive University Course on Building Intelligent Physical Systems

Welcome to the complete textbook on Physical AI and Humanoid Robotics...

[Course description, target audience, prerequisites from spec]

## Course Structure

This textbook consists of 5 chapters:

1. **Physical AI Foundations**: Embodiment, sensing, action
2. **ROS 2 & Robot Control**: Architecture and implementation
3. **Simulation**: Gazebo and Unity platforms
4. **NVIDIA Isaac**: GPU-accelerated robotics
5. **VLA & Humanoid Capstone**: Integration and deployment

## How to Use This Textbook

[Navigation guidance, prerequisites, exercises]
```

#### 3.4 Create Resource Pages

Create files under `docs/resources/`:
- `prerequisites.md`: Detailed prerequisite knowledge
- `software-setup.md`: Step-by-step installation instructions
- `hardware-requirements.md`: Detailed hardware specifications
- `glossary.md`: Technical terms and definitions

#### 3.5 Local Testing

```bash
# Start development server
npm run start

# Build production site
npm run build

# Serve built site locally
npm run serve
```

**Validation Checklist**:
- [ ] All pages render without errors
- [ ] Navigation works (prev/next, sidebar)
- [ ] Code syntax highlighting displays correctly
- [ ] Math equations render properly (KaTeX)
- [ ] Images load with correct paths
- [ ] Tables format correctly
- [ ] Admonitions display properly
- [ ] Mobile responsive design works
- [ ] No broken links (use broken link checker)

### Outputs
- Fully configured Docusaurus project
- All chapter content integrated
- Local build validated

### Success Criteria
- Docusaurus build completes without errors (SC-004)
- All 5 chapters navigable via sidebar (SC-005)
- Code highlighting functional (SC-008)
- Math rendering functional (SC-007)
- No broken links

---

## Phase 4: Version Control Workflow

### Git Repository Structure

**Branch Strategy**:
- `main`: Production-ready content (deployed to GitHub Pages)
- `001-textbook-blueprint`: Feature branch for initial development (current)
- `chapter/01-physical-ai`: Optional per-chapter development branches
- `chapter/02-ros2-control`: ...
- `chapter/03-simulation`: ...
- `chapter/04-nvidia-isaac`: ...
- `chapter/05-vla-humanoid`: ...

### Commit Workflow

#### Initial Setup
```bash
# Ensure on feature branch
git checkout 001-textbook-blueprint

# Add Docusaurus project files
git add docusaurus.config.js sidebars.js package.json package-lock.json
git add .gitignore README.md

# Commit project structure
git commit -m "Initialize Docusaurus project structure

- Configure Docusaurus v3.x with KaTeX for math rendering
- Set up sidebar navigation for 5 chapters
- Add Prism syntax highlighting for Python, C++, YAML, Bash

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Per-Chapter Commits
```bash
# After completing a chapter
git add docs/chapter-01/
git commit -m "Add Chapter 1: Physical AI Foundations

Complete chapter coverage:
- Embodiment and physical constraints
- Sensor modalities (cameras, LiDAR, IMUs, tactile)
- Actuators and control basics
- Perception-action loops
- 6 code examples with Python and C++
- Advanced topics: sensor fusion, real-time systems
- 8 review questions

Meets FR-001, FR-002, FR-006, FR-026, FR-027

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Quality Standards for Commits
- **Atomic commits**: One logical change per commit
- **Descriptive messages**: Explain WHAT and WHY
- **Reference requirements**: Cite FR-XXX or SC-XXX when applicable
- **Include co-author tag**: Maintain attribution per constitution

### Merge Strategy

After all chapters complete and validated:
```bash
# Ensure all changes committed
git status

# Switch to main branch
git checkout main

# Merge feature branch
git merge --no-ff 001-textbook-blueprint -m "Complete Physical AI & Humanoid Robotics textbook

Deliverables:
- 5 complete chapters with 40+ sections total
- 25+ validated code examples
- Full Docusaurus website configuration
- Zero hallucinated content (all sourced)
- Meets all 30 functional requirements (FR-001 to FR-030)
- Achieves all 15 success criteria (SC-001 to SC-015)

Ready for deployment to GitHub Pages.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push to remote
git push origin main
```

### .gitignore Configuration

```gitignore
# Dependencies
node_modules/
package-lock.json  # or keep if locking dependencies

# Docusaurus build output
build/
.docusaurus/
.cache-loader/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Temporary
*.tmp
*.temp
```

---

## Phase 5: Deployment Strategy

### Option A: GitHub Pages Deployment (Primary)

#### Prerequisites
- GitHub account
- Repository created: `github.com/[username]/[repo-name]`
- GitHub Pages enabled in repository settings

#### Deployment via GitHub Actions

**Create `.github/workflows/deploy.yml`**:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build Docusaurus site
        run: npm run build
        env:
          NODE_ENV: production

      - name: Upload build artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: build

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v3
```

#### Manual Deployment (alternative)

```bash
# On main branch
npm run build

# Deploy using gh-pages branch
npm install --save-dev gh-pages

# Add deploy script to package.json
{
  "scripts": {
    "deploy": "GIT_USER=[username] USE_SSH=true npm run deploy"
  }
}

# Deploy
npm run deploy
```

#### GitHub Pages Configuration
1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / root (if using gh-pages package)
4. Or: Source: GitHub Actions (if using workflow above)
5. Custom domain (optional): Configure DNS and add CNAME

**Result**: Site live at `https://[username].github.io/[repo-name]/`

---

### Option B: Vercel Deployment (Alternative)

#### Prerequisites
- Vercel account (free tier available)
- Vercel CLI installed: `npm install -g vercel`

#### Deployment Steps

**Via Vercel CLI**:
```bash
# Login to Vercel
vercel login

# Deploy from main branch
vercel --prod
```

**Via Vercel Git Integration**:
1. Connect GitHub repository to Vercel
2. Configure build settings:
   - **Framework Preset**: Docusaurus
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
3. Auto-deploy on push to `main` branch

**Environment Variables** (if needed):
- `NODE_VERSION`: 18

**Result**: Site live at auto-generated Vercel URL (e.g., `[repo-name].vercel.app`)

---

### Deployment Validation Checklist

After deployment to either platform:

- [ ] Homepage loads correctly at deployed URL
- [ ] All 5 chapters accessible via navigation
- [ ] Code syntax highlighting functional
- [ ] Math equations render properly (KaTeX)
- [ ] Images display correctly (check paths)
- [ ] Links between pages work (no 404s)
- [ ] Mobile responsive design works
- [ ] Page load performance <2s (test with Lighthouse)
- [ ] SEO metadata present (check page source)
- [ ] No console errors in browser developer tools

### Continuous Deployment Workflow

**For ongoing updates**:
1. Create feature branch for content updates: `git checkout -b update/chapter-01-fixes`
2. Make changes to markdown files
3. Test locally: `npm run start`
4. Commit changes with descriptive message
5. Push branch: `git push origin update/chapter-01-fixes`
6. Create Pull Request to `main`
7. Review changes (diff view)
8. Merge PR to `main`
9. GitHub Actions (or Vercel) automatically deploys updated content
10. Validate deployment at live URL

---

## Quality Gates

### Gate 1: Content Completeness (after each chapter)
- [ ] All sections from outline present
- [ ] Learning objectives stated (3-5 items)
- [ ] Prerequisites documented
- [ ] Minimum 5 code examples included
- [ ] Advanced topics section complete
- [ ] Summary with key takeaways
- [ ] Review questions (5-10 items)
- [ ] All content traceable to sources (no hallucination)

### Gate 2: Technical Validation (after all chapters)
- [ ] All code examples syntax-checked
- [ ] Version numbers specified for all tools
- [ ] Mathematical formulas validated
- [ ] Cross-references verified as working links
- [ ] Images/diagrams have alt text
- [ ] Tables properly formatted

### Gate 3: Docusaurus Build (before deployment)
- [ ] `npm run build` completes without errors
- [ ] No broken links detected
- [ ] All frontmatter valid
- [ ] Sidebar navigation complete
- [ ] Math rendering functional (KaTeX)
- [ ] Code highlighting works

### Gate 4: Constitutional Compliance (final check)
- [ ] Content Fidelity: Zero hallucination, all content sourced
- [ ] Academic Rigor: University-level standards maintained
- [ ] Structural Completeness: All 5 chapters complete
- [ ] Docusaurus Compatibility: Standard features only
- [ ] Pedagogical Structure: 10-part architecture followed
- [ ] Engineering Focus: No marketing language
- [ ] Multi-Modal Learning: Code, tables, diagrams, math, admonitions used

### Gate 5: Deployment Validation (post-deployment)
- [ ] Site accessible at deployment URL
- [ ] All navigation functional
- [ ] Performance acceptable (<2s page load)
- [ ] Mobile responsive
- [ ] No console errors

---

## Risk Assessment & Mitigation

### Risk 1: Incomplete Source Documentation
**Impact**: HIGH - Cannot create content without source material
**Probability**: MEDIUM
**Mitigation**:
- Phase 0 research identifies gaps early
- Flag gaps explicitly (no hallucination)
- Request additional source material from user
- Document assumptions clearly

### Risk 2: Code Example Syntax Errors
**Impact**: MEDIUM - Damages credibility and student trust
**Probability**: MEDIUM
**Mitigation**:
- Validate all code examples before inclusion
- Test in appropriate environments (Python, C++, ROS 2)
- Include version requirements explicitly
- Provide troubleshooting guidance

### Risk 3: Docusaurus Build Failures
**Impact**: HIGH - Cannot deploy without successful build
**Probability**: LOW
**Mitigation**:
- Test builds incrementally (after each chapter)
- Use `onBrokenLinks: 'throw'` to catch link errors early
- Validate frontmatter format consistency
- Keep Docusaurus dependencies updated

### Risk 4: Deployment Issues (GitHub Pages/Vercel)
**Impact**: MEDIUM - Delays going live
**Probability**: LOW
**Mitigation**:
- Test deployment to staging environment first
- Use GitHub Actions workflow for automated deployment
- Validate DNS/CNAME configuration if using custom domain
- Have alternative deployment option (Vercel) ready

### Risk 5: Content Drift from Spec Requirements
**Impact**: MEDIUM - Fails to meet functional requirements
**Probability**: MEDIUM
**Mitigation**:
- Reference spec (FR-XXX, SC-XXX) during writing
- Use quality gates after each chapter
- Maintain checklist of requirements
- User review after each chapter completion

### Risk 6: Version Changes in Referenced Tools
**Impact**: LOW - Content becomes outdated over time
**Probability**: HIGH (long-term)
**Mitigation**:
- Explicitly document versions used (FR-024)
- Add "last updated" dates to chapters
- Plan for periodic content review/updates
- Note known version compatibility issues

---

## Timeline & Milestones

**Estimated Timeline**: 8-12 weeks (assumes source documentation available)

### Milestone 1: Foundation Setup (Week 1-2)
- ✅ Specification complete (done)
- ✅ Planning complete (this document)
- Phase 0: Source analysis complete
- Phase 3: Docusaurus project initialized

### Milestone 2: First Chapter Complete (Week 3-4)
- Chapter 1 (Physical AI Foundations) written, reviewed, finalized
- Quality gates 1 & 2 passed for Chapter 1
- Local Docusaurus build validated

### Milestone 3: Core Chapters Complete (Week 5-8)
- Chapter 2 (ROS 2) complete
- Chapter 3 (Simulation) complete
- Chapter 4 (NVIDIA Isaac) complete
- Quality gates 1 & 2 passed for each chapter

### Milestone 4: Capstone Complete (Week 9-10)
- Chapter 5 (VLA & Humanoid Capstone) complete
- All cross-references between chapters validated
- Resource pages (prerequisites, setup, glossary) complete

### Milestone 5: Deployment Ready (Week 11)
- Quality gates 3 & 4 passed (build & constitution)
- GitHub Actions workflow configured
- Test deployment to staging environment

### Milestone 6: Production Launch (Week 12)
- Deployed to GitHub Pages (primary)
- Deployed to Vercel (alternative)
- Quality gate 5 passed (deployment validation)
- Announcement and documentation complete

**Note**: Timeline assumes:
- Comprehensive source documentation available upfront
- Single author working sequentially
- User review cycles 2-3 days per chapter
- No major rework required

**Parallel Track Option**: With multiple authors, Chapters 1-4 could be written concurrently (Weeks 3-8), reducing timeline to 8 weeks.

---

## Success Metrics

### Quantitative Metrics
- ✅ 5 chapters complete (SC-001)
- ✅ 25+ code examples across chapters (SC-002: 5 per chapter minimum)
- ✅ 100% content sourced from provided documentation (SC-003)
- ✅ Docusaurus build passes without errors (SC-004)
- ✅ 15-25 review questions per chapter (SC-006: 5-10 minimum)
- ✅ 3-5 learning objectives per chapter (SC-006)
- ✅ All FR-001 to FR-030 requirements met (30 total)
- ✅ All SC-001 to SC-015 success criteria achieved (15 total)

### Qualitative Metrics
- Content maintains university-level academic rigor
- Pedagogical progression (beginner → advanced) clear
- Engineering focus maintained (zero marketing language)
- Code examples production-quality (not toy demos)
- Technical accuracy verifiable against sources

### Deployment Metrics
- Page load time <2s (Lighthouse performance)
- Mobile responsiveness score >90 (Lighthouse)
- Accessibility score >90 (Lighthouse)
- Zero broken links
- Site uptime >99.9% (GitHub Pages/Vercel SLA)

---

## Appendices

### Appendix A: Docusaurus Version & Dependencies

**Recommended Versions**:
- Docusaurus: v3.5.2 or latest stable
- Node.js: v18.20.0 or v20.x (LTS)
- React: v18.3.1 (bundled with Docusaurus)
- remark-math: v3.0.1
- rehype-katex: v5.0.0

**package.json** (minimal):
```json
{
  "name": "physical-ai-robotics-textbook",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "docusaurus": "docusaurus",
    "start": "docusaurus start",
    "build": "docusaurus build",
    "swizzle": "docusaurus swizzle",
    "deploy": "docusaurus deploy",
    "clear": "docusaurus clear",
    "serve": "docusaurus serve",
    "write-translations": "docusaurus write-translations",
    "write-heading-ids": "docusaurus write-heading-ids"
  },
  "dependencies": {
    "@docusaurus/core": "^3.5.2",
    "@docusaurus/preset-classic": "^3.5.2",
    "@mdx-js/react": "^3.0.0",
    "clsx": "^2.1.1",
    "prism-react-renderer": "^2.3.1",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "rehype-katex": "^5.0.0",
    "remark-math": "^3.0.1"
  },
  "devDependencies": {
    "@docusaurus/module-type-aliases": "^3.5.2"
  },
  "browserslist": {
    "production": [
      ">0.5%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "engines": {
    "node": ">=18.0"
  }
}
```

### Appendix B: Frontmatter Reference

**Complete frontmatter fields** (all optional except `id` and `title`):
```yaml
---
id: unique-page-id                # Required: unique identifier
title: Full Page Title            # Required: display title
sidebar_label: Short Label        # Optional: shorter label for sidebar
sidebar_position: N               # Optional: order in sidebar (1, 2, 3...)
description: Page description     # Optional: SEO meta description
keywords: [keyword1, keyword2]    # Optional: SEO keywords
slug: /custom-url                 # Optional: custom URL path
hide_title: false                 # Optional: hide title in page
hide_table_of_contents: false     # Optional: hide TOC
---
```

### Appendix C: Markdown Cheat Sheet for Authors

**Headings**: `#` H1, `##` H2, `###` H3 (use H2 for main sections)
**Bold**: `**text**` or `__text__`
**Italic**: `*text*` or `_text_`
**Code inline**: `` `code` ``
**Code block**:
\`\`\`python
code here
\`\`\`

**Links**: `[text](url)` or `[text](./relative/path.md)`
**Images**: `![alt](./assets/image.png)`
**Lists**:
- Unordered: `- item` or `* item`
- Ordered: `1. item`

**Tables**:
```
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

**Admonitions**:
```
:::note
Content
:::

:::tip
Content
:::

:::warning
Content
:::

:::danger
Content
:::
```

**Math**:
- Inline: `$E = mc^2$`
- Block: `$$\int_0^1 x^2 dx$$`

---

## Next Steps

### Immediate Actions (before starting Phase 0)
1. ✅ User reviews and approves this plan
2. User provides source documentation covering all 5 chapters
3. Create `specs/001-textbook-blueprint/tasks.md` using `/sp.tasks` command (breaks plan into actionable tasks)

### Phase 0 Kickoff (once sources available)
1. Analyze source documentation
2. Create `research/source-analysis.md` and `research/code-inventory.md`
3. Flag any content gaps requiring clarification
4. Validate minimum 25 code examples available

### Development Sequence
1. Phase 0: Research (source analysis)
2. Phase 1: Design (detailed outlines, templates)
3. Phase 3: Docusaurus setup (initialize project)
4. Phase 2: Content writing (Chapters 1→2→3→4→5 sequentially)
5. Phase 4: Version control (commit strategy, final merge to main)
6. Phase 5: Deployment (GitHub Pages + Vercel)

---

**Plan Status**: ✅ **COMPLETE - Ready for Task Breakdown**

**Next Command**: `/sp.tasks` to create actionable task list from this plan
