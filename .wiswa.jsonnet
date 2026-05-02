local utils = import 'utils.libjsonnet';

{
  uses_user_defaults: true,
  package_manager: 'uv',
  project_name: 'bascom',
  description: 'Core library that my tools use.',
  keywords: ['library', 'logging', 'utilities'],
  want_main: false,
  version: '0.1.3',
  python_deps+: {
    main+: {
      colorlog: utils.latestPypiPackageVersionCaret('colorlog'),
    },
  },
  security_policy_supported_versions: { '0.1.x': ':white_check_mark:' },
}
