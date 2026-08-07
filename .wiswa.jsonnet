local utils = import 'utils.libjsonnet';

{
  uses_user_defaults: true,
  package_manager: 'uv',
  project_name: 'bascom',
  description: 'Core library that my tools use.',
  keywords: ['library', 'logging', 'utilities'],
  want_main: false,
  version: '0.2.0',
  python_deps+: {
    main+: {
      click: utils.latestPypiPackageVersionCaret('click'),
      colorlog: utils.latestPypiPackageVersionCaret('colorlog'),
    },
  },
  security_policy_supported_versions: { '0.2.x': ':white_check_mark:' },
}
