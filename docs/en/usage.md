---
title: "Usage Guide"
description: "How to run GixyNG locally or in CI, scan rendered configs, filter findings, and produce reports in text or JSON."
---

# Usage

GixyNG ships as the `gixy` CLI. It statically analyzes NGINX configuration (your `nginx.conf` plus any files it includes) and reports security and hardening issues, along with a few common performance footguns.

## Basic scan

If you have a standard NGINX install, this is usually enough:

```bash
gixy
```

If you want to point it at a specific config file:

```bash
# Scan a specific nginx.conf
gixy /etc/nginx/nginx.conf

# Or something custom
gixy /opt/nginx/nginx.conf
```

## Scan a rendered config dump

One of the easiest ways to get consistent results from `gixy` is to scan the fully rendered configuration that NGINX sees. NGINX can print that with `nginx -T`.

On the machine that has NGINX (or inside your NGINX container):

```bash
# Dump the full rendered NGINX config to a single file
nginx -T > nginx-dump.conf
```

Then you can copy `nginx-dump.conf` anywhere and scan it there:

```bash
gixy ./nginx-dump.conf
```

This workflow is especially handy when:

* Your NGINX config is spread across many `include` files
* You want your CI pipeline to scan exactly what NGINX is loading
* You are auditing production config without giving the scanner direct filesystem access

## Severity filtering

By default, `gixy` reports everything it finds. If you only care about higher-severity issues, use `-l` repeats:

```bash
# LOW and above
gixy -l

# MEDIUM and above
gixy -ll

# HIGH only
gixy -lll
```

## Choose which checks run

You can run a focused subset of checks with `--tests`:

```bash
# Only run these checks
gixy --tests http_splitting,ssrf,version_disclosure
```

Or skip a few noisy checks with `--skips`:

```bash
# Run everything except these checks
gixy --skips low_keepalive_requests,worker_rlimit_nofile_vs_connections
```

## Output formats

`gixy` can print to the console for humans or emit clean output for tooling:


```bash
# Console (default): colored outputs, readable sections.
gixy -f console

# Plaintext: readable sections without ANSI color codes.
gixy -f text

# JSON: Reproducible JSON, best for CI and post-processing.
gixy -f json
```

## Write reports to a file

To save the report instead of printing it:

```bash
# Write plain text output to a file
gixy -f text -o gixy-report.txt

# Write JSON output to a file
gixy -f json -o gixy-report.json
```

## Debug mode

If something looks off (missing includes, weird parsing, unexpected results), debug mode is your friend:

```bash
gixy --debug
```

## Include processing

By default, `gixy` processes `include` directives so it can analyze the full config tree. If you want to treat the input file as standalone, you can disable include processing:

```bash
gixy --disable-includes /path/to/nginx.conf
```

When scanning a rendered `nginx -T` dump, leaving includes enabled is usually fine, but disabling them can fix any odd edge cases such as when an include file could not be found on the system the dump was performed on.

## Custom variable drop-ins

If you ever see warnings about unknown variables, you may wish to specify them manually. You can point `gixy` to a directory containing files which define additional variables:

```bash
gixy --vars-dirs ./vars,/etc/gixy/vars
```

More information about the expected files in these directories can be found in [Custom Variables & Drop-Ins](https://gixy.io/variables-dropins).

## Using a config file

If you do not want to pass the same flags every time you run `gixy`, you can load options from a config file:

```bash
gixy --config ./gixy.conf
```

You can also generate a config file from your current CLI arguments:

```bash
gixy --write-config ./gixy.conf
```

Full details (including plugin-specific settings) found in the [Configuration Guide](https://gixy.io/configuration).
