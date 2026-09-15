#!/usr/bin/env python3
"""Create or repair the private evaluator, then report its actual doctor result."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def setup(target: Path, data_root: Path, wheel: Path) -> int:
    if sys.version_info < (3, 11):
        raise ValueError("Provide Python 3.11 or later with venv and ensurepip.")
    import ensurepip  # Report an unavailable prerequisite before creating files.
    import venv

    target = target.expanduser().resolve(strict=True)
    wheel = wheel.expanduser().resolve(strict=True)
    environment = data_root.expanduser().absolute() / "verity-plane" / "evaluator"
    if environment.resolve() != environment or environment.is_relative_to(target):
        raise ValueError("Select an unlinked private data directory outside the repository.")
    if not wheel.is_file() or wheel.suffix != ".whl":
        raise ValueError("Supply the selected se-harness wheel.")
    # venv reuses its directory and repairs missing interpreter/pip files.
    subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
    python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    subprocess.run([str(python), "-I", "-m", "pip", "install", "--disable-pip-version-check",
                    "--no-index", "--no-deps", "--force-reinstall", str(wheel)], check=True)
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
    except (OSError, ValueError, ImportError, subprocess.CalledProcessError) as exc:
        print(f"Setup failed: {exc}. Check the supplied Python and wheel, then rerun the same command.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
