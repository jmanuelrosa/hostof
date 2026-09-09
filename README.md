# hostof

`hostof` reports which service and region host a site while keeping edge, origin, and network attribution separate.
It reads public DNS, TLS, HTTP, and linked asset data, and uses only the Python standard library at runtime.

## Install

Download `hostof` and `hostof.sha256` from a release, verify the checksum, then put the executable on your `PATH`:

```sh
shasum -a 256 -c hostof.sha256
chmod +x hostof
mv hostof ~/.local/bin/
```

Python 3.12 or later is supported.
`dig` is used when available; DNS-over-HTTPS is the fallback.

## Usage

```text
hostof [--json] [--doh] [--deep] target
```

`target` may be a hostname or URL.
Use `--json` for machine-readable output and `--doh` to resolve with DNS-over-HTTPS instead of the system resolver.

`--deep` requests a small fixed set of conventional paths and is refused unless the hostname has a current authorization entry in `~/.config/hostof/authorized.json`:

```json
{
  "hosts": [
    {
      "host": "example.com",
      "basis": "own-infra",
      "expires": "2030-01-01"
    }
  ]
}
```

Exit codes are `0` for success, `1` for usage errors, `2` when the target is unreachable, and `3` when a deep probe is refused.

## State

Provider prefix data is cached in `~/.cache/hostof`.
Override the cache directory with `HOSTOF_CACHE` and the authorization file with `HOSTOF_AUTHORIZED`.

## Development

The test dependency is pytest; the command itself remains stdlib-only.

```sh
python3 -m pip install pytest
python3 -m pytest
python3 scripts/build.py
./dist/hostof --help
```

The build is a deterministic, uncompressed Python zip application containing the command, its private runtime helpers, and the license.
It produces the standalone executable `dist/hostof` and `dist/hostof.sha256`.

## Release

1. Run `python3 -m pytest`.
2. Run `python3 scripts/build.py` and smoke-test `dist/hostof` outside the source tree.
3. Verify `dist/hostof.sha256` and review the release changes.
4. After approval, create and push a `v<major>.<minor>.<patch>` tag.

The release workflow repeats the tests and build, validates the tag, and publishes `hostof` with its checksum to the corresponding GitHub Release.
Do not reuse or move a published release tag.

## License

[MIT](LICENSE) Copyright (c) 2022 José Manuel Rosa Moncayo.
