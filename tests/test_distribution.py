"""Tests for the standalone release artifact."""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build.py"


def test_built_asset_is_standalone_executable_with_matching_checksum(tmp_path):
    subprocess.run([sys.executable, str(BUILD)], check=True, cwd=ROOT)

    source_asset = ROOT / "dist" / "hostof"
    checksum = ROOT / "dist" / "hostof.sha256"
    assert source_asset.stat().st_mode & 0o111

    standalone = tmp_path / "hostof"
    shutil.copy2(source_asset, standalone)
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["HOME"] = str(tmp_path)
    result = subprocess.run(
        [str(standalone), "--help"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=environment,
        timeout=30,
    )

    assert result.returncode == 0
    assert "hostof" in result.stdout
    expected, filename = checksum.read_text(encoding="ascii").split()
    assert filename == "hostof"
    assert hashlib.sha256(source_asset.read_bytes()).hexdigest() == expected
