# AGENTS.md

## Repository purpose

`hostof` is a single-purpose Python CLI that reports which service and region host a site while keeping edge, origin, and network attribution separate.
It runs once per invocation and has no daemon, plugin system, or background state.
Python 3.12 or later is supported, and the runtime uses only the standard library.

## Commands

```sh
python3 -m pytest
python3 -m pytest tests/test_hostof.py
python3 -m pytest tests/test_distribution.py
python3 -m py_compile hostof _hostof_runtime/*.py scripts/build.py tests/*.py
python3 scripts/build.py
./dist/hostof --help
(cd dist && shasum -a 256 -c hostof.sha256)
```

`pytest` is the only test dependency.
The command itself must remain free of third-party runtime dependencies.

## Architecture

- `hostof` is the executable source and owns argument parsing, resolution, probing, attribution, and reporting.
- `_hostof_runtime/` is private output support bundled into the release artifact.
- `tests/test_hostof.py` exercises behavior without network access.
- `tests/test_distribution.py` proves the release asset runs without the source tree and matches its checksum.
- `scripts/build.py` creates the deterministic executable `dist/hostof` and `dist/hostof.sha256`.
- `.github/workflows/pull-request.yml` validates tests, compilation, build, checksum, and the standalone smoke test.
- `.github/workflows/release.yml` publishes the executable and checksum for approved `v<major>.<minor>.<patch>` tags.

The source may remain modular, but a release has exactly one runtime artifact named `hostof`.
The installed artifact must not require this checkout or a sibling package.
`dist/` is generated and must not be edited or committed.

## Compatibility contract

Preserve unless a reviewed change explicitly says otherwise:

- Command name: `hostof`.
- Usage: `hostof [--json] [--doh] [--deep] target`.
- Exit codes: `0` success, `1` usage error, `2` unreachable target, `3` refused deep probe.
- Cache default: `~/.cache/hostof`, overridable with `HOSTOF_CACHE`.
- Authorization default: `~/.config/hostof/authorized.json`, overridable with `HOSTOF_AUTHORIZED`.
- Human and JSON output remain compatible with existing consumers.

Do not add `--version` as part of the extraction work.
Do not relocate or delete user cache or authorization state during installation, upgrades, rollback, or removal.

## Testing

Tests must not access real DNS, HTTP services, user configuration, or user cache paths.
Mock network boundaries and redirect cache, authorization, and home paths to temporary directories.
Every behavior change needs coverage at the public CLI or pure-function boundary.
Every build change must retain the isolated executable and checksum test.

The full test suite is required before a release.
If pytest cannot be installed locally, run compilation, build, checksum, and standalone smoke checks, then require CI to pass before publishing.

## Build and release rules

`scripts/build.py` is the only supported release builder.
Keep its file list explicit so unexpected files cannot enter the executable.
Build output must be deterministic for identical source content and must use executable mode `0755`.

A release tag uses `v<major>.<minor>.<patch>` and publishes `hostof` with `hostof.sha256`.
Do not reuse or move a published tag.
Do not publish a release unless tests, standalone execution, and checksum verification pass.

This repository owns application behavior, tests, documentation, and release artifacts.
