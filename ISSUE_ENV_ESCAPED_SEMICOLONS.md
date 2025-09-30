# Issue Resolution: env Directive with Escaped Semicolons

## Issue Description

The issue reported that gixy 0.2.7 failed to parse nginx configurations containing `env` directives with escaped semicolons, such as:

```nginx
env LUA_PATH=\;\;\;/nix/store/7bn0dr50s3cg2pvcl2d6k3apbpgxj0fk-lua5.2-luasocket-3.1.0-1/share/lua/5.2/?.lua;
env LUA_CPATH=\;\;\;/nix/store/7bn0dr50s3cg2pvcl2d6k3apbpgxj0fk-lua5.2-luasocket-3.1.0-1/lib/lua/5.2/?.so;
```

The error was:
```
[nginx_parser] ERROR Failed to parse config "/etc/nginx/nginx.conf": char 7642 (line:157, col:16)
```

## Root Cause

The issue was related to the old pyparsing-based parser used in earlier versions of gixy. The parser had difficulty handling escaped semicolons in directive arguments because semicolons are normally used as statement terminators in nginx configuration syntax.

## Resolution

This issue has been **resolved** by the migration from pyparsing to crossplane for nginx configuration parsing. The crossplane parser correctly handles escaped semicolons according to nginx's parsing rules.

### Why Escaped Semicolons?

In nginx configuration, semicolons (`;`) are used as statement terminators. When you need a literal semicolon in a value (common in environment variables like LUA_PATH and LUA_CPATH), you must escape them with a backslash (`\;`).

Example:
- **Without escaping**: `env LUA_PATH=;;;/path` - Would be parsed incorrectly as the semicolons would terminate the statement
- **With escaping**: `env LUA_PATH=\;\;\;/path` - Correctly parsed with literal semicolons in the value

### Verification

The fix has been verified through:

1. **Unit Test**: Added `test_env_with_escaped_semicolons()` in `tests/parser/test_raw_parser.py` to ensure the parser correctly handles these directives.

2. **Integration Test**: Tested with a complete nginx configuration file containing env directives with escaped semicolons. The gixy CLI tool successfully parses the configuration without errors.

3. **Programmatic Test**: Verified that the NginxParser correctly extracts and preserves the escaped semicolons in the parsed directive arguments.

### Test Results

```bash
# Unit test passes
$ pytest tests/parser/test_raw_parser.py::test_env_with_escaped_semicolons -v
tests/parser/test_raw_parser.py::test_env_with_escaped_semicolons PASSED

# All 345 tests pass
$ pytest tests/ -v
======================== 345 passed in 0.47s ==============================

# CLI tool works correctly
$ gixy /tmp/test_env_nginx.conf
# No parsing errors - only configuration best practice warnings
```

## Technical Details

The crossplane library (version 0.5.8 or higher) is used for parsing nginx configurations. It natively understands nginx's escape sequence handling, including:
- Escaped quotes: `\"` and `\'`
- Escaped semicolons: `\;`
- Other nginx-specific escape sequences

The parsed value correctly preserves the escaped semicolons as `\;` in the internal representation, which matches nginx's behavior.

## Conclusion

**Status**: ✅ **RESOLVED**

The issue is resolved in the current version of gixy (0.2.7) after the migration to crossplane. Users can now safely use env directives with escaped semicolons without encountering parsing errors.

No code changes were required beyond adding a regression test to prevent this issue from occurring again in the future.
