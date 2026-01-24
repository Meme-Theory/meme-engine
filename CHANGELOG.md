# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-24

### Added
- Initial release of Python-based Ralph Loop plugin
- Cross-platform support (Windows, macOS, Linux)
- `stop-hook.py` - Python implementation of the Stop hook for self-referential loops
- `setup-ralph-loop.py` - Python setup script for loop initialization
- `/ralph-loop` command to start iterative development loops
- `/cancel-ralph` command to cancel active loops
- `/help` command for documentation
- Comprehensive README with usage examples and best practices

### Changed
- Replaced bash scripts with Python for native Windows compatibility
- No longer requires WSL, Git Bash, or Cygwin on Windows

### Fixed
- Windows compatibility issue ([#17257](https://github.com/anthropics/claude-code/issues/17257))
