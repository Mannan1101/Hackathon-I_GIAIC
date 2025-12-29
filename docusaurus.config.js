// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
    title: 'Physical AI & Humanoid Robotics',
    tagline: 'From Foundations to Deployment - A Comprehensive University Course',
    favicon: 'img/favicon.ico',

    // Set the production url of your site here
    url: 'https://hackathon-1-giaic-omega.vercel.app/',
    // Set the /<baseUrl>/ pathname under which your site is served
    // For GitHub pages deployment, it is often '/<projectName>/'
    baseUrl: '/',

    // GitHub pages deployment config.
    // If you aren't using GitHub pages, you don't need these.
    organizationName: 'your-org', // Usually your GitHub org/user name.
    projectName: 'physical-ai-textbook', // Usually your repo name.

    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',

    // Even if you don't use internationalization, you can use this field to set
    // useful metadata like html lang. For example, if your site is Chinese, you
    // may want to replace "en" with "zh-Hans".
    i18n: {
        defaultLocale: 'en',
        locales: ['en'],
    },

    presets: [
        [
            'classic',
            /** @type {import('@docusaurus/preset-classic').Options} */
            ({
                docs: {
                    routeBasePath: '/',
                    sidebarPath: './sidebars.js',
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    remarkPlugins: [require('remark-math')],
                    rehypePlugins: [require('rehype-katex')],
                },
                blog: false,
                theme: {
                    customCss: './src/css/custom.css',
                },
            }),
        ],
    ],



    // Client modules to inject chatbot on all pages
    clientModules: [
        require.resolve('./src/clientModules/chatbot.js'),
    ],


    stylesheets: [
        {
            href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
            type: 'text/css',
            integrity:
                'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
            crossorigin: 'anonymous',
        },
    ],

    themeConfig:
        /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
        ({
            // Replace with your project's social card
            image: 'img/docusaurus-social-card.jpg',
            navbar: {
                title: 'Physical AI & Humanoid Robotics',
                //logo: {
                //  alt: 'Course Logo',
                //src: 'img/logo.svg',
                //},
                items: [
                    {
                        type: 'docSidebar',
                        sidebarId: 'tutorialSidebar',
                        position: 'left',
                        label: 'Textbook',
                    },
                    {
                        href: 'https://github.com/',
                        label: 'GitHub',
                        position: 'right',
                    },
                ],
            },
            footer: {
                style: 'dark',
                links: [
                    {
                        title: 'Chapters',
                        items: [
                            {
                                label: 'Ch 1: Physical AI Foundations',
                                to: '/chapter-01',
                            },
                            {
                                label: 'Ch 2: ROS 2 & Robot Control',
                                to: '/chapter-02',
                            },
                            {
                                label: 'Ch 3: Simulation',
                                to: '/chapter-03',
                            },
                            {
                                label: 'Ch 4: Isaac & Perception',
                                to: '/chapter-04',
                            },
                            {
                                label: 'Ch 5: VLA & Capstone',
                                to: '/chapter-05',
                            },
                        ],
                    },
                    {
                        title: 'Resources',
                        items: [
                            {
                                label: 'Prerequisites',
                                to: '/resources/prerequisites',
                            },
                            {
                                label: 'Software Setup',
                                to: '/resources/software-setup',
                            },
                            {
                                label: 'Hardware Requirements',
                                to: '/resources/hardware-requirements',
                            },
                        ],
                    },
                    {
                        title: 'More',
                        items: [
                            {
                                label: 'GitHub',
                                href: 'https://github.com/your-org/physical-ai-textbook',
                            },
                        ],
                    },
                ],
                copyright: `Copyright � ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
            },
            prism: {
                theme: prismThemes.github,
                darkTheme: prismThemes.dracula,
                additionalLanguages: ['bash', 'python', 'cpp', 'c', 'cmake', 'yaml', 'json'],
            },
        }),
};

export default config;
