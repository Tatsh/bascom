(import 'defaults.libjsonnet') + {
  // Shared
  github_username: 'Tatsh',
  social+: {
    mastodon+: { id: '109370961877277568' },
  },
  // Project-specific
  project_name: 'bascom',
  description: 'Core library that my tools use.',
  keywords: ['library', 'logging', 'utilities'],
  want_main: false,
  version: '0.0.1',
  pyproject+: {
    tool+: {
      poetry+: {
        dependencies+: {
          colorlog: '^6.9.0',
        },
      },
    },
  },
  copilot: {
    intro: 'Bascom is a core library that provides basic functionality such as logging configuration.',
  },
  // Common
  authors: [
    {
      'family-names': 'Udvare',
      'given-names': 'Andrew',
      email: 'audvare@gmail.com',
      name: '%s %s' % [self['given-names'], self['family-names']],
    },
  ],
  github+: {
    funding+: {
      ko_fi: 'tatsh2',
      liberapay: 'tatsh2',
      patreon: 'tatsh2',
    },
  },
}
