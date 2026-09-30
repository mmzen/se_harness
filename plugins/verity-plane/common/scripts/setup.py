#!/usr/bin/env python3
"""Create or repair the private evaluator, then report its actual doctor result."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_runtime import (DeliveryError, safe_path, read_regular, private_data,
    environment_path, python_path, query_identity, match_identity, release_selection,
    exclusive, atomic_json, unique_object)


def setup(target: Path, data_root: Path, wheel: Path) -> int:
    if sys.version_info < (3, 11):
        raise ValueError("Provide Python 3.11 or later with venv and ensurepip.")
    import ensurepip  # Report an unavailable prerequisite before creating files.
    import venv

    target = safe_path(target.expanduser())
    if not target.is_dir():
        raise ValueError("Select an existing target directory.")
    data_root = private_data("codex", data_root.expanduser(), target)
    wheel = safe_path(wheel.expanduser())
    match = re.fullmatch(r"se_harness-([0-9]+\.[0-9]+\.[0-9]+)-py3-none-any.whl", wheel.name)
    if not match:
        raise ValueError("Supply the explicitly selected se-harness wheel.")
    raw = read_regular(wheel, 128 * 1024 * 1024)
    identity = {"version":match[1], "archive_name":wheel.name,
                "archive_sha256":hashlib.sha256(raw).hexdigest()}
    expected = identity
    if (target/".engineering-harness.toml").exists() or (target/".engineering-harness.lock").exists():
        _, lock, _ = release_selection(target)
        if lock["tool_version"] == identity["version"]:
            expected = lock["evaluator"]
            # Reject a same-version archive substitution before running its code.
            if expected.get("archive_sha256") and expected["archive_sha256"] != identity["archive_sha256"]:
                raise DeliveryError("supplied wheel does not match the repository's selected archive")
    environment = environment_path(data_root, expected)
    ready = environment/"ready.json"
    with exclusive(environment.with_name(environment.name + ".lock")):
        python = python_path(environment)
        if environment.exists():
            if not ready.is_file():
                raise DeliveryError("incomplete private environment; inspect the interrupted setup and retire that exact unused directory before retrying")
            observed = query_identity(python)
            match_identity(expected, observed)
            match_identity(identity, observed)
            match_identity(json.loads(read_regular(ready, 16384), object_pairs_hook=unique_object), observed)
        else:
            # This path is never reused or repaired over a running installation.
            # Delivery requires ready.json; partial preparation is not usable.
            subprocess.run([sys.executable, "-I", "-m", "venv", "--copies", str(environment)], check=True)
            subprocess.run([str(python), "-I", "-m", "pip", "install", "--disable-pip-version-check",
                            "--no-index", "--no-deps", str(wheel)], check=True)
            if read_regular(wheel, 128 * 1024 * 1024) != raw:
                raise DeliveryError("selected wheel changed during setup")
            observed = query_identity(python)
            match_identity(expected, observed)
            match_identity(identity, observed)
            atomic_json(ready, observed)
    print(f"Evaluator Python: {python}", flush=True)
    return subprocess.run([str(python), "-I", "-m", "se_harness", "doctor", str(target), "--json"],
                          cwd=environment.parent).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    args = parser.parse_args()
    try:
        return setup(args.target, args.data_root, args.wheel)
    except (OSError, ValueError, ImportError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"Setup failed: {exc}. Check the supplied Python and wheel, then rerun the same command.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
