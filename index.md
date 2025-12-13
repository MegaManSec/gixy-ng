# Gixy-ng: NGINX Security Scanner & Configuration Checker for Security Audits

## Overview

Gixy-ng is an open source NGINX security scanner and configuration checker. It statically analyzes your NGINX configuration for security issues and misconfigurations before they reach production. Use Gixy-ng to run an automated NGINX configuration security audit and harden your nginx.conf against SSRF, HTTP response splitting, host header spoofing, version disclosure, and other vulnerabilities, as well as misconfigurations which lead to degraded performance and slow nginx servers.

The main goal of Gixy-ng is to automate NGINX configuration security checks and prevent misconfiguration.

### What is Gixy?

Gixy is a popular NGINX configuration analyzer originally developed by Yandex. Gixy-ng is a maintained fork of Gixy that adds new checks, performance improvements, and support for modern Python and NGINX versions. If you are looking for an NGINX config scanner that is actively maintained, use Gixy-ng.

## What it can do

Gixy-ng can can find various nginx configuration security issues, as well as nginx configuration performance issues, based on your `nginx.conf` and other nginx configuration files. The following plugins are supported to detect these misconfigurations

- [[add_header_content_type] Setting Content-Type via add_header](https://gixy.io/plugins/add_header_content_type/index.md)
- [[add_header_multiline] Multiline response headers](https://gixy.io/plugins/add_header_multiline/index.md)
- [[add_header_redefinition] Redefining of response headers by "add_header" directive](https://gixy.io/plugins/add_header_redefinition/index.md)
- [[alias_traversal] Path traversal via misconfigured alias](https://gixy.io/plugins/alias_traversal/index.md)
- [[allow_without_deny] Allow specified without deny](https://gixy.io/plugins/allow_without_deny/index.md)
- [[default_server_flag] Missing default_server flag](https://gixy.io/plugins/default_server_flag/index.md)
- [[error_log_off] `error_log` set to `off`](https://gixy.io/plugins/error_log_off/index.md)
- [[hash_without_default] Missing default in hash blocks](https://gixy.io/plugins/hash_without_default/index.md)
- [[host_spoofing] Request's Host header forgery](https://gixy.io/plugins/host_spoofing/index.md)
- [[http_splitting] HTTP Response Splitting](https://gixy.io/plugins/http_splitting/index.md)
- [[if_is_evil] If is evil when used in location context](https://gixy.io/plugins/if_is_evil/index.md)
- [[invalid_regex] Invalid regex capture groups](https://gixy.io/plugins/invalid_regex/index.md)
- [[low_keepalive_requests] Low `keepalive_requests`](https://gixy.io/plugins/low_keepalive_requests/index.md)
- [[origins] Problems with referer/origin header validation](https://gixy.io/plugins/origins/index.md)
- [[proxy_pass_normalized] `proxy_pass` path normalization issues](https://gixy.io/plugins/proxy_pass_normalized/index.md)
- [[regex_redos] Regular expression denial of service (ReDoS)](https://gixy.io/plugins/regex_redos/index.md)
- [[resolver_external] Using external DNS nameservers](https://gixy.io/plugins/resolver_external/index.md)
- [[return_bypasses_allow_deny] Return directive bypasses allow/deny restrictions](https://gixy.io/plugins/return_bypasses_allow_deny/index.md)
- [[ssrf] Server Side Request Forgery](https://gixy.io/plugins/ssrf/index.md)
- [[try_files_is_evil_too] `try_files` directive is evil without open_file_cache](https://gixy.io/plugins/try_files_is_evil_too/index.md)
- [[unanchored_regex] Unanchored regular expressions](https://gixy.io/plugins/unanchored_regex/index.md)
- [[valid_referers] none in valid_referers](https://gixy.io/plugins/valid_referers/index.md)
- [[version_disclosure] Using insecure values for server_tokens](https://gixy.io/plugins/version_disclosure/index.md)
- [[worker_rlimit_nofile_vs_connections] `worker_rlimit_nofile` must be at least twice `worker_connections`](https://gixy.io/plugins/worker_rlimit_nofile_vs_connections/index.md)

Something not detected? Please open an [issues labeled with "new plugin"](https://github.com/megamansec/gixy-ng/issues?q=is%3Aissue+is%3Aopen+label%3A%22new+plugin%22).

## Installation

### CentOS/RHEL and other RPM-based systems

```
yum -y install https://extras.getpagespeed.com/release-latest.rpm
yum -y install gixy
```

#### Other systems

Gixy is distributed on [PyPI](https://pypi.python.org/pypi/gixy-ng). The best way to install it is with pip:

```
pip install gixy-ng
```

## Usage

By default, Gixy-ng (the `gixy` CLI) will try to analyze your NGINX configuration placed in `/etc/nginx/nginx.conf`.

But you can always specify the needed path:

```
$ gixy /etc/nginx/nginx.conf

==================== Results ===================

Problem: [http_splitting] Possible HTTP-Splitting vulnerability.
Description: Using variables that can contain "\n" may lead to http injection.
Additional info: https://gixy.io/plugins/http_splitting/
Reason: At least variable "$action" can contain "\n"
Pseudo config:
include /etc/nginx/sites/default.conf;

    server {

        location ~ /v1/((?<action>[^.]*)\.json)?$ {
            add_header X-Action $action;
        }
    }


==================== Summary ===================
Total issues:
    Unspecified: 0
    Low: 0
    Medium: 0
    High: 1
```

Or skip some tests:

```
$ gixy --skips http_splitting /etc/nginx/nginx.conf

==================== Results ===================
No issues found.

==================== Summary ===================
Total issues:
    Unspecified: 0
    Low: 0
    Medium: 0
    High: 0
```

Or something else, you can find all other `gixy` arguments with the help command: `gixy --help`

#### Plugin options

Some plugins expose options which you can set via CLI flags or config file. CLI flags follow the pattern `--<PluginName>-<option>` with dashes, while config file uses `[PluginName]` sections with dashed keys.

- `origins`:
- `--origins-domains domains`: Comma-separated list of trusted registrable domains. Use `*` to disable third‑party checks. Example: `--origins-domains example.com,foo.bar`. Default: `*`.
- `--origins-https-only true|false`: When true, only the `https` scheme is considered valid for `Origin`/`Referer`. Default: `false`.
- `--origins-lower-hostname true|false`: Normalize hostnames to lowercase before validation. Default: `true`.
- `add_header_redefinition`:
- `--add-header-redefinition-headers headers`: Comma-separated allowlist of header names (case-insensitive). When set, only dropped headers from this list will be reported; when unset, all dropped headers are reported. Example: `--add-header-redefinition-headers x-frame-options,content-security-policy`. Default: unset (report all).

Examples (config file):

```
[origins]
domains = example.com, example.org
https-only = true

[add_header_redefinition]
headers = x-frame-options, content-security-policy
```

You can also make `gixy` use pipes (stdin), like so:

```
echo "resolver 1.1.1.1;" | gixy -
```

### Docker usage

Gixy-ng is available as a Docker image [from the Docker hub](https://hub.docker.com/r/getpagespeed/gixy/). To use it, mount the configuration that you want to analyse as a volume and provide the path to the configuration file when running the Gixy-ng image.

```
$ docker run --rm -v `pwd`/nginx.conf:/etc/nginx/conf/nginx.conf getpagespeed/gixy /etc/nginx/conf/nginx.conf
```

If you have an image that already contains your nginx configuration, you can share the configuration with the Gixy-ng container as a volume.

```
$  docker run --rm --name nginx -d -v /etc/nginx
nginx:alpinef68f2833e986ae69c0a5375f9980dc7a70684a6c233a9535c2a837189f14e905

$  docker run --rm --volumes-from nginx megamansec/gixy-ng /etc/nginx/nginx.conf

==================== Results ===================
No issues found.

==================== Summary ===================
Total issues:
    Unspecified: 0
    Low: 0
    Medium: 0
    High: 0
```

### Kubernetes usage

Given you are using the official NGINX ingress controller, not the kubernetes one, you can use this <https://github.com/nginx/kubernetes-ingress>

```
kubectl exec -it my-release-nginx-ingress-controller-54d96cb5cd-pvhx5 -- /bin/bash -c "cat /etc/nginx/conf.d/*" | docker run -i getpagespeed/gixy -
```

```
==================== Results ===================

>> Problem: [version_disclosure] Do not enable server_tokens on or server_tokens build
Severity: HIGH
Description: Using server_tokens on; or server_tokens build;  allows an attacker to learn the version of NGINX you are running, which can be used to exploit known vulnerabilities.
Additional info: https://gixy.io/plugins/version_disclosure/
Reason: Using server_tokens value which promotes information disclosure
Pseudo config:

server {
    server_name XXXXX.dev;
    server_tokens on;
}

server {
    server_name XXXXX.dev;
    server_tokens on;
}

server {
    server_name XXXXX.dev;
    server_tokens on;
}

server {
    server_name XXXXX.dev;
    server_tokens on;
}

==================== Summary ===================
Total issues:
    Unspecified: 0
    Low: 0
    Medium: 0
    High: 4
```

## Why Gixy-ng is Essential for NGINX Security and Compliance

Unlike running `nginx -t`, which only checks syntax, Gixy-ng analyzes your configuration for security. With Gixy-ng, you can perform an automated NGINX configuration security review that can run locally or in CI/CD on every change.

Currently supported Python versions are 3.6 through 3.13.

Disclaimer: Gixy-ng is well tested only on GNU/Linux, other OSs may have some issues.

## Contributing

Contributions to Gixy-ng are always welcome! You can help us in different ways:

- Open an issue with suggestions for improvements and errors you're facing in the [GitHub repository](https://github.com/MegaManSec/gixy-ng);
- Fork this repository and submit a pull request;
- Improve the documentation.

Code guidelines:

- Python code style should follow [pep8](https://www.python.org/dev/peps/pep-0008/) standards whenever possible;
- Pull requests with new plugins must have unit tests for them.
