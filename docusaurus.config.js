// @ts-check
// `@type` JSDoc annotations allow IDEs and type checkers to autocomplete and validate types

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline:
    'A Comprehensive Guide to ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA Technologies',
  favicon: 'img/favicon.ico',

  // Production URL
  url: 'https://your-docusaurus-site.example.com',
  baseUrl: '/',

  // GitHub Pages deployment
  organizationName: 'your-github-username',
  projectName: 'Humanoid-Robotics',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/your-github-username/humanoid-robotics',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/physical-ai-humanoid-robotics.svg',

      navbar: {
        title: 'Physical AI Book',
        logo: {
          alt: 'Physical AI & Humanoid Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Modules',
          },
          {
            href: 'https://github.com/your-github-username/humanoid-robotics',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },

      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {
                label: 'Module 1: ROS 2',
                to: '/docs/modules/module1-ros2/chapter1-introduction',
              },
              {
                label: 'Module 2: Digital Twins',
                to: '/docs/modules/module2-digital-twin/chapter1-digital-twins',
              },
              {
                label: 'Module 3: AI Brain',
                to: '/docs/modules/module3-ai-brain/chapter1-isaac-ecosystem',
              },
              {
                label: 'Module 4: VLA',
                to: '/docs/modules/module4-vla/chapter1-vla-introduction',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discord',
                href: 'https://discord.gg/',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href:
                  'https://github.com/your-github-username/humanoid-robotics',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Built with Docusaurus.`,
      },

      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.nightOwl,
      },
    }),
};

module.exports = config;