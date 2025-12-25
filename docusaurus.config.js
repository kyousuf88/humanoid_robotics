// @ts-check
// type-check enabled for this file
/*
/** @type {import('@docusaurus/types').Config} */
//const config = {
  //title: 'Physical AI & Humanoid Robotics',
  //tagline: 'An AI-Native Guide to Building Humanoid Robots',
  //url: 'https://your-docusaurus-site.com', // Replace with your site's URL
  //baseUrl: '/',
  //onBrokenLinks: 'throw',
  //onBrokenMarkdownLinks: 'warn',
  //favicon: 'img/favicon.ico',

  //organizationName: 'your-github-username-or-org', // Replace with your GitHub org/user name
  //projectName: 'humanoid_robotics', // Replace with your repo name
  //deploymentBranch: 'gh-pages',

  //i18n: {
    //defaultLocale: 'en',
    //locales: ['en'],
  //},

  //presets: [
    //[
      //'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      //({
        //docs: {
          //sidebarPath: require.resolve('./sidebar.js'),
          //editUrl:
            //'https://github.com/your-github-username-or-org/humanoid_robotics/tree/main/',
        //},
        //blog: {
          //showReadingTime: true,
          //editUrl:
            //'https://github.com/your-github-username-or-org/humanoid_robotics/tree/main/',
        //},
        //theme: {
        //  customCss: require.resolve('./src/css/custom.css'),
        //},
      //}),
    //],
  //],

  //themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    //({
      //image: 'img/docusaurus-social-card.jpg',
      //navbar: {
        //title: 'Physical AI & Humanoid Robotics',
        //logo: {
          //alt: 'Book Logo',
          //src: 'img/logo.svg',
        //},
        //items: [
          //{
            //type: 'docSidebar',
            //sidebarId: 'tutorialSidebar',
            //position: 'left',
            //label: 'Book',
          //},
          //{ to: '/blog', label: 'Blog', position: 'left' },
          //{
            //href: 'https://github.com/your-github-username-or-org/humanoid_robotics',
            //label: 'GitHub',
            //position: 'right',
          //},
        //],
      //},
      //footer: {
        //style: 'dark',
        //links: [
          //{
            //title: 'Docs',
            //items: [
              //{
                //label: 'Book',
               // to: '/docs/intro',
              //},
            //],
          //},
          //{
            //title: 'Community',
            //items: [
              //{ label: 'Stack Overflow', href: 'https://stackoverflow.com/questions/tagged/docusaurus' },
              //{ label: 'Discord', href: 'https://discordapp.com/invite/docusaurus' },
              //{ label: 'Twitter', href: 'https://twitter.com/docusaurus' },
            //],
          //},
          //{
            //title: 'More',
            //items: [
              //{ label: 'Blog', to: '/blog' },
              //{ label: 'GitHub', href: 'https://github.com/your-github-username-or-org/humanoid_robotics' },
            //],
          //},
        //],
        //copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
      //},
      //prism: {
        // No need to import themes manually, Docusaurus provides defaults
        //theme: undefined, 
        //darkTheme: undefined,
      //},
    //}),
//};

//module.exports = config;

// @ts-check
// type-check-enable

// ✅ NEW/FIXED CODE


//2nd
// const { themes } = require('prism-react-renderer');
// const lightCodeTheme = themes.vsLight;
// const darkCodeTheme = themes.vsDark;
// /** @type {import('@docusaurus/types').Config} */
// const config = {
//   title: 'Physical AI & Humanoid Robotics',
//   tagline: 'An AI-Native Guide to Building Humanoid Robots',
//   url: 'https://your-docusaurus-site.com',
//   baseUrl: '/',
//   onBrokenLinks: 'throw',
//   //onBrokenMarkdownLinks: 'warn', // can remove if you migrate to v4 style
//   favicon: 'img/favicon.ico',

//   organizationName: 'your-github-username-or-org',
//   projectName: 'humanoid_robotics',
//   deploymentBranch: 'gh-pages',

//   i18n: {
//     defaultLocale: 'en',
//     locales: ['en'],
//   },

//   presets: [
//     [
//       'classic',
//       /** @type {import('@docusaurus/preset-classic').Options} */
//       ({
//         docs: {
//           path: 'docs',               // folder for your docs
//           routeBasePath: 'docs',      // URL route
//           sidebarPath: require.resolve('./sidebar.js'),
//           editUrl: 'https://github.com/your-github-username-or-org/humanoid_robotics/tree/main/',
//         },
//         blog: {
//           showReadingTime: true,
//           editUrl: 'https://github.com/your-github-username-or-org/humanoid_robotics/tree/main/',
//         },
//        // ✅ CORRECT
// theme: {
//   customCss: './src/css/custom.css',
// },
//       }),
//     ],
//   ],

//   themeConfig:
//     /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
//     ({
//       image: 'img/docusaurus-social-card.jpg',
//       navbar: {
//         title: 'Physical AI & Humanoid Robotics',
//         logo: {
//           alt: 'Book Logo',
//           src: 'img/logo.svg',
//         },
//         items: [
//           { type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Book' },
//           { to: '/blog', label: 'Blog', position: 'left' },
//           {
//             href: 'https://github.com/your-github-username-or-org/humanoid_robotics',
//             label: 'GitHub',
//             position: 'right',
//           },
//         ],
//       },
//       footer: {
//         style: 'dark',
//         links: [
//           {
//             title: 'Docs',
//             items: [
//               { label: 'Book', to: '/docs/intro' }, // must point to existing doc
//             ],
//           },
//           {
//             title: 'Community',
//             items: [
//               { label: 'Stack Overflow', href: 'https://stackoverflow.com/questions/tagged/docusaurus' },
//               { label: 'Discord', href: 'https://discordapp.com/invite/docusaurus' },
//               { label: 'Twitter', href: 'https://twitter.com/docusaurus' },
//             ],
//           },
//           {
//             title: 'More',
//             items: [
//               { label: 'Blog', to: '/blog' },
//               { label: 'GitHub', href: 'https://github.com/your-github-username-or-org/humanoid_robotics' },
//             ],
//           },
//         ],
//         copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
//       },
//       prism: {
//         theme: lightCodeTheme,
//         darkTheme: darkCodeTheme,
//       },
//     }),
// };

// module.exports = config;
/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'AI Systems in the Physical World',
  url: 'https://kyousuf88.github.io', // Replace with your production domain
  baseUrl: '/humanoid_robotics/',
  favicon: 'img/favicon.ico',
  organizationName: 'kyousuf88',
  projectName: 'humanoid_robotics',
  trailingSlash: false, // Set to false for Vercel compatibility
  // deploymentBranch only needed for GitHub Pages deployment
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn', // Note: This will be moved in Docusaurus v4
  markdown: {
    mermaid: true,
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};

