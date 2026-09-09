#!/usr/bin/env python3
"""Build or independently recheck Codex/Claude archives from an exact Git plan."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from repository_tools.plugin_distribution import AssemblyError, accept, build, prepare


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "check"))
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--revision", required=True, help="full committed source ID")
    parser.add_argument("--plan", required=True, help="committed repository-relative assembly plan")
    parser.add_argument("--release-revision", required=True, help="trusted full commit containing the released record")
    parser.add_argument("--release-record", required=True, help="repository-relative released RLS record")
    parser.add_argument("--expected-wheel-sha256", required=True, help="independently obtained published archive SHA-256")
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--evaluator-python", required=True, type=Path, help="absolute external released-evaluator Python")
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()
    try:
        assembly = prepare(args.repository, args.revision, args.plan, args.release_revision,
                           args.release_record, args.expected_wheel_sha256, args.wheel, args.evaluator_python)
        result = (build if args.action == "build" else accept)(assembly, args.output_directory.absolute())
    except (AssemblyError, OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        print(json.dumps({"accepted": False, "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
