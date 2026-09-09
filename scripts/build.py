#!/usr/bin/env python3
"""Build the standalone hostof zip application and its SHA-256 checksum."""

import hashlib
import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ASSET = DIST / "hostof"
CHECKSUM = DIST / "hostof.sha256"
SHEBANG = b"#!/usr/bin/env python3\n"
TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FILES = (
    (ROOT / "hostof", "__main__.py"),
    (ROOT / "_hostof_runtime" / "__init__.py", "_hostof_runtime/__init__.py"),
    (ROOT / "_hostof_runtime" / "colors.py", "_hostof_runtime/colors.py"),
    (ROOT / "_hostof_runtime" / "ui.py", "_hostof_runtime/ui.py"),
    (ROOT / "LICENSE", "LICENSE"),
)


def build():
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as output:
        for source, destination in FILES:
            entry = zipfile.ZipInfo(destination, TIMESTAMP)
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            output.writestr(entry, source.read_bytes())

    DIST.mkdir(exist_ok=True)
    ASSET.write_bytes(SHEBANG + archive.getvalue())
    ASSET.chmod(0o755)
    digest = hashlib.sha256(ASSET.read_bytes()).hexdigest()
    CHECKSUM.write_text(f"{digest}  {ASSET.name}\n", encoding="ascii")


if __name__ == "__main__":
    build()
