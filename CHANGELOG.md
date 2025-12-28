<!-- markdownlint-configure-file {"MD024": { "siblings_only": true } } -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2025-12-27

### Fixed

- Fix calling ColoredFormatter with custom arguments.

## [0.1.1] - 2025-12-27

### Added

- `log_colors` argument to `setup_logging` to allow overriding the colours.

### Changed

- INFO level now logs with light white text (escape code 97).
- CRITICAL level now logs with bold light red text (escape code 91 + 1).

It is expected that the most popular terminals have no problems displaying these colours. If there
are issues, set environment variable `NO_COLOR=1`.

## [0.1.0] - 2025-11-24

### Added

- GitHub workflow for publishing to PyPI with OIDC and uploading wheels to releases.

### Changed

- Switch to simpler log format by default; debug mode enables detailed format.
- The environment variable `BASCOM_CONSOLE_FORMATTER` may be used to control the `console`
  formatter.

## [0.0.4] - 2025-11-08

This release is solely for testing the publishing workflow.

## [0.0.3] - 2025-10-09

### Changed

- Bump Python constraint.

## [0.0.2] - 2025-09-30

### Changed

- Improve typing of `setup_logging()`.

## [0.0.1] - 2025-08-27

First version.

[unreleased]: https://github.com/Tatsh/bascom/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/Tatsh/bascom/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/Tatsh/bascom/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Tatsh/bascom/compare/v0.0.4...v0.1.0
[0.0.4]: https://github.com/Tatsh/bascom/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/Tatsh/bascom/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/Tatsh/deltona/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/Tatsh/bascom/releases/tag/v0.0.1
