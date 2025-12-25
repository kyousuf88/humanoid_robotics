// module.exports = {
//   tutorialSidebar: [
//     'intro',
//     {
//       type: 'category',
//       label: 'Foundations',
//       items: [
//         'foundations/overview',
//         'foundations/what-is-physical-ai',
//         'foundations/history-of-humanoid-robotics',
//         'foundations/modern-robotics-stack',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Mechanics',
//       items: [
//         'mechanics/overview',
//         'mechanics/robot-anatomy',
//         'mechanics/actuators-and-motors',
//         'mechanics/materials-and-structures',
//         'mechanics/cad-design-basics',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Electronics',
//       items: [
//         'electronics/overview',
//         'electronics/sensors',
//         'electronics/motor-controllers',
//         'electronics/power-systems',
//         'electronics/wiring-and-pcb-basics',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'AI-Robot Brain',
//       items: [
//         'ai-brain/overview',
//         'ai-brain/motion-planning',
//         'ai-brain/reinforcement-learning',
//         'ai-brain/vision-and-perception',
//         'ai-brain/speech-and-language',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Capstone',
//       items: [
//         'capstone/overview',
//         'capstone/capstone-project',
//         'capstone/hardware-assembly',
//         'capstone/electronics-integration',
//         'capstone/ai-brain-integration',
//         'capstone/demo-and-testing',
//       ],
//     },
//   ],
// };


/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
module.exports = {
  tutorialSidebar: [
    'preface',
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      collapsible: true,
      collapsed: false,
      items: [
        'module-1/module-1-chapter-1',
        'module-1/module-1-chapter-2',
        'module-1/module-1-chapter-3',
        'module-1/module-1-chapter-4',
        'module-1/module-1-chapter-5',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      collapsible: true,
      collapsed: false,
      items: [
        'module-2/module-2-chapter-1',
        'module-2/module-2-chapter-2',
        'module-2/module-2-chapter-3',
        'module-2/module-2-chapter-4',
        'module-2/module-2-chapter-5',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      collapsible: true,
      collapsed: false,
      items: [
        'module-3/module-3-chapter-1',
        'module-3/module-3-chapter-2',
        'module-3/module-3-chapter-3',
        'module-3/module-3-chapter-4',
        'module-3/module-3-chapter-5',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      collapsible: true,
      collapsed: false,
      items: [
        'module-4/module-4-chapter-1',
        'module-4/module-4-chapter-2',
        'module-4/module-4-chapter-3',
        'module-4/module-4-chapter-4',
        'module-4/module-4-chapter-5',
      ],
    },
    'appendix',
  ],
};
