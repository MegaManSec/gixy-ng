# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.14] - 2025-12-06

### Added
- **ReDoS detection rewrite**: Complete rewrite of `regex_redos` plugin using Python's built-in `sre_parse` module - no external dependencies required. Detects nested quantifiers (exponential O(2^n)), overlapping alternatives (polynomial O(n²)), and adjacent greedy quantifiers.
- **nginx 1.29.3 support**: `add_header_redefinition` plugin now respects `add_header_inherit on;` directive.
- **Integration testing**: Added comprehensive WordPress production config (~380 lines) as integration test to catch false positives.
- **Documentation**: Added missing `try_files_is_evil_too.md`, updated plugin list in index.md (now 25 plugins).
- **`if` block variable capture**: `if` blocks with regex conditions (`~`, `~*`) now properly expose capture groups as variables with correct boundary inheritance.

### Changed
- ReDoS plugin now covers `location`, `if`, `rewrite`, `server_name`, and `map` directives.
- Documentation updated for `add_header_redefinition` with nginx 1.29.3+ solution.
- Expanded regex_redos.md with detailed vulnerability patterns and examples.

### Fixed
- Code quality improvements: explicit `autoescape=False` for Jinja2 (plain text output), noqa comments for intentional test patterns and random module usage.
- Legacy code cleanup in regexp.py: replaced alternation with character class, merged string concatenation, improved comments.

## [0.2.13] - 2025-12-06

### Added
- **Rich console formatter**: New beautiful terminal output with colors, panels, and progress indicators using the [Rich](https://github.com/Textualize/rich) library. Automatically enabled in TTY when `rich` is installed. Install with `pip install gixy-ng[rich]`.
- **Line numbers in output**: Issues now display the line number and file path where they were detected.
- **Security score**: The rich console formatter shows a security score (0-100) based on issue severity.
- Directives now track `line` and `file` attributes for better error reporting.
- New CLI tests for plugin options, boolean flag parsing, and module invocation.
- Formatter tests for the new rich console output.

### Changed
- Parser refactored: `parse()` method is now an alias for `parse_string()` for backward compatibility.
- Parser internals cleaned up with new `_build_tree_from_parsed()` method that handles both file and dump parsing uniformly.
- Line number propagation through the parser pipeline for accurate issue location reporting.

### Fixed
- README.md now lists all available plugins including `default_server_flag`, `hash_without_default`, and `return_bypasses_allow_deny`.
- Rich console formatter tests now skip gracefully when `rich` library is not installed.
- CLI default formatter selection now correctly checks if `rich_console` is actually registered (all rich submodules available), preventing argparse failures with partial rich installations.
- Lua blocks (`content_by_lua_block`, etc.) now include line number information for accurate issue location reporting.
- Fixed `TypeError: argument of type 'NoneType' is not iterable` in `add_header_multiline` plugin when header value is None ([#35](https://github.com/dvershinin/gixy/issues/35)).

### Dependencies
- Added optional `rich>=13.0.0` dependency for enhanced terminal output.

## [0.2.12] and earlier

See [GitHub Releases](https://github.com/dvershinin/gixy/releases) for previous changelog entries.

