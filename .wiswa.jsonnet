local utils = import 'utils.libjsonnet';

{
  project_name: 'bascom',
  description: 'Core library that my tools use.',
  keywords: ['library', 'logging', 'utilities'],
  want_main: false,
  version: '0.0.1',
  pyproject+: {
    tool+: {
      poetry+: {
        dependencies+: {
          colorlog: utils.latestPypiPackageVersionCaret('colorlog'),
        },
      },
    },
  },
  copilot+: {
    intro: 'Bascom is a core library that provides basic functionality such as logging configuration.',
  },
}
