---
title: "Configuration Guide"
description: "Configure GixyNG using a config file: set defaults for output, includes, selected checks, and variable drop-ins so scans are consistent across runs and environments."
---

# Configuration

You can run `gixy` entirely from CLI flags, but a configuration file may also be used to read a small set of global settings: output formatting, where to write reports, which checks to run, whether to process `include` directives, and where to look for custom variable drop-ins.

If you are looking for day-to-day CLI usage examples, see the [Usage Guide](https://gixy.io/usage).

## Where config files live

By default, `gixy` looks in these locations (first match wins):

- `/etc/gixy/gixy.cfg`
- `~/.config/gixy/gixy.conf`

You can also point to a specific file:

```bash
gixy --config ./gixy.conf
```

And if you want a starting point, you can generate a config file from your current command-line args:

```bash
gixy --write-config ./gixy.conf
```

## File format

The format is intentionally boring:

* `key = value`
* `#` starts a comment
* optional `[sections]` (mainly used for advanced settings)
* lists can be written as `[a, b, c]`

Most keys match the long CLI flags with the leading `--` removed. For example:

* CLI: `--disable-includes`
* Config: `disable-includes = true`

## Settings you can configure

These are the knobs you can set in the config file.

### format

Choose the output format:

```ini
format = console   # default, colored output
# format = text    # plain text (no ANSI)
# format = json    # machine-readable JSON
```

This matches `--format / -f`.

### output

Write results to a file instead of stdout:

```ini
output = ./gixy-report.json
```

This matches `--output / -o`.

If you set `output`, the file format still depends on `format` (text vs JSON), so it is common to set them together:

```ini
format = json
output = ./gixy-report.json
```

### tests

Run only a specific set of checks (allowlist):

```ini
tests = http_splitting,ssrf,version_disclosure
```

This matches `--tests`.

### skips

Skip specific checks (blocklist):

```ini
skips = low_keepalive_requests,worker_rlimit_nofile_vs_connections
```

This matches `--skips`.

If you set both `tests` and `skips`, think of it as: "run tests, then remove skips."

### disable-includes

By default, `gixy` follows `include` directives so it can analyze the full config tree. You can disable that behavior:

```ini
disable-includes = true
```

This matches `--disable-includes`.

This setting is mainly useful when you are scanning a config on a machine that does not have the full include layout available. If you scan a rendered `nginx -T` dump, you usually do not need to touch it.

### vars-dirs

Provide directories containing custom variable drop-ins:

```ini
vars-dirs = [./vars, /etc/gixy/vars]
```

This matches `--vars-dirs`.

If you do not know what this is, you probably do not need it. When you do, the dedicated guide is in [Custom Variables & Drop-Ins](https://gixy.io/variables-dropins).

## Minimal example

A tiny config that still pulls its weight:

```ini
# gixy.conf
format = json
output = ./gixy-report.json
skips = low_keepalive_requests
```

Run it like this:

```bash
gixy --config ./gixy.conf
```

## Plugin-specific flags

Most `gixy` settings are global and work well as shared defaults in a config file. Some plugins also expose their own flags (and those can be set via CLI or via the config file), but the details are specific to each check.

If you need to tune a specific plugin, start with its documentation:

- [add_header_redefinition](https://gixy.io/plugins/add_header_redefinition)
- [origins](https://gixy.io/plugins/origins)
- [regex_redos](https://gixy.io/plugins/regex_redos)

## Severity filtering

Severity filtering is CLI-only via `-l` repeats (`-l`, `-ll`, `-lll`). It is not read from the config file.
