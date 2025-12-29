/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Course Home',
    },
    {
      type: 'category',
      label: 'Chapter 1: Physical AI Foundations',
      collapsible: true,
      collapsed: false,
      items: [
        'chapter-01',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: ROS 2 & Robot Control',
      collapsible: true,
      collapsed: true,
      items: [
        'chapter-02',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: Simulation & Digital Twins',
      collapsible: true,
      collapsed: true,
      items: [
        'chapter-03',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4: Isaac & Perception',
      collapsible: true,
      collapsed: true,
      items: [
        'chapter-04',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5: VLA & Humanoid Capstone',
      collapsible: true,
      collapsed: true,
      items: [
        'chapter-05',
      ],
    },
  ],
};

export default sidebars;
