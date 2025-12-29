// @ts-check

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide to ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA Technologies',
  favicon: 'img/favicon.ico',

  // Set the production URL to your Vercel domain
  // IMPORTANT: Update this to your actual Vercel URL
  url: 'https://humanoid-robotics.vercel.app',

  // For Vercel deployment at root, baseUrl must be '/'
  baseUrl: '/',

  // Disable trailing slash to avoid routing issues
  trailingSlash: false,

  // GitHub Pages config (not used for Vercel, but keeping for reference)
  organizationName: 'kyousuf88',
  projectName: 'humanoid_robotics',

  // Ignore broken links during build (can change to 'throw' once all links are fixed)
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  onBrokenAnchors: 'warn',

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
          sidebarPath: './sidebars.js',
          // Update to your actual GitHub repo
          editUrl: 'https://github.com/kyousuf88/humanoid_robotics/tree/001-physical-ai-book/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card image
      image: 'img/docusaurus-social-card.jpg',

      navbar: {
        title: 'Physical AI Book',
        logo: {
          alt: 'Physical AI Logo',
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
            href: 'https://github.com/kyousuf88/humanoid_robotics',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },

      footer: {
        style: 'dark',
        links: [
          {
            title: 'Book Content',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Module 1: ROS 2',
                to: '/docs/module-1',
              },
              {
                label: 'Module 2: Digital Twins',
                to: '/docs/module-2',
              },
              {
                label: 'Module 3: AI Brain',
                to: '/docs/module-3',
              },
              {
                label: 'Module 4: VLA',
                to: '/docs/module-4',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Hardware Requirements',
                to: '/docs/appendix/hardware-requirements',
              },
              {
                label: 'Tools Setup',
                to: '/docs/appendix/tools-setup',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/kyousuf88/humanoid_robotics',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Built with Docusaurus.`,
      },

      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
      },
    }),
};

module.exports = config;
